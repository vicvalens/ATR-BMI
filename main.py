from data_handling.aura_signal_handler import AuraSignalHandler
from data_handling.csv_aura_data_writer import AuraDataWriter

if __name__ == '__main__':
    signal_handler = AuraSignalHandler('1', 'EGG')
    writer = AuraDataWriter('1')
    for i in range(100):
        data = signal_handler.get_data_from_streams()
        writer.write_data(data[0][0], data[0][1], data[1][0], data[1][1], '')
        signal_handler.close_streams()