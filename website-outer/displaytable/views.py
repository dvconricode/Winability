import time
starttime = time.time()
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from .forms import TickerForm

# Create your views here. 

########################################################

import os
import sys
import yfinance as fyf
import numpy as np
import pandas as pd
from datetime import date
from pandas_datareader import data as pdr
import requests
import math
import matplotlib.pyplot as plt
from .configinfo import client_id
from scipy.stats import norm

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
# Grab historical data from yahoo finance
def grab_OHLC_to_csv(ticker):
    ohlc_dir = subfolder_dir('OHLC')

    if sys.platform.startswith('win32'):
        filename = ohlc_dir + '{}'.format(windowslash) + ticker + '_ohlc.csv'
    elif sys.platform.startswith('darwin'):
        filename = ohlc_dir + '{}'.format(macslash) + ticker + '_ohlc.csv'

    data = pdr.get_data_yahoo(ticker, start='1970-1-1', end=Today)
    data.dropna(inplace=True)
    data.to_csv(filename, index=True)

# Calculate volatility in the previous created OHLC csv file
def calc_Vol(ticker):
    ohlc_dir = subfolder_dir('OHLC')

    if sys.platform.startswith('win32'):
        filename = ohlc_dir + '{}'.format(windowslash) + ticker + '_ohlc.csv'
    elif sys.platform.startswith('darwin'):
        filename = ohlc_dir + '{}'.format(macslash) + ticker + '_ohlc.csv'

    file = pd.read_csv(filename)
    file['Volatility'] = file['Adj Close'].rolling(window=30, center=False).std()*np.sqrt(252)
    file.to_csv(filename, index=True)                                               # replacing the previous file.

    return file

# Grab Earnings from Macrotrends
def grab_historical_EPS(ticker):
    source = pd.read_html('https://www.macrotrends.net/stocks/charts/' + ticker + '/' + ticker +'/pe-ratio')    # source of the ticker

    # type(source) #check source type 'list'

    earnings_dir = subfolder_dir('Earnings')

    if sys.platform.startswith('win32'):                                                # save location
        filename = earnings_dir + '{}'.format(windowslash) + ticker + '_eps.csv'
    elif sys.platform.startswith('darwin'):
        filename = earnings_dir + '{}'.format(macslash) + ticker + '_eps.csv'

    df = source[0]                                                                      # grabbing the table directly
    df.dropna(inplace=True)                                                             # remove NaN
    df.to_csv(filename, index=False, header=["Date", "Stock_Price", "TTM_Net_EPS", "PE_Ratio"])     # covert dataframe to csv

    # reading the data back in to sort
    data = pd.read_csv(filename)            # reading back the data
    data['Date'] = pd.to_datetime(data['Date'])                     # converting table str to "dates" to be able to sort
    data = data.sort_values(by="Date")                              # sorting
    data.to_csv(filename, index=False)

    return data


# This function reads in OHLC and earnings, loops through columns of OHLC creating a new series with a date index.
# If market data date is less than the eps date then assign EPS
# Creates Merged file
def merge_OHLC_EPS(ticker):
    ohlc_dir = subfolder_dir('OHLC')
    earnings_dir = subfolder_dir('Earnings')
    merged_dir = subfolder_dir('Merged')

    if sys.platform.startswith('win32'):
        filepath1 = ohlc_dir + '{}'.format(windowslash) + ticker + '_ohlc.csv'           # get the 1st file to be edited
        filepath2 = earnings_dir + '{}'.format(windowslash) + ticker + '_eps.csv'           # get 2nd file
        filepath3 = merged_dir + '{}'.format(windowslash) + ticker + '_merged.csv'
    elif sys.platform.startswith('darwin'):
        filepath1 = ohlc_dir + '{}'.format(macslash) + ticker + '_ohlc.csv'
        filepath2 = earnings_dir + '{}'.format(macslash) + ticker + '_eps.csv'
        filepath3 = merged_dir + '{}'.format(macslash) + ticker + '_merged.csv'

    ohlc_data = pd.read_csv(filepath1, index_col=0)  # get the Main File and set indexcolumn to 0
    eps_data = pd.read_csv(filepath2)  # get eps from fps file

    eps = []                # create empty array
    j = 0                   # set beginning step

    for i in ohlc_data.index:           # allow indexing
        while j < len(eps_data) and ohlc_data.loc[i, 'Date'] >= eps_data.loc[j, 'Date']:  # while the date of ohlc is greater than the eps date
            j += 1                      # increment

        if j != 0:                      # checks base case
            j -= 1                      # if passes use the previous

        eps.append(eps_data.loc[j, 'TTM_Net_EPS'])          # appending into empty eps file
        df_eps = pd.DataFrame(eps, columns=["EPS"])         # convert to dataframe to be able to add later

    ohlc_data['EPS'] = df_eps                               # add EPS to the ohlc_data
    ohlc_data.to_csv(filepath3, index=False)                # create a new ohlc_data

    return ohlc_data


