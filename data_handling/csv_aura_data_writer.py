import os
import csv
import threading
from datetime import datetime

from data_handling.aura_signal_handler import AuraSignalHandler


class AuraDataWriter:
    __DEFAULT_FOLDER_PATH = "participants"
    def __init__(self, participant_id: str, signal_handler: AuraSignalHandler):
        self.folder_path = None
        self.state = None
        self.state_lock = threading.Lock()  # Add a lock for thread-safe state updates
        self.participant_id = participant_id
        self.signal_handler = signal_handler

        self.folder_path = os.path.join(self.__DEFAULT_FOLDER_PATH, self.participant_id)
        os.makedirs(self.folder_path, exist_ok=True)

        self.aura_writer, self.aura_file = self.create_writer(self.participant_id)
        self.aura_writer_eeg, self.aura_eeg_file = self.create_writer(self.participant_id, suffix='egg')

    def create_writer(self, session_name, suffix="",):
        """
        Creates a writer for a csv file, the name given is the exact date of the experiment.
        :param session_name: The name of the session
        :param suffix: modifier depending on the channel
        :return: A tuple containing the writer and the path where the data is going to be written.
        """
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{session_name}_{suffix}_{now}.csv" if suffix else f"{session_name}_{now}.csv"
        csv_path = os.path.join(self.folder_path, filename)
        file = open(csv_path, "w", newline="")

        return csv.writer(file), file
    
    def set_state(self, new_state):
        with self.state_lock:
            self.state = new_state

    def get_state(self):
        with self.state_lock:
            return self.state

    def write_data(self):
        """
        Writes the data to a csv file of the current session.
        :return: None
        """
        # TODO
        #  bWell Data
        data = self.signal_handler.get_data_from_streams()
        aura_data = data[0]
        aura_eeg = data[1]

        if self.state is not None:
            self.aura_writer.writerow([aura_data[1]] + aura_data[0] + [self.state])
            self.aura_writer_eeg.writerow([aura_eeg[1]] + aura_eeg[0] + [self.state])
            self.state = None
        else:
            self.aura_writer.writerow([aura_data[1]] + aura_data[0] + [])
            self.aura_writer_eeg.writerow([aura_eeg[1]] + aura_eeg[0] + [])
        # if status_label is None:
        #     status_label = []
        #
        # if b_well_data is None:
        #     b_well_data = []
        # self.aura_writer.writerow([data_timestamp] + data + ['status_label'] + b_well_data)
        # self.aura_writer_eeg.writerow([data_egg_timestamp] + data_eeg + ['status_label'] + b_well_data)

    def close_writer(self):
        """
        Closes the files of the CSVs that are being written.
        :return: None
        """
        self.aura_file.close()
        self.aura_eeg_file.close()
