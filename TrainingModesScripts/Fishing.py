from TrainingModesScripts.CognitiveFunctions import CognitiveFunctions

import time

class FishingMultitasking(CognitiveFunctions):
    def __init__(self, participant_id, mode, gui_terminal, duration):
        super().__init__(participant_id, mode)
        self.gui_terminal = gui_terminal
        self.length_of_experiment = duration

    def routine(self):
        self.gui_terminal.clear_text()
        self.gui_terminal.write_text('Sending: start_trial')
        self.outlet_channel.push_sample(["start_session:theater"])
        for i in range(self.length_of_experiment):
            self.gui_terminal.write_text('----> Trial: ' + str(i + 1))
            self.__fishing_trial_routine()
        self.outlet_channel.push_sample(["Sending: end_session:theater"])
        self.gui_terminal.write_text('End Theater memory routine')

    def trial_routine(self):
        pass

    def experiment_routine(self):
        pass

    def __fishing_trial_routine(self):
        self.outlet_channel.push_sample(["start_trial"])  # start_trial
        self.gui_terminal.write_text("sending: start_trial")
        time.sleep(2)
        self.outlet_channel.push_sample(["open_scene"])  # start_trial
        self.gui_terminal.write_text("sending: open_scene")
        time.sleep(10)
        self.outlet_channel.push_sample(["activate_fishing"])  # sound_pot
        self.gui_terminal.write_text("sending: activate_fishing")
        time.sleep(10)
        self.outlet_channel.push_sample(["close_scene"])  # start_trial
        self.gui_terminal.write_text("sending: close_scene")
        time.sleep(1)
        self.outlet_channel.push_sample(["end_trial"])  # end_trial
        self.gui_terminal.write_text("sending: end_trial")
        time.sleep(2)