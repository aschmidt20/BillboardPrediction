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

# change the provided end date to the Saturday of the same week, since the Hot 100 comes out on Saturday
weekdayIdx = (endDate.weekday() + 1) % 7
adjustedEndDate = endDate - dt.timedelta(weekdayIdx - 6) # end date is adjusted to Saturday of the week passed in
chart = billboard.ChartData('artist-100', adjustedEndDate.strftime('%Y-%m-%d')) # get first chart

# print each weekly chart in the given time range
while chart.previousDate and datetime.strptime(chart.previousDate, '%Y-%m-%d') >= startDate:
	with open('Artist100Output\Artist 100 ' + chart.date + '.csv', 'w', newline='') as csvfile:
	
		# create csv writer
		csvWriter = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
		
		# write headers
		csvWriter.writerow(['ChartDate', 'Artist', 'PeakPosition', 'LastPosition', 'WeeksOnChart', 'CurrentPosition'])	
		
		# write data rows
		for index, item in enumerate(chart.entries):
			csvWriter.writerow([chart.date, str(item.artist).replace(",","_"), item.peakPos, item.lastPos, item.weeks, item.rank])
			
		# get next chart
		chart = billboard.ChartData('artist-100', chart.previousDate)

