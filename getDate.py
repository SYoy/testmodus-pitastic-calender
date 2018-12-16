from datetime import datetime

def getDate():
    date = datetime.now()
    month = date.month
    day = date.day
    year = date.year
    string = ['{}-{}-{}'.format(day,month,year)]
    
    return day, month, year, string

def days_between(d1, d2):
    d1 = datetime.strptime(d1[0], "%d-%m-%Y")
    d2 = datetime.strptime(d2[0], "%d-%m-%Y")
    return abs((d2 - d1).days)
