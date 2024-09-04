import pylsl
import csv
import os
from datetime import datetime

from pylsl import StreamInfo, StreamInlet
from scipy.constants import value

DEFAULT_FOLDER_PATH = "participants"
STREAM_NAMES = ['AURA_Power', 'AURA_Filtered', 'test_triggers']

def initialize_b_well_stream() -> StreamInlet:
    """
    Creates the b_well_stream that is going to be used and makes it and inlet
    :return: the inlet of the bWell Stream
    """
    stream_marker = pylsl.resolve_stream('name', 'bWell.Markers')
    inlet_markers_stream = None
    if len(stream_marker) == 0:
        print("No se encontró el stream 'bWell.Markers'. Asegúrate de que esté siendo enviado por otro programa.")
    else:
        inlet_markers_stream = pylsl.StreamInlet(stream_marker[0])
        print("Connected!")
    return inlet_markers_stream


def create_streams():
    """
    Creates the streams that are going to be used for the AURA by the size of stream names it only creates 3 streams
    :return: a list of streams
    """
    return [pylsl.resolve_stream('name', name) for name in STREAM_NAMES]


def create_inlets(streams):
    """
    Creates a dictionary containing all the inlets.
    :param streams: the list of streams to create inlets
    :return: a dictionary containing all the inlets
    """
    return {name: pylsl.StreamInlet(stream[0]) for name, stream in zip(STREAM_NAMES, streams)}


def create_directory(participant_id):
    """
    Checks weather or not a directory exists and creates it if it doesn't.
    :param participant_id: the id of the participant
    :return: the created directory or the found directory
    """
    folder_path = os.path.join(DEFAULT_FOLDER_PATH, participant_id)
    os.makedirs(folder_path, exist_ok=True)
    print(f"Directory: {participant_id} {'created' if not os.path.isdir(folder_path) else 'found'}")
    return folder_path


def check_streams(channels) -> (bool, str):
    """
    Checks if the created streams exist or not.
    :param channels: the list of channels to check
    :return: a boolean indicating if the stream exists or not and a string containing the name of the fault channel,
    in case there's no fault channel the string returned is empty
    """
    for i in range(len(channels)):
        if len(channels[i]) == 0:
            return False, STREAM_NAMES[i]
    return True, ''


def create_writer(folder_path, session_name, suffix=""):
    """
    Creates a writer for a csv file, the name given is the date of the experiment
    :param folder_path: the path where the CSV will be created
    :param session_name: The name of the session
    :param suffix: modifier depending on the channel
    :return: A tuple containing the writer, path and file
    """
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"{session_name}_{suffix}_{now}.csv" if suffix else f"{session_name}_{now}.csv"
    csv_path = os.path.join(folder_path, filename)
    file = open(csv_path, "w", newline="")
    return csv.writer(file), csv_path, file


def process_trigger(trigger, participant_id, session_name, recording_state):
    """
    Handles the different states of the signals
    :param trigger: Incoming trigger data
    :param participant_id: Current participant ID
    :param session_name: Current session name
    :param recording_state: A dictionary keeping track whether the recording is in progress or not
    :return: A tuple containing the trigger label, participant ID, session name, recording state and bWell.Markers inlet
    """
    if ':' not in str(trigger[0]):
        return trigger, participant_id, session_name, recording_state, None

    str_split = str(trigger[0]).split(":")
    action = str_split[0]
    value_action = str_split[-1]
    print(trigger[0])
    if action == "participant_id":
        participant_id = value_action
        folder_path = create_directory(participant_id)
        return "0", participant_id, session_name, recording_state, initialize_b_well_stream()
    elif action == "start_session":
        session_name = value_action
        if not recording_state['is_recording']:
            recording_state['is_recording'] = True
            return f"start_session_{session_name}", participant_id, session_name, recording_state, None
    elif action == "end_session":
        if recording_state['is_recording']:
            recording_state['is_recording'] = False
            return f"end_session_{session_name}", participant_id, session_name, recording_state, None

    return "0", participant_id, session_name, recording_state, None

def run():
    """
    Entry point to the scripts in this file
    :return: None
    """
    print("Solving Streams")
    streams = create_streams()
    ok, failed_stream = check_streams(streams)
    if not ok:
        print(f"Stream '{failed_stream}' not found. Ensure it's being sent by another program.")
        return

    streams_inlets = create_inlets(streams)
    bwell_markers_inlet = None

    recording_state = {'is_recording': False}
    participant_id = ""
    session_name = ""
    writers = {}

    print("Waiting for data from AURA_Power, AURA_Filtered, and test_triggers streams...")

    try:
        while True:
            samples = {name: inlet.pull_sample() for name, inlet in streams_inlets.items()}
            triggers, _ = streams_inlets['test_triggers'].pull_sample(0)

            marker_label = "0"

            if bwell_markers_inlet:
                markers, _ = bwell_markers_inlet.pull_sample(0)
                marker_label = markers[0] if markers else "0"

            trigger_label, participant_id, session_name, recording_state, new_bwell_inlet = process_trigger(
                triggers or ["0"], participant_id, session_name, recording_state
            )

            if new_bwell_inlet:
                bwell_markers_inlet = new_bwell_inlet

            if trigger_label == "exit":
                print("Finished")
                break

            if recording_state['is_recording']:
                if not writers:
                    folder_path = create_directory(participant_id)
                    writers['aura'], _, aura_file = create_writer(folder_path, session_name)
                    writers['eeg'], _, eeg_file = create_writer(folder_path, session_name, "eeg")
                    print("Recording started...")
                for stream_type, (sample, timestamp) in samples.items():
                    if stream_type in ['AURA_Power', 'AURA_Filtered']:
                        writers[stream_type.split('_')[1].lower()].writerow(
                            [timestamp] + sample + [trigger_label, marker_label])

            elif writers:
                for file in [aura_file, eeg_file]:
                    file.close()
                writers.clear()
                print("Recording finished...")
    finally:
        # Close any open files and inlets
        for file in [aura_file, eeg_file]:
            file.close()
        for inlet in streams_inlets.values():
            inlet.close_stream()
        if bwell_markers_inlet:
            bwell_markers_inlet.close_stream()
        writers.clear()

run()