# Calculates daily PE ratio in the Merged file
def calc_PE(ticker):
    merged_dir = subfolder_dir('Merged')

    if sys.platform.startswith('win32'):                                                # get the filename
        filename = merged_dir + '{}'.format(windowslash) + ticker + '_merged.csv'
    elif sys.platform.startswith('darwin'):
        filename = merged_dir + '{}'.format(macslash) + ticker + '_merged.csv'

    file = pd.read_csv(filename)                                                        # get the file
    if file['EPS'].dtypes != np.float:
        file['EPS'] = file['EPS'].str.replace('$', '')
    else:
        pass
    file['EPS'] = file.EPS.astype(float)
    file['PE_ratio'] = file['Adj Close']/file['EPS']
    file.to_csv(filename, index=False)                                                 # replacing the previous file.

    return file


# TDAmeritrade API base code to get it to work
def get_quotes(**kwargs):
    
    url = 'https://api.tdameritrade.com/v1/marketdata/quotes'
    
    params = {}
    params.update({'apikey':client_id})
    
    symbol_list = []
    
    for symbol in kwargs.get('symbol'):
        symbol_list.append(symbol)
    params.update({'symbol' : symbol_list})
    
    return requests.get(url,params=params).json()


## Method to get lastprice of stock
def get_lastPrice(**kwargs):
    data = get_quotes(symbol=kwargs.get('symbol'))
    for symbol in kwargs.get('symbol'):
        #print(symbol)
        #print(data[symbol]['lastPrice'])

        return data[symbol]['lastPrice']

# get latest EPS from EPS file
def get_latestEPS(ticker):
    earnings_dir = subfolder_dir('Earnings')

    if sys.platform.startswith('win32'):
        filename = earnings_dir + '{}'.format(windowslash) + ticker + '_eps.csv'
    elif sys.platform.startswith('darwin'):
        filename = earnings_dir + '{}'.format(macslash) + ticker + '_eps.csv'

    data = pd.read_csv(filename)
    latestEPS = data['TTM_Net_EPS'][data.index[-1]] #grabs latest EPS from the already created File
    latestEPS = float(latestEPS.replace('$', ''))
    #print(latestEPS)
    #print(type(latestEPS))

    return latestEPS

# get historic PE mean from the Merged file
def get_historic_PE_mean(ticker):
    merged_dir = subfolder_dir('Merged')

    if sys.platform.startswith('win32'):
        filename = merged_dir + '{}'.format(windowslash) + ticker + '_merged.csv'
    elif sys.platform.startswith('darwin'):
        filename = merged_dir + '{}'.format(macslash) + ticker + '_merged.csv'

    data = pd.read_csv(filename)
    data['PE_ratio'] = data['PE_ratio'].replace([np.inf, -np.inf, np.nan], 0)
    mean = np.mean(data['PE_ratio'])
    print("this is the mean: "+ str(mean))

    return mean

