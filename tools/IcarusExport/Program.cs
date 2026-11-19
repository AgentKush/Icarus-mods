using System.Diagnostics;
using System.Reflection;

namespace IcarusExport;

internal static class Program
{
    static int Main(string[] args)
    {
        Options opt;
        try
        {
            opt = Options.Parse(args);
        }
        catch (Exception e) when (e is ArgumentException or FormatException)
        {
            Console.Error.WriteLine(e.Message);
            Console.Error.WriteLine();
            Console.Error.WriteLine(Options.Usage);
            return 2;
        }

        using var log = new Log();
        try
        {
            return Run(opt, log);
        }
        catch (Exception e)
        {
            // Notify first: if the log itself is what failed, the notification still goes out.
            if ((opt.Scheduled || opt.Notify) && !opt.NoNotify)
                Toast.Show("Icarus export failed", e.Message, log.FilePath ?? "", log);
            log.Info($"FAILED: {e}");
            return 1;
        }
    }

    static int Run(Options opt, Log log)
    {
        if (opt.Help)
        {
            Console.WriteLine(Options.Usage);
            return 0;
        }
        if (opt.TestNotify)
        {
            Toast.Show("Icarus build 12345678 exported", "This is what the export notification looks like.", "IcarusExport", log);
            return 0;
        }

        var logDir = Path.Combine(opt.OutDir, "Logs", "IcarusExport");
        using var mutex = new Mutex(false, @"Local\IcarusExport");
        bool owned;
        try { owned = mutex.WaitOne(0); }
        catch (AbandonedMutexException) { owned = true; }
        if (!owned)
        {
            Note(opt, log, logDir, "Another export is already running.");
            return 0;
        }
        try
        {
            var game = Steam.Find(opt.GameDir)
                       ?? throw new DirectoryNotFoundException("Icarus was not found in any Steam library. Pass --game <folder>.");
            var manifest = game.ManifestPath != null ? Steam.ReadManifest(game.ManifestPath) : null;
            var state = ExportState.Load(opt.OutDir);

            if (opt.Scheduled)
            {
                string? skip =
                    manifest == null ? "No Steam manifest for Icarus, so the build cannot be checked."
                    : !manifest.FullyInstalled ? $"Steam is still updating Icarus (StateFlags {manifest.StateFlags}); will check again later."
                    : state.Complete && state.BuildId == manifest.BuildId ? $"Build {manifest.BuildId} is already exported."
                    : Steam.GameRunning()
                        ? state.BuildId == manifest.BuildId
                            ? $"Build {manifest.BuildId} was only partly exported, but Icarus is running; will export it fully after it closes."
                            : $"Build {manifest.BuildId} is new, but Icarus is running; will export after it closes."
                    : null;
                if (skip != null)
                {
                    Note(opt, log, logDir, skip);
                    return 0;
                }
                Note(opt, log, logDir, state.BuildId == manifest!.BuildId
                    ? $"Build {manifest.BuildId} was only partly exported last time; exporting it fully."
                    : $"Build {manifest.BuildId} is new (last exported: {state.Basis?.BuildId ?? (state.Complete ? state.BuildId : null) ?? "none"}); exporting.");
            }
            // Below normal: the export only gets CPU time other programs are not using.
            try { Process.GetCurrentProcess().PriorityClass = ProcessPriorityClass.BelowNormal; }
            catch (Exception) { /* not important */ }

            log.OpenFile(Path.Combine(logDir, $"{DateTime.Now:yyyy-MM-dd_HHmmss}.log"));
            Log.Prune(logDir, "20*.log", 30);
            var version = Assembly.GetExecutingAssembly().GetName().Version?.ToString(3);
            log.Info($"IcarusExport {version} (CUE4Parse {Exporter.Cue4ParseVersion}), {opt.Threads} threads");
            log.Info($"Game: {game.GameDir} (build {manifest?.BuildId ?? "unknown"})");
            log.Info($"Output: {opt.OutDir}");
            if (state.Complete)
                log.Info($"Last export: build {state.BuildId}, {state.ExportedAt:yyyy-MM-dd HH:mm}");
            else if (state.BuildId != null)
                log.Info($"The last run (build {state.BuildId}) was partial or did not finish; comparing with the last complete export " +
                         (state.Basis != null ? $"(build {state.Basis.BuildId}, {state.Basis.ExportedAt:yyyy-MM-dd HH:mm})" : "(none yet)"));

            var exporter = new Exporter(opt, log);
            var (result, next) = exporter.Run(game, manifest?.BuildId, state);
            next.LastRunAt = DateTime.Now;
            next.Tool = $"IcarusExport {version} / CUE4Parse {Exporter.Cue4ParseVersion}";
            next.Save(opt.OutDir);
            exporter.CommitTableSnapshot();          // only once the state that matches it is on disk
            Exporter.ClearRunMarker(opt.OutDir);
            if (result.Partial)
                log.Info("This was a partial run (--paks, --no-raw, --no-json, or a pak could not be read), so the build does not " +
                         "count as exported yet: the next full run compares with the last complete export again.");

            var (reportPath, summary) = Report.Write(result);
            log.Info($"Done in {Fmt.Time(result.Duration)}. {summary}");
            if (reportPath != null) log.Info($"Report: {reportPath}");
            foreach (var w in result.Warnings) log.Info($"Warning: {w}");
            if (opt.Scheduled) Note(opt, log, logDir, $"Exported build {manifest?.BuildId}: {summary}");

            if ((opt.Scheduled || opt.Notify) && !opt.NoNotify)
                Toast.Show($"Icarus build {manifest?.BuildId ?? "?"} exported", summary,
                    reportPath != null ? $"Report: {Path.GetRelativePath(opt.OutDir, reportPath)}" : $"Output: {opt.OutDir}", log);
            return 0;
        }
        finally
        {
            mutex.ReleaseMutex();
        }
    }

    /// <summary>One line in Logs\IcarusExport\scheduled.log, which records every scheduled check.</summary>
    static void Note(Options opt, Log log, string logDir, string message)
    {
        log.Info(message);
        if (!opt.Scheduled) return;
        try
        {
            Directory.CreateDirectory(logDir);
            var path = Path.Combine(logDir, "scheduled.log");
            if (File.Exists(path) && new FileInfo(path).Length > 1_000_000)
                File.WriteAllLines(path, File.ReadAllLines(path).TakeLast(2000));
            File.AppendAllText(path, $"{DateTime.Now:yyyy-MM-dd HH:mm:ss} {message}{Environment.NewLine}");
        }
        catch (IOException) { }
    }
}
