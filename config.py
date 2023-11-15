"""Settings"""

# Root directory to backup files to
DESTINATION_ROOT_DIRECTORY = "E:\\"

# drives to exclude from importing
DRIVE_BLACK_LIST = ["C:\\", "D:\\", "E:\\"]

# file types to allow
FILE_TYPE_WHITE_LIST = [".jpg", ".jpeg", ".dng", ".nef", ".crw", ".arw",
                        ".pef", ".orf", ".rw2", ".tiff", ".cr2", ".cr3",
                        ".raf"]

# how much to increment/decrement the hours spinbox
HOURS_INCREMENT = 0.5

# defaults amount of hours to back up
HOURS_DEFAULT = 2

# minimum amount of hours to back up
HOURS_MIN = 1

# max amount of hours to back up
HOURS_MAX = 12
