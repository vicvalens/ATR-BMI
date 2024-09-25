import tkinter as tk
import csv
from tkinter import Toplevel
from PIL import Image, ImageTk
import pylsl
from pylsl import StreamInlet
import time
from datetime import datetime
import os
import threading

from tensorflow.python.distribute.device_util import current


class CountdownApp(Toplevel):
    def __init__(self, participant_id):
        super().__init__()
        self.title("EEG Data Acquisition Protocol - Motor Imagery")
        # self.attributes("-fullscreen", True) # Does not work in macOS maybe in windows there's no problem
        self.geometry("1920x1080")
        self.center_window(self)

        self.cycle_count = 1
        self.max_cycles = 5

        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(os.path.dirname(current_dir))
        self.folder_path = os.path.join('participants', participant_id)

        self.folder_path = os.path.join(project_root, self.folder_path)
        os.makedirs(self.folder_path, exist_ok=True)
        self.csv_file_path = os.path.join(self.folder_path, 'training.csv')
        self.csv_file = open(self.csv_file_path, 'w', newline='')

        self.csv_writer = csv.writer(self.csv_file)
        lsl_headers = [f'{band} {i}' for band in ['Delta', 'Theta', 'Alpha', 'Beta', 'Gamma'] for i in range(1, 9)]
        self.csv_writer.writerow(['Timestamp', 'Cycle', 'Countdown Type'] + lsl_headers)

        self.cycle_label = tk.Label(self, text=f"Cycle: {self.cycle_count}/{self.max_cycles}", font=("Century Gothic", 14))
        self.cycle_label.pack(anchor='ne', padx=5, pady=5)

        self.japanese_cycle_label = tk.Label(self, text=f"循環: {self.cycle_count}/{self.max_cycles}", font=("Century Gothic", 14))
        self.japanese_cycle_label.pack(anchor='ne', padx=5, pady=5)

        self.legend_label = tk.Label(self, text="Relax your muscles, try to think about your tongue", font=("Century Gothic", 44))
        self.legend_label.pack(pady=5)

        self.japanese_legend_label = tk.Label(self, text="力を抜いて、舌を考えてみてください", font=("Century Gothic", 44))
        self.japanese_legend_label.pack(pady=50)

        self.label = tk.Label(self, text="5", font=("Century Gothic", 150))
        self.label.pack(pady=20)

        # Store image objects as instance variables
        self.left_extend_image = self.create_image('Assets/ExtendLeft.png')
        self.left_flex_image = self.create_image('Assets/FlexLeft.png')
        self.right_extend_image = self.create_image('Assets/ExtendRight.png')
        self.right_flex_image = self.create_image('Assets/FlexRight.png')

        # Create image labels but don't pack them yet
        self.left_extend_guide_label = tk.Label(self, image=self.left_extend_image)
        self.left_flex_guide_label = tk.Label(self, image=self.left_flex_image)
        self.right_extend_guide_label = tk.Label(self, image=self.right_extend_image)
        self.right_flex_guide_label = tk.Label(self, image=self.right_flex_image)

        self.current_countdown_type = None
        self.number_cycle = None
        self.inlet = None
        self.setup_lsl()

        self.countdown_phases = [
            ("Rest", "Relax your muscles, try to think about your tongue", "力を抜いて、舌を想像してみてください", 0),
            ("Left Arm Flex", "Imagine you flex your left arm", "左手を曲げるのを想像してください", 1),
            ("Left Arm Extend", "Imagine you extend your left arm", "左手を伸ばすのを想像してください", 2),
            ("Right Arm Flex", "Imagine you flex your right arm", "右手を曲げるのを想像してください", 3),
            ("Right Arm Extend", "Imagine you extend your right arm", "右手を伸ばすのを想像してください", 4)
        ]

        self.current_phase = -1  # Start with -1 to account for preparation phase
        self.running = True
        self.data_thread = threading.Thread(target=self.data_collection_thread)
        self.data_thread.start()

        self.start_preparation()

    def create_image(self, image_path):
        image_size = (500, 500)
        image = Image.open(image_path)
        image = image.resize(image_size)
        return ImageTk.PhotoImage(image)

    def update_displayed_image(self):
        # Unpack all images first
        for label in [self.left_extend_guide_label, self.left_flex_guide_label,
                      self.right_extend_guide_label, self.right_flex_guide_label]:
            label.pack_forget()
        # Then pack the correct image based on the current phase
        if self.current_phase == 1:  # Left Arm Flex
            self.left_flex_guide_label.pack(side='left', anchor='ne', padx=5, pady=5)
        elif self.current_phase == 2:  # Left Arm Extend
            self.left_extend_guide_label.pack(side='left', anchor='ne', padx=5, pady=5)
        elif self.current_phase == 3:  # Right Arm Flex
            self.right_flex_guide_label.pack(side='right', anchor='ne', padx=5, pady=5)
        elif self.current_phase == 4:  # Right Arm Extend
            self.right_extend_guide_label.pack(side='right', anchor='ne', padx=5, pady=5)

    def start_preparation(self):
        self.legend_label.config(text="Prepare for the test")
        self.japanese_legend_label.config(text="テストの準備をしてください")
        self.countdown(5, self.start_protocol)

    def start_protocol(self):
        self.next_phase()

    def center_window(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        height = win.winfo_height()
        x = (win.winfo_screenwidth() // 2) - (width // 2)
        y = (win.winfo_screenheight() // 2) - (height // 2)
        win.geometry(f'{width}x{height}+{x}+{y}')

    def setup_lsl(self):
        brain_stream = pylsl.resolve_stream("name", "AURA_Power")
        self.inlet = StreamInlet(brain_stream[0])

    def data_collection_thread(self):
        while self.running:
            if self.current_countdown_type:
                sample, timestamp = self.inlet.pull_sample()
                self.csv_writer.writerow([datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S.%f'),
                                          self.cycle_count, self.number_cycle] + sample)
            time.sleep(0.1)

    def next_phase(self):
        self.current_phase += 1
        self.update_displayed_image()

        if self.current_phase >= len(self.countdown_phases):
            self.cycle_count += 1
            if self.cycle_count > self.max_cycles:
                self.finish_protocol()
                return
            self.current_phase = 0
            self.cycle_label.config(text=f"Cycle: {self.cycle_count}/{self.max_cycles}")
            self.japanese_cycle_label.config(text=f"循環: {self.cycle_count}/{self.max_cycles}")

        phase_name, instruction, japanese_instruction, cycle_number = self.countdown_phases[self.current_phase]
        self.current_countdown_type = phase_name
        self.legend_label.config(text=instruction)
        self.japanese_legend_label.config(text=japanese_instruction)
        self.number_cycle = cycle_number
        self.countdown(5, self.next_phase)

    def countdown(self, count, next_function):
        self.label.config(text=str(count))
        if count > 0:
            self.after(1000, self.countdown, count - 1, next_function)
        else:
            self.after(100, next_function)  # Short delay before starting next phase

    def finish_protocol(self):
        self.legend_label.config(text="Training completed. Terminating...!")
        self.japanese_legend_label.config(text="お疲れ様でした")
        self.label.config(text="")
        self.csv_file.close()
        self.running = False
        self.exit()

    def exit(self):
        self.destroy()
