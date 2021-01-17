
import os
import sys
import yfinance as fyf
import pandas as pd
from datetime import date
from pandas_datareader import data as pdr


macslash = '/'
windowslash = r'\\'


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

    return new_path


# the following creates 3 subfolders for windows OS
def create_subfolders_windows(path):
    subfolders = [r'\OHLC', r'\Earnings', r'\Merged']

    for f in subfolders:
        if not os.path.exists(path + f):
            os.makedirs(path + f)
        else:
            print(f[1:] + ' already exists')


# the following creates new folder on user desktop for mac OS
def create_new_desktop_folder_mac():
    home = os.path.expanduser("~")
    path = (home + '/Desktop/StockData')
    if os.path.exists(path):
        print("StockData Folder already exists")

    else:
        os.makedirs(path)
        print("Created StockData Folder")
    create_subfolders_mac(path)

    return path


# the following creates 3 subfolders for Mac OS
def create_subfolders_mac(path):
    subfolders = ['/OHLC', '/Earnings', '/Merged']

    for f in subfolders:
        if not os.path.exists(path + str(f)):
            os.makedirs(path + str(f))
        else:
            print(f[1:] + ' already exists')


# The following gets the directory of subfolders
def subfolder_dir(subfolder):
    if sys.platform.startswith('win32'):
        desktop_path = os.path.join(os.environ['USERPROFILE'], 'Desktop')
        subfolder_path = desktop_path + r'\StockData' + r'\\' + str(subfolder)

    elif sys.platform.startswith('darwin'):
        home = os.path.expanduser("~")
        subfolder_path = (home + '/Desktop/StockData/' + str(subfolder))

    return subfolder_path


Today = date.today()
print(Today)


def grab_OHLC_to_csv(ticker):
    ohlc_dir = subfolder_dir('OHLC')

    if sys.platform.startswith('win32'):
        filename = ohlc_dir + '{}'.format(windowslash) + ticker + '_ohlc.csv'
    elif sys.platform.startswith('darwin'):
        filename = ohlc_dir + '{}'.format(macslash) + ticker + '_ohlc.csv'

    data = pdr.get_data_yahoo(ticker, start='1970-1-1', end=Today)
    data.dropna(inplace=True)
    data.to_csv(filename, index=True)


create_folders_by_system()
grab_OHLC_to_csv('AAPL')
