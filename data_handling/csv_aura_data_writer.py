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
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"{self.mode}_{session_name}_{suffix}_{now}.csv" if suffix else f"{self.mode}_{session_name}_{now}.csv"
        csv_path = os.path.join(self.folder_path, filename)
        file = open(csv_path, "w", newline="")
        return csv.writer(file), file

    def set_state(self, new_state):
        with self.state_lock:
            if not self.end_session_flag:
                self.state = new_state
                if new_state is not None and new_state.startswith("end_session"):
                    self.end_session_flag = True

    def get_state(self):
        with self.state_lock:
            return self.state

    def write_data(self):
        data = self.signal_handler.get_data_from_streams()
        aura_data = data[0]
        aura_eeg = data[1]

        current_state = self.get_state()

        # Only write the state if it's not None or if it's an end_session state
        state_to_write = current_state if current_state is not None or self.end_session_flag else ""

        self.aura_writer.writerow([aura_data[1]] + aura_data[0] + [state_to_write])
        self.aura_writer_eeg.writerow([aura_eeg[1]] + aura_eeg[0] + [state_to_write])

        # Reset the state to None after writing, unless it's an end_session state
        if not self.end_session_flag:
            self.set_state(None)
        elif current_state is not None:
            # If it's an end_session state, only write it once
            self.set_state(None)

        # Flush the data to ensure it's written to the file
        self.aura_file.flush()
        self.aura_eeg_file.flush()

    def close_writer(self):
        self.aura_file.close()
        self.aura_eeg_file.close()