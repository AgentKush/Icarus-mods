using System.Collections.Concurrent;
using System.Diagnostics;
using System.Reflection;
using System.Text;
using CUE4Parse.Compression;
using CUE4Parse.FileProvider;
using CUE4Parse.FileProvider.Objects;
using CUE4Parse.UE4.AssetRegistry;
using CUE4Parse.UE4.Assets;
using CUE4Parse.UE4.Assets.Exports.Material;
using CUE4Parse.UE4.Localization;
using CUE4Parse.UE4.Versions;
using CUE4Parse.UE4.VirtualFileSystem;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace IcarusExport;

internal sealed class RunResult
{
    public string? BuildId, PrevBuildId, Baseline, JsonFormat, PrevJsonFormat;
    public DateTime? PrevExportedAt;
    public string GameDir = "", OutDir = "";
    public bool FirstRun, Filtered, RawSkipped, JsonSkipped, Partial;
    public string JsonMode = "";
    public int PaksMounted, PaksRead, PaksUnchanged;
    public long FilesTotal, FilesSelected, DocsSelected, PackagesTotal, BytesRead, JsonUnchanged, JsonWrittenBytes;
    public readonly List<string> PaksAdded = new(), PaksRemoved = new();
    public readonly ConcurrentBag<string> RawAdded = new(), RawChanged = new(), RawRemoved = new();
    public readonly ConcurrentBag<string> JsonAdded = new(), JsonChanged = new();
    public readonly List<string> JsonRemoved = new();
    public readonly List<TableChange> Tables = new();
    public readonly List<string> BaselineAssetsAdded = new(), BaselineAssetsRemoved = new();
    public readonly ConcurrentBag<(string Path, string Error)> Errors = new();
    public readonly List<string> Warnings = new();
    public TimeSpan Duration;
    public long RawWritten, JsonWritten;

    public bool NothingChanged =>
        !FirstRun && PaksAdded.Count == 0 && PaksRemoved.Count == 0 && RawAdded.IsEmpty && RawChanged.IsEmpty &&
        RawRemoved.IsEmpty && JsonAdded.IsEmpty && JsonChanged.IsEmpty && JsonRemoved.Count == 0 && Tables.Count == 0 && Errors.IsEmpty;
}

/// <summary>
/// Mounts the game's paks with CUE4Parse and writes:
///   Raw\&lt;pak&gt;\...       every file byte for byte, one folder per pak
///   Exports\&lt;table&gt;     data.pak's data tables, re-indented like FModel (the layout check_mod.py reads)
///   Exports\&lt;asset&gt;.json one JSON per asset, text and localization file, exactly like FModel's "Save Properties"
/// Only files whose content changed are written; files the game no longer has are deleted. Each run is compared
/// with the last complete export (ExportBasis), so an interrupted or partial run never hides a change.
/// </summary>
internal sealed class Exporter(Options opt, Log log)
{
    /// <summary>Bump when the tool's own JSON output rules change, to make the next run re-serialise everything.</summary>
    const int FormatRevision = 1;
    /// <summary>The CUE4Parse build (NuGet 1.2.2.202611) every export before state version 2 was made with.</summary>
    public const string Cue4Parse1_2_2_202611 = "1.2.2+e76778c10ed25860e11ec488750753224d067d87";
    public static string FormatOf(string cue4ParseVersion) => $"{FormatRevision}:{cue4ParseVersion}";
    public static string Cue4ParseVersion =>
        typeof(DefaultFileProvider).Assembly.GetCustomAttribute<AssemblyInformationalVersionAttribute>()?.InformationalVersion
        ?? typeof(DefaultFileProvider).Assembly.GetName().Version?.ToString() ?? "unknown";

    const string TmpSuffix = ".icarusexport-tmp";
    static readonly UTF8Encoding Utf8 = new(false);
    static readonly string[] PackageParts = [".uasset", ".umap", ".uexp", ".ubulk", ".uptnl"];
    static readonly StringComparer Cmp = StringComparer.OrdinalIgnoreCase;
    readonly ConcurrentDictionary<string, byte> knownDirs = new(Cmp);
    readonly ConcurrentDictionary<string, byte> touchedDirs = new(Cmp);
    readonly object checkpointGate = new();
    SemaphoreSlim writeGate = new(4);
    string exportsDir = "", rawDir = "";
    Dictionary<string, string> pakKeys = new(Cmp); // pak file path -> key (folder name in Raw\, key in the state)
    HashSet<string> dataPaths = new(Cmp);          // data.pak's entries, never exported as asset JSON
    readonly ConcurrentDictionary<string, byte> failedDeletes = new(Cmp); // relative to the export folder
    (string[] Tables, string Marker)? pendingSnapshot;

    string SnapshotDir => Path.Combine(opt.OutDir, ".icarusexport", "basis-tables");
    string SnapshotMarkerPath => Path.Combine(SnapshotDir, ".basis");

