import threading
import tkinter as tk
from tkinter import ttk

from pylsl import pylsl

from TrainingModesScripts.EggAttention import EGGAttention
from TrainingModesScripts.Fishing import FishingMultitasking
from TrainingModesScripts.TheaterTrialRoutine import TheaterTrialRoutine
from TrainingModesScripts.Mole import Mole
from tkinter import messagebox

class ConfirmationAndExperimentSettings(tk.Frame):
    __BACKGROUND_COLOR = "white"

    def __init__(self, parent, terminal):
        super().__init__(parent, bg=self.__BACKGROUND_COLOR)
        # Data fields required to start experiment
        self.experiment_2 = None
        self.fishing_text = None
        self.fishing_label = None
        self.experiment_thread = None
        self.start_button = None
        self.mode = None
        self.experiment = None
        self.participant_id = None
        self.on_experiment = False
        self.details_and_configuration_frame = None
        self.value_label = None
        self.information_label = None
        self.fishing_label = None

        self.__experiment_duration = tk.IntVar(value=5)
        self.__fishing_duration = tk.IntVar(value=5)
        self.terminal = terminal


    def egg_attention_menu(self):
        if not self.on_experiment:
            self.mode = 'EGG'
            self.clear_frame()
            self.create_side_frame()
            self.create_title('Egg Attention')
            self.information_label = 'Minutos de duración: '
            self.create_slider()
            self.create_start_button()

    def theater_memory_menu(self):
        if not self.on_experiment:
            self.mode = 'THEATER'
            self.clear_frame()
            self.create_side_frame()
            self.create_title('Theater Memory')
            self.information_label = 'Numero de pruebas: '
            self.create_slider()
            self.create_start_button()

    def mole_control_inhibition_menu(self):
        if not self.on_experiment:
            self.mode = 'MOLE'
            self.clear_frame()
            self.create_side_frame()
            self.create_title('Mole control inhibition')
            self.information_label = 'Minutos de duración: '
            self.create_slider()
            self.create_start_button()

    def fishing_multitasking_bmi_menu(self):
        if not self.on_experiment:
            self.mode = 'FISHING'
            self.clear_frame()
            self.create_side_frame()
            self.create_title('Fishing multitasking')
            self.information_label = 'Número de entrenamientos: '
            self.fishing_text = 'Número de Trials: '
            self.create_slider()
            self.create_start_button()


    def create_start_button(self):
        self.start_button = tk.Button(self.details_and_configuration_frame, text='Start experiment', fg='black', bg='#D3D3D3', height=5, width=15, command=self.start_experiment)
        self.start_button.pack(side='bottom', fill='x')

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def __update_slider_value(self, event):
        value = round(float(self.__experiment_duration.get()))
        self.__experiment_duration.set(value)
        self.value_label.config(text=self.information_label + str(self.__experiment_duration.get()))

    def __update_fishing_slider(self, event):
        value = round(float(self.__fishing_duration.get()))
        self.__fishing_duration.set(value)
        self.fishing_label.config(text=self.fishing_text + str(self.__fishing_duration.get()))

    def get_experiment_duration(self):
        return self.__experiment_duration.get()

    def set_experiment_duration(self, value):
        self.__experiment_duration.set(value)
        self.value_label.config(text=str(value))

    def create_side_frame(self):
        self.details_and_configuration_frame = tk.Frame(self, bg='#D3D3D3')
        self.details_and_configuration_frame.pack(side='left', fill='y')

    def create_title(self, title):
        title = tk.Label(self.details_and_configuration_frame, text=title, bg='#D3D3D3', fg='black', font='Helvetica 18 bold')
        title.pack(side='top', fill='x')

    def create_slider(self):
        slider = ttk.Scale(
            self.details_and_configuration_frame,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=self.__experiment_duration,
            command=self.__update_slider_value,
            length=200,
        )
        slider.pack(side='top', padx=(10, 5), pady=5)

        self.value_label = tk.Label(
            self.details_and_configuration_frame,
            text=self.information_label + str(self.__experiment_duration.get()),
            bg='#D3D3D3'
        )

        self.value_label.pack(side='top', pady=0)

    def set_participant_id(self, participant_id):
        self.participant_id = participant_id

    def start_experiment(self):
        if not self.check_streams():
            messagebox.showerror("Missing Channels", "Essential channels are missing please ensure they're running.")
            return

        if not self.on_experiment:
            if self.mode == 'EGG':
                self.experiment = EGGAttention(self.participant_id, self.mode, self.terminal,
                                               self.__experiment_duration.get(), self.on_experiment_completed)
            elif self.mode == 'THEATER':
                self.experiment = TheaterTrialRoutine(self.participant_id, self.mode, self.terminal,self.__experiment_duration.get(),self.on_experiment_completed)
            elif self.mode == 'MOLE':
                self.experiment = Mole(self.participant_id, self.mode, self.terminal, self.__experiment_duration.get(),
                                       self.on_experiment_completed)
            else:
                self.experiment = FishingMultitasking(self.participant_id, self.mode, self.terminal,
                                                      self.__experiment_duration.get(), self.__fishing_duration.get(),
                                                      self.on_experiment_completed, 'trial')

            self.on_experiment = True
            self.start_button.config(state=tk.DISABLED)
            self.experiment_thread = threading.Thread(target=self.run_experiment)
            self.experiment_thread.start()

    def run_experiment(self):
        try:
            self.experiment.start_routine()
        finally:
            self.after(0, self.on_experiment_completed)


    def on_experiment_completed(self):
        self.on_experiment = False
        self.start_button.config(state=tk.NORMAL)
        self.terminal.write_text("All experiments completed.")

    def check_streams(self):
        streams = pylsl.resolve_streams()
        names_of_available_streams = [stream.name() for stream in streams]

        streams_required = ['AURA_Power', 'AURA_Filtered']
        if self.mode != 'FISHING':
            streams_required.append('bWell.markers')

        for stream in streams_required:
            if stream not in names_of_available_streams:
                return False
        return True

    def on_first_experiment_completed(self):
        self.terminal.write_text("First experiment (trial) completed. Starting second experiment (run).")
        self.experiment_2.start_routine()
        self.after(0, self.on_experiment_completed)
