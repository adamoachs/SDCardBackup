"""This class handles copying files from one dir to another"""

import shutil
import os
from pathlib import Path
from datetime import datetime
import config

class FileHandler:
    """This class handles copying files from one dir to another"""
    def __init__(self, from_dir, to_dir):
        self.from_dir = from_dir
        self.to_dir = to_dir

    def do_copy(self):
        """Start the copy process"""
        files = self.__get_files_to_copy()
        self.__copy_files(files)

    def __get_files_to_copy(self):
        """Returns string array of file paths"""

        root_dir = Path(self.from_dir)
        files = list(root_dir.glob("**/*"))
        return [file for file in files if file.suffix.lower() in config.FILE_TYPE_WHITE_LIST]

    def __copy_files(self, files):
        date = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        path = Path(config.DESTINATION_ROOT_DIRECTORY) / date
        os.makedirs(path, exist_ok = True)

        for file in files:

            shutil.copyfile(file, path / file.name)
        return
