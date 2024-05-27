import tkinter as tk
from tkinter import filedialog
import subprocess
import os
import webbrowser

class TaskLauncher(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Task Launcher")

        # Labels and entries for URLs and file paths
        self.labels_entries = [
            ("Google URL:", tk.StringVar()),
            ("Folder Path:", tk.StringVar()),
            ("VS Code Path:", tk.StringVar()),
            ("PDF Path:", tk.StringVar())
        ]

        for i, (label_text, var) in enumerate(self.labels_entries):
            label = tk.Label(self, text=label_text)
            label.grid(row=i, column=0, padx=10, pady=5)
            entry = tk.Entry(self, textvariable=var, width=50)
            entry.grid(row=i, column=1, padx=10, pady=5)
            browse_button = tk.Button(self, text="Browse", command=lambda var=var: self.browse_file(var))
            browse_button.grid(row=i, column=2, padx=10, pady=5)

        # Buttons to open the tasks
        open_button = tk.Button(self, text="Open All", command=self.open_all)
        open_button.grid(row=len(self.labels_entries), column=0, padx=10, pady=5, columnspan=3)

        # Buttons to save and load the configurations
        save_button = tk.Button(self, text="Save", command=self.save_config)
        save_button.grid(row=len(self.labels_entries) + 1, column=0, padx=10, pady=5, columnspan=3)
        load_button = tk.Button(self, text="Load", command=self.load_config)
        load_button.grid(row=len(self.labels_entries) + 2, column=0, padx=10, pady=5, columnspan=3)

    def browse_file(self, var):
        filename = filedialog.askopenfilename()
        if filename:
            var.set(filename)

    def open_all(self):
        for label_text, var in self.labels_entries:
            path = var.get()
            if path:
                if "URL" in label_text:
                    webbrowser.open(path)
                else:
                    if os.path.isdir(path):
                        self.open_directory(path)
                    elif os.path.isfile(path):
                        if path.endswith(".pdf"):
                            self.open_file(path)
                        elif path.endswith(".code-workspace") or path.endswith(".py"):
                            subprocess.Popen(["code", path])
                        else:
                            self.open_file(path)

    def open_directory(self, path):
        if os.name == 'nt':  # Windows
            os.startfile(path)
        elif os.name == 'posix':  # macOS, Linux
            subprocess.Popen(['open', path] if sys.platform == 'darwin' else ['xdg-open', path])

    def open_file(self, path):
        if os.name == 'nt':  # Windows
            os.startfile(path)
        elif os.name == 'posix':  # macOS, Linux
            subprocess.Popen(['open', path] if sys.platform == 'darwin' else ['xdg-open', path])

    def save_config(self):
        config = {label_text: var.get() for label_text, var in self.labels_entries}
        with open("config.txt", "w") as f:
            for key, value in config.items():
                f.write(f"{key}:{value}\n")

    def load_config(self):
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as f:
                for line in f:
                    key, value = line.strip().split(":", 1)
                    for label_text, var in self.labels_entries:
                        if key == label_text:
                            var.set(value)

if __name__ == "__main__":
    app = TaskLauncher()
    app.mainloop()
