import tkinter as tk
from tkinter import ttk

from UserInterface.Frames.left_side_bar_widget import LeftControlPanel
from UserInterface.Frames.right_side_bar_widget import RightControlPanel
from UserInterface.Frames.status_panel import StatusPanel
from UserInterface.UI_buttons_functions import ConfirmationAndExperimentSettings


class CognitiveTrainingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ATR-BMI")
        self.geometry("1250x650")
        self.configure(bg="#f0f0f0")  # Light gray background
        self.minsize(1250, 650)

        self.create_main_widget()

    def create_main_widget(self):
        # Frames
        # Main frame
        main_frame = ttk.Frame(self)
        right_frame = tk.Frame(main_frame)
        upper_control_area = tk.Frame(right_frame, bg="white")

        # Create the control UI objects
        terminal_panel = StatusPanel(right_frame)
        control_experiment_panel = ConfirmationAndExperimentSettings(upper_control_area, terminal_panel)
        left_control_area = LeftControlPanel(main_frame, control_experiment_panel)

        right_control_panel = RightControlPanel(right_frame, left_control_area, control_experiment_panel)

        # Place the objects in the UI
        main_frame.pack(fill="both", expand=True)
        right_frame.pack(side="right", fill="both", expand=True)

        left_control_area.pack(side="left", fill="y")
        terminal_panel.pack(side="bottom", fill="x")

        right_control_panel.pack(side="right", fill="y")

        upper_control_area.pack(side="top", fill="both", expand=True)

        control_experiment_panel.pack(side="top", fill="both", expand=True)