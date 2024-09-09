from abc import ABC, abstractmethod
from data_handling.aura_signal_handler import AuraSignalHandler
from data_handling.csv_aura_data_writer import AuraDataWriter
import threading
import time

class CognitiveFunctions(ABC):
    def __init__(self, participant_id, mode):

        self.signal_handler = AuraSignalHandler(mode)
        self.data_writer = AuraDataWriter(participant_id, self.signal_handler)

        self.routine_thread = None
        self.data_writer_thread = None
        self.stop_event = threading.Event()

    @abstractmethod
    def routine(self):
        pass

    def start_routine(self):
        self.stop_event.clear()
        self.routine_thread = threading.Thread(target=self._routine_wrapper)
        self.data_writer_thread = threading.Thread(target=self.data_writer_routine)
        self.routine_thread.start()
        self.data_writer_thread.start()

    def _routine_wrapper(self):
        self.routine()
        self.stop_event.set()  # Signal to stop data_writer_routine when main routine is done

    def stop_routine(self):
        self.stop_event.set()
        if self.routine_thread and self.routine_thread.is_alive():
            self.routine_thread.join()
        if self.data_writer_thread and self.data_writer_thread.is_alive():
            self.data_writer_thread.join()

    def data_writer_routine(self):
        while not self.stop_event.is_set():
            self.data_writer.write_data()