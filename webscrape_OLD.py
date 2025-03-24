import requests
from datetime import datetime
from bs4 import BeautifulSoup as BS
import pytz

def testWeb():
    print("Hello World!")

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
    # make full link
    reqUrl = "https://news.google.com/search?q="
    reqUrl += convert( stockName, "stock" )
    # get request
    req = requests.get(reqUrl)
    # get HTML content of page
    soup = BS(req.content, 'html.parser')

    # find all instances of <a> tags with class WwrzSb
    content = soup.find_all('a', class_='WwrzSb')

    # for every instance of <a> w/ class
    for test in content:
        # search the article
        searchArticle(test['href'])

# main function
def main():
    # EST(Not used right now, may be for now if/if not aftermarket)
    EST = datetime.now(pytz.timezone("America/New_York"))

    # get stock name
    name  = input("Enter a stock name: ")

    # searchStock using stock name
    searchStock( name )

main()
