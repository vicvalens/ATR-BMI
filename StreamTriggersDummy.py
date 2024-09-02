from pylsl import StreamInfo, StreamOutlet

# Solicitar el nombre del stream al usuario
stream_name = input("Ingresa el nombre del stream: ")

# Crear un nuevo stream LSL con el nombre proporcionado
info = StreamInfo(stream_name, 'Markers', 1, 0, 'string')
outlet = StreamOutlet(info)

# Función para enviar un trigger
def send_trigger(trigger_name):
    outlet.push_sample([trigger_name])
    print(f'Trigger enviado: {trigger_name}')

# Bucle para enviar triggers manualmente
print("Ingresa los nombres de los triggers que deseas enviar (escribe 'exit' para salir):")
while True:
    trigger_name = input("Trigger: ")
    if trigger_name.lower() == 'exit':
        break
    send_trigger(trigger_name)

print("Programa finalizado.")
