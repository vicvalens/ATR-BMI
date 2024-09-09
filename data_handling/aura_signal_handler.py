import pylsl

from pylsl import StreamInlet

class AuraSignalHandler:
    __STREAM_NAMES = ['AURA_Power', 'AURA_Filtered']

    def __init__(self, mode):
        """
        Creates a new object that is used to manage the Signals from different streams. The
        :param mode:
        """
        self.streams = []
        self.mode = mode
        self.writing_data = False
        self.b_well_inlet = None
        self.inlets = {}
        self.__create_streams()
        self.stream_created_successfully, self.failed_stream = self.check_streams()
        if self.stream_created_successfully:
            for i in range(len(self.__STREAM_NAMES)):
                self.inlets[self.__STREAM_NAMES[i]] = StreamInlet(self.streams[i][0])

        if mode != 'FISHING':
            pass
            # self.__create_b_well()


    def __create_b_well(self):
        """
        If needed this function creates a b-well stream for the modes that requiere this data.
        :return: None
        """
        b_well_stream = pylsl.resolve_stream('name', 'bWell.Markers')
        if len(b_well_stream) != 0:
            self.b_well_inlet = pylsl.StreamInlet(b_well_stream[0])

    def __create_streams(self):
        """
        Creates the streams related to aura connections, if more channels are desired they must be added to the
        `__STREAM_NAMES` list.
        :return: None
        """
        for stream in self.__STREAM_NAMES:
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
        """
        Gets data from the streams. one piece at the time, if the bWell channel is open also gets the data from this
        inlet.
        :return: Data gathered from the streams in the form of a list of tuples of an array of floats and a timestamp.
        """
        all_data = []
        for i in range(len(self.streams)):
            inlet_data, timestamp = self.inlets[self.__STREAM_NAMES[i]].pull_sample()
            all_data.append((inlet_data, timestamp))

        if self.b_well_inlet is not None:
            all_data.append((self.b_well_inlet.pull_sample(), 0))
        return all_data

    def close_streams(self):
        """
        Terminates connection with the streams in the current session.
        :return: None
        """
        for _, inlet in self.inlets.items():
            inlet.close_stream()

        if self.b_well_inlet is not None:
            self.b_well_inlet.close_stream()