    public (RunResult Result, ExportState Next) Run(Steam.Install game, string? buildId, ExportState prev)
    {
        var clock = Stopwatch.StartNew();
        exportsDir = Path.Combine(opt.OutDir, "Exports");
        rawDir = Path.Combine(opt.OutDir, "Raw");
        writeGate = new SemaphoreSlim(opt.WriteThreads);

        // What this run is compared with: the last complete export. While a run is unfinished or partial it
        // stays in the state as the basis, so the next run still sees every change since that export.
        var basis = prev.Complete ? ExportBasis.Of(prev) : prev.Basis;
        var basisPaks = basis?.Paks ?? prev.Paks;
        var basisJson = basis?.Json ?? prev.Json;
        var r = new RunResult
        {
            BuildId = buildId, PrevBuildId = basis?.BuildId, PrevExportedAt = basis?.ExportedAt, GameDir = game.GameDir,
            OutDir = opt.OutDir, FirstRun = basis == null, Filtered = opt.PakFilters.Count > 0,
            RawSkipped = opt.NoRaw, JsonSkipped = opt.NoJson, PrevJsonFormat = prev.JsonFormat, JsonFormat = FormatOf(Cue4ParseVersion),
        };
        if (r.FirstRun && opt.Baseline != null)
        {
            var full = Path.GetFullPath(opt.Baseline).TrimEnd(Path.DirectorySeparatorChar);
            if (!Directory.Exists(full)) r.Warnings.Add($"Baseline folder not found: {opt.Baseline}");
            else if (IsUnder(full, exportsDir) || IsUnder(exportsDir, full))
                r.Warnings.Add($"The baseline {full} is (or contains) the export being written, so it was not used. Point --baseline at a copy.");
            else r.Baseline = full;
        }
        var next = new ExportState
        {
            BuildId = buildId, ExportedAt = prev.ExportedAt, Tool = prev.Tool, JsonFormat = prev.JsonFormat,
            Complete = false, Basis = basis,
        };

        // The marker exists from here until Program has saved the final state: if it is already there, a run was
        // killed (possibly before its first checkpoint), so clean up its half-written files.
        var runMarker = ExportState.RunMarkerFor(opt.OutDir);
        bool killedBefore = File.Exists(runMarker);
        Directory.CreateDirectory(Path.GetDirectoryName(runMarker)!);
        File.WriteAllText(runMarker, DateTime.Now.ToString("o"));
        if (killedBefore || (!prev.Complete && prev.Paks.Count > 0)) RemoveStaleTemps();
        RetryPendingDeletes(prev);

        InitCompression();
        var dataPak = Path.GetFullPath(Path.Combine(game.GameDir, "Icarus", "Content", "Data", "data.pak"));
        if (!File.Exists(dataPak)) r.Warnings.Add($"data.pak not found at {dataPak}");
        var provider = Mount(game);

        // Natural order (s1, s2 ... s10), so the log reads like the Paks folder.
        var paks = provider.MountedVfs.OrderBy(v => NaturalKey(v.Name), Cmp).ToList();
        if (paks.Count == 0) throw new InvalidOperationException("No paks could be mounted.");
        pakKeys = PakKeys(game.GameDir, paks, dataPak);
        // A copy of data.pak elsewhere in the game folder must never turn the tables into asset JSON.
        foreach (var v in paks.Where(v => KeyOf(v) == "data"))
            foreach (var p in v.Files.Keys) dataPaths.Add(p.TrimStart('/'));
        // A pak that is on disk but could not be mounted (encrypted, damaged, half-written) must not look removed.
        var mountedPaths = new HashSet<string>(paks.Select(v => Path.GetFullPath(v.Path)), Cmp);
        var unreadable = GamePaks(game).Where(p => !mountedPaths.Contains(Path.GetFullPath(p))).ToList();
        if (unreadable.Count > 0)
            r.Warnings.Add($"{unreadable.Count} pak(s) could not be read, so nothing was deleted and the build counts as not exported yet: " +
                           string.Join(", ", unreadable.Select(Path.GetFileName)));
        bool canDelete = unreadable.Count == 0;
        r.Partial = opt.PakFilters.Count > 0 || opt.NoRaw || opt.NoJson || unreadable.Count > 0;

        r.PaksMounted = paks.Count;
        r.FilesTotal = paks.Sum(v => (long)v.FileCount);
        r.FilesSelected = paks.Where(v => opt.Selects(KeyOf(v))).Sum(v => (long)v.FileCount);
        var allFiles = provider.Files.Values.ToList();
        r.PackagesTotal = allFiles.Count(f => f.IsUePackage);
        log.Info($"Mounted {paks.Count} paks: {Fmt.N(r.FilesTotal)} files, {Fmt.N(r.PackagesTotal)} assets ({Fmt.Time(clock.Elapsed)})");

        // Each worker thread gets its own mounted copy of the paks. A CUE4Parse pak reader is not safe to
        // share between threads, and its IsConcurrent mode clones the reader on every read, which makes a
        // map that references 10,000 other objects take 35 seconds instead of 1.
        var workerClock = Stopwatch.StartNew();
        workers = Enumerable.Range(0, opt.Threads).AsParallel().WithDegreeOfParallelism(Math.Min(opt.Threads, 8))
            .Select(_ => new Worker(Mount(game))).ToList();
        log.Info($"Started {workers.Count} workers ({Fmt.Time(workerClock.Elapsed)})");

        // ---- 1. Raw files: read every file of each changed pak, hash it, write what differs ----
        var mountedKeys = new HashSet<string>(paks.Select(KeyOf), Cmp);
        var dataFiles = new ConcurrentDictionary<string, byte[]>(Cmp);
        string[]? dataEntries = null;
        foreach (var vfs in paks)
        {
            var key = KeyOf(vfs);
            bool isData = key.Equals("data", StringComparison.OrdinalIgnoreCase);
            prev.Paks.TryGetValue(key, out var prevPak);
            if (!opt.Selects(key))
            {
                if (prevPak != null) next.Paks[key] = prevPak;
                continue;
            }
            if (isData) dataEntries = vfs.Files.Keys.ToArray();

            var info = new FileInfo(vfs.Path);
            bool rawInSync = opt.NoRaw || (prevPak?.Raw == true && Directory.Exists(Path.Combine(rawDir, key)));
            if (!opt.Full && !isData && prevPak != null && prevPak.Size == info.Length &&
                prevPak.MTime == info.LastWriteTimeUtc.Ticks && rawInSync)
            {
                next.Paks[key] = prevPak;
                r.PaksUnchanged++;
                continue;
            }

            r.PaksRead++;
            var pakClock = Stopwatch.StartNew();
            bool trustRaw = prevPak?.Raw == true && !opt.Full;
            var hashes = new ConcurrentDictionary<string, string>(Cmp);
            var entries = vfs.Files.Values.OrderByDescending(e => e.Size).ToArray();
            int done = 0, failed = 0;
            using (new Ticker(TimeSpan.FromSeconds(15), () =>
                       log.Info($"  {key}: {Fmt.N(Volatile.Read(ref done))}/{Fmt.N(entries.Length)} files")))
            {
                RunWorkers(entries, (w, e) =>
                {
                    try
                    {
                        var data = w.Paks[vfs.Path].Files[e.Path].Read();
                        Interlocked.Add(ref r.BytesRead, data.Length);
                        var h = Hashes.Of(data);
                        if (isData) dataFiles[e.Path] = data;
                        if (!opt.NoRaw)
                        {
                            var target = Path.Combine(rawDir, key, Rel(e.Path));
                            string? old = null;
                            bool had = prevPak != null && prevPak.Files.TryGetValue(e.Path, out old);
                            if (!trustRaw || !had || old != h || !File.Exists(target))
                            {
                                WriteBytes(target, data);
                                Interlocked.Increment(ref r.RawWritten);
                            }
                        }
                        hashes[e.Path] = h;
                    }
                    catch (Exception ex)
                    {
                        Interlocked.Increment(ref failed);
                        Fail(r, $"{key}/{e.Path}", ex);
                        // Keep the old hash so the file does not look removed; the pak is read again next run.
                        if (prevPak != null && prevPak.Files.TryGetValue(e.Path, out var keep)) hashes[e.Path] = keep;
                    }
                    Interlocked.Increment(ref done);
                });
            }

            // Files the pak no longer has. Deleted even on a --no-raw run: the state forgets them, so a later run could not.
            if (prevPak != null)
                foreach (var p in prevPak.Files.Keys.Where(p => !hashes.ContainsKey(p) && !vfs.Files.ContainsKey(p)))
                    DeleteFile(Path.Combine(rawDir, key, Rel(p)));
            next.Paks[key] = new PakState
            {
                Size = info.Length, MTime = failed > 0 ? 0 : info.LastWriteTimeUtc.Ticks, Raw = !opt.NoRaw,
                Files = new Dictionary<string, string>(hashes, Cmp),
            };
            log.Info($"  {key}: {Fmt.N(entries.Length)} files in {Fmt.Time(pakClock.Elapsed)}{(failed > 0 ? $", {failed} could not be read" : "")}");
        }

        // Paks the game no longer has. Kept when they were not selected, when some pak could not be read, or
        // when so many vanished at once that it looks like a broken install rather than an update.
        var vanished = prev.Paks.Keys.Where(k => !mountedKeys.Contains(k)).ToList();
        var dropping = vanished.Where(opt.Selects).ToList();
        foreach (var k in vanished.Except(dropping, Cmp)) next.Paks[k] = prev.Paks[k];
        if (dropping.Count > 0 && (!canDelete || (dropping.Count > 3 && !opt.AllowMassDelete)))
        {
            if (canDelete)
                r.Warnings.Add($"{dropping.Count} paks have disappeared ({string.Join(", ", dropping)}). Their raw files were kept; " +
                               "run with --allow-mass-delete if the game really dropped them.");
            foreach (var k in dropping) next.Paks[k] = prev.Paks[k];
        }
        else
        {
            foreach (var k in dropping) DeleteDir(Path.Combine(rawDir, k));
        }
        DiffRaw(r, basisPaks, next.Paks);
        if (!opt.NoRaw) log.Info($"Raw files: {Fmt.N(r.RawWritten)} written, {Fmt.Gb(r.BytesRead)} read ({Fmt.Time(clock.Elapsed)})");
        Checkpoint(next, prev, null);

        // ---- 2. Data tables: data.pak's JSON goes to Exports\<Category>\ ----
        if (dataEntries != null) CopyDataTables(r, basis, prev, dataFiles, dataEntries, canDelete);
        else if (opt.Selects("data")) r.Warnings.Add("data.pak was not mounted; data tables were left as they were.");

        // ---- 3. JSON for every asset, text file and localization file ----
        if (!opt.NoJson) ExportJson(r, provider, allFiles, prev, next, basis, basisPaks, basisJson, canDelete);
        else
        {
            foreach (var kv in prev.Json) next.Json[kv.Key] = kv.Value;
            next.RetryJson.UnionWith(prev.RetryJson);
        }

        if (r.Baseline != null) CompareBaselineAssets(r, allFiles);
        PruneEmptyDirs();
        workers = new();
        next.PendingDeletes.UnionWith(failedDeletes.Keys);
        if (!failedDeletes.IsEmpty)
            r.Warnings.Add($"{Fmt.N(failedDeletes.Count)} file(s) the game removed could not be deleted (in use?); the next run tries again.");

        // A complete run becomes the new basis; a partial one keeps the old basis so nothing it skipped is lost.
        // The copy of the data tables is committed by Program only after this state is saved (CommitTableSnapshot).
        if (!r.Partial)
        {
            var now = DateTime.Now;
            next.Complete = true;
            next.Basis = null;
            next.ExportedAt = now;
            next.JsonFormat = r.JsonFormat;
            if (dataEntries != null) pendingSnapshot = (dataEntries, new ExportBasis { BuildId = buildId, ExportedAt = now }.Marker);
        }
        r.Duration = clock.Elapsed;
        return (r, next);
    }

