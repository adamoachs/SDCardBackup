"""This class handles copying files from one dir to another"""

import shutil
import os
from pathlib import Path
from datetime import datetime, timedelta
import config

class FileHandler:
    """This class handles copying files from one dir to another"""
    def __init__(self, from_dir, to_dir, hours_filter,
                 on_file_copied, on_file_error,
                 on_backup_finished, on_backup_error):
        self.from_dir = from_dir
        self.to_dir = to_dir
        self.hours_filter = hours_filter
        self.on_file_copied = on_file_copied
        self.on_file_error = on_file_error
        self.on_backup_finished = on_backup_finished
        self.on_backup_error = on_backup_error

    def do_copy(self):
        """Start the copy process"""
        files = self.__get_files_to_copy()
        if len(files) == 0:
            return

        # only filter by date if a filter has been provided
        if self.hours_filter is not None and self.__file_has_date_taken(files[0]):
            files = self.__filter_photos_by_date_taken(files)

        self.__copy_files(files)

    def __get_files_to_copy(self):
        """Returns string array of all file paths"""
        root_dir = Path(self.from_dir)
        files = list(root_dir.glob("**/*"))
        return [file for file in files if file.suffix.lower() in config.FILE_TYPE_WHITE_LIST]

    def __copy_files(self, files):
        date = datetime.now().strftime("%Y-%m-%d %H-%M-%S")
        path = Path(config.DESTINATION_ROOT_DIRECTORY) / date
        os.makedirs(path, exist_ok = True)
        error_count = 0
        try:
            for file in files:
                try:
                    shutil.copy2(file, path / file.name)
                    self.on_file_copied(file, files.index(file) + 1, len(files))
                except Exception as ex:
                    error_count += 1
                    self.on_file_error(file, ex)
        except Exception as ex:
            self.on_backup_error(ex)
        finally:
            file_count = len(files)
            self.on_backup_finished(file_count - error_count, file_count)
        return

    def __get_date_taken(self, file):
        """Get file date"""
        # changed to use the file date instead of EXIF date taken, 
        # to eliminate risk of certain formats not being supported
        # Use modified date instead of created date, because created date is not accessible in Linux
        # (https://stackoverflow.com/a/39501288)
        epoch_time = file.stat().st_mtime
        dt = datetime.fromtimestamp(epoch_time)
        return dt

    def __file_has_date_taken(self, file):
        """Check whether file has date taken exif data"""
        try:
            self.__get_date_taken(file)
            return True
        except Exception:
            return False

    def __get_latest_date_taken(self, files):
        """Get latest date taken from all files' EXIF data"""
        sorted_files = sorted(files, key = lambda file: self.__get_date_taken(file), reverse = True)
        return self.__get_date_taken(sorted_files[0])

    def __filter_photos_by_date_taken(self, files):
        """Filter photots list to photos taken after (latest date - self.hours_filter)"""
        # we filter based on the time most recent photo was taken, rather than datetime.now()
        # this prevents issues when the camera's date isn't set
        filter_date = self.__get_latest_date_taken(files) - timedelta(hours = self.hours_filter)
        return [file for file in files if self.__get_date_taken(file) >= filter_date]
