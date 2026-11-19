using System.Text;
using Newtonsoft.Json.Linq;

namespace IcarusExport;

/// <summary>How one data table differs from the previous export, row by row.</summary>
internal sealed class TableChange
{
    public string Path = "";
    public string Kind = "changed"; // added | removed | changed
    public readonly List<string> RowsAdded = new(), RowsRemoved = new(), RowsChanged = new();
    public bool DefaultsChanged, StructChanged, OtherChanged;
    public string? Note;

    public static TableChange Added(string path) => new() { Path = path, Kind = "added" };
    public static TableChange Removed(string path) => new() { Path = path, Kind = "removed" };

    /// <summary>Null when the two files hold the same data (only formatting differs).</summary>
    public static TableChange? Compare(string path, byte[] oldBytes, byte[] newBytes)
    {
        JToken o, n;
        try
        {
            o = Parse(oldBytes);
            n = Parse(newBytes);
        }
        catch (Exception e)
        {
            return new TableChange { Path = path, OtherChanged = true, Note = $"could not be parsed ({e.Message})" };
        }
        if (JToken.DeepEquals(o, n)) return null;

        var c = new TableChange { Path = path };
        if (o is JObject oo && n is JObject no && oo["Rows"] is JArray oldRows && no["Rows"] is JArray newRows)
        {
            var before = Rows(oldRows);
            var after = Rows(newRows);
            foreach (var (name, row) in after)
            {
                if (!before.TryGetValue(name, out var was)) c.RowsAdded.Add(name);
                else if (!JToken.DeepEquals(was, row)) c.RowsChanged.Add(name);
            }
            c.RowsRemoved.AddRange(before.Keys.Where(k => !after.ContainsKey(k)));
            c.DefaultsChanged = !JToken.DeepEquals(oo["Defaults"], no["Defaults"]);
            c.StructChanged = !JToken.DeepEquals(oo["RowStruct"], no["RowStruct"]);
            c.OtherChanged = oo.Properties().Select(p => p.Name).Union(no.Properties().Select(p => p.Name))
                .Except(["Rows", "Defaults", "RowStruct"]).Any(k => !JToken.DeepEquals(oo[k], no[k]));
            if (c.RowsAdded.Count + c.RowsRemoved.Count + c.RowsChanged.Count == 0 && !c.DefaultsChanged && !c.StructChanged && !c.OtherChanged)
                c.Note = "only the order of rows changed";
        }
        else
        {
            c.OtherChanged = true;
        }
        return c;
    }

    static Dictionary<string, JToken> Rows(JArray rows)
    {
        var d = new Dictionary<string, JToken>(StringComparer.Ordinal);
        int i = 0;
        foreach (var row in rows)
        {
            var name = (row as JObject)?["Name"]?.ToString();
            d.TryAdd(string.IsNullOrEmpty(name) ? $"(row {i})" : name, row);
            i++;
        }
        return d;
    }

    static JToken Parse(byte[] bytes) => JToken.Parse(Encoding.UTF8.GetString(bytes).TrimStart('﻿'));

    public string Describe()
    {
        if (Kind == "added") return "new table";
        if (Kind == "removed") return "table removed";
        var parts = new List<string>();
        if (RowsAdded.Count > 0) parts.Add(Fmt.Plural(RowsAdded.Count, "row added", "rows added"));
        if (RowsRemoved.Count > 0) parts.Add(Fmt.Plural(RowsRemoved.Count, "row removed", "rows removed"));
        if (RowsChanged.Count > 0) parts.Add(Fmt.Plural(RowsChanged.Count, "row changed", "rows changed"));
        if (DefaultsChanged) parts.Add("defaults changed");
        if (StructChanged) parts.Add("row struct changed");
        if (OtherChanged) parts.Add("other content changed");
        if (Note != null) parts.Add(Note);
        return string.Join(", ", parts);
    }
}

/// <summary>Writes Reports\&lt;date&gt;-build&lt;id&gt;.md and a -files.txt with the complete lists.</summary>
internal static class Report
{
    const int MaxAssets = 300, MaxRows = 60;

