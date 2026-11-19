using Newtonsoft.Json;

namespace IcarusExport;

/// <summary>
/// What is on disk, kept in &lt;out&gt;\.icarusexport\state.json. It lets the next run write only what changed,
/// delete what the game removed, and report the difference.
/// </summary>
internal sealed class ExportState
{
    public int Version { get; set; } = 2;
    /// <summary>The build the files on disk were last updated from (also after a partial or unfinished run).</summary>
    public string? BuildId { get; set; }
    /// <summary>When the last complete export finished; null until one has.</summary>
    public DateTime? ExportedAt { get; set; }
    public DateTime? LastRunAt { get; set; }
    public string? Tool { get; set; }
    /// <summary>
    /// Format of the asset JSON on disk ("revision:CUE4Parse version"). It moves on only when a complete run
    /// finishes, so a partial run in a new format still leaves the next full run re-serialising everything.
    /// </summary>
    public string? JsonFormat { get; set; }
    /// <summary>
    /// True when the last run was a complete export: every pak, raw files and JSON, every pak readable, and not
    /// interrupted. A partial or unfinished run leaves it false, so the scheduled task exports the build again.
    /// </summary>
    public bool Complete { get; set; }
    /// <summary>Pak key -> its size, timestamp and a hash of every file in it, as on disk now.</summary>
    public Dictionary<string, PakState> Paks { get; set; } = new(StringComparer.OrdinalIgnoreCase);
    /// <summary>Asset path without extension -> hash of the JSON on disk now.</summary>
    public Dictionary<string, string> Json { get; set; } = new(StringComparer.OrdinalIgnoreCase);
    /// <summary>
    /// The last complete export, kept while a run is unfinished or partial. The next run compares against it, so
    /// the changes of an interrupted run are still re-serialised and reported rather than taken as done.
    /// </summary>
    public ExportBasis? Basis { get; set; }
    /// <summary>Files whose JSON failed last time. The next run serialises them again whatever their inputs.</summary>
    public HashSet<string> RetryJson { get; set; } = new(StringComparer.OrdinalIgnoreCase);
    /// <summary>Output files and folders (relative to the export folder) that could not be deleted; retried every run.</summary>
    public HashSet<string> PendingDeletes { get; set; } = new(StringComparer.OrdinalIgnoreCase);

    public static string PathFor(string outDir) => Path.Combine(outDir, ".icarusexport", "state.json");
    /// <summary>Exists while a run is in progress, so the next run knows to clean up after one that was killed.</summary>
    public static string RunMarkerFor(string outDir) => Path.Combine(outDir, ".icarusexport", "running");

    public static ExportState Load(string outDir)
    {
        var path = PathFor(outDir);
        if (!File.Exists(path)) return new ExportState();
        ExportState state;
        using (var reader = new JsonTextReader(new StreamReader(path)))
            state = JsonSerializer.CreateDefault().Deserialize<ExportState>(reader) ?? new ExportState();
        // Version 1 recorded only CUE4Parse's assembly version, which monthly releases do not change. Every
        // export made before version 2 used CUE4Parse 1.2.2.202611, so that is the format of its JSON.
        if (state.JsonFormat == "1.2.2.0") state.JsonFormat = Exporter.FormatOf(Exporter.Cue4Parse1_2_2_202611);
        return state;
    }

    public void Save(string outDir)
    {
        var path = PathFor(outDir);
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        var tmp = path + ".tmp";
        using (var w = new StreamWriter(tmp, false, new System.Text.UTF8Encoding(false)))
        using (var jw = new JsonTextWriter(w) { Formatting = Formatting.Indented })
            JsonSerializer.CreateDefault().Serialize(jw, this);
        File.Move(tmp, path, true);
    }
}

/// <summary>A complete export: what a run compares against.</summary>
internal sealed class ExportBasis
{
    public string? BuildId { get; set; }
    public DateTime? ExportedAt { get; set; }
    public Dictionary<string, PakState> Paks { get; set; } = new(StringComparer.OrdinalIgnoreCase);
    public Dictionary<string, string> Json { get; set; } = new(StringComparer.OrdinalIgnoreCase);

    public static ExportBasis Of(ExportState s) =>
        new() { BuildId = s.BuildId, ExportedAt = s.ExportedAt, Paks = s.Paks, Json = s.Json };

    /// <summary>Identifies the basis, e.g. in the marker of the saved data-table copies.</summary>
    public string Marker => $"{BuildId}|{ExportedAt?.ToUniversalTime().Ticks}";
}

internal sealed class PakState
{
    public long Size { get; set; }
    /// <summary>The pak's timestamp; 0 forces the next run to read the pak again (set when some of its files failed).</summary>
    public long MTime { get; set; }
    /// <summary>True when Raw\&lt;pak&gt;\ was written from these hashes (false after a --no-raw run).</summary>
    public bool Raw { get; set; }
    public Dictionary<string, string> Files { get; set; } = new(StringComparer.OrdinalIgnoreCase);
}
