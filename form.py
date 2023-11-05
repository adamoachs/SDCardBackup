"""GUI functionality"""

from tkinter import Tk, Label, OptionMenu, StringVar, Button, messagebox
from threading import Thread
from file_handler import FileHandler
import config

class BackupForm:
    """GUI functionality"""

    def __init__(self, options):

        # main window
        root = Tk()
        root.geometry("400x200")
        root.title("Card Backup")
        root.maxsize(400, 200)
        root.minsize(400, 200)

        # Card select dropdown
        var = StringVar(root)
        var.set("Select Card")
        source = OptionMenu(root, var, *options, command = self.__source_selected)
        source.grid(row = 0, column = 0, rowspan = 2, columnspan = 5,
                    padx = 5, pady = 15, sticky = "we")

        # hours label
        hours_label = Label(root, text = "Backup window in hours")
        hours_label.grid(row = 2, column = 0, rowspan = 2, columnspan = 2,
                         padx = 5, pady = 15 )

        # hours entry
        # tkinter's spinbox class doesn't look to have any option to have buttons on the side
        # so we'll build our own with a label and a few buttons
        hours_minus = Button(root, text = "-", command = self.__hours_minus)
        hours_minus.grid(row = 2, column = 2, padx = 5, pady = 15)
        hours_value = StringVar(root, format(config.HOURS_DEFAULT, ".1f"))
        hours_value_label = Label(root, textvariable = hours_value)
        hours_value_label.grid(row = 2, column = 3, padx = 1, pady = 15)
        hours_plus = Button(root, text = "+", command = self.__hours_plus)
        hours_plus.grid(row = 2, column = 4, padx = 5, pady = 15)

        # Start copy button
        button_start_copy = Button(root, text = "Start copy",
                       command = self.__do_copy, state = "disabled")
        button_start_copy.grid(row = 6, column = 0, rowspan = 2, columnspan = 5,
                               padx = 5, pady = 15, sticky = "we")

        self.root = root
        self.button_start_copy = button_start_copy
        self.source_selection = None
        self.hours_value = hours_value
        self.backup_in_progress = False

    def show(self):
        """Show the form"""
        self.root.mainloop()

    def __do_copy(self):
        """Handler for button click"""
        fh = FileHandler(self.source_selection, config.DESTINATION_ROOT_DIRECTORY, 2,
                         self.on_file_copied_handler, self.on_file_error_handler,
                         self.on_backup_finished_handler, self.on_backup_error_handler)
        thread = Thread(target = fh.do_copy)
        self.button_start_copy["state"] = "disabled"
        self.button_start_copy["text"] = "Copying..."
        self.backup_in_progress = True
        thread.start()

    def on_file_copied_handler(self, file, files_done, files_total):
        """Callback ran per file finished"""
        self.button_start_copy["text"] = f"Copying... {files_done}/{files_total}"

    def on_file_error_handler(self, file, exception):
        """Callback when encountering an error with a single file"""
        messagebox.showerror(title = "Error", message = f"Could not copy {file}: {exception}")

    def on_backup_finished_handler(self, file_successful_count, file_total_colunt):
        """Callback when copy job is finished"""
        self.backup_in_progress = False
        self.__check_button_reset()
        messagebox.showinfo(title = "Finished",
            message = f"Successfully copied {file_successful_count} of {file_total_colunt} photos")

    def on_backup_error_handler(self, exception):
        """Callback when the backup job as a whole fails"""
        messagebox.showerror(title = "Error", message = f"Backup job failed: {exception}")
        self.backup_in_progress = False
        self.__check_button_reset()

    def __source_selected(self, selection):
        """Callback for handling source OptionMenu change"""
        self.source_selection = selection
        self.__check_button_reset()

    def __hours_plus(self):
        self.__hours_update(config.HOURS_INCREMENT)

    def __hours_minus(self):
        self.__hours_update(-config.HOURS_INCREMENT)

    def __hours_update(self, val):
        hours = float(self.hours_value.get())
        hours += val
        hours = max(config.HOURS_MIN, min(hours, config.HOURS_MAX))
        self.hours_value.set(format(hours, ".1f"))

    def __check_button_reset(self):
        if self.source_selection is not None or self.backup_in_progress is False:
            self.button_start_copy["state"] = "normal"
            self.button_start_copy["text"] = "Sart copy"
