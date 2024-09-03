# from venv import create
#
# import pylsl
# import csv
# import os
# from datetime import datetime
#
# DEFAULT_FOLDER_PATH = "participants"
# stream_markers = None
# markers = None
#
# def initialize_bWell_stream():
#     global stream_markers
#
#     print("Connecting to bWell.Markers stream")
#     stream_markers = pylsl.resolve_stream('name', 'bWell.Markers')
#
#     if len(stream_markers) == 0:
#         print("No se encontró el stream 'bWell.Markers'. Asegúrate de que esté siendo enviado por otro programa.")
#         return None
#
#     inlet_markers=pylsl.StreamInlet(stream_markers[0])
#     print("Connected!")
#     return inlet_markers
#
#
# def check_len_streams(channels, eeg_channels, trigger_channels) -> (bool, str):
#     ok = True
#     fail_channel = ''
#     if len(channels) == 0 or len(eeg_channels) == 0 or len(trigger_channels) == 0:
#         ok = False
#         if len(channels) == 0:
#             fail_channel = 'AURA_Power'
#         elif len(eeg_channels) == 0:
#             fail_channel = 'AURA_Filtered'
#         else:
#             fail_channel = 'Test_Triggers'
#
#     return ok, fail_channel
#
# def create_directory(participant_id):
#     folder_path = os.path.join(DEFAULT_FOLDER_PATH, participant_id)
#     if not os.path.isdir(folder_path):
#         os.makedirs(folder_path)
#         print("Directory: " + participant_id + " created")
#     else:
#         print("Directory: " + participant_id + " found")
#
#     return folder_path
#
#
# def create_writers(session_name, folder_path):
#     now = datetime.now()
#     now_str = now.strftime("%Y-%m-%d_%H-%M-%S")
#     my_filename = session_name + "_" + now_str
#     csv_path = os.path.join(folder_path, f'{my_filename}.csv')
#     archivo_csv = open(csv_path, "w", newline="")
#     writer = csv.writer(archivo_csv)
#     print("Recording started...")
#     my_filename_eeg = session_name + "_eeg_" + now_str
#     csv_path_eeg = os.path.join(folder_path, f'{my_filename_eeg}.csv')
#     archivo_eeg_csv = open(csv_path_eeg, "w", newline="")
#     writer_eeg = csv.writer(archivo_eeg_csv)
#     return writer, writer_eeg, csv_path, csv_path_eeg
#
#
# # Lo mas cercano a main
# def esperar_stream():
#     global markers
#     print("Resolviendo Streams")
#
#     # Resolver el stream "AURA_Power"
#     canales = pylsl.resolve_stream('name', 'AURA_Power')
#     canales_eeg = pylsl.resolve_stream('name', 'AURA_Filtered')
#     canales_triggers = pylsl.resolve_stream('name', 'test_triggers')
#
#     streams_status = check_len_streams(canales, canales_eeg, canales_triggers)
#     if streams_status[0]:
#         # Create an object for the streams
#         entrada = pylsl.StreamInlet(canales[0])
#         entrada_eeg = pylsl.StreamInlet(canales_eeg[0])
#         entrada_triggers = pylsl.StreamInlet(canales_triggers[0])
#
#         print("Esperando datos desde el stream 'AURA_Power', Triggers...")
#
#         grabando = False
#         writer = None
#         participant_id = ""
#         folder_path = DEFAULT_FOLDER_PATH
#         session_name = ""
#
#         archivo_csv = None
#         inlet_markers = None
#         archivo_eeg_csv = None
#         writer_eeg = None
#
#         while True:
#             sample, timestamp = entrada.pull_sample()
#             sample_eeg, timestamp_eeg = entrada_eeg.pull_sample()
#             triggers, _ = entrada_triggers.pull_sample(0)
#
#             if inlet_markers is not None:
#                 markers, _ = inlet_markers.pull_sample(0)
#                 if markers is None:
#                     marker_label = "0"
#                 else:
#                     marker_label = markers
#
#             if triggers is None:
#                 trigger_label = "0"
#             elif ':' in str(triggers[0]):
#                 trigger_entry = str(triggers[0]).split(":")
#                 if trigger_entry[0] == "participant_id":
#                     participant_id = trigger_entry[1]
#                     print("Id: " + participant_id)
#                     folder_path = create_directory(participant_id)
#                     inlet_markers = initialize_bWell_stream()
#                 elif trigger_entry[0] == "start_session":
#                     print("Start Session: " + trigger_entry[1])
#                     session_name = trigger_entry[1]
#                     if not grabando:
#                         trigger_label = "start_session_" + session_name
#                         grabando = True
#                         writer, writer_eeg, archivo_csv, archivo_eeg_csv = create_writers(session_name, folder_path)
#                 elif trigger_entry[0] == "end_session":
#                     print("End Session: " + trigger_entry[1])
#                     if grabando:
#                         trigger_label = "end_session_" + session_name
#                         writer.writerow([timestamp] + sample + [trigger_label])
#                         writer_eeg.writerow([timestamp] + sample_eeg + [trigger_label])
#                         grabando = False
#                         archivo_csv.close()
#                         archivo_eeg_csv.close()
#                         print(trigger_label)
#                         print("Recording finished...")
#                         folder_path = os.path.join(DEFAULT_FOLDER_PATH, participant_id)
#             elif str(triggers[0]) == "exit":
#                 print("Finished")
#                 break
#             else:
#                 trigger_label = triggers
#                 print(str(triggers[0]))
#
#             if grabando:
#                 writer.writerow([timestamp] + sample + [trigger_label] + [marker_label[0]])
#                 writer_eeg.writerow([timestamp] + sample_eeg + [trigger_label] + [marker_label[0]])
#     else:
#         print(f"No se encontró el stream {streams_status[1]}. Asegúrate de que esté siendo enviado por otro programa.")
#
#
# # Esto no debe de estar aqui
# esperar_stream()
