import threading

import pandas as pd
from Models.Logistic_Regression import logistic_regression
from TrainingModesScripts.CognitiveFunctions import CognitiveFunctions
import time
import os
import shutil

class FishingMultitasking(CognitiveFunctions):
    def __init__(self, participant_id, mode, gui_terminal, duration, routine_length, on_completion_callback):
        super().__init__(participant_id, mode, on_completion_callback)
        self.bmi_thread = None
        self.participant_id = participant_id
        self.gui_terminal = gui_terminal
        self.length_of_experiment = duration
        self.routine_length = routine_length

    def routine(self):
        self.trial_routine()
        self.experiment_routine()

    def trial_routine(self):
        self.gui_terminal.write_text("**** Calibration Stage ****")
        self.gui_terminal.write_text("Press Enter to start Fishing Calibration session...")
        self.gui_terminal.write_text("sending: start_session:fishing")
        self.data_writer.set_state("start_session:fishing")

        for i in range(self.length_of_experiment):
            self.gui_terminal.write_text("----> Trial: " + str(i + 1))
            self.__fishing_trial_routine()
        self.data_writer.set_state("end_session:fishing")
        self.gui_terminal.write_text("sending: end_session:fishing")
        self.gui_terminal.write_text("End fishing Calibration routine")

        directory = os.path.join('participants/', self.participant_id)
        source_filename = self.search_and_copy(directory)
        self.gui_terminal.write_text(source_filename)
        shutil.copyfile(source_filename, "../../Data/fishing.csv")
        self.gui_terminal.write_text(f'File {source_filename} has been copied as fishing.csv')

    def experiment_routine(self):
        self.gui_terminal.write_text("*****Lunching BMI Control Sender ****")
        time.sleep(2)
        self.bmi_thread = threading.Thread(target=self.bmi_calibration)
        self.bmi_thread.start()
        # repeat Fishing scene
        self.gui_terminal.write_text("**** Evaluation Stage ****")
        self.gui_terminal.write_text("Press Enter to start Fishing Evaluation session...")
        self.data_writer.set_state("start_session:fishing_evaluation")
        self.gui_terminal.write_text("sending: start_session:fishing_evaluation")
        for i in range(self.routine_length):
            self.gui_terminal.write_text("----> Trial: " + str(i + 1))
            self.__fishing_trial_routine()
        self.data_writer.set_state("end_session:fishing_evaluation")

        self.gui_terminal.write_text("sending: end_session:fishing_evaluation")
        self.gui_terminal.write_text("End fishing Calibration routine")

    def __fishing_trial_routine(self):
        self.data_writer.set_state("start_trial")
        self.gui_terminal.write_text("sending: start_trial")
        time.sleep(2)
        self.data_writer.set_state("open_scene")
        self.gui_terminal.write_text("sending: open_scene")
        time.sleep(10)
        self.data_writer.set_state("activate_fishing")
        self.gui_terminal.write_text("sending: activate_fishing")
        time.sleep(10)
        self.data_writer.set_state('close_scene')
        self.gui_terminal.write_text("sending: close_scene")
        time.sleep(1)
        self.data_writer.set_state('end_trial')
        self.gui_terminal.write_text("sending: end_trial")
        time.sleep(2)

    def search_and_copy(self, directory):
        source = ""
        for filename in os.listdir(directory):
            if filename.endswith(".csv") and 'fishing' in filename:
                source = os.path.join(directory, filename)
                break
        else:
            self.gui_terminal.write_text('No CSV file containing "fishing" found in the directory')
        return source

    def bmi_calibration(self, filename):
        self.gui_terminal.write_text("*** Creating Datasets ***")
        self.create_datasets(filename)
        self.gui_terminal.write_text("*** Trining Logistic Regression ***")
        model = logistic_regression(self.gui_terminal)

        return model

    def create_datasets(self, filename):
        # Read the csv file into a pandas dataframe
        df = pd.read_csv(filename)

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
        multitask.to_csv('multitask.csv', index=False)
        bmi.to_csv('bmi.csv', index=False)
