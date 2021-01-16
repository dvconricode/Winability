
import os
import sys

# the following function creates new .csv file on user desktop, Windows OS and MacOS

def create_folders_by_system():
    if sys.platform.startswith('win32'):
        create_new_desktop_folder_windows()

    elif sys.platform.startswith('darwin'):
        create_new_desktop_folder_mac()


# the following if creates new folder on user desktop for windows OS

def create_new_desktop_folder_windows():
    if sys.platform.startswith('win32'):
        desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        new_path = desktop_path + r'\StockData'
        if not os.path.exists(new_path):
            os.makedirs(new_path)

def create_new_desktop_folder_mac():
    home = os.path.expanduser("~")
    print(home)
    if os.path.exists(home + '/Desktop/StockData'):
        print("File already exists")
    else:
        os.makedirs(home + '/Desktop/StockData')
        print("Created")