import pylsl
from pylsl import StreamInlet, LostError

class AuraSignalHandler:
    __STREAM_NAMES = ['AURA_Power', 'AURA_Filtered']

    def __init__(self, mode):
        """
        Creates a new object that is used to manage the Signals from different streams.
        :param mode: The training mode that is currently in use.
        """
        self.streams = []
        self.sample_list = []
        self.mode = mode
        self.writing_data = False
        self.b_well_inlet = None
        self.inlets = {}
        self.__create_streams()
        self.stream_created_successfully, self.failed_stream = self.check_streams()
        if self.stream_created_successfully:
            for i in range(len(self.__STREAM_NAMES)):
                self.inlets[self.__STREAM_NAMES[i]] = StreamInlet(self.streams[i][0])

        # Crear el stream bWell solo si el modo no es 'FISHING'
        if mode != 'FISHING':
            self.__create_b_well()

    def __create_b_well(self):
        """
        Creates the b-well stream inlet if the stream is available.
        :return: None
        """
        try:
            b_well_stream = pylsl.resolve_stream('name', 'bWell.Markers')
            if len(b_well_stream) != 0:
                self.b_well_inlet = pylsl.StreamInlet(b_well_stream[0])
                print("Conectado al stream 'bWell.Markers'")
            else:
                print("No se encontró el stream 'bWell.Markers'")
        except Exception as e:
            print(f"Error al conectar con el stream 'bWell.Markers': {e}")

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
        Gets data from the streams. one piece at a time, if the bWell channel is open also gets the data from this
        inlet. If the stream is lost, it attempts to reconnect.
        :return: Data gathered from the streams in the form of a list of tuples of an array of floats and a timestamp.
        """
        all_data = []

        # Obtener datos de las streams Aura
        for i in range(len(self.streams)):
            try:
                inlet_data, timestamp = self.inlets[self.__STREAM_NAMES[i]].pull_sample(timeout=0.1)
                all_data.append((inlet_data, timestamp))
            except LostError:
                print(f"Stream perdido: {self.__STREAM_NAMES[i]}. Intentando reconectar...")
                self.__create_streams()  # Intentar reconectar en caso de pérdida
            except Exception as e:
                print(f"Error al leer el stream {self.__STREAM_NAMES[i]}: {e}")

        # Obtener datos de bWell si está disponible
        if self.b_well_inlet is not None:
            try:
                sample, timestamp = self.b_well_inlet.pull_sample(timeout=0.1)
                all_data.append((sample, timestamp))
            except LostError:
                print("Stream 'bWell.Markers' perdido. Intentando reconectar...")
                self.__create_b_well()  # Intentar reconectar en caso de pérdida
            except Exception as e:
                print(f"Error al leer el stream 'bWell.Markers': {e}")

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
