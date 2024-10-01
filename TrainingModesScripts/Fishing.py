from pylsl import pylsl, StreamOutlet, StreamInfo

from Models.CreateModel import ModelCreator

from TrainingModesScripts.CognitiveFunctions import CognitiveFunctions
import time
import os
import shutil

from TrainingModesScripts.winry import Winry
from UserInterface.GatherDataInterface.GatherTrainDataInterface import CountdownApp


class FishingMultitasking(CognitiveFunctions):
    def __init__(self, participant_id, mode, gui_terminal, duration, routine_length, on_completion_callback, model_type):
        super().__init__(participant_id, mode, on_completion_callback)
        # Create a new StreamInfo
        self.model = None
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
        self.model_type = model_type

    def routine(self):
        self.gui_terminal.write_text("**** Launching Calibration process ****")
        self.is_writing_on = False
        countdown = CountdownApp(self.participant_id, self.model_type)
        self.gui_terminal.write_text("Gathering training data...")
        self.gui_terminal.write_text(self.model_type)
        while countdown.running:
            pass
        else:
            self.is_writing_on = True
            self.gui_terminal.write_text("**** Calibration process terminated ****")
            self.gui_terminal.write_text("Creating model for patient")
            self.model = ModelCreator(f"participants/{self.participant_id}/training.csv", self.participant_id, self.gui_terminal, self.model_type)
            self.model.search_and_create_best_model()
            self.model.save_model()
            self.winry = Winry(self.participant_id)
            self.winry.start()
            self.trial_routine()


    def trial_routine(self):
        self.gui_terminal.clear_text()
        self.gui_terminal.write_text("******** Routine session ********")
        self.gui_terminal.write_text("**** Model in use ****")
        self.gui_terminal.write_text(self.model.get_best_model().summary())
        self.gui_terminal.write_text("sending: start_session:fishing")
        self.data_writer.set_state("start_session:fishing")

        for i in range(self.length_of_experiment):
            self.gui_terminal.write_text("----> Trial: " + str(i + 1))
            if self.model_type == "5 Classes model":
                self.__fishing_trial_routine_5_classes()
            else:
                self.__fishing_trial_routine_3_classes()
        self.data_writer.set_state("end_session:fishing")
        self.gui_terminal.write_text("sending: end_session:fishing")
        self.gui_terminal.write_text("End fishing routine")
        self.stop_event.set()

        directory = os.path.join('participants/', self.participant_id)
        source_filename = self.search_and_copy(directory)
        self.gui_terminal.write_text(source_filename)
        shutil.copyfile(source_filename, str('participants/' + self.participant_id + '/' + 'fishing.csv'))
        self.filename_training =  'participants/' + self.participant_id + '/' + 'fishing.csv'
        self.gui_terminal.write_text(f'File {source_filename} has been copied as fishing.csv')
        self.winry.stop()

    def __begin_trial(self):
        # Resolviendo el stream de 'testtriggers2' para recibir triggers
        self.gui_terminal.write_text("Resolviendo stream de 'testtriggers2' para recibir triggers...")
        streams = pylsl.resolve_stream('name', 'testtriggers2')
        if not streams:
            self.gui_terminal.write_text("No se encontró el stream 'testtriggers2'.")
            return

        self.inlet = pylsl.StreamInlet(streams[0])
        # Enviar trigger inicial de start_trial
        self.data_writer.set_state("start_trial")
        self.gui_terminal.write_text("sending: start_trial")
        self.outlet.push_sample(["start_trial"])
        time.sleep(5)

        self.data_writer.set_state("open_scene")
        self.gui_terminal.write_text("sending: open_scene")
        self.outlet.push_sample(["open_scene"])
        time.sleep(10)

        self.data_writer.set_state("intro")
        self.gui_terminal.write_text("sending: intro")
        self.outlet.push_sample(["intro"])
        time.sleep(15)

    def __end_trial(self):
        self.data_writer.set_state("close_scene")
        self.gui_terminal.write_text("sending: close_scene")
        self.outlet.push_sample(["close_scene"])
        time.sleep(1)

        # Terminar prueba
        self.data_writer.set_state("end_trial")
        self.gui_terminal.write_text("sending: end_trial")
        self.outlet.push_sample(["end_trial"])
        time.sleep(5)

    def check_trigger(self, expected_trigger):
        timeout = 15  # Tiempo máximo para esperar el trigger esperado (15 segundos)
        start_time = time.time()

        while time.time() - start_time < timeout:
            trigger, _ = self.inlet.pull_sample(timeout=0.5)
            if trigger:
                self.gui_terminal.write_text(f"Trigger recibido: {trigger[0]}")
                if trigger[0] == expected_trigger:
                    return True  # Trigger coincide con el esperado
        return False  # No se recibió el trigger esperado a tiempo

    def __fishing_trial_routine_3_classes(self):

        self.__begin_trial()

        # Movement of right arm (MR)
        for _ in range(2):
            if self.check_trigger("2"):
                self.gui_terminal.write_text("Trigger coincide: move_right_arm")
                self.outlet.push_sample(["2"])
                self.data_writer.set_state("move_right_arm")
            else:
                self.gui_terminal.write_text("No se recibió el trigger esperado. Enviando: move_right_arm forzado")
                self.data_writer.set_state("move_right_arm_forced")  # Enviar el trigger de todas formas
                self.outlet.push_sample(["2"])
            time.sleep(15)

        # Movement of left arm (ML)
        for _ in range(2):
            if self.check_trigger("1"):
                self.gui_terminal.write_text("Trigger coincide: move_left_arm")
                self.data_writer.set_state("move_left_arm")
                self.outlet.push_sample(["1"])
            else:
                self.gui_terminal.write_text("No se recibió el trigger esperado. Enviando: move_left_arm forzado")
                self.data_writer.set_state("move_left_arm_forced")  # Enviar el trigger de todas formas
                self.outlet.push_sample(["1"])
            time.sleep(15)

        self.__end_trial()

    def __fishing_trial_routine_5_classes(self):

        # Enviar trigger inicial de start_trial
        self.__begin_trial()

        # Extensión del brazo derecho (RA)
        if self.check_trigger("3"):
            self.gui_terminal.write_text("Trigger coincide: lower_right_arm")
            self.outlet.push_sample(["3"])
            self.data_writer.set_state("lower_right_arm")
        else:
            self.gui_terminal.write_text("No se recibió el trigger esperado. Enviando: lower_right_arm forzado")
            self.data_writer.set_state("lower_right_arm_forced")  # Enviar el trigger de todas formas
            self.outlet.push_sample(["3"])
        time.sleep(15)

        # Flexión del brazo derecho (RA)
        if self.check_trigger("2"):
            self.gui_terminal.write_text("Trigger coincide: rise_right_arm")
            self.outlet.push_sample(["2"])
            self.data_writer.set_state("rise_right_arm")
        else:
            self.gui_terminal.write_text("No se recibió el trigger esperado. Enviando: rise_right_arm forzado")
            self.data_writer.set_state("rise_right_arm_forced")  # Enviar el trigger de todas formas
            self.outlet.push_sample(["2"])
        time.sleep(15)

        # Extensión del brazo izquierdo (LA)
        if self.check_trigger("1"):
            self.gui_terminal.write_text("Trigger coincide: lower_left_arm")
            self.data_writer.set_state("lower_left_arm")
            self.outlet.push_sample(["1"])
        else:
            self.gui_terminal.write_text("No se recibió el trigger esperado. Enviando: lower_left_arm forzado")
            self.data_writer.set_state("lower_left_arm_forced")  # Enviar el trigger de todas formas
            self.outlet.push_sample(["1"])
        time.sleep(15)

        # Flexión del brazo izquierdo (LA)
        if self.check_trigger("0"):
            self.gui_terminal.write_text("Trigger coincide: rise_left_arm")
            self.data_writer.set_state("rise_left_arm")
            self.outlet.push_sample(["0"])
        else:
            self.gui_terminal.write_text("No se recibió el trigger esperado. Enviando: rise_left_arm forzado")
            self.data_writer.set_state("rise_left_arm_forced")  # Enviar el trigger de todas formas
            self.outlet.push_sample(["0"])
        time.sleep(15)

        # Cerrar escena
        self.__end_trial()

    def search_and_copy(self, directory):
        source = ""
        for filename in os.listdir(directory):
            if filename.endswith(".csv") and 'fishing' in filename and not 'egg' in filename:
                source = os.path.join(directory, filename)
                break
        else:
            self.gui_terminal.write_text('No CSV file containing "fishing" found in the directory')
        return source

    def get_winry(self):
        return self.winry
