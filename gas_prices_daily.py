import urllib.request
from html.parser import HTMLParser
import datetime
import csv

daily_data = []
this_is_date = False
this_is_value = False

def date_handler(data):
    ''' Normalizes dates;
    handles 5 days dates in a week;
    appends these dates into daily_data array '''
    data = data.strip()
    yyyyMmmdd = data[:4] + data[5:8] + data[9:11]
    date = datetime.datetime.strptime(yyyyMmmdd, "%Y%b%d")
    for i in range(5):
        new_date = date + datetime.timedelta(days=i)
        daily_data.append(new_date.date())

def price_handler(data):
    ''' Appends daily prices into daily_data array '''
    if 'r' in data:
        daily_data.append(None)
    else:
        daily_data.append(float(data))

class DataFinder(HTMLParser):
    ''' This is a child class of HTMLParser '''
    def handle_starttag(self, tag, attrs):
        ''' it searches for specific attributes '''
        global this_is_date, this_is_value
        if ('class','B6') in attrs:
            this_is_date = True
        elif ('class', 'B3') in attrs:
            this_is_value = True

    def handle_data(self, data):
        ''' takes dates and daily_data then passes further '''
        global this_is_date, this_is_value
        if this_is_date:
            date_handler(data)
            this_is_date = False
        elif this_is_value:
            price_handler(data)
            this_is_value = False

# getting page content
f = urllib.request.urlopen('http://www.eia.gov/dnav/ng/hist/rngwhhdD.htm')
f = str(f.read()) # data is encoded but we only need to convert it into string
table = DataFinder()
table.feed(f)
table.close()

# writing data from daily_data array into csv file
filepath = './data_daily.csv'
with open(filepath, 'w', newline='') as csvfile:
    data_writer = csv.writer(csvfile)
    data_writer.writerow(['date'] + ['price']) # metadata
    n = len(daily_data)
    for i in range(0,n,10): # looping over daily_data
        for j in range(5):
            data_writer.writerow([daily_data[i+j]] + [daily_data[i+j+5]])
