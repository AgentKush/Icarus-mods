# IcarusExport

Exports Icarus's game files after every Steam update, so nobody has to click through FModel each week. It reads the game's paks with [CUE4Parse](https://github.com/FabianFG/CUE4Parse), the library FModel is built on. The JSON it writes is byte-for-byte what FModel's **Save Properties** produces.

## What you get

Everything goes into one export folder (default `D:\Fmod Exports for Icarus`):

| Folder | Contents |
|---|---|
| `Exports\` | The same layout as an FModel export, which `check_mod.py` reads. Data tables are at `Exports\<Category>\D_*.json`. Assets are at `Exports\Icarus\Content\...\<Asset>.json`, and `.ini`/`.uplugin`/`.locres` and similar files are saved as `.json`, as FModel does. |
| `Raw\<pak>\` | Every file in every pak, byte for byte (`.uasset`, `.uexp`, `.ubulk`, `.umap`, textures, data.pak's JSON), with one folder per pak. |
| `Reports\` | One report per export, e.g. `2026-11-18-build26613838.md`, plus a `-files.txt` with the full lists. |
| `Logs\IcarusExport\` | A log for each export, and `scheduled.log` with one line per scheduled check. |
| `.icarusexport\state.json` | What the last export wrote. The next export uses it to find what changed. |

Each report lists, for every data table that changed, which rows were added, removed or changed. It also lists the assets that were added, removed or changed. That makes it a quick check of what a game update did to the tables your mods touch.

## Setup

1. Install the [.NET 10 SDK](https://dotnet.microsoft.com/download).
2. Run `build.bat`. It downloads CUE4Parse from NuGet the first time and builds into `publish\`. That folder, `bin\` and `obj\` are never committed.
3. Make sure Oodle is available: `oodle-data-shared.dll` must be in `<export folder>\.data\`. FModel downloads this file into its own `Output\.data\` folder, and the exporter looks there too.

## Export now

Double-click `export-now.bat`, or run it from a terminal with options:

```
export-now.bat                 only what changed since the last export
export-now.bat --full          re-check every file
export-now.bat --paks data     only data.pak (all paks are still mounted)
```

`publish\IcarusExport.exe --help` lists every option.

## Automatic export after each update

```powershell
.\install-task.ps1             # register the task (-Hours 6 to check less often)
.\install-task.ps1 -Remove     # remove it again
```

This registers a Windows scheduled task, **Icarus Export**, that runs `IcarusExportBackground.exe --scheduled` at logon and every 3 hours. Each run reads `appmanifest_1149460.acf` and stops straight away unless all of these are true:

- Steam has finished installing the game (`StateFlags` 4).
- The build id is one that has not been exported yet.
- Icarus is not running. A new build waits until you close the game.

When there is a new build, the task exports at below-normal priority and then shows a Windows notification with a one-line summary and the name of the report. The background exe is the same program marked as a Windows app, so no console window ever appears over the game.

## How it decides what changed

- **Raw files:** each pak's files are hashed (xxHash3). Only files whose content changed are rewritten. Files a pak no longer has are deleted, and a pak whose size and timestamp have not changed is skipped.
- **JSON:** assets whose own files changed are serialised again, and so are the assets that import them. An asset's JSON names each imported object as `Package.ExportIndex`. When the Bear skeleton gained a socket, the export indexes shifted in every animation that uses it, even though those animations' own files didn't change. The new JSON is compared with the hash of what was written last time, and only differences are written. Everything is re-serialised on `--full`, after a CUE4Parse update, or when English localization or a plugin descriptor changes.
- **Removed files:** an asset the game no longer has gets its JSON deleted. Nothing is deleted if a pak on disk could not be read. If more than 10% of the assets seem to vanish at once, nothing is deleted and the report warns instead; pass `--allow-mass-delete` if that was real. A file that can't be deleted because another program has it open is retried on every run until it goes.
- **The comparison point:** every run is compared with the last *complete* export, meaning every pak, raw files and JSON, nothing unreadable and not interrupted. That export stays saved in the state until another complete run finishes.
  - **Interrupted runs:** progress is saved as it goes, so the next run picks up where it stopped. It still re-checks and reports every change since the last complete export, not just what was left.
  - **Partial runs:** a run with `--paks`, `--no-raw` or `--no-json` does not count as exporting the build. The scheduled task still exports it fully, compared with the last complete export.
- **Failures:** a file that can't be read or serialised is listed in the report and retried on the next run. Its older output is kept until then.
- **Data tables:** a copy of the previous export's tables is kept in `.icarusexport\basis-tables\`, so the report can list row changes even after the files in `Exports\` were overwritten.

## Matching FModel

These settings were checked against an FModel 4.4.4 export:

- **Asset JSON:** the provider loads plugin virtual paths and English localization, as FModel does.
- **Data tables:** they are re-indented the way FModel saves JSON (Newtonsoft, 2 spaces, CRLF). `Raw\data\` keeps the game's own formatting.
- **Text files:** `.ini`, `.uplugin`, `.uproject`, `.tps` and similar files are saved as text with a `.json` name.
- **Other formats:** `.locres`, `.locmeta`, `AssetRegistry.bin` and the global shader cache are serialised the way FModel serialises them. When a file and an asset share a name (`Jura-Medium.ufont` and `Jura-Medium.uasset`), the asset's JSON wins.

In that comparison, every difference was a real change in the game. If a CUE4Parse update changes the JSON format, every asset is re-serialised on the next run. Assets whose output did not change are not rewritten.

Every pak the game installs is read, except mods. That means `Icarus\Content\Paks\*.pak`, `Icarus\Content\Data\data.pak` and `Engine\Programs\CrashReportClient\Content\Paks\CrashReportClient.pak`, and any pak a later update adds is picked up the same way. Folders named `mods`, `~mods` or `LogicMods` hold installed mods, including the Mod Manager's merged pak, and are never read.

The crash reporter's pak holds Unreal's ICU language data, Slate UI images and fonts, and a few shaders. 3,767 of its files are also in the main paks, byte for byte. `Raw\CrashReportClient\` has all of its files, and `Exports\` uses the main paks' copy of any shared file.
