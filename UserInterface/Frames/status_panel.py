import tkinter as tk

class StatusPanel(tk.Frame):
    __BACKGROUND_COLOR = "#000F26"
    __TEXT_COLOR = "white"

    def __init__(self, parent):
        super().__init__(parent, bg=self.__BACKGROUND_COLOR, height=200)
        self.terminal_frame = None
        self.create_widgets()
        self.write_text('Panel de estado. Aquí se mostrará el estado de los experimentos que se están realizando.')

    def create_widgets(self):
        self.terminal_frame = tk.Text(self, bg=self.__BACKGROUND_COLOR, fg=self.__TEXT_COLOR, wrap=tk.WORD)
        self.terminal_frame.pack(fill="both", expand=True)
        self.terminal_frame.config(state='disabled')  # Make the Text widget read-only

    def write_text(self, text):
        if text is not None:
           self.terminal_frame.config(state='normal')  # Enable the Text widget for modification
           self.terminal_frame.insert(tk.END, text + "\n")
           self.terminal_frame.see(tk.END)  # Autoscroll to the bottom
           self.terminal_frame.config(state='disabled')  # Make the Text widget read-only again

    def clear_text(self):
        self.terminal_frame.config(state='normal')  # Enable the Text widget for modification
        self.terminal_frame.delete(1.0, tk.END)
        self.terminal_frame.config(state='disabled')  # Make the Text widget read-only again

    def get_text(self):
        return self.terminal_frame.get(1.0, tk.END)
