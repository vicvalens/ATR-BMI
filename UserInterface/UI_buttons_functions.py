import tkinter as tk
from tkinter import ttk

class ConfirmationAndExperimentSettings(tk.Frame):
    __BACKGROUND_COLOR = "white"

    def __init__(self, parent):
        super().__init__(parent, bg=self.__BACKGROUND_COLOR)
        self.details_and_configuration_frame = None
        self.value_label = None
        self.information_label = None
        self.__experiment_duration = tk.IntVar(value=5)

    def egg_attention_menu(self):
        self.clear_frame()
        self.create_side_frame()
        self.create_title('Egg Attention')
        self.information_label = 'Minutos de duración: '
        self.create_slider()
        self.create_start_button()

    def theater_memory_menu(self):
        self.clear_frame()
        self.create_side_frame()
        self.create_title('Theater Memory')
        self.information_label = 'Numero de pruebas: '
        self.create_slider()
        self.create_start_button()


    def mole_control_inhibition_menu(self):
        self.clear_frame()
        self.create_side_frame()
        self.create_title('Mole control inhibition')
        self.information_label = 'Minutos de duración: '
        self.create_slider()
        self.create_start_button()


    def fishing_multitasking_bmi_menu(self):
        self.clear_frame()
        self.create_side_frame()
        self.create_title('Fishing multitasking')
        self.information_label = 'Numero de pruebas: '
        self.create_slider()
        self.create_start_button()


    def create_start_button(self):
        start_button = tk.Button(self.details_and_configuration_frame, text='Start experiment', fg='black', bg='#D3D3D3', height=5, width=15)
        start_button.pack(side='bottom', fill='x')

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def __update_slider_value(self, event):
        value = round(float(self.__experiment_duration.get()))
        self.__experiment_duration.set(value)
        self.value_label.config(text=self.information_label + str(self.__experiment_duration.get()))

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
            to=60,
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
