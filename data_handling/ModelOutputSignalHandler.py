import numpy as np
from pylsl import StreamInfo, StreamOutlet


def control_sender(self, model):
    # Create a new StreamInfo and outlet
    info = StreamInfo('fishing_triggers', 'markers', 1, 0, 'string', 'myuidw43536')
    outlet = StreamOutlet(info)
    while True:
        sample, timestamp = self.inlets['AURA_Power'].pull_sample()
        self.sample_list.append(sample)

        if len(self.sample_list) >= 175:
            # convert list of samples into a 2D numpy array
            data_array = np.array(self.sample_list)

            # compute the average of the samples
            avg_sample = np.mean(data_array, axis=0)

            # reshape the averaged sample
            avg_sample = avg_sample.reshape(1, -1)

            # feed the averaged sample into the model and print the prediction
            result = model.predict(avg_sample)
            outlet.push_sample([str(result[0])])  # start_trial

            # clear the sample list to start collecting next 175 samples
            self.sample_list = []
