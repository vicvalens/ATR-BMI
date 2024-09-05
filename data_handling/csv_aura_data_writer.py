import os
import csv
from datetime import datetime


class AuraDataWriter:
    __DEFAULT_FOLDER_PATH = "participants"
    def __init__(self, participant_id: str):
        self.folder_path = None
        self.participant_id = participant_id

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

    def write_data(self, data, data_timestamp, data_eeg, data_egg_timestamp, b_well_data, status_label=''):
        """
        Writes the data to a csv file of the current session.
        :param data: data from AURA power stream
        :param data_timestamp: timestamp of the data from AURA power stream
        :param data_eeg: data from AURA EEG stream
        :param data_egg_timestamp: timestamp of the data from AURA EEG stream
        :param b_well_data: Data from bWell stream if available
        :param status_label: signal of experiment status
        :return: None
        """
        self.aura_writer.writerow([data_timestamp] + data + [status_label] + b_well_data)
        self.aura_writer_eeg.writerow([data_egg_timestamp] + data_eeg + [status_label] + b_well_data)

    def close_writer(self):
        """
        Closes the files of the CSVs that are being written.
        :return: None
        """
        self.aura_file.close()
        self.aura_eeg_file.close()
