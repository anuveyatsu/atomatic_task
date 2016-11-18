import urllib.request
from html.parser import HTMLParser
import datetime
import csv

monthly_data = []
this_is_date = False
this_is_value = False

def date_handler(data):
    ''' Normalizes dates;
    takes year and puts first day of each month as a date into array'''
    year = data.strip()
    for i in range(1,13):
        date = year + '/' + str(i) + '/1'
        new_date = datetime.datetime.strptime(date, '%Y/%m/%d')
        monthly_data.append(new_date.date())

def price_handler(data):
    ''' Appends monthly prices into monthly_data array '''
    if 'r' in data: #for empty cells data is '\r'
        monthly_data.append(None)
    else:
        monthly_data.append(float(data))

class DataFinder(HTMLParser):
    ''' This is a child class of HTMLParser '''
    def handle_starttag(self, tag, attrs):
        ''' it searches for specific attributes '''
        global this_is_date, this_is_value
        if ('class','B4') in attrs:
            this_is_date = True
        elif ('class', 'B3') in attrs:
            this_is_value = True

    def handle_data(self, data):
        ''' takes dates and monthly_data then passes further '''
        global this_is_date, this_is_value
        if this_is_date:
            date_handler(data)
            this_is_date = False
        elif this_is_value:
            price_handler(data)
            this_is_value = False

# getting page content
f = urllib.request.urlopen('http://www.eia.gov/dnav/ng/hist/rngwhhdM.htm')
f = str(f.read()) # data is encoded but we only need to convert it into string
table = DataFinder()
table.feed(f)
table.close()

# writing data from monthly_data array into csv file
filepath = './data_monthly.csv'
with open(filepath, 'w', newline='') as csvfile:
    data_writer = csv.writer(csvfile)
    data_writer.writerow(['date'] + ['price']) # metadata
    n = len(monthly_data)
    for i in range(0,n,24): # looping over monthly_data
        for j in range(12):
            data_writer.writerow([monthly_data[i+j]] + [monthly_data[i+j+12]])
