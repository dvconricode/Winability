
import os
import sys

if sys.platform.startswith('win32'):
    username = os.getlogin()
    file = open(f'C:\\Users\\{username}\\Desktop\\stock_tickers.csv', 'x')
    file.close()

elif sys.platform.startswith('darwin'):
    home = os.path.expanduser("~")
    print(home)
    if os.path.exists(home+'/Desktop/StockData'):
        print("exist")
    else:
        print("gotta Create")
        os.makedirs(home+'/Desktop/StockData')
    #file = open(os.path.expanduser('~/Desktop/stock_tickers.csv'), 'x')
    #file.close()
