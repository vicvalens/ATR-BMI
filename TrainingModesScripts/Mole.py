from TrainingModesScripts.CognitiveFunctions import CognitiveFunctions

import time
import threading

class Mole(CognitiveFunctions):
    def __init__(self, participant_id, mode, gui_terminal, duration, on_completion_callback):
        super().__init__(participant_id, mode, on_completion_callback)
        self.gui_terminal = gui_terminal
        self.length_of_experiment = duration
        self.routine_thread = None
        self.data_writer_thread = None
        self.stop_event = threading.Event()

    def routine(self):
        self.gui_terminal.clear_text()
        self.gui_terminal.write_text('Starting Egg Attention session')
        self.data_writer.set_state("start_session:mole")

        start_time = time.time()
        elapsed_time = 0
        prev_time = 0
        while elapsed_time < self.length_of_experiment * 60:  # Convert minutes to seconds
            if self.stop_event.is_set():
                break

            prev_minute = int(elapsed_time / 60) + 1
            if prev_minute != prev_time:
                self.gui_terminal.write_text(f'----> Minute: {prev_minute} <----')
                prev_time = prev_minute

            # Sleep for shorter intervals to allow more responsive stopping
            time.sleep(1)
            elapsed_time = time.time() - start_time

        self.data_writer.set_state("end_session:mole")
        self.gui_terminal.write_text('End mole_control_inhibition routine')

        self.stop_event.set()