    /// <summary>
    /// Called after the final state is saved: replaces the copy of the basis data tables with this complete run's
    /// tables. Doing it later than the save means a crash in between leaves an old marker, which the next run
    /// notices and rebuilds from Exports\ (which then holds exactly the basis tables).
    /// </summary>
    public void CommitTableSnapshot()
    {
        if (pendingSnapshot is { } s) SaveTableSnapshot(s.Tables, s.Marker);
        pendingSnapshot = null;
    }

    /// <summary>Removes the in-progress marker; Program calls this once the final state is on disk.</summary>
    public static void ClearRunMarker(string outDir)
    {
        try { File.Delete(ExportState.RunMarkerFor(outDir)); } catch (IOException) { }
    }

    /// <summary>Deletes what an earlier run could not (a file in use, say). What still fails stays pending.</summary>
    void RetryPendingDeletes(ExportState prev)
    {
        foreach (var rel in prev.PendingDeletes)
        {
            var path = Path.Combine(opt.OutDir, rel);
            if (Directory.Exists(path)) DeleteDir(path);
            else DeleteFile(path);
        }
        if (prev.PendingDeletes.Count > 0)
            log.Info($"Retried {prev.PendingDeletes.Count} earlier failed deletes, {failedDeletes.Count} still failing");
    }

    /// <summary>Raw-file changes since the basis, for the report (also catches changes an interrupted run already wrote).</summary>
    void DiffRaw(RunResult r, Dictionary<string, PakState> basisPaks, Dictionary<string, PakState> nowPaks)
    {
        if (r.FirstRun) return;
        foreach (var key in basisPaks.Keys.Union(nowPaks.Keys, Cmp).Where(opt.Selects).Order(Cmp))
        {
            basisPaks.TryGetValue(key, out var was);
            nowPaks.TryGetValue(key, out var now);
            if (ReferenceEquals(was, now)) continue;
            if (was == null && now != null)
            {
                r.PaksAdded.Add(key);
                foreach (var f in now.Files.Keys) r.RawAdded.Add($"{key}/{f}");
            }
            else if (was != null && now == null)
            {
                r.PaksRemoved.Add(key);
                foreach (var f in was.Files.Keys) r.RawRemoved.Add($"{key}/{f}");
            }
            else if (was != null && now != null)
            {
                foreach (var (f, h) in now.Files)
                    if (!was.Files.TryGetValue(f, out var wh)) r.RawAdded.Add($"{key}/{f}");
                    else if (wh != h) r.RawChanged.Add($"{key}/{f}");
                foreach (var f in was.Files.Keys)
                    if (!now.Files.ContainsKey(f)) r.RawRemoved.Add($"{key}/{f}");
            }
        }
    }

    // ---------------------------------------------------------------- data tables

    /// <summary>
    /// data.pak's tables go to Exports\&lt;Category&gt;\D_*.json re-indented the way FModel saves JSON
    /// (Newtonsoft, 2 spaces, CRLF), so they match the old FModel exports byte for byte.
    /// Raw\data\ keeps the game's own formatting. The row-by-row report compares with a copy of the tables
    /// as they were in the basis export (.icarusexport\basis-tables), or with --baseline on a first run.
    /// </summary>
    void CopyDataTables(RunResult r, ExportBasis? basis, ExportState prev, ConcurrentDictionary<string, byte[]> files,
        string[] entries, bool canDelete)
    {
        bool snapshot = false;
        PakState? basisData = null;
        if (basis != null)
        {
            basis.Paks.TryGetValue("data", out basisData);
            snapshot = File.Exists(SnapshotMarkerPath) && File.ReadAllText(SnapshotMarkerPath) == basis.Marker;
            // After a complete run the tables in Exports are the basis's tables: copy them before overwriting.
            if (!snapshot && prev.Complete && basisData != null)
                snapshot = SaveTableSnapshot(basisData.Files.Keys.ToArray(), basis.Marker);
            if (!snapshot) r.Warnings.Add("No complete copy of the previous export's data tables was found, so their changes are compared with the files on disk.");
        }
        // Without a copy, which tables the last complete export had comes from its file list (not from a later,
        // possibly unfinished run's list).
        var prevData = basisData ?? prev.Paks.GetValueOrDefault("data");
        int written = 0;
        foreach (var (path, raw) in files.OrderBy(kv => kv.Key, Cmp))
        {
            var rel = Rel(path);
            var target = Path.Combine(exportsDir, rel);
            var output = Utf8.GetBytes(ReindentOrKeep(DecodeText(raw)));
            byte[]? onDisk = File.Exists(target) ? File.ReadAllBytes(target) : null;
            var beforeFile = r.FirstRun ? (r.Baseline == null ? null : Path.Combine(r.Baseline, rel))
                : snapshot ? Path.Combine(SnapshotDir, rel) : null;
            byte[]? was = beforeFile != null ? (File.Exists(beforeFile) ? File.ReadAllBytes(beforeFile) : null)
                : r.FirstRun ? null : onDisk;
            if (was == null)
            {
                // New, unless (without a copy to compare with) it is a table whose file was simply deleted since.
                if (r.FirstRun ? r.Baseline != null : snapshot || prevData?.Files.ContainsKey(path) != true)
                    r.Tables.Add(TableChange.Added(rel));
            }
            else if (!was.AsSpan().SequenceEqual(output) && TableChange.Compare(rel, was, output) is { } change)
            {
                r.Tables.Add(change);
            }
            if (onDisk == null || !onDisk.AsSpan().SequenceEqual(output))
            {
                WriteBytes(target, output);
                written++;
            }
        }

        var now = new HashSet<string>(entries.Select(Rel), Cmp);
        var before = new HashSet<string>(
            r.FirstRun ? (r.Baseline != null ? BaselineTables(r.Baseline) : [])
            : snapshot ? Directory.EnumerateFiles(SnapshotDir, "*.json", SearchOption.AllDirectories).Select(f => Path.GetRelativePath(SnapshotDir, f))
            : prevData != null ? prevData.Files.Keys.Select(Rel) : [], Cmp);
        foreach (var rel in before.Where(b => !now.Contains(b)).Order(Cmp))
            r.Tables.Add(TableChange.Removed(rel));
        // Delete every table on disk the game no longer has, including one an unfinished run wrote and the game
        // dropped since (it is in the latest file list but not in the basis).
        if (canDelete)
        {
            var onDiskLists = before.Concat(prev.Paks.TryGetValue("data", out var latest) ? latest.Files.Keys.Select(Rel) : []);
            foreach (var rel in onDiskLists.Where(b => !now.Contains(b)).Distinct(Cmp))
                DeleteFile(Path.Combine(exportsDir, rel));
        }
        log.Info($"Data tables: {files.Count} in data.pak, {written} written, {r.Tables.Count} with changes");
    }

