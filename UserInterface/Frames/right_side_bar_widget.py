import tkinter as tk

class RightControlPanel(tk.Frame):
    BUTTON_FONT_COLOR = 'black'

    def __init__(self, parent):
        super().__init__(parent, bg="#2c3e50", width=200)
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self, text="Información del participante", bg="#2c3e50", fg='white', font=("Arial", 14))
        title_label.pack(side="top", fill="x", pady=10)

        button_frame = tk.Frame(self, bg="#2c3e50")
        button_frame.pack(side="bottom", fill="x", pady=20)

        btn1 = tk.Button(button_frame, text="Set", bg="#34495e", fg=self.BUTTON_FONT_COLOR,
                         activebackground="#2c3e50", activeforeground="#ecf0f1",
                         bd=0, pady=10, font=("Arial", 12))
        btn1.pack(side="left", expand=True, padx=5)

        btn2 = tk.Button(button_frame, text="Release", bg="#34495e", fg=self.BUTTON_FONT_COLOR,
                         activebackground="#2c3e50", activeforeground="#ecf0f1",
                         bd=0, pady=10, font=("Arial", 12))
        btn2.pack(side="left", expand=True, padx=5)
