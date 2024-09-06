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
        terminal_status_frame = tk.Frame(right_frame, bg="#f0f0f0")

        # Create the control UI objects
        control_experiment_panel = ConfirmationAndExperimentSettings(upper_control_area)
        left_control_area = LeftControlPanel(main_frame, control_experiment_panel)
        right_control_panel = RightControlPanel(right_frame, left_control_area)
        terminal_panel = StatusPanel(terminal_status_frame)

        # Place the objects in the UI
        main_frame.pack(fill="both", expand=True)
        left_control_area.pack(side="left", fill="y")
        terminal_status_frame.pack(side="left", fill="both", expand=True)
        terminal_panel.pack(side="bottom", fill="x")
        terminal_panel.write_text("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")

        right_frame.pack(side="right", fill="both", expand=True)
        right_control_panel.pack(side="right", fill="y")
        upper_control_area.pack(side="top", fill="both", expand=True)
        control_experiment_panel.pack(side="top", fill="both", expand=True)

