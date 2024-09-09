import time
import threading

import pylsl
from pylsl import StreamInlet

from TrainingModesScripts.CognitiveFunctions import CognitiveFunctions

class EGGAttention(CognitiveFunctions):
    def __init__(self, participant_id, mode, gui_terminal, duration):
        super().__init__(participant_id, mode)
        self.gui_terminal = gui_terminal
        self.length_of_experiment = duration

    def routine(self):
        self.gui_terminal.clear_text()
        self.gui_terminal.write_text('Starting Egg Attention session')
        self.data_writer.set_state("start_session:egg")
        for i in range(self.length_of_experiment):
            if self.stop_event.is_set():
                break
            self.gui_terminal.write_text('----> Minute: ' + str(i + 1) + ' <----')
            time.sleep(60)
        self.data_writer.set_state("end_session:egg")
        self.gui_terminal.write_text('Finishing Egg Attention session')