    /// <summary>
    /// Copies the data tables now in Exports\ to .icarusexport\basis-tables\ for the next run to compare with.
    /// True only when the copy is complete: the marker is written last, so a half-made copy never counts.
    /// </summary>
    bool SaveTableSnapshot(IEnumerable<string> tablePaths, string marker)
    {
        try
        {
            if (Directory.Exists(SnapshotDir)) Directory.Delete(SnapshotDir, true);
            Directory.CreateDirectory(SnapshotDir);
            foreach (var path in tablePaths)
            {
                var rel = Rel(path);
                var from = Path.Combine(exportsDir, rel);
                if (!File.Exists(from)) continue;
                var to = Path.Combine(SnapshotDir, rel);
                Directory.CreateDirectory(Path.GetDirectoryName(to)!);
                File.Copy(from, to, true);
            }
            File.WriteAllText(SnapshotMarkerPath, marker);
            return true;
        }
        catch (Exception e) when (e is IOException or UnauthorizedAccessException or InvalidDataException)
        {
            log.Info($"Could not save the copy of the data tables: {e.Message}");
            try { File.Delete(SnapshotMarkerPath); } catch (IOException) { }
            return false;
        }
    }

    static IEnumerable<string> BaselineTables(string baseline)
    {
        foreach (var f in Directory.EnumerateFiles(baseline, "*.json", SearchOption.TopDirectoryOnly))
            yield return Path.GetFileName(f);
        foreach (var dir in Directory.EnumerateDirectories(baseline))
        {
            var name = Path.GetFileName(dir);
            if (name.Equals("Icarus", StringComparison.OrdinalIgnoreCase) || name.Equals("Engine", StringComparison.OrdinalIgnoreCase)) continue;
            foreach (var f in Directory.EnumerateFiles(dir, "*.json", SearchOption.AllDirectories))
                yield return Path.GetRelativePath(baseline, f);
        }
    }

    // ---------------------------------------------------------------- asset JSON

    enum DocKind { Package, Text, Json, Locres, Locmeta, AssetRegistry, ShaderCache }

    sealed record Doc(GameFile File, DocKind Kind, string Key);

    /// <summary>Plain-text files FModel shows (and saves as .json) as they are.</summary>
    static readonly HashSet<string> TextExtensions = new(Cmp)
    {
        "ini", "txt", "log", "po", "bat", "dat", "cfg", "ide", "ipl", "zon", "xml", "h", "csv",
        "uproject", "uplugin", "upluginmanifest", "archive", "manifest", "tps",
        "hlsl", "glsl", "usf", "ush", // shader source (the crash reporter's standalone renderer)
    };

    static DocKind? KindOf(GameFile f) => f.IsUePackage ? DocKind.Package : f.Extension.ToLowerInvariant() switch
    {
        "json" => DocKind.Json,
        "locres" => DocKind.Locres,
        "locmeta" => DocKind.Locmeta,
        "bin" when f.Name.Contains("AssetRegistry", StringComparison.OrdinalIgnoreCase) => DocKind.AssetRegistry,
        "bin" when f.Name.Contains("GlobalShaderCache", StringComparison.OrdinalIgnoreCase) => DocKind.ShaderCache,
        var e when TextExtensions.Contains(e) => DocKind.Text,
        _ => null,
    };

    /// <summary>
    /// Everything FModel's "Save Properties" writes a .json for: every .uasset/.umap, plus text files,
    /// localization, the asset registry and the global shader cache. An asset wins a name clash
    /// (Jura-Medium.uasset and Jura-Medium.ufont both want Jura-Medium.json). data.pak is handled separately.
    /// </summary>
    List<Doc> BuildDocs(List<GameFile> files)
    {
        var docs = new List<Doc>();
        var keys = new HashSet<string>(Cmp);
        foreach (var f in files.Where(f => f.IsUePackage))
            if (keys.Add(f.PathWithoutExtension)) docs.Add(new Doc(f, DocKind.Package, f.PathWithoutExtension));
        foreach (var f in files.Where(f => !f.IsUePackage && !IsDataPak(f) && !dataPaths.Contains(f.Path.TrimStart('/'))))
        {
            var key = f.PathWithoutExtension.TrimStart('/');
            if (KindOf(f) is { } kind && keys.Add(key)) docs.Add(new Doc(f, kind, key));
        }
        return docs;
    }

    bool IsDataPak(GameFile f) => f is VfsEntry v && KeyOf(v.Vfs).Equals("data", StringComparison.OrdinalIgnoreCase);

    /// <summary>Loads a doc through the worker's own provider (never the main one, which is not thread-safe).</summary>
    static object Load(Worker w, Doc d)
    {
        var file = w.Provider.Files[d.File.Path];
        switch (d.Kind)
        {
            case DocKind.Package: return w.Provider.LoadPackage(file);
            case DocKind.Text: return DecodeText(file.Read());
            case DocKind.Json: return ReindentOrKeep(DecodeText(file.Read()));
        }
        using var archive = file.CreateReader();
        return d.Kind switch
        {
            DocKind.Locres => new FTextLocalizationResource(archive),
            DocKind.Locmeta => new FTextLocalizationMetaDataResource(archive),
            DocKind.AssetRegistry => new FAssetRegistryState(archive),
            _ => new FGlobalShaderCache(archive),
        };
    }