# get historic PE std from the Merged file
def get_historic_PE_std(ticker):
    merged_dir = subfolder_dir('Merged')

    if sys.platform.startswith('win32'):
        filename = merged_dir + '{}'.format(windowslash) + ticker + '_merged.csv'
    elif sys.platform.startswith('darwin'):
        filename = merged_dir + '{}'.format(macslash) + ticker + '_merged.csv'

    data = pd.read_csv(filename)
    data['PE_ratio'] = data['PE_ratio'].replace([np.inf, -np.inf, np.nan], 0)
    std = np.std(data['PE_ratio'])
    print("this is the std: " + str(std))

    return std

# calculates the latest PE by using the get_lastPrice() and get_latestEPS() functions
def get_latest_PE(ticker):
    latest_price = get_lastPrice(symbol=[ticker])
    print("this is the latest price: " + str(latest_price))
    latest_earnings = get_latestEPS(ticker)
    print("this is the latest earning: " + str(latest_earnings))
    latest_PE = latest_price/latest_earnings
    print("this is the latest PE: " + str(latest_PE))

    return latest_PE

# utilizes get_historic_PE_mean(), get_historic_PE_std(), and get_latest_PE() functions to get required (x,mean,std)
# run norm.cdf(x,mean,std) to get the cdf probability
def get_prob_without_graph(ticker):
    historic_PE_mean = get_historic_PE_mean(ticker)
    #print(historic_PE_mean)
    historic_PE_std = get_historic_PE_std(ticker)
    #print(historic_PE_std)
    latest_PE = get_latest_PE(ticker)
    #print(latest_PE)
    probability = norm.cdf(latest_PE, historic_PE_mean, historic_PE_std)
    print("The probability of winning the trade is: " +str(1-probability))

    return 1-probability

def get_prob_with_graph(ticker):
    historic_PE_mean = get_historic_PE_mean(ticker)
    #print(historic_PE_mean)
    historic_PE_std = get_historic_PE_std(ticker)
    #print(historic_PE_std)
    latest_PE = get_latest_PE(ticker)
    #print(latest_PE)
    probability = norm.cdf(latest_PE, historic_PE_mean, historic_PE_std)
    print("The probability of winning the trade is: " +str(1-probability))
    normal_distribution_curve(historic_PE_mean,historic_PE_std,latest_PE)

    return 1-probability

# running the following shows a normal distribution curve with the cdf of x shaded in
def normal_distribution_curve(mean, std, x):

    # Creating the distribution

    start = math.floor(mean - (3 * std))
    stop = math.ceil(mean + (3 * std))
    data = np.arange(start, stop + 1, 0.01)
    pdf = norm.pdf(data, loc=mean, scale=std)               # loc is the mean, scale is the standard deviation

    # Visualizing the distribution

    plt.plot(data, pdf, color='black')
    plt.fill_between(data, pdf, 0, where=(data <= x), color='#f59592')
    plt.fill_between(data, pdf, 0, where=(data > x), color='#97f4a6')
    plt.xlabel('PE ratio')
    plt.ylabel('probability density')
    plt.show()

# Debug purposes grab maximum historic PE
def get_historic_PE_max(ticker):
    merged_dir = subfolder_dir('Merged')

    if sys.platform.startswith('win32'):
        filename = merged_dir + '{}'.format(windowslash) + ticker + '_merged.csv'
    elif sys.platform.startswith('darwin'):
        filename = merged_dir + '{}'.format(macslash) + ticker + '_merged.csv'

    data = pd.read_csv(filename)
    data['PE_ratio'] = data['PE_ratio'].replace([np.inf, -np.inf, np.nan], 0)
    maxPE = np.max(data['PE_ratio'])
    print(maxPE)

    return maxPE

