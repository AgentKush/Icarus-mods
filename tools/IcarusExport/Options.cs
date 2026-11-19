namespace IcarusExport;

internal sealed class Options
{
    public const string DefaultOut = @"D:\Fmod Exports for Icarus";

    public string? GameDir { get; private set; }
    public string OutDir { get; private set; } = DefaultOut;
    public string? Baseline { get; private set; }
    public string? OodlePath { get; private set; }
    public bool Scheduled { get; private set; }
    public bool Full { get; private set; }
    public bool NoRaw { get; private set; }
    public bool NoJson { get; private set; }
    public bool Notify { get; private set; }
    public bool NoNotify { get; private set; }
    public bool AllowMassDelete { get; private set; }
    public bool TestNotify { get; private set; }
    public bool Help { get; private set; }
    public List<string> PakFilters { get; } = new();
    public int Threads { get; private set; }
    public int WriteThreads { get; private set; } = 4;

    public const string Usage = """
        IcarusExport - exports Icarus's paks as raw files and FModel-style JSON.

        Usage: IcarusExport [options]

          --out <dir>          Export root (default: D:\Fmod Exports for Icarus)
                                 Exports\   merged JSON: data tables + one .json per asset (FModel layout)
                                 Raw\<pak>\ every file exactly as stored, one folder per pak
                                 Reports\   what changed, one report per run
          --game <dir>         Icarus install folder (default: found through Steam)
          --scheduled          For the scheduled task: export only when Steam has installed a new
                               Icarus build, never while the game is running, then show a notification
          --full               Ignore the saved state: re-read every pak and re-serialise every asset
          --no-raw             Skip the Raw\ folder
          --no-json            Skip asset JSON (data tables are still copied)
          --paks <list>        Only export these paks, e.g. data,pakchunk0_s33* (all are still mounted)
          --baseline <dir>     An older export to compare data tables and asset lists with when
                               there is no saved state yet (first run)
          --oodle <file>       oodle-data-shared.dll (default: <out>\.data\ or FModel's .data folder)
          --threads <n>        Worker threads (default: cores - 4, or half the cores when scheduled)
          --write-threads <n>  Files written at once (default 4; the export drive is a hard disk)
          --notify             Show the notification after a manual run too
          --no-notify          Never show a notification
          --allow-mass-delete  Delete outputs even if more than 10% of assets seem to have vanished
          --test-notify        Show a sample notification and exit
        """;

    public static Options Parse(string[] args)
    {
        var o = new Options();
        for (int i = 0; i < args.Length; i++)
        {
            string a = args[i];
            string Next() => i + 1 < args.Length ? args[++i] : throw new ArgumentException($"{a} needs a value");
            switch (a.ToLowerInvariant())
            {
                case "--out": o.OutDir = Path.GetFullPath(Next()); break;
                case "--game": o.GameDir = Path.GetFullPath(Next()); break;
                case "--baseline": o.Baseline = Path.GetFullPath(Next()); break;
                case "--oodle": o.OodlePath = Path.GetFullPath(Next()); break;
                case "--scheduled": o.Scheduled = true; break;
                case "--full": o.Full = true; break;
                case "--no-raw": o.NoRaw = true; break;
                case "--no-json": o.NoJson = true; break;
                case "--notify": o.Notify = true; break;
                case "--no-notify": o.NoNotify = true; break;
                case "--allow-mass-delete": o.AllowMassDelete = true; break;
                case "--test-notify": o.TestNotify = true; break;
                case "--paks":
                    o.PakFilters.AddRange(Next().Split(',', StringSplitOptions.RemoveEmptyEntries | StringSplitOptions.TrimEntries)
                        .Select(p => p.EndsWith(".pak", StringComparison.OrdinalIgnoreCase) ? p[..^4] : p));
                    break;
                case "--threads": o.Threads = int.Parse(Next()); break;
                case "--write-threads": o.WriteThreads = Math.Max(1, int.Parse(Next())); break;
                case "-h": case "--help": case "/?": o.Help = true; break;
                default: throw new ArgumentException($"Unknown option: {a}");
            }
        }
        if (o.Threads <= 0)
            o.Threads = o.Scheduled ? Math.Max(2, Environment.ProcessorCount / 2) : Math.Max(2, Environment.ProcessorCount - 4);
        return o;
    }

    /// <summary>True when the pak (name without .pak) is selected by --paks, or when no filter was given.</summary>
    public bool Selects(string pakKey) =>
        PakFilters.Count == 0 || PakFilters.Any(f => Wildcard(f, pakKey));

    static bool Wildcard(string pattern, string text) =>
        System.Text.RegularExpressions.Regex.IsMatch(text,
            "^" + System.Text.RegularExpressions.Regex.Escape(pattern).Replace(@"\*", ".*").Replace(@"\?", ".") + "$",
            System.Text.RegularExpressions.RegexOptions.IgnoreCase);
}
