import requests
import datetime
from bs4 import BeautifulSoup as BS
import pytz

# function to get time, in seconds from 12/31/1969 17:00:07 to now
# no idea why, but this is how yahoo finance gets its present time
def timeSince():
    dif = datetime.datetime.now() - datetime.datetime(1969, 12, 31, 17, 0, 7)

    dif = int(dif.total_seconds())

    return dif


# cleans up stock name or articles unique link for the full google link
def makeURL( stockName ):
    # make full link
    # add ticker to the standard csv download url
    reqUrl = "https://query1.finance.yahoo.com/v7/finance/download/"
    reqUrl += stockName
    # if not S&P, do standard oldest possible date
    if ( stockName != "^GSPC" ):
        reqUrl += "?period1=-9999999999&period2="
    # S&P is weird, you have to make the earliest date(period1) a specific date
    # (about late 1927 or so)
    else:
        reqUrl += "?period1=-1325583000&period2="
    # concat with time since 12/31/69 17:00:07
    reqUrl += str(timeSince())
    # concat with rest of url
    reqUrl += "&interval=1d&events=history&includeAdjustedClose=true"

    return reqUrl

# searches news for articles relevant to stock
def searchStock( fullURL, stockName ):
    # https headers to convince site you are not a bot
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
    })

    # get csv from url:
    req = requests.get(fullURL, headers=headers)
    # set file name to TICKER_HistoricalData.csv
    # will overwrite old data files
    fileName = stockName
    fileName += "_HistoricalData.csv"
    # save file
    with open(fileName, "wb") as f_out:
        # print downloading file
        print("Downloading " + fileName)
        # write page content to file
        f_out.write(req.content)

# convert csv to only close data
def closeData( ticker ):
    fileName = ticker
    fileName += "_HistoricalData.csv"
    # try to open
    try:
        with open( fileName ) as file:
            # open output file to put exclusively the stock close data in
            with open("output.csv", "w") as f_out:
                print( "File found!" )
                # skip first line of csv
                file.readline()
                # for every line
                for line in file:
                    # turn comma-delimited str into a list
                    listVals = line.split(',')
                    # write 4th object(close data for market day) into file
                    f_out.write(str(float(listVals[4])))
                    # add new line
                    f_out.write('\n')
    # if not found, return an error
    except:
        print( "File not found." )

# main function
def main():
    # EST(Not used right now, may be for now if/if not aftermarket)
    EST = datetime.now(pytz.timezone("America/New_York"))

    # get stock name
    name  = input("Enter a stock name: ")

    # searchStock using stock name
    searchStock( name )
