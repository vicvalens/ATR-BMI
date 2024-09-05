import tkinter as tk
from tkinter import ttk
from UserInterface.Frames.left_side_bar_widget import LeftControlPanel
from UserInterface.Frames.right_side_bar_widget import RightControlPanel
from UserInterface.Frames.status_panel import StatusPanel

class CognitiveTrainingApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("ATR-BMI")
        self.geometry("1250x650")
        self.configure(bg="#f0f0f0")  # Light gray background
        self.minsize(1250, 650)

        self.create_main_widget()

    def create_main_widget(self):
        # Main frame
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        # Create left control panel
        control_sidebar = LeftControlPanel(main_frame)
        control_sidebar.pack(side="left", fill="y")

        # Create right frame to contain both central area and right control panel
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)

        # Create right control panel
        right_control_panel = RightControlPanel(right_frame)
        right_control_panel.pack(side="right", fill="y")

        # Create central area
        central_area = tk.Frame(right_frame, bg="#f0f0f0")
        central_area.pack(side="left", fill="both", expand=True)

        # Create terminal panel at the bottom of the central area
        terminal_panel = StatusPanel(central_area)
        terminal_panel.pack(side="bottom", fill="x")

