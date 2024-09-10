import tkinter as tk

class RightControlPanel(tk.Frame):
    __BUTTON_FONT_COLOR = 'black'
    __BACKGROUND_COLOR = "#033DA6"
    def __init__(self, parent, left_panel, experiment_config_panel):
        super().__init__(parent, bg=self.__BACKGROUND_COLOR, width=200)
        self.release_participant_button = None
        self.set_participant_button = None
        self.participant_id_entry = None
        self.participant_id = tk.StringVar()
        self.left_panel = left_panel
        self.experiment_config_panel = experiment_config_panel

        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Información del participante", bg=self.__BACKGROUND_COLOR, fg='white', font=("Arial", 14))
        title_label.pack(side="top", fill="x", pady=10)

        button_frame = tk.Frame(self, bg=self.__BACKGROUND_COLOR)
        button_frame.pack(side="bottom", fill="x", pady=20)

        self.participant_id_entry = tk.Entry(self , bg='white', textvariable=self.participant_id)
        self.participant_id_entry.pack(side="bottom", fill="x")

        information_label = tk.Label(self, text="Ingresa el ID del participante: ", bg=self.__BACKGROUND_COLOR, fg='white')
        information_label.pack(side="bottom", fill="x")

        self.set_participant_button = tk.Button(button_frame, text="Set", bg=self.__BACKGROUND_COLOR, fg=self.__BUTTON_FONT_COLOR,
                         activebackground="#2c3e50", activeforeground="#ecf0f1",
                         bd=0, pady=10, font=("Arial", 12), command=self.set_participant_id)
        self.set_participant_button.pack(side="left", expand=True, padx=5)

        self.release_participant_button = tk.Button(button_frame,
                        text="Release", bg=self.__BACKGROUND_COLOR, fg=self.__BUTTON_FONT_COLOR,
                         activebackground="#2c3e50", activeforeground="#ecf0f1",
                         bd=0, pady=10, font=("Arial", 12), state=tk.DISABLED, command=self.release_participant_id)
        self.release_participant_button.pack(side="left", expand=True, padx=5)

    def get_participant_id(self):
        return self.participant_id.get()

    def clear_participant_id(self):
        self.participant_id_entry.delete(0, 'end')
        self.participant_id.set('')

    def set_participant_id(self):
        if self.get_participant_id() != '':
            self.participant_id.set(self.participant_id_entry.get())
            self.set_participant_button['state'] = tk.DISABLED
            self.release_participant_button['state'] = tk.NORMAL
            self.left_panel.enable_buttons()
            self.experiment_config_panel.set_participant_id(self.get_participant_id())

    def release_participant_id(self):
        if not self.experiment_config_panel.on_experiment:
            self.clear_participant_id()
            self.set_participant_button['state'] = tk.NORMAL
            self.release_participant_button['state'] = tk.DISABLED
            self.left_panel.disable_buttons()
            self.experiment_config_panel.clear_frame()

    def lock_buttons_in_experiment(self):
        self.release_participant_button['state'] = tk.DISABLED

    def unlock_buttons_in_experiment(self):
        self.release_participant_button['state'] = tk.NORMAL
