import tkinter as tk

class StatusPanel(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, bg="#2c3e50", height=200)
        self.create_widgets()

    def create_widgets(self):
        terminal_frame = tk.Text(self, bg="#D3D3D3")
        terminal_frame.pack(fill="both", expand=True)