"""GUI functionality"""

from tkinter import Tk, Label, OptionMenu, StringVar, Button
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
        fh = FileHandler(self.source_selection, config.DESTINATION_ROOT_DIRECTORY)
        fh.do_copy()
