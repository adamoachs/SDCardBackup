""" Application entry point """

from tkinter import messagebox
import psutil

import config
from form import BackupForm


def get_drives():
    """Get list of mounted drives"""
    drives = psutil.disk_partitions()
    return [drive.mountpoint for drive in drives if drive.mountpoint not in config.DRIVE_BLACK_LIST]

options = get_drives()
if len(options) == 0:
    messagebox.showerror(title = "Error",
                         message = "No card detected. Please reinsert card and try again.")
    exit()

form = BackupForm(options)
form.show()
