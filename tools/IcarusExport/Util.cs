using System.Diagnostics;
using System.IO.Hashing;
using System.Text;

namespace IcarusExport;

/// <summary>
/// Writes to the console and to a log file. IcarusExportBackground.exe (the scheduled task's copy)
/// has no console, so there the console lines simply go nowhere.
/// </summary>
internal sealed class Log : IDisposable
{
    readonly object gate = new();
    StreamWriter? file;
    public bool ToConsole { get; set; } = true;
    public string? FilePath { get; private set; }

    public void OpenFile(string path)
    {
        Directory.CreateDirectory(Path.GetDirectoryName(path)!);
        file = new StreamWriter(path, true, new UTF8Encoding(false)) { AutoFlush = true };
        FilePath = path;
    }

    public void Info(string message)
    {
        var line = $"{DateTime.Now:HH:mm:ss} {message}";
        lock (gate)
        {
            // A full disk or a locked log must not stop the export itself.
            try { file?.WriteLine(line); } catch (Exception e) when (e is IOException or ObjectDisposedException) { }
            try { if (ToConsole) Console.WriteLine(line); } catch (IOException) { }
        }
    }

    public void Dispose() { lock (gate) { file?.Dispose(); file = null; } }

    /// <summary>Keeps the newest <paramref name="keep"/> files matching the pattern.</summary>
    public static void Prune(string dir, string pattern, int keep)
    {
        if (!Directory.Exists(dir)) return;
        foreach (var f in new DirectoryInfo(dir).GetFiles(pattern).OrderByDescending(f => f.LastWriteTimeUtc).Skip(keep))
            try { f.Delete(); } catch (IOException) { }
    }
}

/// <summary>Passes bytes through to another stream (or nowhere) while hashing them.</summary>
internal sealed class HashingStream(Stream inner) : Stream
{
    readonly XxHash3 hash = new();
    public long Written { get; private set; }
    public string Hex => Hashes.ToHex(hash.GetCurrentHashAsUInt64());

    public override void Write(byte[] buffer, int offset, int count) => Write(buffer.AsSpan(offset, count));
    public override void Write(ReadOnlySpan<byte> buffer)
    {
        hash.Append(buffer);
        Written += buffer.Length;
        inner.Write(buffer);
    }
    public override void Flush() => inner.Flush();
    public override bool CanRead => false;
    public override bool CanSeek => false;
    public override bool CanWrite => true;
    public override long Length => Written;
    public override long Position { get => Written; set => throw new NotSupportedException(); }
    public override int Read(byte[] buffer, int offset, int count) => throw new NotSupportedException();
    public override long Seek(long offset, SeekOrigin origin) => throw new NotSupportedException();
    public override void SetLength(long value) => throw new NotSupportedException();
    protected override void Dispose(bool disposing) { if (disposing) inner.Dispose(); base.Dispose(disposing); }
}

internal static class Hashes
{
    public static string Of(ReadOnlySpan<byte> data) => ToHex(XxHash3.HashToUInt64(data));
    public static string ToHex(ulong h) => h.ToString("x16");
}

/// <summary>Windows toast notification, shown through Windows PowerShell's registered app id.</summary>
internal static class Toast
{
    const string Script = """
        $ErrorActionPreference = 'Stop'
        [void][Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime]
        [void][Windows.Data.Xml.Dom.XmlDocument, Windows.Data.Xml.Dom.XmlDocument, ContentType = WindowsRuntime]
        $x = New-Object Windows.Data.Xml.Dom.XmlDocument
        $x.LoadXml('<toast><visual><binding template="ToastGeneric"><text/><text/><text/></binding></visual></toast>')
        $t = $x.GetElementsByTagName('text')
        [void]$t.Item(0).AppendChild($x.CreateTextNode($env:IE_TOAST_TITLE))
        [void]$t.Item(1).AppendChild($x.CreateTextNode($env:IE_TOAST_BODY))
        [void]$t.Item(2).AppendChild($x.CreateTextNode($env:IE_TOAST_FOOT))
        $app = '{1AC14E77-02E7-4E5D-B744-2EB1AE5198B7}\WindowsPowerShell\v1.0\powershell.exe'
        [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier($app).Show((New-Object Windows.UI.Notifications.ToastNotification $x))
        """;

    public static void Show(string title, string body, string foot, Log log)
    {
        try
        {
            var psi = new ProcessStartInfo(Path.Combine(Environment.SystemDirectory, @"WindowsPowerShell\v1.0\powershell.exe"))
            {
                UseShellExecute = false,
                CreateNoWindow = true,
                RedirectStandardOutput = true,
                RedirectStandardError = true,
            };
            foreach (var a in new[] { "-NoProfile", "-NonInteractive", "-Command", Script }) psi.ArgumentList.Add(a);
            psi.Environment["IE_TOAST_TITLE"] = title;
            psi.Environment["IE_TOAST_BODY"] = body;
            psi.Environment["IE_TOAST_FOOT"] = foot;
            using var p = Process.Start(psi)!;
            var err = p.StandardError.ReadToEnd();
            p.WaitForExit(30_000);
            if (p.ExitCode != 0) log.Info($"Notification failed: {err.Trim()}");
        }
        catch (Exception e)
        {
            log.Info($"Notification failed: {e.Message}");
        }
    }
}

internal static class Fmt
{
    public static string N(long n) => n.ToString("N0", System.Globalization.CultureInfo.InvariantCulture);
    public static string Gb(long bytes) => (bytes / 1e9).ToString("0.0", System.Globalization.CultureInfo.InvariantCulture) + " GB";
    public static string Time(TimeSpan t) => t.TotalHours >= 1 ? $"{(int)t.TotalHours}h {t.Minutes:00}m" : t.TotalMinutes >= 1 ? $"{(int)t.TotalMinutes}m {t.Seconds:00}s" : $"{t.TotalSeconds:0.0}s";
    public static string Plural(long n, string one, string many) => $"{N(n)} {(n == 1 ? one : many)}";
}
