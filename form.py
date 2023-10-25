"""GUI functionality"""

from tkinter import Tk, Label, OptionMenu, StringVar, Button
from threading import Thread
from file_handler import FileHandler
import config

class BackupForm:
    """GUI functionality"""
    def __init__(self, options):

        root = Tk()
        root.geometry("400x200")
        root.maxsize(400, 200)
        root.minsize(400, 200)

        label_title = Label(root, text = "Card Backup")
        label_title.grid(row = 0, column = 0, columnspan = 4, padx = 5, pady = 5, sticky = "nwse")

        var = StringVar(root)
        var.set("Select Card")
        source = OptionMenu(root, var, *options, command = self.source_selected)
        source.grid(row = 1, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = "w")

        button_start_copy = Button(root, text = "Start copy",
                       command = self.do_copy, state = "disabled")
        button_start_copy.grid(row = 1, column = 2, columnspan = 2,
                               padx = 5, pady = 5, sticky = "e")

        self.root = root
        self.button_start_copy = button_start_copy
        self.source_selection = None

    def show(self):
        """Show the form"""
        self.root.mainloop()

    def source_selected(self, selection):
        """Callback for handling source OptionMenu change"""
        self.source_selection = selection
        self.button_start_copy["state"] = "normal"

    def do_copy(self):
        """Handler for button click"""
        fh = FileHandler(self.source_selection, config.DESTINATION_ROOT_DIRECTORY,
                         self.on_file_copied_handler, self.on_file_error_handler,
                         self.on_backup_finished_handler, self.on_backup_error_handler)
        thread = Thread(target = fh.do_copy)
        self.button_start_copy["state"] = "disabled"
        thread.start()

    def on_file_copied_handler(self, file, files_done, files_total):
        """Callback ran per file finished"""
        print(f"Copied {file}. {files_done}/{files_total}")

    def on_file_error_handler(self, file):
        """Callback when encountering an error with a single file"""

    def on_backup_finished_handler(self):
        """Callback when copy job is finished"""
        self.button_start_copy["state"] = "normal"

    def on_backup_error_handler(self):
        """Callback when the backup job as a whole fails"""
