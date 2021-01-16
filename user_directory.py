
import os
import sys

# the following function creates new files for user desktop, Windows OS or MacOS
def create_folders_by_system():
    if sys.platform.startswith('win32'):
        create_new_desktop_folder_windows()

    elif sys.platform.startswith('darwin'):
        create_new_desktop_folder_mac()

# the following creates new folder and its subfolders on user desktop for windows OS
def create_new_desktop_folder_windows():

    desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    new_path = desktop_path + r'\StockData'
    if not os.path.exists(new_path):
        os.makedirs(new_path)
        print("Created StockData Folder")
    else:
        print("StockData Folder already exists")

    create_subfolders_windows(new_path)


# the following creates 3 subfolders for windows OS
def create_subfolders_windows(path):
    subfolders = [r'\OHLC', r'\Earnings', r'\Merged']

    for f in subfolders:
        if not os.path.exists(path + f):
            os.makedirs(path + f)
        else:
            print(f[1:] + ' already exists')


# the following creates new folder and its subfolders on user desktop for mac OS
def create_new_desktop_folder_mac():
    home = os.path.expanduser("~")
    #print(home)
    path = (home + '/Desktop/StockData')
    if os.path.exists(path):
        print("StockData Folder already exists")

    else:
        os.makedirs(path)
        print("Created StockData Folder")
    create_subfolders_mac(path)

# the following creates 3 subfolders for mac OS
def create_subfolders_mac(path):
    subfolders = ['/OHLC', '/Earnings', '/Merged']

    for f in subfolders:
        if not os.path.exists(path + str(f)):
            os.makedirs(path + str(f))
        else:
            print(f[1:] + ' already exists')



# running the actual command
create_folders_by_system()
