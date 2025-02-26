"""
Functions for make guitar audio using VSTi plugin in the Reaper.
"""

import reaper_python as rp
import time

# constant
start_time = 0.0  # sec
end_time = 4.0  # sec
velocity = 32
proj_idx = 0
track_idx = 0


def make_audio(path, guitar_info):
    """
    Generate and save the guitar audio in the Reaper.

    Args:
        path(pathlib.Path): Path to the audio file.
        guitar_info(dataset_config.GuitarInfo): Information about the guitar play to be processed.
    """
    rp.RPR_PreventUIRefresh(1)
    rp.RPR_InsertTrackAtIndex(track_idx, False)
    track = rp.RPR_GetTrack(proj_idx, track_idx)
    add_inst(track, guitar_info.gt_plugin)
    add_midi(track, guitar_info)
    render(path)
    clear_project(track)
    rp.RPR_PreventUIRefresh(-1)


def add_inst(track, gt_plugin):
    """
    Add VSTi guitar plugin to the track and set as clean tone by preset.

    Args:
        track(rp.MediaTrack): Media track to which instruments are added.
        gt_plugin(dataset_config.GuitarInfo.gt_plugin): VSTi plugin name.
    """
    rp.RPR_TrackFX_AddByName(track, gt_plugin, False, -1)
    rp.RPR_TrackFX_SetPreset(track, 0, "Clean")  # "Clean" is an user preset in Reaper
    time.sleep(6)  # silent files may be generated without short wait time


def add_midi(track, guitar_info):
    """
    Add MIDI note to the track.

    Args:
        track(rp.MediaTrack): Media track to which MIDI note are added.
        guitar_info(dataset_config.GuitarInfo): Information about the guitar play to be processed.
    """
    item = rp.RPR_CreateNewMIDIItemInProj(track, start_time, end_time, False)
    take = rp.RPR_GetMediaItemTake(item[0], 0)
    start_ppq = rp.RPR_MIDI_GetPPQPosFromProjTime(take, start_time)
    end_ppq = rp.RPR_MIDI_GetPPQPosFromProjTime(take, end_time)
    pitch, string_force = get_midi_note_num(guitar_info)
    rp.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 1, pitch, velocity, False)
    rp.RPR_MIDI_InsertNote(take, False, False, start_ppq, end_ppq, 1, string_force, velocity, False)  # string force key switch


def render(path):
    """
    Render audio file.

    Args:
        path(pathlib.Path): Path to the audio file.
    """
    dir_path = str(path.parent)
    file_name = path.name
    rp.RPR_GetSetProjectInfo_String(0, "RENDER_FILE", dir_path, 1)
    rp.RPR_GetSetProjectInfo_String(0, "RENDER_PATTERN", file_name, 1)
    rp.RPR_Main_OnCommand(42230, 0)  # render


def clear_project(track):
    """
    Clear the Reaper project.

    Args:
        track(rp.MediaTrack): Old media track.
    """
    rp.RPR_DeleteTrack(track)
    rp.RPR_SetEditCurPos(start_time, True, False)


def get_midi_note_num(guitar_info):
    """
    Generate the MIDI note number from the information about the guitar play.

    Args:
        guitar_info(dataset_config.GuitarInfo): Information about the guitar play to be processed.

    Returns:
        pitch(int): MIDI note number:
        string_force(int): String force key switch for Ample Guitar plugins.
    """
    tune = [40, 45, 50, 55, 59, 64]  # E2, A2, D3, G3, B3, E4
    string_force_base = 19  # G0
    pitch = tune[guitar_info.string - 1] + guitar_info.fret
    string_force = string_force_base + guitar_info.string - 1
    return pitch, string_force
