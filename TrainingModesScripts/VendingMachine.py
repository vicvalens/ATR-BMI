from TrainingModesScripts.CognitiveFunctions import CognitiveFunctions
import time
from pylsl import StreamOutlet, StreamInfo, cf_string

class VendingMachine(CognitiveFunctions):
    def __init__(self, participant_id, mode, gui_terminal, duration, on_completion_callback):
        super().__init__(participant_id, mode, on_completion_callback)
        self.gui_terminal = gui_terminal
        self.length_of_experiment = duration

        stream_name = "test_triggers"
        stream_type = "triggers"
        stream_info = StreamInfo(stream_name, stream_type, 1, 0, cf_string, "uniqueid12345")
        self.outlet = StreamOutlet(stream_info)

    def routine(self):
        time.sleep(0.1)
        self.gui_terminal.clear_text()
        self.gui_terminal.write_text('Sending: start_trial')
        self.data_writer.set_state("start_session:vending_machine")
        time.sleep(0.1)
        for i in range(self.length_of_experiment):
            self.gui_terminal.write_text('----> Trial: ' + str(i + 1))
            self.__theater_trial_routine()
        self.data_writer.set_state("end_session:vending_machine")
        self.gui_terminal.write_text('End Vending Machine memory routine')

        # Stop the data writer thread
        self.stop_event.set()

    def __theater_trial_routine(self):
        self.data_writer.set_state("open_scene")
        self.gui_terminal.write_text("sending: open_scene")
        time.sleep(4)
        self.data_writer.set_state("start_trial")
        self.gui_terminal.write_text("sending: start_trial")
        self.outlet.push_sample(["start_trial"])
        time.sleep(2)
        self.data_writer.set_state("start_memorizing_task")
        self.gui_terminal.write_text("sending: start_memorizing_task")
        time.sleep(12)
        self.data_writer.set_state("start_performing_task")
        self.gui_terminal.write_text("sending: start_performing_task")
        time.sleep(62)        
        self.data_writer.set_state("task_evaluation")
        self.gui_terminal.write_text("sending: task_evaluation")
        time.sleep(5)
        self.data_writer.set_state("end_trial")
        self.gui_terminal.write_text("sending: end_trial")
