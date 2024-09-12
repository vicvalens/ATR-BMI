import threading

import pandas as pd
from pylsl import pylsl, StreamOutlet, StreamInfo

from Models.Logistic_Regression import logistic_regression
from TrainingModesScripts.CognitiveFunctions import CognitiveFunctions
import time
import os
import shutil

class FishingMultitasking(CognitiveFunctions):
    def __init__(self, participant_id, mode, gui_terminal, duration, routine_length, on_completion_callback, run_trial):
        super().__init__(participant_id, mode, on_completion_callback)
        # Create a new StreamInfo
        info = StreamInfo(name='test_triggers', type='Markers', channel_count=1, channel_format='string',
                          source_id='test_triggers_id')

        # Create a new outlet
        self.outlet = StreamOutlet(info)

        self.filename_training = None
        self.bmi_thread = None
        self.participant_id = participant_id
        self.gui_terminal = gui_terminal
        self.length_of_experiment = duration
        self.routine_length = routine_length
        self.run_trial = run_trial

    def routine(self):
        self.trial_routine()

    def trial_routine(self):
        self.gui_terminal.clear_text()
        self.gui_terminal.write_text("**** Calibration Stage ****")
        self.gui_terminal.write_text("sending: start_session:fishing")
        self.data_writer.set_state("start_session:fishing")

        for i in range(self.length_of_experiment):
            self.gui_terminal.write_text("----> Trial: " + str(i + 1))
            self.__fishing_trial_routine()
        self.data_writer.set_state("end_session:fishing")
        self.gui_terminal.write_text("sending: end_session:fishing")
        self.gui_terminal.write_text("End fishing Calibration routine")
        self.stop_event.set()

        directory = os.path.join('participants/', self.participant_id)
        source_filename = self.search_and_copy(directory)
        self.gui_terminal.write_text(source_filename)
        shutil.copyfile(source_filename, str('participants/' + self.participant_id + '/' + 'fishing.csv'))
        self.filename_training =  'participants/' + self.participant_id + '/' + 'fishing.csv'
        self.gui_terminal.write_text(f'File {source_filename} has been copied as fishing.csv')

    def experiment_routine(self):
        self.gui_terminal.clear_text()
        self.gui_terminal.write_text("*****Lunching BMI Control Sender ****")
        time.sleep(2)
        self.bmi_thread = threading.Thread(target=self.bmi_calibration)
        self.bmi_thread.start()
        # repeat Fishing scene
        self.gui_terminal.write_text("**** Evaluation Stage ****")
        self.data_writer.set_state("start_session:fishing_evaluation")
        self.gui_terminal.write_text("sending: start_session:fishing_evaluation")

        for i in range(self.routine_length):
            self.gui_terminal.write_text("----> Trial: " + str(i + 1))
            self.__fishing_trial_routine()
        self.data_writer.set_state("end_session:fishing_evaluation")
        self.gui_terminal.write_text("sending: end_session:fishing_evaluation")
        self.stop_event.set()
        self.gui_terminal.write_text("End fishing Calibration routine")

    def __fishing_trial_routine(self):
        # Resolviendo el stream de 'testtriggers2' para recibir triggers
        self.gui_terminal.write_text("Resolviendo stream de 'testtriggers2' para recibir triggers...")
        streams = pylsl.resolve_stream('name', 'testtriggers2')
        if not streams:
            self.gui_terminal.write_text("No se encontró el stream 'testtriggers2'.")
            return

        inlet = pylsl.StreamInlet(streams[0])

        # Enviar trigger inicial de start_trial
        self.data_writer.set_state("start_trial")
        self.gui_terminal.write_text("sending: start_trial")
        time.sleep(5)

        self.data_writer.set_state("open_scene")
        self.gui_terminal.write_text("sending: open_scene")
        time.sleep(15)

        # Función para verificar si el trigger recibido coincide con el esperado
        def check_trigger(expected_trigger):
            timeout = 15  # Tiempo máximo para esperar el trigger esperado (15 segundos)
            start_time = time.time()

            while time.time() - start_time < timeout:
                trigger, _ = inlet.pull_sample(timeout=0.5)
                if trigger:
                    self.gui_terminal.write_text(f"Trigger recibido: {trigger[0]}")
                    if trigger[0] == expected_trigger:
                        return True  # Trigger coincide con el esperado
            return False  # No se recibió el trigger esperado a tiempo

        # Extensión del brazo derecho (RA)
        if check_trigger("3"):
            self.gui_terminal.write_text("Trigger coincide: lower_right_arm")
            self.outlet.push_sample(["3"])
            self.data_writer.set_state("3")
        else:
            self.gui_terminal.write_text("No se recibió el trigger esperado. Enviando: lower_right_arm forzado")
            self.outlet.push_sample(["3"])
            self.data_writer.set_state("3")  # Enviar el trigger de todas formas
        time.sleep(15)

        # Flexión del brazo derecho (RA)
        if check_trigger("2"):
            self.gui_terminal.write_text("Trigger coincide: rise_right_arm")
            self.outlet.push_sample(["2"])
            self.data_writer.set_state("2")
        else:
            self.gui_terminal.write_text("No se recibió el trigger esperado. Enviando: rise_right_arm forzado")
            self.data_writer.set_state("2")  # Enviar el trigger de todas formas
            self.outlet.push_sample(["2"])
        time.sleep(15)

        # Extensión del brazo izquierdo (LA)
        if check_trigger("1"):
            self.gui_terminal.write_text("Trigger coincide: lower_left_arm")
            self.data_writer.set_state("1")
            self.outlet.push_sample(["1"])
        else:
            self.gui_terminal.write_text("No se recibió el trigger esperado. Enviando: lower_left_arm forzado")
            self.data_writer.set_state("1")  # Enviar el trigger de todas formas
            self.outlet.push_sample(["1"])
        time.sleep(15)

        # Flexión del brazo izquierdo (LA)
        if check_trigger("0"):
            self.gui_terminal.write_text("Trigger coincide: rise_left_arm")
            self.data_writer.set_state("0")
            self.outlet.push_sample(["0"])
        else:
            self.gui_terminal.write_text("No se recibió el trigger esperado. Enviando: rise_left_arm forzado")
            self.data_writer.set_state("0")  # Enviar el trigger de todas formas
            self.outlet.push_sample(["0"])
        time.sleep(15)

        # Cerrar escena
        self.data_writer.set_state("close_scene")
        self.gui_terminal.write_text("sending: close_scene")
        time.sleep(1)

        # Terminar prueba
        self.data_writer.set_state("end_trial")
        self.gui_terminal.write_text("sending: end_trial")
        time.sleep(5)

    def search_and_copy(self, directory):
        source = ""
        for filename in os.listdir(directory):
            if filename.endswith(".csv") and 'fishing' in filename and not 'egg' in filename:
                source = os.path.join(directory, filename)
                break
        else:
            self.gui_terminal.write_text('No CSV file containing "fishing" found in the directory')
        return source

    def bmi_calibration(self):
        self.gui_terminal.write_text("*** Creating Datasets ***")
        self.create_datasets()
        self.gui_terminal.write_text("*** Training Logistic Regression ***")
        model = logistic_regression(self.gui_terminal, self.participant_id)

        return model

    def create_datasets(self):
        if self.filename_training is None:
            self.filename_training = 'participants/' + self.participant_id + '/' + 'fishing.csv'
        # Read the csv file into a pandas dataframe
        df = pd.read_csv(self.filename_training)
        # Initiate the multitask and bmi datasets as empty lists
        multitask = []
        bmi = []

        # Initialize flags for data capture
        capture_multitask = False
        capture_bmi = False

        trial = 0
        bmi_entries = 0
        multitask_entries = 0

        # Loop through each row in the dataframe
        for index, row in df.iterrows():
            # Check the 42nd column for keywords and set capture flags accordingly
            if row[41] == "['open_scene']":
                trial += 1
                self.gui_terminal.write_text("Collecting Trial " + str(trial))
                capture_multitask = True
            elif row[41] == "['activate_fishing']":
                multitask_entries = 0
                capture_multitask = False
                capture_bmi = True
                continue  # skip adding this row to any dataset
            elif row[41] == "['close_scene']":
                bmi_entries = 0
                capture_bmi = False

            # Add the row to corresponding dataset based on capture flags
            if capture_multitask:
                multitask.append(row)
                multitask_entries = multitask_entries + 1
            elif capture_bmi:
                bmi.append(row)
                bmi_entries = bmi_entries + 1

        # Convert the lists to dataframes using pandas.concat
        multitask = pd.concat(multitask, axis=1).transpose()
        bmi = pd.concat(bmi, axis=1).transpose()

        # Remove the 1st and last columns from each dataframe
        multitask = multitask.iloc[:, 1:-2]
        bmi = bmi.iloc[:, 1:-2]

        # Save the resultant dataframes to csv files
        multitask.to_csv('participants/' + self.participant_id + '/multitask.csv', index=False)
        bmi.to_csv('participants/' + self.participant_id + '/bmi.csv', index=False)
