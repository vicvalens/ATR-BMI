import time
from abc import ABC, abstractmethod
from data_handling.aura_signal_handler import AuraSignalHandler
from data_handling.csv_aura_data_writer import AuraDataWriter
import threading

class CognitiveFunctions(ABC):
    def __init__(self, participant_id, mode, on_completion_callback):
        self.signal_handler = AuraSignalHandler(mode)
        self.data_writer = AuraDataWriter(participant_id, self.signal_handler, mode)

        self.routine_thread = None
        self.data_writer_thread = None
        self.stop_event = threading.Event()
        self.on_completion_callback = on_completion_callback

    @abstractmethod
    def routine(self):
        pass

    def start_routine(self):
        self.stop_event.clear()
        self.routine_thread = threading.Thread(target=self._routine_wrapper)
        self.data_writer_thread = threading.Thread(target=self.data_writer_routine)
        self.routine_thread.start()
        self.data_writer_thread.start()
        # Wait for both threads to complete
        self.routine_thread.join()
        self.data_writer_thread.join()
        # Call the completion callback
        if self.on_completion_callback:
            self.on_completion_callback()

    def _routine_wrapper(self):
        try:
            self.routine()
        finally:
            self.stop_event.set()  # Signal to stop data_writer_routine when main routine is done

    def stop_routine(self):
        self.stop_event.set()
        if self.routine_thread and self.routine_thread.is_alive():
            self.routine_thread.join()
        if self.data_writer_thread and self.data_writer_thread.is_alive():
            self.data_writer_thread.join()
        if self.on_completion_callback:
            self.on_completion_callback()

    def data_writer_routine(self):
        while not self.stop_event.is_set():
            self.data_writer.write_data()
            time.sleep(0.1)  # Add a small sleep to prevent busy-waiting

        # Write one last time after the stop event is set
        self.data_writer.write_data()

    def finish_routine(self):
        self.data_writer.close_writer()
