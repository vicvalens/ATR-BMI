import os
import time

# Ruta de los dos códigos Python que deseas ejecutar
ruta_codigo1 = "Scripts/Script1/main_eeg_trigger_saver_eeg_refactored.py"
ruta_codigo2 = "Scripts/Script2/main_trigger_server_Cognitive_Training_Group.py"
ruta_codigo3 = "Scripts/Script3/dummyStream.py"

# Abrir código 1 en una nueva terminal (para Windows)La f
os.system(f"start cmd /c python {ruta_codigo1}")

# Esperar 2 segundos
time.sleep(2)

# Abrir código 2 en una nueva terminal (para Windows)
os.system(f"start cmd /c python {ruta_codigo2}")

# Esperar 2 segundos
time.sleep(2)

# Abrir código 3 en una nueva terminal (para Windows)
os.system(f"start cmd /c python {ruta_codigo3}")