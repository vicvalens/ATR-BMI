import pylsl

from pylsl import StreamInlet

class AuraSignalHandler:
    __STREAM_NAMES = ['AURA_Power', 'AURA_Filtered', 'bWell.Markers']

    def __init__(self, mode):
        print('solving streams')
        self.streams = []
        self.mode = mode
        self.writing_data = False
        self.inlets = {}
        self.__create_streams()
        self.stream_created_successfully, self.failed_stream = self.check_streams()
        print(self.stream_created_successfully)
        if self.stream_created_successfully:
            for i in range(len(self.__STREAM_NAMES)):
                if self.mode == 'FISHING' and self.__STREAM_NAMES[-1] == self.__STREAM_NAMES[i]:
                    continue
                self.inlets[self.__STREAM_NAMES[i]] = StreamInlet(self.streams[i][0])

    def __create_streams(self):
        for stream in self.__STREAM_NAMES:
            if self.mode == 'FISHING' and self.__STREAM_NAMES[-1] == stream:
                continue
            new_stream = pylsl.resolve_stream('name', stream)
            self.streams.append(new_stream)


    def check_streams(self) -> (bool, str):
        """
        Checks if the created streams exist or not.
        :return: a boolean indicating if the stream exists or not and a string containing the name of the fault channel,
        in case there's no fault channel the string returned is empty
        """
        for i in range(len(self.streams)):
            if len(self.streams[i]) == 0:
                return False, self.__STREAM_NAMES[i]
        return True, ''

    def get_data_from_streams(self):
        all_data = []
        for i in range(len(self.streams)):
            if self.mode == 'FISHING' and self.__STREAM_NAMES[-1] == self.__STREAM_NAMES[i]:
                continue
            inlet_data, timestamp = self.inlets[self.__STREAM_NAMES[i]].pull_sample()
            all_data.append(inlet_data)
            print(self.__STREAM_NAMES[i])
            print(inlet_data)
            print(timestamp)

        return all_data

    def close_streams(self):
        for _, inlet in self.inlets.items():
            inlet.close_stream()
