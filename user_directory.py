
import os
import sys

if sys.platform.startswith('win32'):
    username = os.getlogin()
    file = open(f'C:\\Users\\{username}\\Desktop\\stock_tickers.csv', 'x')
    file.close()

elif sys.platform.startswith('darwin'):
    file = open(os.path.expanduser('~/Desktop/stock_tickers.csv'), 'x')
    file.close()
