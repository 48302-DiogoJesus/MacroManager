import tkinter as tk
from typing import Callable

from ..framework.types.MacroStatus import MacroStatus

listbox_item_font = ("Arial", 12)
listbox_selected_item_font = ("Arial", 12, "bold")

class MacroMonitorGUI:
    def __init__(
        self,
        macro_name: str,
        onStart: Callable[[], None],
        onPause: Callable[[], None],
        onStop:  Callable[[], None],
        onSchedule: Callable[['MacroMonitorGUI', str], None],
        onUpdate: Callable[[], None]
    ) -> None:
        self.root = tk.Tk()
        self.root.title("Monitor") # Minimalist name to avoid conflict with window.select() by title
        self.root.attributes('-topmost', 1) # Make window always on top
        screen_width = self.root.winfo_screenwidth()
        window_width = 550
        window_height = 400
        x_position = screen_width - window_width
        y_position = 0
        self.root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
        title = tk.Label(self.root, text=f"Macro: {macro_name}", font=("Arial", 18))
        self.label = tk.Label(self.root, text="Status: " + MacroStatus.READY.name, font=("Arial", 11, "bold"))
        updateBtn = tk.Button(self.root, text="Update", command=onUpdate, font=("Arial", 12))
        startBtn = tk.Button(self.root, text="Start", command=onStart, font=("Arial", 12))
        stopBtn = tk.Button(self.root, text="Stop", command=onStop, font=("Arial", 12))
        pauseBtn = tk.Button(self.root, text="Pause", command=onPause, font=("Arial", 12))
        selected_option = tk.StringVar(self.root)
        def _onSchedule(time): onSchedule(self, time.split(' ')[0])
        option_menu = tk.OptionMenu(self.root, selected_option, "1 min", "5 mins", "10 mins", "30 mins", "60 mins", command=_onSchedule)
        # Create a Listbox widget
        self.listbox = tk.Listbox(self.root, font=listbox_item_font, width=window_width) 
        
        # Packing
        title.pack(padx=5, pady=5)
        updateBtn.pack(padx=5, pady=5)
        self.label.pack(padx=5, pady=5)
        self.listbox.pack()
        startBtn.pack(side=tk.LEFT)
        stopBtn.pack(side=tk.LEFT)
        pauseBtn.pack(side=tk.LEFT)
        option_menu.pack(side=tk.LEFT)
        pass

    def launchGUI(self):
        self.root.mainloop()

    def updateStatus(self, status: MacroStatus):
        def _change(): self.label.config(text="Status: " + status.name)
        self.root.after(0, _change)

    def setMessage(self, msg: str):
        def _change(): self.label.config(text=break_text_into_lines(msg))
        self.root.after(0, _change)

    def updateInstructionsWindow(self, currentInstructionIdx: int, instructionsWindow: list[str]):
        def changeInstructionsWindow():
            self.listbox.delete(0, tk.END)
            for item in instructionsWindow:
                self.listbox.insert(tk.END, item)
            self.listbox.selection_clear(0, tk.END)
            self.listbox.select_set(currentInstructionIdx)
            self.listbox.yview(tk.END)

        self.root.after(0, changeInstructionsWindow)

    def clearInstructionsWindow(self):
        def clear():
            self.listbox.delete(0, tk.END)
        self.root.after(0, clear)

    def showPopup(self, msg: str):
        popup = tk.Toplevel(self.root)
        popup.title("Popup Window")
        popup.attributes('-topmost', 1)

        # Calculate the screen width and height
        x = (popup.winfo_screenwidth() - popup.winfo_reqwidth()) // 2
        y = (popup.winfo_screenheight() - popup.winfo_reqheight()) // 2
        popup.geometry(f"+{x}+{y}")
        # popup.attributes('-topmost', 1)  # Make the popup window always on top

        # Add content to the popup window
        label = tk.Label(popup, text=break_text_into_lines(msg))
        label.pack(padx=20, pady=20)

        # Add a button to close the popup
        close_button = tk.Button(popup, text="OK", command=popup.destroy)
        close_button.pack(pady=10)

        popup.wait_window()
    
def break_text_into_lines(text, words_per_line=6):
    words = text.split()
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        if len(current_line) >= words_per_line:
            lines.append(" ".join(current_line))
            current_line = []

    if current_line:
        lines.append(" ".join(current_line))

    return "\n".join(lines)