import subprocess
import signal
import sys
import os
from UserInterface.ui_main_file import CognitiveTrainingApp

def run_eeg_classifier():
    # Start the EEG classifier subprocess
    eeg_process = subprocess.Popen([sys.executable, 'winry.py'], stdout=open(os.devnull, 'wb'))
    return eeg_process

def kill_subprocess(process):
    if process:
        process.send_signal(signal.SIGTERM)
        process.wait()

class MainApp(CognitiveTrainingApp):
    def __init__(self):
        super().__init__()
        self.eeg_process = None

    def on_start(self):
        self.eeg_process = run_eeg_classifier()

    def on_closing(self):
        kill_subprocess(self.eeg_process)
        self.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.on_start()
    app.mainloop()