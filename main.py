import subprocess
import signal
import sys
import os
from UserInterface.ui_main_file import CognitiveTrainingApp


class MainApp(CognitiveTrainingApp):
    def __init__(self):
        super().__init__()
        self.eeg_process = None



if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
