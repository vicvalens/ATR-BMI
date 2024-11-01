import os
import csv
import threading
from datetime import datetime

from data_handling.aura_signal_handler import AuraSignalHandler


class AuraDataWriter:
    __DEFAULT_FOLDER_PATH = "participants"

    # Public methods
    def __init__(self, participant_id: str, signal_handler: AuraSignalHandler, mode: str):
        self.folder_path = None
        self.mode = mode.lower()
        self.state_lock = threading.Lock()
        self.participant_id = participant_id
        self.signal_handler = signal_handler

        self.folder_path = os.path.join(self.__DEFAULT_FOLDER_PATH, self.participant_id)
        os.makedirs(self.folder_path, exist_ok=True)

        self.aura_writer, self.aura_file = self.create_writer(self.participant_id)
        self.aura_writer_eeg, self.aura_eeg_file = self.create_writer(self.participant_id, suffix='egg')

        self.end_session_flag = False

    def create_writer(self, session_name, suffix=""):
        """
        Creates a CSV Writer object for the aura signals.
        :param session_name: The name of the participant taking the experiment
        :param suffix: The suffix of the csv file considering if it is the RAW or filtered data
        :return: The writer object and the file
        """
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.mode}_{session_name}_{suffix}_{now}.csv" if suffix else f"{self.mode}_{session_name}_{now}.csv"
        csv_path = os.path.join(self.folder_path, filename)
        file = open(csv_path, "w", newline="")

        return csv.writer(file), file

    def set_state(self, new_state):
        """
        Calls the writer with the desired trigger this should avoid any wrong recording in the data. This is part of a
        new implementation of the writing class.
        :param new_state: A string containing the new state
        :return: None
        """
        self.write_data(state=new_state)


    def write_data(self, state=None):
        """
        Writes the data from the aura streams to the CSV file. Also handles the state of the writer. which is used to
        simulate the trigger of the program. In order to actually send a trigger, must be done separately.
        If the mode is appropriate, it also gets the data from the bWell stream.
        :return: None
        """
        # Only write the state if it's not None or if it's an end_session state
        aura_data_list_0, aura_data_list_1, aura_eeg_data_list_0, aura_eeg_data_list_1, b_well_data = self.__retrieve_data()
        if state is not None and state.startswith("end_session"):
            self.end_session_flag = True

        if state is None:
            state = ""

        if b_well_data is None:
            b_well_data = ""

        if self.mode == 'fishing':
            # For fishing, write aura data only
            self.aura_writer.writerow(aura_data_list_1 + aura_data_list_0 + [state])
            self.aura_writer_eeg.writerow(aura_eeg_data_list_1 + aura_eeg_data_list_0 + [state])
        else:
            # For other modes, include b_well_data if available
            if b_well_data is not None:
                self.aura_writer.writerow(aura_data_list_1 + aura_data_list_0 + [state] + [b_well_data])
                self.aura_writer_eeg.writerow(aura_eeg_data_list_1 + aura_eeg_data_list_0 + [state] + [b_well_data])
            else:
                # If no b_well_data, write aura data only
                self.aura_writer.writerow(aura_data_list_1 + aura_data_list_0 + [state])
                self.aura_writer_eeg.writerow(aura_eeg_data_list_1 + aura_eeg_data_list_0 + [state])

        # Ensure the data is flushed to the file
        self.aura_file.flush()
        self.aura_eeg_file.flush()

    def close_writer(self):
        """
        Closes the CSV Writer objects.
        :return: None
        """
        if self.aura_file:
            self.aura_file.close()
        if self.aura_eeg_file:
            self.aura_eeg_file.close()

    def __retrieve_data(self):
        """
        Retrieves the data from the aura streams, this function simplifies the write_data function. So is easier to
        read and maintain the main writer code.
        :return: A tuple containing the aura data, aura eeg data, and bWell data, the data from aura are lists, and the bWell
        data is a string.
        """
        data = self.signal_handler.get_data_from_streams()
        aura_data = data[0]
        aura_eeg = data[1]

        aura_data_list_0 = aura_data[0] if aura_data[0] is not None else []
        aura_data_list_1 = [aura_data[1]] if aura_data[1] is not None else []

        aura_eeg_data_list_0 = aura_eeg[0] if aura_eeg[0] is not None else []
        aura_eeg_data_list_1 = [aura_eeg[1]] if aura_eeg[1] is not None else []

        b_well_data = None
        if len(data) == 3 and data[2] is not None:
            # Get the first element from bWell, and extract the string inside the list
            b_well_data = data[2][0][0] if isinstance(data[2][0], list) else data[2][0]

        return aura_data_list_0, aura_data_list_1, aura_eeg_data_list_0, aura_eeg_data_list_1, b_well_data
