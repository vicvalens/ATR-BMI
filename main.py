from data_handling.aura_signal_handler import AuraSignalHandler
from data_handling.csv_aura_data_writer import AuraDataWriter

if __name__ == '__main__':
    signal_handler = AuraSignalHandler('FISHING')
    writer = AuraDataWriter('3')
    for i in range(10):
        print('writing')
        data = signal_handler.get_data_from_streams()
        aura_data, aura_data_time = data[0]
        aura_data_eeg, aura_data_eeg_time = data[1]
        writer.write_data(aura_data, aura_data_time, aura_data_eeg, aura_data_eeg_time, [], 'FISHING')

    signal_handler.close_streams()
    writer.close_writer()
