import tkinter as tk
from tkinter import ttk, messagebox
import time

from PIL.Image import MODES
from pylsl import StreamInfo, StreamOutlet
from UI_buttons_functions import *
import os
import shutil
import subprocess

class CognitiveTrainingApp(tk.Tk):
    BUTTON_FONT_COLOR = 'black'
    SIDE_FRAME_COLOR = '#34495e'
    MODES = [
        ('Egg: Attention', egg_attention),
        ('Theater: Working Memory', theater_memory),
        ('Mole: Control and Inhibition', mole_control_inhibition),
        ('Fishing: Multitasking + BMI', fishing_multitasking_bmi)
    ]

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
        control_sidebar = tk.Frame(main_frame, bg="#2c3e50", width=200)  # Dark blue background
        control_sidebar.pack(side="left", fill="y")

        # Create right frame to contain both central area and right control panel
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side="right", fill="both", expand=True)

        # Create right control panel
        right_control_panel = tk.Frame(right_frame, bg="#2c3e50", width=200)  # Dark blue background
        right_control_panel.pack(side="right", fill="y")

        # Create central area
        central_area = tk.Frame(right_frame, bg="#f0f0f0")
        central_area.pack(side="left", fill="both", expand=True)

        # Create terminal panel at the bottom of the central area
        terminal_panel = tk.Frame(central_area, bg="#2c3e50", height=200)
        terminal_panel.pack(side="bottom", fill="x")

        self.create_left_control_panel_widget(control_sidebar)
        self.create_status_panel(terminal_panel)
        self.create_right_control_panel(right_control_panel)


    def create_left_control_panel_widget(self, frame):
        # Label at the top
        title_label = tk.Label(frame, text="Tipo de Experimento", bg="#2c3e50", fg='white', font=("Arial", 14))
        title_label.pack(side="top", fill="x", pady=10)

        # Experiment mode buttons
        for text, command in self.MODES:
            btn = tk.Button(frame, text=text, command=command,
                            bg="#34495e",  # Slightly lighter blue
                            fg=self.BUTTON_FONT_COLOR,
                            activebackground="#2c3e50",
                            activeforeground="#ecf0f1",
                            bd=0, pady=10, font=("Arial", 12))
            btn.pack(side='bottom', fill="x", padx=5, pady=5)

        # Frame for Start and Stop buttons
        control_frame = tk.Frame(frame, bg="#2c3e50")
        control_frame.pack(side='bottom', fill='x', padx=5, pady=10)

        # Start button
        start_button = tk.Button(control_frame, text="Start", command=start_experiment,
                                 bg="#27ae60",  # Green background
                                 fg=self.BUTTON_FONT_COLOR,
                                 activebackground="#2ecc71",
                                 activeforeground="white",
                                 bd=0, pady=10, font=("Arial", 12))

        start_button.pack(side='left', fill="x", expand=True,
                          padx=(0, 5))  # Expand horizontally with spacing on the right

        # Stop button
        stop_button = tk.Button(control_frame, text="Stop", command=stop_experiment,
                                bg="#e74c3c",  # Red background
                                fg=self.BUTTON_FONT_COLOR,
                                activebackground="#c0392b",
                                activeforeground="white",
                                bd=0, pady=10, font=("Arial", 12))
        stop_button.pack(side='right', fill="x", expand=True,
                         padx=(5, 0))  # Expand horizontally with spacing on the left


    def create_right_control_panel(self, frame):
        title_label = tk.Label(frame, text="Información del participante", bg="#2c3e50", fg='white', font=("Arial", 14))
        title_label.pack(side="top", fill="x", pady=10)

        button_frame = tk.Frame(frame, bg="#2c3e50")
        button_frame.pack(side="bottom", fill="x", pady=20)

        btn1 = tk.Button(button_frame, text="Set", bg="#34495e", fg=self.BUTTON_FONT_COLOR,
                         activebackground="#2c3e50", activeforeground="#ecf0f1",
                         bd=0, pady=10, font=("Arial", 12))
        btn1.pack(side="left", expand=True, padx=5)

        btn2 = tk.Button(button_frame, text="Release", bg="#34495e", fg=self.BUTTON_FONT_COLOR,
                         activebackground="#2c3e50", activeforeground="#ecf0f1",
                         bd=0, pady=10, font=("Arial", 12))
        btn2.pack(side="left", expand=True, padx=5)

    def create_status_panel(self, main_frame):
        terminal_frame = tk.Text(main_frame, bg="#D3D3D3")
        terminal_frame.pack(fill="both", expand=True)




if __name__ == "__main__":
    app = CognitiveTrainingApp()
    app.mainloop()
