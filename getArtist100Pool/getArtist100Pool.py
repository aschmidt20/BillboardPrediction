# grab some libraries
import sys
import billboard
from datetime import datetime
import datetime as dt
from datetime import date
import csv

# turn start/end date arguments into datetime objects
startDate = datetime.strptime(sys.argv[1], '%Y-%m-%d')
endDate = datetime.strptime(sys.argv[2], '%Y-%m-%d')
#startDate = datetime.strptime('2017-08-01', '%Y-%m-%d')
#endDate = datetime.strptime('2018-11-10', '%Y-%m-%d')

# change the provided end date to the Saturday of the same week, since the Hot 100 comes out on Saturday
weekdayIdx = (endDate.weekday() + 1) % 7
adjustedEndDate = endDate - dt.timedelta(weekdayIdx - 6) # end date is adjusted to Saturday of the week passed in
chart = billboard.ChartData('artist-100', adjustedEndDate.strftime('%Y-%m-%d')) # get first chart

# print each weekly chart in the given time range
artists=[]
while chart.previousDate and datetime.strptime(chart.previousDate, '%Y-%m-%d') >= startDate:
   # write data rows to list
   for index, item in enumerate(chart.entries):
      artistStr = str(item.artist).replace(",","_")
      if (artistStr not in artists and artistStr != ''):
          artists.append(artistStr)
          print("Adding " + artistStr + "...")
         
   # get next chart
   chart = billboard.ChartData('artist-100', chart.previousDate)

with open('Artist100Output\Artist 100 Pool ' + startDate.strftime('%Y-%m-%d') + ' - ' + endDate.strftime('%Y-%m-%d') + '.csv', 'w', newline='') as csvfile:
    # create csv writer
    csvWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)

    # write headers
    print("Writing to CSV...")
    for artist in artists:
        csvWriter.writerow([artist])
    print("Done.")



