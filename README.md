# B2-PATCH-UPDATER
A simple standalone tool for automatically updating competitive patches and plugins

## How to use

Head to the [most recent release](https://github.com/B2ORG/B2-PATCH-UPDATER/releases/latest) and download `B2-patch-updater.exe` file. You may place it in any directory on your PC.

## Windows is telling me this program is potentially dangerous / is a virus

Python programs exported as an executable usually cause Windows to be suspitious, in order to deal with that I'd have to pay for a certificate, and it doesn't make sense for this project.

This program can be ran from source, in which case you will not get similar prompts, however it requires some tech savviness.

## What does it do

It scans Plutonium script/plugin folders, then compares the signatures against known patches on [B2](https://b2.wtf/gsc/hash/), if it finds known signatures that have known newer versions, they're automatically updated.

> [!NOTE]
> Actual files from your hard drive are never uploaded anywhere, only their checksums

> [!WARNING]
> This script is NOT compatibile with Plutonium R2905 (or any Plutonium version from before recent refactor). We prioritize new versions and it automatically upgrades your patch location to the currently recommended path, that was not supported back then.

## Config

This programs configuration file is located in

```
%localappdata%\B2PatchUpdater\b2_patch_updater.json
```

| Option | Type | Explanation |
| :---: | :---: | :--- |
| `scan_folders` | array | Stores a set of directories that are scanned by the script while looking for patches, those are always present on your PC assuming Plutonium installation was not customized |
| `confirm_update` | bool | Whether to confirm update of each file, makes the script to no longer be one-click utility |

### Customizing scan folders

Scan folders can be adjusted, since config file is a json file, the backslashes `\` need to be escaped, in order to escape a backslash, place another backslash in front of it, like so `\\`. If you're changing paths here, it does not need to use any shortcuts like `%localappdata%`, it can just be absolute path including your individual username, for example this would be a perfectly valid path.

```
C:\\Users\\B2ORG\\AppData\\Local\\Plutonium\\storage\\t6\\raw\\scripts\\zm
```

> [!WARNING]
> The scan is NON-RECURSIVE, it means it'll only scan files in a specified directory, and won't by itself check files that are in subdirectories of specified path. This is a subject to change if we were to ever support patches that use multiple file structure, however it's not currently on a roadmap.

### I messed up my config and the program no longer works

That's not a problem, simply remove the `b2_patch_updater.json` file, a fresh config will be generated on next program launch

### I want to customize the config before the program runs for the first time

You need to launch the program using a `--config` starting argument. In order to do that, head to the folder the program is placed in, click on an address bar (where you see the current folder and folder that are "in front of it"). Press on the address bar and type in `cmd`, then press enter. A command prompt will open, with working directory already set as a directory you were just in. Now proceed to type

```sh
B2-patch-updater.exe --config
``` 

and press enter. The program will now generate the config and terminate.

> [!WARNING]
> If you changed the name of the executable (or it's different for any other reason), you'll need to replace the executable name from above to one matching name on your system.

## Currently supported patches

At the moment following community patches are supported. This list may not always be up to date, since I don't need to update the program to support additional patches (for the most part), I just need to define them in B2 web application.

| Patch/Plugin | Game | Author | Note |
| :---: | :---: | :---: | :--- |
| WaW-Community-Patch | T4 | Evelyn | First Room versions are correctly updated to the main one |
| CT5 | T5 | Evelyn | T5 Competitive plugin, Currently only versions 1.4+ |
| B2OP | T6 | Zi0 | Only Plutonium versions 2.0+ |
| B2FR | T6 | Zi0 | B2FR HUD and NOHUD version are independent, meaning HUD version will update to newer HUD version and NO HUD version will update to newer NO HUD version |

## Run from source

- Download or clone the codebase
- Make sure you have a modern Python version (this is created on Python 3.14, but should work all the way back to 3.12)
- Create a virtual environment and activate it

```sh
python -m venv venv
venv\scripts\activate.bat       # CMD
.\venv\scripts\Activate.ps1     # PowerShell
```

- Download libraries

```sh
pip install -r requirements.txt     # CMD
pip install -r .\requirements.txt   # PowerShell
```

- Run the program

```sh
python main.py      # CMD
python .\main.py    # PowerShell
```

> [!TIP]
> Create a .bat file for running the program, the .bat file can be placed in a convenient spot such as desktop
