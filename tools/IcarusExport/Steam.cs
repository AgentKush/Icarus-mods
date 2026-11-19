using System.Text.RegularExpressions;
using Microsoft.Win32;

namespace IcarusExport;

/// <summary>Finds Icarus through Steam and reads its app manifest (build id, install state).</summary>
internal static class Steam
{
    public const string AppId = "1149460";

    public sealed record Manifest(string? BuildId, string? StateFlags, string? InstallDir, long LastUpdated)
    {
        /// <summary>StateFlags 4 = fully installed. Anything else means Steam is updating, validating or downloading.</summary>
        public bool FullyInstalled => StateFlags == "4";
    }

    public sealed record Install(string GameDir, string? ManifestPath);

    public static Install? Find(string? gameDirOverride)
    {
        if (gameDirOverride != null)
        {
            // An explicit folder: still look for its manifest so the build id is known.
            var lib = Directory.GetParent(gameDirOverride)?.Parent?.Parent?.FullName; // <lib>\steamapps\common\Icarus
            var acf = lib == null ? null : Path.Combine(lib, "steamapps", $"appmanifest_{AppId}.acf");
            return new Install(gameDirOverride, acf != null && File.Exists(acf) ? acf : null);
        }
        foreach (var lib in Libraries())
        {
            var acf = Path.Combine(lib, "steamapps", $"appmanifest_{AppId}.acf");
            if (!File.Exists(acf)) continue;
            var m = ReadManifest(acf);
            var dir = Path.Combine(lib, "steamapps", "common", m.InstallDir ?? "Icarus");
            if (Directory.Exists(dir)) return new Install(dir, acf);
        }
        return null;
    }

    public static Manifest ReadManifest(string acfPath)
    {
        var values = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        foreach (Match m in Regex.Matches(File.ReadAllText(acfPath), "\"([^\"]+)\"\\s+\"([^\"]*)\""))
            values.TryAdd(m.Groups[1].Value, m.Groups[2].Value);
        long.TryParse(values.GetValueOrDefault("lastupdated"), out var lu);
        return new Manifest(values.GetValueOrDefault("buildid"), values.GetValueOrDefault("StateFlags"),
            values.GetValueOrDefault("installdir"), lu);
    }

    static IEnumerable<string> Libraries()
    {
        var steamRoots = new List<string>();
        if (OperatingSystem.IsWindows())
        {
            foreach (var (hive, key, name) in new[]
                     {
                         (Registry.CurrentUser, @"Software\Valve\Steam", "SteamPath"),
                         (Registry.LocalMachine, @"SOFTWARE\WOW6432Node\Valve\Steam", "InstallPath"),
                     })
            {
                if (hive.OpenSubKey(key)?.GetValue(name) is string p && Directory.Exists(p))
                    steamRoots.Add(Path.GetFullPath(p));
            }
        }
        steamRoots.Add(@"C:\Program Files (x86)\Steam");

        var seen = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        foreach (var root in steamRoots)
        {
            if (seen.Add(root)) yield return root;
            var vdf = Path.Combine(root, "steamapps", "libraryfolders.vdf");
            if (!File.Exists(vdf)) continue;
            foreach (Match m in Regex.Matches(File.ReadAllText(vdf), "\"path\"\\s+\"([^\"]+)\""))
            {
                var lib = m.Groups[1].Value.Replace(@"\\", @"\");
                if (Directory.Exists(lib) && seen.Add(Path.GetFullPath(lib))) yield return Path.GetFullPath(lib);
            }
        }
    }

    public static bool GameRunning() =>
        new[] { "Icarus-Win64-Shipping", "Icarus" }
            .Any(n => System.Diagnostics.Process.GetProcessesByName(n).Length > 0);
}
