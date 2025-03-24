import requests
from datetime import datetime
from bs4 import BeautifulSoup as BS
import pytz
from get_CSV import *
from prediction import *
from prediction_OLD import *
from prediction_OLD_Modified import *

# ensures that stock ticker is uppercase
def upperCase( inputStr ):
    # new string
    newStr = ""
    # iterate through string
    for i in range( len( inputStr ) ):
        # set newStr at index to capitalized inputStr at index
        newStr += inputStr[i].capitalize()
    # return newStr
    return newStr

# get stock ticker
def getName():
    # request stock ticker
    name = input("Enter the ticker of the stock you'd like to predict: ")
    # make sure it's caps
    name = upperCase( name )
    # return ticker
    return name

# main func
def main():
    # get ticker name
    newName = getName()
    # get URL to use
    link = makeURL( newName )
    print(link)
    # get csv of historical data
    searchStock( link, newName )
    # open csv
    print("New:")
    predict( newName )
    print("Old:")
    predictOld(newName)
    print("Old(Modified):")
    predictOldMod(newName)

main()
