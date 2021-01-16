
import os
import sys


# the following if creates new folder on user desktop for windows OS

def create_new_desktop_folder_windows():

    if sys.platform.startswith('win32'):
        desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        new_path = desktop_path + r'\StockData'
        if not os.path.exists(new_path):
            os.makedirs(new_path)