    void ExportJson(RunResult r, DefaultFileProvider provider, List<GameFile> allFiles, ExportState prev, ExportState next,
        ExportBasis? basis, Dictionary<string, PakState> basisPaks, Dictionary<string, string> basisJson, bool canDelete)
    {
        var clock = Stopwatch.StartNew();
        var docs = BuildDocs(allFiles);
        var selected = docs.Where(d => opt.Selects(KeyOf(((VfsEntry)d.File).Vfs)))
            // Biggest first (the workers share one queue), so a huge map does not finish alone at the end.
            .OrderByDescending(d => d.Kind == DocKind.Package ? PackageSize(provider, d.File) : d.File.Size).ToArray();
        r.DocsSelected = selected.Length;
        log.Info($"JSON: {Fmt.N(selected.Length)} files ({Fmt.N(selected.Count(d => d.Kind == DocKind.Package))} assets, " +
                 $"{Fmt.N(selected.Count(d => d.Kind != DocKind.Package))} text/localization/registry files)");

        // Files the game no longer has, decided once: deleted (and rippled to their importers) only when every
        // pak could be read and not so many vanished at once that it looks like a broken install.
        var current = new HashSet<string>(docs.Select(d => d.Key), Cmp);
        var gone = basisJson.Keys.Concat(prev.Json.Keys).Where(k => !current.Contains(k)).Distinct(Cmp).Order(Cmp).ToList();
        bool massDelete = gone.Count > Math.Max(500, basisJson.Count / 10) && !opt.AllowMassDelete;
        bool deleteGone = canDelete && !massDelete;
        var redo = PlanJson(r, provider, docs, prev, next, basis, basisPaks, basisJson, deleteGone ? gone : []);

        var results = new ConcurrentDictionary<string, string>(Cmp);
        var failedKeys = new ConcurrentDictionary<string, byte>(Cmp);
        int done = 0, sinceCheckpoint = 0;
        long errors0 = r.Errors.Count;

        void Classify(string key, string hash)
        {
            if (r.FirstRun) return;
            if (!basisJson.TryGetValue(key, out var was)) r.JsonAdded.Add(key);
            else if (was != hash) r.JsonChanged.Add(key);
        }

        using (new Ticker(TimeSpan.FromSeconds(20), () =>
                   log.Info($"  JSON: {Fmt.N(Volatile.Read(ref done))}/{Fmt.N(selected.Length)}, " +
                            $"{Fmt.N(Interlocked.Read(ref r.JsonWritten))} written, {Fmt.N(r.Errors.Count - errors0)} errors, {Fmt.Time(clock.Elapsed)}")))
        {
            RunWorkers(selected, (w, d) =>
            {
                var key = d.Key;
                bool had = prev.Json.TryGetValue(key, out var onDiskHash);
                try
                {
                    var target = Path.Combine(exportsDir, Rel(key) + ".json");
                    bool onDisk = had && File.Exists(target);
                    if (onDisk && redo != null && !redo.Contains(key))
                    {
                        results[key] = onDiskHash!;
                        Interlocked.Increment(ref r.JsonUnchanged);
                        Classify(key, onDiskHash!);
                    }
                    else
                    {
                        var loaded = Load(w, d);
                        string? hash = onDisk ? Serialize(loaded, Stream.Null).Hash : null;
                        if (hash != null && hash == onDiskHash)
                        {
                            Interlocked.Increment(ref r.JsonUnchanged);
                        }
                        else
                        {
                            EnsureDir(Path.GetDirectoryName(target)!);
                            var tmp = target + TmpSuffix;
                            try
                            {
                                // Serialize disposes the stream when it is done.
                                (hash, long size) = Serialize(loaded,
                                    new FileStream(tmp, FileMode.Create, FileAccess.Write, FileShare.None, 1 << 16));
                                File.Move(tmp, target, true);
                                Interlocked.Add(ref r.JsonWrittenBytes, size);
                            }
                            catch
                            {
                                try { File.Delete(tmp); } catch (IOException) { }
                                throw;
                            }
                            Interlocked.Increment(ref r.JsonWritten);
                        }
                        results[key] = hash;
                        Classify(key, hash);
                    }
                }
                catch (Exception ex)
                {
                    // Its last good file stays on disk with the last hash; RetryJson makes the next run try again.
                    failedKeys[key] = 0;
                    if (had) results[key] = onDiskHash!;
                    else results.TryRemove(key, out _);
                    Fail(r, d.File.Path, ex);
                }
                Interlocked.Increment(ref done);
                if (Interlocked.Increment(ref sinceCheckpoint) % 2_000 == 0) Checkpoint(next, prev, results, failedKeys);
            }, d => MemoryWeight(d.Kind == DocKind.Package ? PackageSize(provider, d.File) : d.File.Size));
        }

        // Every pak is mounted even when --paks narrows the export, so a file missing from all of them is
        // gone from the game: delete its JSON. Files that were not selected this time keep their entry.
        foreach (var kv in results) next.Json[kv.Key] = kv.Value;
        foreach (var kv in prev.Json)
            if (current.Contains(kv.Key)) next.Json.TryAdd(kv.Key, kv.Value);
        next.RetryJson.UnionWith(failedKeys.Keys);
        var selectedKeys = new HashSet<string>(selected.Select(d => d.Key), Cmp);
        foreach (var k in prev.RetryJson)
            if (current.Contains(k) && !selectedKeys.Contains(k)) next.RetryJson.Add(k);
        if (gone.Count > 0 && !deleteGone)
        {
            if (canDelete)
                r.Warnings.Add($"{Fmt.N(gone.Count)} assets seem to have vanished, so nothing was deleted. " +
                               "If the game really removed them, run again with --allow-mass-delete.");
            foreach (var k in gone) if (prev.Json.TryGetValue(k, out var h)) next.Json[k] = h;
        }
        else
        {
            foreach (var k in gone)
            {
                DeleteFile(Path.Combine(exportsDir, Rel(k) + ".json"));
                if (basisJson.ContainsKey(k)) r.JsonRemoved.Add(k);
            }
        }
        log.Info($"JSON: {Fmt.N(selected.Length)} files, {Fmt.N(r.JsonWritten)} written ({Fmt.Gb(r.JsonWrittenBytes)}), " +
                 $"{Fmt.N(r.JsonUnchanged)} unchanged, {Fmt.N(r.JsonRemoved.Count)} removed, {Fmt.N(r.Errors.Count - errors0)} errors in {Fmt.Time(clock.Elapsed)}");
    }

