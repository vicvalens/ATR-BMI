import tkinter as tk
from UserInterface.UI_buttons_functions import *

class LeftControlPanel(tk.Frame):
    BUTTON_FONT_COLOR = 'black'
    SIDE_FRAME_COLOR = '#34495e'
    MODES = [
        ('Egg: Attention', egg_attention),
        ('Theater: Working Memory', theater_memory),
        ('Mole: Control and Inhibition', mole_control_inhibition),
        ('Fishing: Multitasking + BMI', fishing_multitasking_bmi)
    ]

    def __init__(self, parent):
        super().__init__(parent, bg="#2c3e50", width=200)
        self.create_widgets()

    def create_widgets(self):
        # Label at the top
        title_label = tk.Label(self, text="Tipo de Experimento", bg="#2c3e50", fg='white', font=("Arial", 14))
        title_label.pack(side="top", fill="x", pady=10)

        # Experiment mode buttons
        for text, command in self.MODES:
            btn = tk.Button(self, text=text, command=command,
                            bg="#34495e",
                            fg=self.BUTTON_FONT_COLOR,
                            activebackground="#2c3e50",
                            activeforeground="#ecf0f1",
                            bd=0, pady=10, font=("Arial", 12))
            btn.pack(side='bottom', fill="x", padx=5, pady=5)

        # Frame for Start and Stop buttons
        control_frame = tk.Frame(self, bg="#2c3e50")
        control_frame.pack(side='bottom', fill='x', padx=5, pady=10)

        # Start button
        start_button = tk.Button(control_frame, text="Start", command=start_experiment,
                                 bg="#27ae60",
                                 fg=self.BUTTON_FONT_COLOR,
                                 activebackground="#2ecc71",
                                 activeforeground="white",
                                 bd=0, pady=10, font=("Arial", 12))
        start_button.pack(side='left', fill="x", expand=True, padx=(0, 5))

        # Stop button
        stop_button = tk.Button(control_frame, text="Stop", command=stop_experiment,
                                bg="#e74c3c",
                                fg=self.BUTTON_FONT_COLOR,
                                activebackground="#c0392b",
                                activeforeground="white",
                                bd=0, pady=10, font=("Arial", 12))
        stop_button.pack(side='right', fill="x", expand=True, padx=(5, 0))