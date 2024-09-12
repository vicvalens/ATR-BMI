from UserInterface.Frames.ConfirmationAndExperimentSettings import *

class LeftControlPanel(tk.Frame):
    BUTTON_FONT_COLOR = 'black'
    SIDE_FRAME_COLOR = '#34495e'
    __BACKGROUND_COLOR = "#033DA6"


    def __init__(self, parent, ui_menu):
        super().__init__(parent, bg=self.__BACKGROUND_COLOR, width=200)
        self.MODES = [
            ('Egg: Attention', ui_menu.egg_attention_menu),
            ('Theater: Working Memory', ui_menu.theater_memory_menu),
            ('Mole: Control and Inhibition', ui_menu.mole_control_inhibition_menu),
            ('Fishing: Multitasking + BMI', ui_menu.fishing_multitasking_bmi_menu)
        ]
        self.option_buttons = []
        self.create_widgets()
        self.disable_buttons()

    def create_widgets(self):
        # Label at the top
        title_label = tk.Label(self, text="Tipo de Experimento", bg=self.__BACKGROUND_COLOR, fg='white', font=("Arial", 14))
        title_label.pack(side="top", fill="x", pady=10)

        # Experiment mode buttons
        for text, command in self.MODES:
            btn = tk.Button(self, text=text, command=command,
                            bg="white",
                            fg=self.BUTTON_FONT_COLOR,
                            activebackground="#2c3e50",
                            activeforeground="#ecf0f1",
                            bd=0, pady=10, font=("Arial", 12))
            self.option_buttons.append(btn)
            btn.pack(side='bottom', fill="x", padx=5, pady=5)

        # Frame for Start and Stop buttons
        control_frame = tk.Frame(self, bg=self.__BACKGROUND_COLOR)
        control_frame.pack(side='bottom', fill='x', padx=5, pady=10)

    def disable_buttons(self):
        for btn in self.option_buttons:
            btn['state'] = 'disabled'

    def enable_buttons(self):
        for btn in self.option_buttons:
            btn['state'] = 'normal'