    /// <summary>
    /// Which files need serialising again, or null for all of them. A file's JSON can change when its own
    /// bytes change, and also when a package it imports changes: the JSON names every imported object as
    /// "Package.ExportIndex", so a new socket in a skeleton shifts the indexes printed in each animation
    /// that uses it. One level is enough, as an index depends only on the imported package's own bytes.
    /// Changes are measured from the basis (the last complete export). Everything is redone with --full, when
    /// the JSON on disk has another format, on the first run, or when English localization (LocalizedString)
    /// or a plugin descriptor (plugin paths) changes.
    /// </summary>
    HashSet<string>? PlanJson(RunResult r, DefaultFileProvider provider, List<Doc> docs, ExportState prev, ExportState next,
        ExportBasis? basis, Dictionary<string, PakState> basisPaks, Dictionary<string, string> basisJson, IReadOnlyList<string> goneKeys)
    {
        string? everything =
            opt.Full ? "--full"
            : prev.Json.Count == 0 ? "first export"
            : prev.JsonFormat != r.JsonFormat ? $"the JSON on disk was written by {prev.JsonFormat ?? "an older version"}, now {r.JsonFormat}"
            : null;
        var changed = new HashSet<string>(Cmp);
        if (everything == null)
        {
            foreach (var d in docs)
                if (InputHash(basisPaks, d) is not { } before || before != InputHash(next.Paks, d)) changed.Add(d.Key);
            everything = docs.FirstOrDefault(d => changed.Contains(d.Key) && AffectsEveryAsset(d)) is { } d2
                ? $"{d2.File.Path} changed" : null;
        }
        if (everything != null)
        {
            r.JsonMode = $"every file re-serialised ({everything}); only changed ones written";
            log.Info($"JSON: re-serialising everything ({everything})");
            return null;
        }

        var current = new HashSet<string>(docs.Select(d => d.Key), Cmp);
        // Removed files ripple to their importers only when they really are deleted (not when a pak was unreadable).
        var ripple = new HashSet<string>(changed.Concat(goneKeys), Cmp);
        var redo = new HashSet<string>(changed, Cmp);
        // Files whose JSON failed last time.
        redo.UnionWith(prev.RetryJson.Where(current.Contains));
        // JSON an unfinished or partial run left different from the last complete export (for example importers
        // serialised while a pak was unreadable): serialise again and keep it only if it is still right.
        if (!prev.Complete && basis != null)
            foreach (var (k, h) in prev.Json)
                if (current.Contains(k) && (!basis.Json.TryGetValue(k, out var was) || was != h)) redo.Add(k);
        int dependents = 0;
        if (ripple.Count > 0)
        {
            var clock = Stopwatch.StartNew();
            var found = new ConcurrentBag<string>();
            RunWorkers(docs.Where(d => d.Kind == DocKind.Package && !changed.Contains(d.Key)).ToArray(), (w, d) =>
            {
                try
                {
                    if (w.Provider.LoadPackage(w.Provider.Files[d.File.Path]) is not Package p ||
                        p.ImportMap.Any(i => i.ClassName.Text == "Package" && (i.OuterIndex?.IsNull ?? true) && i.ObjectName.Text is { } name &&
                                             ripple.Contains(PackageKey(w.Provider, name))))
                        found.Add(d.Key);
                }
                catch (Exception)
                {
                    found.Add(d.Key); // unreadable header: re-serialise it to be safe
                }
            }, d => MemoryWeight(PackageSize(provider, d.File)));
            redo.UnionWith(found);
            dependents = found.Count;
            log.Info($"JSON: {Fmt.N(changed.Count)} changed or new files, {Fmt.N(dependents)} more assets import them ({Fmt.Time(clock.Elapsed)})");
        }
        r.JsonMode = $"incremental: {Fmt.N(changed.Count)} changed or new files, {Fmt.N(dependents)} assets that import them, " +
                     $"{Fmt.N(redo.Count - changed.Count - dependents)} to retry or re-check, and any file missing from Exports were serialised";
        return redo;
    }

    /// <summary>English localization feeds LocalizedString everywhere; plugin descriptors decide plugin paths.</summary>
    static bool AffectsEveryAsset(Doc d) =>
        (d.Kind == DocKind.Locres && d.Key.Contains("/en/", StringComparison.OrdinalIgnoreCase)) ||
        d.File.Extension.Equals("uplugin", StringComparison.OrdinalIgnoreCase) ||
        d.File.Extension.Equals("upluginmanifest", StringComparison.OrdinalIgnoreCase) ||
        d.File.Extension.Equals("uproject", StringComparison.OrdinalIgnoreCase);

    /// <summary>"/Game/ASS/Foo" -> "Icarus/Content/ASS/Foo" (plugin paths too), the key the docs use.</summary>
    static string PackageKey(DefaultFileProvider provider, string packageName)
    {
        var path = provider.FixPath(packageName);
        foreach (var ext in new[] { ".uasset", ".umap" })
            if (path.EndsWith(ext, StringComparison.OrdinalIgnoreCase)) return path[..^ext.Length];
        return path;
    }

    /// <summary>
    /// Same output as FModel: JsonConvert.SerializeObject(x, Formatting.Indented) (or the text as it is),
    /// UTF-8 without BOM, CRLF. Streams straight to <paramref name="sink"/> and disposes it, so even the
    /// 800 MB map files never sit in memory.
    /// </summary>
    static (string Hash, long Bytes) Serialize(object loaded, Stream sink)
    {
        var hashing = new HashingStream(sink);
        using (var text = new StreamWriter(hashing, Utf8, 1 << 16))
        {
            if (loaded is string s)
            {
                text.Write(s);
            }
            else
            {
                using var json = new JsonTextWriter(text) { Formatting = Formatting.Indented, CloseOutput = false };
                var serializer = JsonSerializer.CreateDefault();
                serializer.Formatting = Formatting.Indented;
                serializer.Serialize(json, loaded is IPackage package ? package.GetExports() : loaded);
            }
        }
        return (hashing.Hex, hashing.Written);
    }

    /// <summary>Text as FModel reads it: UTF-8 unless a byte order mark says otherwise.</summary>
    static string DecodeText(byte[] bytes)
    {
        using var reader = new StreamReader(new MemoryStream(bytes));
        return reader.ReadToEnd();
    }

    static string ReindentOrKeep(string json)
    {
        try { return JToken.Parse(json).ToString(Formatting.Indented); }
        catch (JsonException) { return json; }
    }

    /// <summary>The hashes of a file's own inputs (for an asset: .uasset/.umap/.uexp/.ubulk/.uptnl), or null.</summary>
    string? InputHash(Dictionary<string, PakState> paks, Doc d)
    {
        if (!paks.TryGetValue(KeyOf(((VfsEntry)d.File).Vfs), out var pak)) return null;
        if (d.Kind != DocKind.Package) return pak.Files.GetValueOrDefault(d.File.Path);
        var sb = new StringBuilder();
        foreach (var ext in PackageParts)
            if (pak.Files.TryGetValue(d.File.PathWithoutExtension + ext, out var h)) sb.Append(ext).Append(h);
        return sb.Length == 0 ? null : sb.ToString();
    }

    static long PackageSize(DefaultFileProvider provider, GameFile f) =>
        f.Size + (provider.Files.TryGetValue(f.PathWithoutExtension + ".uexp", out var uexp) ? uexp.Size : 0);

    /// <summary>First run with --baseline: which JSON files the old export had that the game no longer has, and the reverse.</summary>
    void CompareBaselineAssets(RunResult r, List<GameFile> allFiles)
    {
        var docs = BuildDocs(allFiles);
        var now = new HashSet<string>(docs.Select(d => d.Key), Cmp);
        // Compare only inside folders that hold assets (Icarus/Content, Engine/Plugins, ...).
        var roots = docs.Where(d => d.Kind == DocKind.Package)
            .Select(d => string.Join('/', d.Key.Split('/').Take(2)) + "/").Distinct(Cmp).ToList();
        var before = new HashSet<string>(Cmp);
        foreach (var root in roots)
        {
            var dir = Path.Combine(r.Baseline!, Rel(root));
            if (!Directory.Exists(dir)) continue;
            foreach (var f in Directory.EnumerateFiles(dir, "*.json", SearchOption.AllDirectories))
                before.Add(Path.GetRelativePath(r.Baseline!, f)[..^5].Replace('\\', '/'));
        }
        if (before.Count == 0) return;
        r.BaselineAssetsAdded.AddRange(now.Where(p => roots.Any(x => p.StartsWith(x, StringComparison.OrdinalIgnoreCase)) && !before.Contains(p))
            .Order(Cmp));
        r.BaselineAssetsRemoved.AddRange(before.Where(p => !now.Contains(p)).Order(Cmp));
    }

    // ---------------------------------------------------------------- helpers

    /// <summary>One worker thread's own mounted copy of the game.</summary>
    sealed class Worker(DefaultFileProvider provider)
    {
        public DefaultFileProvider Provider { get; } = provider;
        /// <summary>Keyed by the pak's full path: two paks in different folders may share a file name.</summary>
        public Dictionary<string, IAesVfsReader> Paks { get; } = provider.MountedVfs.ToDictionary(v => v.Path, Cmp);
    }

    List<Worker> workers = new();

