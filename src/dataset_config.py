"""
Data and functions for guitar dataset configuration.
"""

import gt_audio_util as util
from pathlib import Path
import os
import json

# path
project_path = Path("path/to/fx_estimate")  # path to the audio effect estimation project
dataset_path = project_path / "gt_dataset"  # path to the directory of the dataset you are about to create

# guitar class
guitars = {
    "sc": "Ample Guitar SC",
    "tc": "Ample Guitar TC",
    "lp": "Ample Guitar LP",
}  # guitar names and plugin names.
strings = range(1, 7)  # string numbers, from low to high pitch, 1-based
frets = range(20)  # fret numbers, from low to high pitch, 0-based


class GuitarInfo:
    """
    Information about guitar play.

    Attributes:
        guitar(str): Guitar name.
        string(int): String numbers. From low to high pitch. 1-based.
        fret(int): Fret numbers. From low to high pitch. 0-based
        gt_plugin(str): VSTi guitar plugin name in Reaper.
    """

    def __init__(self, guitar, string, fret):
        self.guitar = guitar
        self.string = string
        self.fret = fret
        self.gt_plugin = guitars[guitar]


def make_data(guitar_info, data_num):
    """
    Generate a dataset of guitar wet signal.

    Args:
        guitar_info(GuitarInfo): Information about the guitar play to be processed.
        data_num(int): Data serial number.
    """
    label_path = get_label_path(guitar_info, data_num)
    audio_path = get_audio_path(guitar_info, data_num)
    save_label(label_path, guitar_info)
    util.make_audio(audio_path, guitar_info)


def save_label(label_path, guitar_info):
    """
    Save label for guitar audio.

    Args:
        label_path(pathlib.Path): Path to the labeled.
        guitar_info(GuitarInfo): Information about guitar play to be labeled.
    """
    label = {"guitar": guitar_info.guitar, "string": guitar_info.string, "fret": guitar_info.fret}
    os.makedirs(label_path.parent, exist_ok=True)
    with open(label_path, "w") as f:
        json.dump(label, f, indent=2)
        f.write("\n")


def get_label_path(guitar_info, data_num):
    """
    Generate path to the wet signal.

    Args:
        guitar_info(GuitarInfo): Information about guitar play.
        data_num(int): Data serial number.

    Returns:
        path(pathlib.Path): Path to the label.
    """
    path = dataset_path / "data" / guitar_info.guitar / "label" / ("gt" + str(data_num).zfill(8) + ".json")
    return path


def get_audio_path(guitar_info, data_num):
    """
    Generate path to the wet signal.

    Args:
        guitar_info(GuitarInfo): Information about guitar play.
        data_num(int): Data serial number.

    Returns:
        path(pathlib.Path): Path to the audio file.
    """
    path = dataset_path / "data" / guitar_info.guitar / "audio" / ("gt" + str(data_num).zfill(8) + ".flac")
    return path
