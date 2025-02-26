# gt_dataset: Clean Guitar Audio Dataset

This is a project for a guitar dry signal dataset.
This repository contains a dataset generation program.
This project is a part of the project "fx_estimate" and the dataset is intended to be used for generating a wet signal dataset [gtfx_dataset](https://github.com/okitayouichi/gtfx_dataset) and an audio effect estimation project [fx_estimate](https://github.com/okitayouichi/fx_estimate).
The dataset generation program is a ReaScript for the Reaper written in Python.

## Dataset

The dataset consists of electric guitar clean tone audio and its labels.
Using an electric guitar with the VSTi plug-in listed below, monophonic single notes are played for 4 seconds at the 1-6 strings and 0-20 frets.
A 2-second interval is added at the end to capture the lingering sound, resulting in an audio length of 6 seconds.

- [Ample Guitar SC](https://www.amplesound.net/en/pro-pd.asp?id=2) (paid)
- [Ample Guitar TC](https://www.amplesound.net/en/pro-pd.asp?id=20) (paid)
- [Ample Guitar LP](https://www.amplesound.net/en/pro-pd.asp?id=1) (paid)


## Setup & Dataset generation

This program has only been tested on Reaper v7.25 (Windows 11), Python 3.11.0 (Ubuntu 20.04.6 LTS (WSL2)).

1. Install Python.
2. Install [Reaper](https://www.reaper.fm/) and activate licenses.
3. Install VSTi plugins listed above and activate licenses.
4. In Reaper, click "Options > Preferences > Plug-ins > VST", add the path to the installed plugins to "VST plug-in paths" and click "Re-scan".
5. In Reaper, click "Track > Insert new track", then click the "FX" button to add installed plugins. Make the following settings (Leave the other settings as default.) in each plugin window and save the settings as Reaper user preset "Clean" by clicking "+ > Save preset".
- FX-Bypassed: Off
- AMP-Enables: Off
- Pickup: Neck + Middle (Ample Guitar SC), Neck (Ample Guitar TC), Neck + Bridge (Ample Guitar LP)
6. In Reaper, click "File > Render", make the following settings (Leave the other settings as default.) and click "Save settings".
- Tail: 2000 ms
- Channels: Mono
- Format: FLAC
- FLAC encoding depth: 16 bit
7. Edit `path/to/fx_estimate` in `src/dataset_config.py` line 11 to your local path.
8. In Reaper, click "Actions > Show action list > New action > New ReaScript" to open the "Actions" window and select `main.py` in this repository.
9. In the "Actions" window, select `main.py` and click "Run".
