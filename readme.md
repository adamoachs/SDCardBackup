# SD Card Backup Utility

As the Photography Department Director for a number of conventions, I have on occasion had issues with staff members disappearing after conventions, or their photos being lost or corrupted. As such, a need was identified to have a backup of photos from all staff before leaving con. That way, if something happens to a staff member or their photos, the organization still has a copy to deliver to attendees.

Such a solution had a number of requirements that made any existing product I found on the market not fit my needs. These requirements were:
- Must be stand standalone, not requiring the use of a laptop or phone in any way
- Must be made by a company that still exists
- Must not be crazy expensive. 
No commercial product that fit these needs was found, thus a homebrew solution was developed.

This SD Card Backup Utility was created to fill that purpose. It is intended to run on a Raspberry Pi with a small built in touchscreen screen. By connecting a card reader and external HDD/SSD to the Pi, you just need to plug in the card and run the script

This readme will guide you through setting up and using the SD Card Backup Utility. It assumes a basic knowledge of Raspberry Pi setup, as well as Linux desktop and terminal

# Features

- Standalone backup tool. No laptop or phone required
- Can be powered off any 5v2a USB power source such as power bank or wall adapter
- Excluding external storage and card readers, costs < $100
- Fully open source and free software
- 

# Bill of materials

You will require:

- A Raspberry Pi board of your choice. I used a 3B+ - https://www.amazon.com/dp/B07P4LSDYV
- A Micro SD card to install the OS
- A case with a built-in touch screen. I used the following - https://www.amazon.com/dp/B07N38B86S
- A power/micro USB cable to power the Pi
- An external SSD or HDD with a USB interface
- An SD/CF/Multi card reader with a USB interface 
- A USB keyboard and mouse or your preferred SSH client for setup

# Setup

1. Assemble the case per manufacturer's instructions
2. Install a Pi-compatible Linux distro of your choice
3. Install the touchscreen driver per manufacturer's instruction
4. Open a terminal and run the following commands:

    pip install psutil
    pip install Pillow
    sudo rm -rf SDCardBackup
    git clone https://github.com/adamoachs/SDCardBackup

# Configuration

The `config.py` file contains a few constants, you will need to update these

To begin, plug in your backup destination drive to your Pi, and unplug all other removable drives. Then, open a terminal and enter the following commands:

    python
    import psutil
    print(psutil.disk_partitions())

The terminal will print an array of disk partitions.  
One of these should your external drive. If it is not listed, ensure it is formatted with a compatible file system.  
The remaining drives are system partitions, such as boot.  
  
Using your preferred text editor, open SDCardBackup/config.py and update the config consts as follows:

`DESTINATION_ROOT_DIRECTORY` - The absolute path of the directory you want photos backed up to. This should start with the `mountpoint` property of your external drive, as returned above, with optional subdirectories  
  
`DRIVE_BLACK_LIST` - Enter the `mountpoint` property of ALL the disks returned above. This will exclude them as a backup option  
  
`FILE_TYPE_WHITE_LIST` - If you shoot in a file format not included, add the file extension here  

# Shortcut
  
Create a .desktop shortcut file on the desktop with the following command:

    python /path/to/repo/main.py

# Use

1. After plugging in external drive and card, run the script created in the Shortcut step (or run `python /path/to/repo/main.py` however else you prefer)
2. Choose your card from the "Select one" dropdown
3. Select how many hours worth of photos you want to back up
4. Click Start Copy.
5. The Start Copy button will disable, and the text will change to monitor progress as files are copied over.
6. When the backup job is finished, you will a message telling you how many files were copied, and a message that your card was safely ejected
7. Remove your card and carry on with your door