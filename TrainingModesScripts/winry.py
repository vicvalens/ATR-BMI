import pylsl
import numpy as np
import pywt
import joblib
from tensorflow.keras.models import load_model
import threading


class Winry:
    def __init__(self, participant_id):
        self.participant_id = participant_id
        self.model = None
        self.scaler = None
        self.best_wavelet = 'db4'
        self.best_level = 5
        self.expected_input_shape = None
        self.sample_rate = None
        self.accumulation_period = 5.0
        self.brain_inlet = None
        self.label_outlet = None
        self.running = False
        self.thread = None

    def load_model(self):
        model_file_path = f'participants/{self.participant_id}/best_model.h5'
        self.model = load_model(model_file_path)
        self.expected_input_shape = self.model.input_shape[1]

        scaler_file_path = f'Models/scaler.joblib'
        self.scaler = joblib.load(scaler_file_path)

    def wavelet_transform(self, data):
        coeffs = pywt.wavedec(data, self.best_wavelet, level=self.best_level)
        return np.concatenate(coeffs, axis=-1)

    def pad_or_truncate(self, data, size):
        if len(data) > size:
            return data[:size]
        elif len(data) < size:
            return np.pad(data, (0, size - len(data)), 'constant')
        else:
            return data

    def setup_lsl_streams(self):
        brain_stream = pylsl.resolve_stream("name", "AURA_Power")
        if not brain_stream:
            raise RuntimeError("No EEG stream found.")

        self.brain_inlet = pylsl.StreamInlet(brain_stream[0])
        info = self.brain_inlet.info()
        self.sample_rate = info.nominal_srate()
        print(f"LSL stream found with sample rate: {self.sample_rate} Hz")
        self.brain_inlet.open_stream()

        label_info = pylsl.StreamInfo('testtriggers2', 'Markers', 1, 0, 'string', 'myuniquelabelid')
        self.label_outlet = pylsl.StreamOutlet(label_info)

    def classify_eeg_data(self):
        num_samples_to_accumulate = int(self.sample_rate * self.accumulation_period)
        accumulated_samples = []

        while self.running:
            sample, timestamp = self.brain_inlet.pull_sample()
            if sample is None:  # timeout occurred
                continue

            accumulated_samples.append(sample)

            if len(accumulated_samples) >= num_samples_to_accumulate:
                accumulated_samples_np = np.array(accumulated_samples)
                print(f"Features before scaling:\n{accumulated_samples_np.shape}")

                accumulated_samples_scaled = self.scaler.transform(accumulated_samples_np)
                samples_wavelet = np.array([self.wavelet_transform(sample) for sample in accumulated_samples_scaled])
                samples_wavelet = samples_wavelet.reshape(1, -1)
                samples_wavelet = self.pad_or_truncate(samples_wavelet[0], self.expected_input_shape)
                samples_wavelet = samples_wavelet.reshape(1, -1)

                print(f"Shape after wavelet transform and reshaping: {samples_wavelet.shape}")

                probabilities = self.model.predict(samples_wavelet)
                label = np.argmax(probabilities, axis=1)

                print(f"Classified label: {label[0]}")
                self.label_outlet.push_sample([str(label[0])])
                print(f"Sent label via LSL: {label[0]}")

                accumulated_samples = []

        print("EEG classification stopped.")

    def run(self):
        self.load_model()
        self.setup_lsl_streams()
        self.running = True
        self.classify_eeg_data()

    def start(self):
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        print("EEG Classifier thread stopped.")
