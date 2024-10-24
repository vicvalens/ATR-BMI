from TrainingModesScripts.CognitiveFunctions import CognitiveFunctions

import time

class VendingMachine(CognitiveFunctions):
    def __init__(self, participant_id, mode, gui_terminal, duration, on_completion_callback):
        super().__init__(participant_id, mode, on_completion_callback)
        self.gui_terminal = gui_terminal
        self.length_of_experiment = duration

    def routine(self):
        self.gui_terminal.clear_text()
        self.gui_terminal.write_text('Sending: start_trial')
        self.data_writer.set_state("start_session:theater")
        time.sleep(0.1)
        for i in range(self.length_of_experiment):
            self.gui_terminal.write_text('----> Trial: ' + str(i + 1))
            self.__theater_trial_routine()
        self.data_writer.set_state("end_session:theater")
        self.gui_terminal.write_text('End Theater memory routine')

        # Stop the data writer thread
        self.stop_event.set()


    def __theater_trial_routine(self):
        self.data_writer.set_state("start_trial")  # start_trial
        self.gui_terminal.write_text("sending: start_trial")
        time.sleep(0.1)
        self.data_writer.set_state("open_curtain")  # start_trial
        self.gui_terminal.write_text("sending: open_curtain")
        time.sleep(10)
        self.data_writer.set_state("close_curtain")  # sound_pot
        self.gui_terminal.write_text("sending: close_curtain")
        time.sleep(12)
        self.data_writer.set_state("start_performing_task")  # sound_pot
        self.gui_terminal.write_text("sending: perform_task")
        time.sleep(20)
        self.data_writer.set_state("open_curtain")  # sound_pot
        self.gui_terminal.write_text("sending: open_curtain")
        time.sleep(7)
        self.data_writer.set_state("close_curtain2")  # sound_pot
        self.gui_terminal.write_text("sending: close_curtain2")
        time.sleep(1)
        self.data_writer.set_state("end_trial")  # end_trial
        self.gui_terminal.write_text("sending: end_trial")