# Debug purposes grab minimum historic PE
def get_historic_PE_min(ticker):
    merged_dir = subfolder_dir('Merged')

    if sys.platform.startswith('win32'):
        filename = merged_dir + '{}'.format(windowslash) + ticker + '_merged.csv'
    elif sys.platform.startswith('darwin'):
        filename = merged_dir + '{}'.format(macslash) + ticker + '_merged.csv'

    data = pd.read_csv(filename)
    data['PE_ratio'] = data['PE_ratio'].replace([np.inf, -np.inf, np.nan], 0)
    minPE = np.min(data['PE_ratio'])
    print(minPE)

    return minPE


# create all the necessary files as well as calculate important columns
def setup_data(ticker):
    grab_OHLC_to_csv(ticker)
    calc_Vol(ticker)
    grab_historical_EPS(ticker)
    merge_OHLC_EPS(ticker)
    calc_PE(ticker)
    get_latestEPS(ticker)


def initial_program_run():
    #START WITH INITIALIZING FOLDERS
    create_folders_by_system()
    #CREATE FOR LOOP TO ITERATE OVER THE TICKERS
    starting_tickers = open('StartingTickers.txt', 'r')
    ticker_list = []
    for line in starting_tickers:
        ticker_list.append(line.strip())
        #setup_data(ticker)
        #get_prob_without_graph(ticker)
    #Save the results either in a list or strings 
    ## things that are relevant 'ticker name','lastprice', 'probability'

    return ticker_list

### Commands to Run
create_folders_by_system()
# setup_data('EGOV')
#get_prob_without_graph('AAPL')
# initial_program_run()
# get_prob_with_graph('EGOV')
########################################################

ticker_list = ["HIMX","CSGS","MEI","VRTU","PRFT","SMCI","SYKE","EGOV","SIMO","SPNS"]  # CAN BE WHATEVER
for ticker2 in ticker_list:
	setup_data(ticker2)

def sortFunc(e):
	return e[2]

def index(request):
	# DEBUG return HttpResponse("Index page <p>{% print(1) %}</p>")
	# DEBUG2 output = " | ".join(x*x for x in [1,2,3])
	# DEBUG2 return HttpResponse(output)

	ticker_data = []
	for just_ticker in ticker_list:
		website_price = get_lastPrice(symbol=[just_ticker])
		prob_win = 100*(get_prob_without_graph(just_ticker))
		prob_lose = 100 - prob_win
		prob_win = str(prob_win)[:6]
		prob_lose = str(prob_lose)[:6]
		ticker_data.append([just_ticker, website_price, prob_win, prob_lose])
	ticker_data.sort(reverse=True, key=sortFunc)  # sort by stock quality
	middleIndex = len(ticker_data)/2
	ticker_data = ticker_data[:int(middleIndex)]
	timetemp = time.asctime(time.localtime())  # updates every refresh
	other_data = [timetemp]

	template = loader.get_template('displaytable/index.html')
	context = {"other_data":other_data, "ticker_data":ticker_data}
	return HttpResponse(template.render(context, request))


# different: search any!
def get_ticker(request):
		if request.method == 'POST':
			form = TickerForm(request.POST)
			if True:
				template = loader.get_template('displaytable/search.html')
				context = {'ticker': request.POST['ticker']} #gotta get the ticker from the form
				my_search = context['ticker']  # the ticker we search for
				print("###### SEARCHING FOR: "+my_search)
				# get ticker info
				setup_data(my_search)
				website_price = get_lastPrice(symbol=[my_search])
				prob_win2 = 100*(get_prob_without_graph(my_search))
				prob_lose2 = 100 - prob_win2 
				prob_win2 = str(prob_win2)[:6]
				prob_lose2 = str(prob_lose2)[:6]
				results_list = [my_search, website_price, prob_win2, prob_lose2]
				context.update({"ticker_data": results_list})
				return HttpResponse(template.render(context, request))
			#print(form.errors)
			#return HttpResponse('test')

endtime = time.time()
totaltime = endtime - starttime
print("##########")
print("###### Total time elapsed: "+str(totaltime)+" seconds")
print("##########")