    /// <summary>Every pak the game installs: Icarus\Content\Paks\*.pak and any other .pak outside a mods folder.</summary>
    static IEnumerable<string> GamePaks(Steam.Install game)
    {
        var paksDir = Path.Combine(game.GameDir, "Icarus", "Content", "Paks");
        return Directory.EnumerateFiles(paksDir, "*.pak", SearchOption.TopDirectoryOnly)
            .Concat(Directory.EnumerateFiles(game.GameDir, "*.pak", SearchOption.AllDirectories)
                .Where(p => !string.Equals(Path.GetDirectoryName(p), paksDir, StringComparison.OrdinalIgnoreCase))
                .Where(p => !InModFolder(game.GameDir, p)));
    }

    /// <summary>
    /// Mounts every pak the game installs: Icarus\Content\Paks\*.pak first, then the rest (Data\data.pak,
    /// Engine\Programs\CrashReportClient\...). Registered later, the others never replace a file the main
    /// paks also have. Folders named mods, ~mods or LogicMods hold installed mods (the Mod Manager's merged
    /// pak among them) and are never mounted.
    /// </summary>
    static DefaultFileProvider Mount(Steam.Install game)
    {
        var paksDir = Path.Combine(game.GameDir, "Icarus", "Content", "Paks");
        if (!Directory.Exists(paksDir)) throw new DirectoryNotFoundException($"No Paks folder at {paksDir}");
        var provider = new DefaultFileProvider(paksDir, SearchOption.TopDirectoryOnly,
            new VersionContainer(EGame.GAME_UE4_LATEST), StringComparer.OrdinalIgnoreCase);
        provider.Initialize();
        foreach (var pak in GamePaks(game).Where(p => !string.Equals(Path.GetDirectoryName(p), paksDir, StringComparison.OrdinalIgnoreCase))
                     .Order(StringComparer.OrdinalIgnoreCase))
            provider.RegisterVfs(pak);
        provider.Mount();
        provider.PostMount();
        provider.LoadVirtualPaths();          // resolves plugin paths like /GFur/... the way FModel does
        provider.LoadLocalization(ELanguage.English);
        return provider;
    }

    /// <summary>
    /// "pakchunk0_s20-WindowsNoEditor.pak" -> "pakchunk0_s20-WindowsNoEditor". If two paks share a file name,
    /// both get a key made from their path inside the game folder instead, so neither overwrites the other.
    /// "data" always means the game's own Icarus\Content\Data\data.pak: a copy of it anywhere else gets a path key.
    /// </summary>
    static Dictionary<string, string> PakKeys(string gameDir, IEnumerable<IAesVfsReader> paks, string dataPak)
    {
        var keys = new Dictionary<string, string>(Cmp);
        foreach (var group in paks.GroupBy(v => Path.GetFileNameWithoutExtension(v.Name), Cmp))
            foreach (var v in group)
            {
                bool realData = Path.GetFullPath(v.Path).Equals(dataPak, StringComparison.OrdinalIgnoreCase);
                bool unique = group.Count() == 1 && !group.Key.Equals("data", StringComparison.OrdinalIgnoreCase);
                keys[v.Path] = realData ? "data" : unique ? group.Key
                    : Path.ChangeExtension(Path.GetRelativePath(gameDir, v.Path), null)!.Replace('\\', '_').Replace('/', '_');
            }
        return keys;
    }

    string KeyOf(IVfsReader vfs) => pakKeys[vfs.Path];

    const long HeavyItem = 8L << 20, HeavyBudget = 1536L << 20;

    /// <summary>
    /// How much of the heavy budget an item of this size takes. Memory grows faster than file size: a
    /// 94 MB heightmap tile becomes 227 MB of JSON, and one of the five 550-870 MB persistent levels needs
    /// 15-20 GB on its own, so those take the whole budget and run one at a time.
    /// </summary>
    static long MemoryWeight(long size) =>
        size >= 256L << 20 ? HeavyBudget : size >= 32L << 20 ? size * 4 : size;

    /// <summary>
    /// Runs <paramref name="body"/> over the items on one thread per worker, taking them in the order given
    /// (biggest first). With a <paramref name="weight"/>, items of 8 MB or more are "heavy": a big map can
    /// need gigabytes of memory while it is serialised, so heavy items only start while the heavy work in
    /// progress stays under 1.5 GB, and the other workers carry on with light items meanwhile.
    /// Each thread has a big stack for deeply nested JSON.
    /// </summary>
    void RunWorkers<T>(IReadOnlyList<T> items, Action<Worker, T> body, Func<T, long>? weight = null)
    {
        var heavy = new ConcurrentQueue<(T Item, long Weight)>();
        var light = new ConcurrentQueue<T>();
        foreach (var item in items)
        {
            long w = weight?.Invoke(item) ?? 0;
            if (w >= HeavyItem) heavy.Enqueue((item, w)); else light.Enqueue(item);
        }
        var gate = new object();
        long inFlight = 0;
        Exception? failure = null;

        bool TryTakeHeavy(out T item, out long w)
        {
            lock (gate)
            {
                if (heavy.TryPeek(out var next) && (inFlight == 0 || inFlight + next.Weight <= HeavyBudget) && heavy.TryDequeue(out next))
                {
                    inFlight += next.Weight;
                    (item, w) = next;
                    return true;
                }
            }
            (item, w) = (default!, 0);
            return false;
        }

        var threads = workers.Select(worker => new Thread(() =>
        {
            try
            {
                while (Volatile.Read(ref failure) == null)
                {
                    if (TryTakeHeavy(out var h, out var hw))
                    {
                        try { body(worker, h); }
                        finally { lock (gate) { inFlight -= hw; Monitor.PulseAll(gate); } }
                    }
                    else if (light.TryDequeue(out var l))
                    {
                        body(worker, l);
                    }
                    else if (heavy.IsEmpty)
                    {
                        break;
                    }
                    else
                    {
                        lock (gate) Monitor.Wait(gate, 250); // only heavy items left and the budget is full
                    }
                }
            }
            catch (Exception e)
            {
                Interlocked.CompareExchange(ref failure, e, null);
            }
        }, 64 * 1024 * 1024) { IsBackground = true, Name = "IcarusExport worker" }).ToList();
        threads.ForEach(t => t.Start());
        threads.ForEach(t => t.Join());
        if (failure != null) throw new InvalidOperationException("A worker thread failed: " + failure.Message, failure);
    }

    /// <summary>Records an error; the first 50 also go to the log straight away.</summary>
    void Fail(RunResult r, string path, Exception e)
    {
        var message = $"{e.GetType().Name}: {e.Message}";
        r.Errors.Add((path, message));
        if (r.Errors.Count <= 50) log.Info($"  ERROR {path}: {message}");
        else if (r.Errors.Count == 51) log.Info("  (more errors are listed in the report)");
    }

