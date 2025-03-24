import datetime
from get_CSV import *

# day class
class Day:
    def __init__(self, location, value, avg):
        self.location = location
        self.value = value
        self.avg = avg

# check for leap year
def isLeap( year ):
    # if perfectly divisble by 4 and not by 100
    if ( year % 4 == 0 and year % 100 != 0 ):
        # is leap year
        return True
    # else if perfectly divisble by 400
    elif ( year % 400 == 0 ):
        # is leap year
        return True
    # neither conditions met
    else:
        # is not leap
        return False

# function to ensure a valid date
def testDate( MM, DD, YYYY ):
    # first, detect if leap year or not:
    leap = isLeap( YYYY )

    # if leap year, feb has 29 days
    if ( leap ):
        # first if one of the 30 day months or feb, check that day is < 31/< 30
        # and > 0:
        if ( MM == 4 or MM == 6 or MM == 9 or MM == 11 ):
            if ( ( MM != 2 and (DD > 0 and DD < 31) ) or ( MM == 2 and
             (DD > 0 and DD < 30)) ):
                # return true
                return True
            # if day > 30 or > 29 for feb, or < 0
            else:
                # return false
                return False
        # else is one of the 31 day months or feb, check that day is < 32/< 30
        # and > 0:
        else:
            if ( ( MM != 2 and (DD > 0 and DD < 32) ) or ( MM == 2 and
             (DD > 0 and DD < 30)) ):
                # return true
                return True
            else:
                # return false
                return False
    # else not a leap year
    else:
        # first if one of the 30 day months or feb, check that day is < 31/< 29
        # and > 0:
        if ( MM == 4 or MM == 6 or MM == 9 or MM == 11 ):
            if ( ( MM != 2 and (DD > 0 and DD < 31) ) or ( MM == 2 and
             (DD > 0 and DD < 29)) ):
                # return true
                return True
            # if day > 30 or > 29 for feb, or < 0
            else:
                # return false
                return False
        # else is one of the 31 day months or feb, check that day is < 32/< 29
        # and > 0:
        else:
            if ( ( MM != 2 and (DD > 0 and DD < 32) ) or ( MM == 2 and
             (DD > 0 and DD < 29)) ):
                # return true
                return True
            # if day > 30 or > 29 for feb, or < 0
            else:
                # return false
                return False

def calcGrowth():
    # find the % growth between each historical data day at closing
    try:
        # open stock close prices
        with open("output.csv", "r") as f_in:
                # create and open file for saving growth between days
            with open("growth.csv", "w") as f_out:
                print("Calculating!")
                # first line has no growth as it's first recorded close
                last = f_in.readline()
                f_out.write("0")
                f_out.write("\n")
                # for every line
                for line in enumerate(f_in):
                    # write growth(new/old - 1) to file
                    f_out.write(str((float(line[1]) / float(last)) - 1))
                    f_out.write("\n")
                    # new old close price
                    last = line[1]
                    # hold on to index w/ current days growth
                    currentDayIndex = line[0] + 1
                return currentDayIndex
    # if file not openable
    except:
        print("Error: Could not calculate growth")

def getCurrentValue():
    try:
        with open("output.csv") as f_in:
            for line in f_in:
                target = line
        return float(target)
    except:
        print("Error: Could not find current stock value")

# find similar days to current day's price
def simDays( daysToDate, ticker ):
    # get the close data for the stock- returns data to output.csv
    closeData( ticker )
    # get the growth between days- returns data to growth.csv
    # returns index of current day
    currentDay = calcGrowth()
    # open growth file to read
    with open("growth.csv") as file:
        # turn data into list for the convenience
        data = file.read()
        data = data.split()
        # save unsorted list
        oldData = data
        # hold on to current value
        target = data[currentDay]
        realPrice = getCurrentValue()
        # sort data list
        data = sorted(data)

        # for items in data
        for i in range(len(data)):
            # if current val found
            if data[i] is target:
                # record sorted list index
                targetIndex = i

        # prime loop
        count = -5
        # create list for days to keep
        dataset = []
        # collect 5 close days < current val, and 5 days > current val
        while count < 6:
            # if not current value itself
            if count != 0:
                print(count)
                # add day index to list
                dataset.append(data[targetIndex + count])
                print(data[targetIndex + count])
            # increment
            count += 1

        # create list for day classes
        days = []
        # for every item in unsorted list
        for int1 in range(len(oldData)):
            # for every item in sorted list
            for int2 in range(len(dataset)):
                # if values the same
                if oldData[int1] is dataset[int2]:
                    # create Day class with location in orig list and it's value
                    days.append(Day(int1, dataset[int2], 0))

        overallAvg = 0
        for i in range(len(days)):
            d = 0
            index = days[i].location
            while d <= daysToDate:
                days[i].avg += float(oldData[index])
                d += 1
                index += 1
            days[i].avg = days[i].avg / daysToDate
            overallAvg += days[i].avg

        overallAvg = overallAvg / 9

        return (realPrice + (realPrice * overallAvg))


# prediction main
def predictOldMod( newName ):
    # initialize variables
    targetMonth = 0
    targetDay = 0
    targetYear = 0

    # current time
    now = datetime.datetime.now()

    # find out how far ahead user wishes to predict
    # while date not entered/not valid:
    while( not testDate( targetMonth, targetDay, targetYear ) ):
        # get MM/DD/YYYY:
        print("Enter a date you would like to predict for")
        targetMonth = int(input("Enter the two digit month: "))
        targetDay = int(input("Enter the two digit day: "))
        targetYear = int(input("Enter the 4 digit year: "))
    # save as a datetime type
    date = datetime.datetime(targetYear, targetMonth, targetDay)
    daysTil = (date - now).days + 1
    print(daysTil)

    if ( now < date ):
        # step 1: find similar days
        predictedValue = simDays( daysTil, newName )
        print(predictedValue)
