from TrainingModesScripts.CognitiveFunctions import CognitiveFunctions

import time
import threading

class Mole(CognitiveFunctions):
    def __init__(self, participant_id, mode, gui_terminal, duration):
        super().__init__(participant_id, mode)
        self.gui_terminal = gui_terminal
        self.length_of_experiment = duration
        self.routine_thread = None
        self.data_writer_thread = None
        self.stop_event = threading.Event()

    def routine(self):
        self.gui_terminal.clear_text()
        self.gui_terminal.write_text('Starting Egg Attention session')
        self.outlet_channel.push_sample(["start_session:mole"])
        for i in range(self.length_of_experiment):
            if self.stop_event.is_set():
                break
            self.gui_terminal.write_text('----> Minute: ' + str(i + 1) + ' <----')
            time.sleep(60)
        self.outlet_channel.push_sample(["end_session:mole"])
        self.gui_terminal.write_text('End mole_control_inhibition routine')