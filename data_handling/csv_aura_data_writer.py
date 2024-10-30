import os
import csv
import threading
from datetime import datetime
from data_handling.aura_signal_handler import AuraSignalHandler


class AuraDataWriter:
    __DEFAULT_FOLDER_PATH = "participants"

    def __init__(self, participant_id: str, signal_handler: AuraSignalHandler, mode: str):
        self.folder_path = None
        self.state = None
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
        
        # Set quoting to csv.QUOTE_NONE to avoid quotes around the values
        return csv.writer(file, quoting=csv.QUOTE_NONE, escapechar='\\'), file

    def set_state(self, new_state):
        """
        Set the state of the writer so if there's a trigger it is handled by an internal change of state
        :param new_state: A string containing the new state
        :return: None
        """
        with self.state_lock:
            if not self.end_session_flag:
                self.state = new_state
                if new_state is not None and new_state.startswith("end_session"):
                    self.end_session_flag = True

    def get_state(self):
        """
        This is implemented so the writing of the data is thread safe.
        :return: the state of the lock
        """
        with self.state_lock:
            return self.state

    def write_data(self):
        """
        Writes the data from the aura streams to the CSV file. If the mode is appropriate, it also gets the data from the
        bWell stream.
        :return: None
        """
        data = self.signal_handler.get_data_from_streams()
        aura_data = data[0]
        aura_eeg = data[1]

        current_state = self.get_state()

        # Only write the state if it's not None or if it's an end_session state
        state_to_write = current_state if current_state is not None or self.end_session_flag else ""

        # Ensure aura_data[0] and aura_data[1] are not None before concatenating
        aura_data_list_0 = aura_data[0] if aura_data[0] is not None else []
        aura_data_list_1 = [aura_data[1]] if aura_data[1] is not None else []

        b_well_data = None
        if len(data) == 3 and data[2] is not None:
            # Get the first element from bWell, and extract the string inside the list
            b_well_data = data[2][0][0] if isinstance(data[2][0], list) else data[2][0]

        if self.mode == 'fishing':
            # For fishing, write aura data only
            self.aura_writer.writerow(aura_data_list_1 + aura_data_list_0 + [state_to_write])
            self.aura_writer_eeg.writerow([aura_eeg[1]] + aura_eeg[0] + [state_to_write])
        else:
            # For other modes, include b_well_data if available
            if b_well_data is not None:
                self.aura_writer.writerow(aura_data_list_1 + aura_data_list_0 + [state_to_write] + [b_well_data])
                self.aura_writer_eeg.writerow([aura_eeg[1]] + aura_eeg[0] + [state_to_write] + [b_well_data])
            else:
                # If no b_well_data, write aura data only
                self.aura_writer.writerow(aura_data_list_1 + aura_data_list_0 + [state_to_write])
                self.aura_writer_eeg.writerow([aura_eeg[1]] + aura_eeg[0] + [state_to_write])

        # Reset the state to None after writing, unless it's an end_session state
        if not self.end_session_flag:
            self.set_state(None)
        elif current_state is not None:
            # If it's an end_session state, only write it once
            self.set_state(None)

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
