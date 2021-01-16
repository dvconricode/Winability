
import os
import sys

# the following function creates new .csv file on user desktop, Windows OS and MacOS

def create_new_csv():

    if sys.platform.startswith('win32'):
        username = os.getlogin()
        file = open(f'C:\\Users\\{username}\\Desktop\\stock_tickers.csv', 'x')
        file.close()

    elif sys.platform.startswith('darwin'):
        home = os.path.expanduser("~")
        print(home)
        if os.path.exists(home + '/Desktop/StockData'):
            return True
        else:
            os.makedirs(home + '/Desktop/StockData')
            return False


# the following if creates new folder on user desktop for windows OS

def create_new_desktop_folder():

    if sys.platform.startswith('win32'):
        desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        new_path = desktop_path + r'\StockData'
        if not os.path.exists(new_path):
            os.makedirs(new_path)