    public static (string? Path, string Summary) Write(RunResult r)
    {
        var summary = Summary(r);
        if (r.NothingChanged && r.Warnings.Count == 0) return (null, summary);

        var dir = Path.Combine(r.OutDir, "Reports");
        Directory.CreateDirectory(dir);
        var stem = $"{DateTime.Now:yyyy-MM-dd}-build{r.BuildId ?? "unknown"}";
        var md = Path.Combine(dir, stem + ".md");
        for (int n = 2; File.Exists(md); n++) md = Path.Combine(dir, $"{stem}-{n}.md");
        var listPath = md[..^3] + "-files.txt";
        var listName = Path.GetFileName(listPath);

        var s = new StringBuilder();
        s.AppendLine($"# Icarus export: build {r.BuildId ?? "unknown"}").AppendLine();
        s.AppendLine(summary).AppendLine();
        s.AppendLine("| | |").AppendLine("|---|---|");
        s.AppendLine($"| Exported | {DateTime.Now:yyyy-MM-dd HH:mm}, took {Fmt.Time(r.Duration)} |");
        if (r.FirstRun)
            s.AppendLine($"| Previous export | none (first run of IcarusExport){(r.Baseline != null ? $"; compared with `{r.Baseline}`" : "")} |");
        else
            s.AppendLine($"| Previous export | build {r.PrevBuildId ?? "?"}, {r.PrevExportedAt:yyyy-MM-dd HH:mm} |");
        s.AppendLine($"| Game | `{r.GameDir}` |");
        s.AppendLine($"| Output | `{r.OutDir}` |");
        s.AppendLine($"| Paks | {r.PaksMounted} mounted, {r.PaksRead} read, {r.PaksUnchanged} unchanged" +
                     (r.PaksAdded.Count > 0 ? $"; new: {string.Join(", ", r.PaksAdded)}" : "") +
                     (r.PaksRemoved.Count > 0 ? $"; removed: {string.Join(", ", r.PaksRemoved)}" : "") +
                     (r.Filtered ? " (only some paks were selected)" : "") + " |");
        s.AppendLine($"| Asset JSON | {(r.JsonSkipped ? "skipped (--no-json)" : r.JsonMode)} |");
        s.AppendLine();

        s.AppendLine("## Summary").AppendLine();
        s.AppendLine("| | New | Changed | Removed |").AppendLine("|---|---:|---:|---:|");
        int tAdded = r.Tables.Count(t => t.Kind == "added"), tRemoved = r.Tables.Count(t => t.Kind == "removed");
        s.AppendLine($"| Data tables | {tAdded} | {r.Tables.Count - tAdded - tRemoved} | {tRemoved} |");
        if (r.FirstRun)
        {
            s.AppendLine($"| Asset JSON | {(r.Baseline != null && r.BaselineAssetsAdded.Count + r.BaselineAssetsRemoved.Count > 0 ? Fmt.N(r.BaselineAssetsAdded.Count) : "-")} | - | {(r.Baseline != null ? Fmt.N(r.BaselineAssetsRemoved.Count) : "-")} |");
            s.AppendLine();
            s.AppendLine($"First export: {Fmt.N(r.DocsSelected)} JSON files and {(r.RawSkipped ? "no" : Fmt.N(r.FilesSelected))} raw files." +
                         (r.Baseline != null ? " New and removed are counted against the baseline folder." : ""));
        }
        else
        {
            s.AppendLine($"| Asset JSON | {Fmt.N(r.JsonAdded.Count)} | {Fmt.N(r.JsonChanged.Count)} | {Fmt.N(r.JsonRemoved.Count)} |");
            s.AppendLine($"| Raw files | {Fmt.N(r.RawAdded.Count)} | {Fmt.N(r.RawChanged.Count)} | {Fmt.N(r.RawRemoved.Count)} |");
        }
        s.AppendLine();

        if (r.Warnings.Count > 0)
        {
            s.AppendLine("## Warnings").AppendLine();
            foreach (var w in r.Warnings) s.AppendLine($"- {w}");
            s.AppendLine();
        }

        if (r.Tables.Count > 0)
        {
            s.AppendLine($"## Data tables ({r.Tables.Count})").AppendLine();
            foreach (var t in r.Tables.OrderBy(t => t.Path, StringComparer.OrdinalIgnoreCase))
            {
                s.AppendLine($"**{t.Path.Replace('\\', '/')}**: {t.Describe()}").AppendLine();
                Rows(s, "Added", t.RowsAdded);
                Rows(s, "Changed", t.RowsChanged);
                Rows(s, "Removed", t.RowsRemoved);
                if (t.RowsAdded.Count + t.RowsChanged.Count + t.RowsRemoved.Count > 0) s.AppendLine();
            }
        }

        if (r.FirstRun)
        {
            Assets(s, "New since the baseline", r.BaselineAssetsAdded, listName);
            Assets(s, "Gone since the baseline", r.BaselineAssetsRemoved, listName);
        }
        else
        {
            Assets(s, "New assets", r.JsonAdded.Order(StringComparer.OrdinalIgnoreCase).ToList(), listName);
            Assets(s, "Removed assets", r.JsonRemoved, listName);
            Assets(s, "Changed assets", r.JsonChanged.Order(StringComparer.OrdinalIgnoreCase).ToList(), listName, 150);
        }

        if (!r.Errors.IsEmpty)
        {
            s.AppendLine($"## Errors ({r.Errors.Count})").AppendLine();
            s.AppendLine("These files could not be read or serialised. Any older output for them was kept.").AppendLine();
            foreach (var (path, error) in r.Errors.OrderBy(e => e.Path, StringComparer.OrdinalIgnoreCase).Take(100))
                s.AppendLine($"- `{path}`: {error}");
            if (r.Errors.Count > 100) s.AppendLine($"- ...and {r.Errors.Count - 100} more in {listName}");
            s.AppendLine();
        }
        File.WriteAllText(md, s.ToString(), new UTF8Encoding(false));

        var l = new StringBuilder();
        void Section(string title, IEnumerable<string> items)
        {
            var list = items.Order(StringComparer.OrdinalIgnoreCase).ToList();
            if (list.Count == 0) return;
            l.AppendLine($"[{title}] {list.Count}");
            foreach (var i in list) l.AppendLine(i);
            l.AppendLine();
        }
        Section("data tables", r.Tables.Select(t => $"{t.Path.Replace('\\', '/')}: {t.Describe()}"));
        Section("new assets", r.FirstRun ? r.BaselineAssetsAdded : r.JsonAdded);
        Section("removed assets", r.FirstRun ? r.BaselineAssetsRemoved : r.JsonRemoved);
        Section("changed assets", r.JsonChanged);
        Section("new raw files", r.RawAdded);
        Section("changed raw files", r.RawChanged);
        Section("removed raw files", r.RawRemoved);
        Section("errors", r.Errors.Select(e => $"{e.Path}: {e.Error}"));
        if (l.Length > 0) File.WriteAllText(listPath, l.ToString(), new UTF8Encoding(false));
        return (md, summary);
    }