    /// <summary>
    /// Saves progress so an interrupted run can resume without redoing finished work. The basis is saved with
    /// it, so the resumed run still compares with the last complete export instead of with half-done work.
    /// </summary>
    void Checkpoint(ExportState next, ExportState prev, ConcurrentDictionary<string, string>? json,
        ConcurrentDictionary<string, byte>? failed = null)
    {
        if (!Monitor.TryEnter(checkpointGate)) return;
        try
        {
            var snapshot = new ExportState
            {
                BuildId = next.BuildId, ExportedAt = prev.ExportedAt, LastRunAt = prev.LastRunAt, Tool = prev.Tool,
                JsonFormat = prev.JsonFormat, Complete = false, Basis = next.Basis,
                Paks = new Dictionary<string, PakState>(next.Paks, Cmp),
                Json = new Dictionary<string, string>(prev.Json, Cmp),
            };
            // Keep the previous run's paks too, so files of paks not reached yet are still known.
            foreach (var kv in prev.Paks) snapshot.Paks.TryAdd(kv.Key, kv.Value);
            if (json != null) foreach (var kv in json.ToArray()) snapshot.Json[kv.Key] = kv.Value;
            snapshot.RetryJson.UnionWith(prev.RetryJson);
            if (failed != null) snapshot.RetryJson.UnionWith(failed.Keys);
            // Earlier failed deletes were retried at the start of this run; whatever still fails is in failedDeletes.
            snapshot.PendingDeletes.UnionWith(failedDeletes.Keys);
            snapshot.Save(opt.OutDir);
        }
        catch (Exception e)
        {
            log.Info($"Could not save progress: {e.Message}");
        }
        finally
        {
            Monitor.Exit(checkpointGate);
        }
    }

    void InitCompression()
    {
        var oodle = FindDll(opt.OodlePath, OodleHelper.OODLE_NAME_CURRENT)
                    ?? throw new FileNotFoundException(
                        $"{OodleHelper.OODLE_NAME_CURRENT} not found. Copy it from FModel's Output\\.data folder into " +
                        $"{Path.Combine(opt.OutDir, ".data")} or pass --oodle <file>.");
        OodleHelper.Initialize(oodle);
        var zlib = FindDll(null, ZlibHelper.DLL_NAME);
        if (zlib != null) ZlibHelper.Initialize(zlib);
        log.Info($"Oodle: {oodle}");
    }

    string? FindDll(string? explicitPath, string name)
    {
        if (explicitPath != null) return File.Exists(explicitPath) ? explicitPath : null;
        var dirs = new List<string> { Path.Combine(opt.OutDir, ".data"), AppContext.BaseDirectory };
        try
        {
            var settings = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.ApplicationData), "FModel", "AppSettings.json");
            if (File.Exists(settings) &&
                JObject.Parse(File.ReadAllText(settings))["OutputDirectory"]?.ToString() is { Length: > 0 } output)
                dirs.Add(Path.Combine(output, ".data"));
        }
        catch (Exception) { /* FModel settings are only a fallback */ }
        return dirs.Select(d => Path.Combine(d, name)).FirstOrDefault(File.Exists);
    }

    /// <summary>Writes through a temporary file, so a run killed mid-write never leaves a truncated file behind.</summary>
    void WriteBytes(string path, byte[] data)
    {
        EnsureDir(Path.GetDirectoryName(path)!);
        var tmp = path + TmpSuffix;
        writeGate.Wait();
        try
        {
            File.WriteAllBytes(tmp, data);
            File.Move(tmp, path, true);
        }
        catch
        {
            try { File.Delete(tmp); } catch (IOException) { }
            throw;
        }
        finally { writeGate.Release(); }
    }

    /// <summary>Temporary files left by a run that was killed (one pass over each folder; it is a hard disk).</summary>
    void RemoveStaleTemps()
    {
        int n = 0;
        foreach (var root in new[] { exportsDir, rawDir }.Where(Directory.Exists))
            foreach (var tmp in Directory.EnumerateFiles(root, "*tmp", SearchOption.AllDirectories))
                if (tmp.EndsWith(TmpSuffix, StringComparison.OrdinalIgnoreCase) ||
                    (root == exportsDir && tmp.EndsWith(".json.tmp", StringComparison.OrdinalIgnoreCase)))
                    try { File.Delete(tmp); n++; } catch (IOException) { }
        if (n > 0) log.Info($"Removed {n} half-written files left by the interrupted run");
    }

    /// <summary>Deletes an output file; one that cannot be deleted (in use, say) is kept pending and retried next run.</summary>
    void DeleteFile(string path)
    {
        try
        {
            if (!File.Exists(path)) return;
            File.Delete(path);
            touchedDirs.TryAdd(Path.GetDirectoryName(path)!, 0);
        }
        catch (Exception e) when (e is IOException or UnauthorizedAccessException)
        {
            log.Info($"Could not delete {path}: {e.Message}");
            failedDeletes.TryAdd(Path.GetRelativePath(opt.OutDir, path), 0);
        }
    }

    void DeleteDir(string dir)
    {
        try
        {
            if (Directory.Exists(dir)) Directory.Delete(dir, true);
        }
        catch (Exception e) when (e is IOException or UnauthorizedAccessException)
        {
            log.Info($"Could not delete {dir}: {e.Message}");
            failedDeletes.TryAdd(Path.GetRelativePath(opt.OutDir, dir), 0);
        }
    }

    void EnsureDir(string dir)
    {
        if (knownDirs.ContainsKey(dir)) return;
        Directory.CreateDirectory(dir);
        knownDirs.TryAdd(dir, 0);
    }

    void PruneEmptyDirs()
    {
        foreach (var start in touchedDirs.Keys.OrderByDescending(d => d.Length))
        {
            var dir = start;
            try
            {
                while (dir.Length > Math.Max(exportsDir.Length, rawDir.Length) && Directory.Exists(dir) &&
                       !Directory.EnumerateFileSystemEntries(dir).Any())
                {
                    Directory.Delete(dir);
                    dir = Path.GetDirectoryName(dir)!;
                }
            }
            catch (Exception e) when (e is IOException or UnauthorizedAccessException)
            {
                // An empty folder that could not be removed is harmless.
            }
        }
    }

    static readonly string[] ModFolders = ["mods", "~mods", "LogicMods"];

    /// <summary>True for a pak inside a folder that holds installed mods rather than the game's own files.</summary>
    static bool InModFolder(string gameDir, string pak) =>
        Path.GetRelativePath(gameDir, Path.GetDirectoryName(pak)!).Split(Path.DirectorySeparatorChar)
            .Any(part => ModFolders.Contains(part, StringComparer.OrdinalIgnoreCase));

    /// <summary>Pads every number so that text order is numeric order: s2 sorts before s10.</summary>
    static string NaturalKey(string name) =>
        System.Text.RegularExpressions.Regex.Replace(name, @"\d+", m => m.Value.PadLeft(10, '0'));

    static bool IsUnder(string path, string root) =>
        path.Equals(root, StringComparison.OrdinalIgnoreCase) ||
        path.StartsWith(root.TrimEnd(Path.DirectorySeparatorChar) + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase);

    static readonly char[] BadNameChars = Path.GetInvalidFileNameChars();

    /// <summary>
    /// A pak path as a relative Windows path. Refuses anything that could leave the output folder: ".." or ".",
    /// a drive or stream colon, a backslash, or any other character Windows does not allow in a file name.
    /// </summary>
    static string Rel(string pakPath)
    {
        var parts = pakPath.Split('/', StringSplitOptions.RemoveEmptyEntries);
        if (parts.Length == 0 || parts.Any(p => p is "." or ".." || p.IndexOfAny(BadNameChars) >= 0))
            throw new InvalidDataException($"Unsafe path in pak: {pakPath}");
        return string.Join('\\', parts);
    }
}

/// <summary>Runs an action every interval until disposed (used for progress lines).</summary>
internal sealed class Ticker(TimeSpan every, Action action) : IDisposable
{
    readonly Timer timer = new(_ => { try { action(); } catch (Exception) { } }, null, every, every);
    public void Dispose() => timer.Dispose();
}
