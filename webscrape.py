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
def convert( inputName, type ):
    # new str to return
    newName = ""
    # if stock name
    if ( type == "stock" ):
        # for length of stock name
        for i in range( len( inputName ) ):
            # replace any spaces with +'s
            if inputName[i] == ' ':
                newName += '+'
            # else just copy
            else:
                newName += inputName[i]
    # else is article link
    else:
        # copy minus the prefixing '.'
        for i in range( len( inputName ) ):
            if i != 0:
                newName += inputName[i]

    # return newName
    return newName

# searches article for relevancy, if so calculate affect on stock
def searchArticle( articleLink ):
    # create full article link
    newLink = "https://news.google.com"
    newLink += convert( articleLink, "link" )

    # get request
    newReq = requests.get( newLink )
    # get HTML content of page
    soup = BS(newReq.content, 'html.parser')

    #content = soup.find_all( string=name )
    print(soup)
    #rateArticle(soup)

# searches news for articles relevant to stock
def searchStock( stockName ):
    # https headers to convince site you are not a bot
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0',
    })
    # make full link
    reqUrl = "https://finance.yahoo.com/quote/"
    reqUrl += stockName
    if ( stockName != "^GSPC" ):
        reqUrl += "/history/?period1=-9999999999&period2="
    else:
        reqUrl += "/history/?period1=-1325583000&period2="
    reqUrl += str(timeSince())

    # get request
    req = requests.get(reqUrl, headers=headers)
    # get HTML content of page
    soup = BS(req.content, 'html.parser')
    print(reqUrl)
    print(soup)

    # find all instances of <a> tags with class WwrzSb
    #content = soup.find_all('a', class_='WwrzSb')

    # for every instance of <a> w/ class
    #for test in content:
        # search the article
    #    searchArticle(test['href'])

# main function
def main():
    # EST(Not used right now, may be for now if/if not aftermarket)
    EST = datetime.now(pytz.timezone("America/New_York"))

    # get stock name
    name  = input("Enter a stock name: ")

    # searchStock using stock name
    searchStock( name )