    /// <summary>One sentence for the notification and the top of the report.</summary>
    public static string Summary(RunResult r)
    {
        int tables = r.Tables.Count;
        string t = tables == 0 ? "no data tables changed" : $"{Fmt.Plural(tables, "data table", "data tables")} changed";
        string s =
            r.FirstRun
                ? $"First export: {Fmt.N(r.DocsSelected)} JSON files and {(r.RawSkipped ? "no" : Fmt.N(r.FilesSelected))} raw files" +
                  (r.Baseline != null ? $"; against the baseline, {t}, {Fmt.N(r.BaselineAssetsAdded.Count)} assets new, {Fmt.N(r.BaselineAssetsRemoved.Count)} gone." : ".")
                : r.NothingChanged
                    ? "Nothing changed since the last export."
                    : $"{char.ToUpperInvariant(t[0])}{t[1..]}; assets: {Fmt.N(r.JsonAdded.Count)} new, {Fmt.N(r.JsonChanged.Count)} changed, {Fmt.N(r.JsonRemoved.Count)} removed.";
        if (!r.Errors.IsEmpty) s += $" {Fmt.Plural(r.Errors.Count, "error", "errors")}.";
        if (r.Warnings.Count > 0) s += $" {Fmt.Plural(r.Warnings.Count, "warning", "warnings")}.";
        if (r.Partial) s += " Partial run: the build is not counted as exported yet.";
        return s;
    }

    static void Rows(StringBuilder s, string label, List<string> rows)
    {
        if (rows.Count == 0) return;
        var shown = string.Join(", ", rows.Take(MaxRows).Select(x => $"`{x}`"));
        s.AppendLine($"- {label}: {shown}{(rows.Count > MaxRows ? $", ...and {rows.Count - MaxRows} more" : "")}");
    }

    static void Assets(StringBuilder s, string title, IReadOnlyList<string> items, string listName, int max = MaxAssets)
    {
        if (items.Count == 0) return;
        s.AppendLine($"## {title} ({Fmt.N(items.Count)})").AppendLine();
        foreach (var i in items.Take(max)) s.AppendLine($"- `{i}`");
        if (items.Count > max) s.AppendLine($"- ...and {Fmt.N(items.Count - max)} more in {listName}");
        s.AppendLine();
    }
}
