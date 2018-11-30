import sys
import os
from nbs_api import API
import csv
import json
from datetime import datetime
from datetime import timedelta

# Open artist data file
#artistFile = open(sys.argv[1])
artistFile = open("artists2.csv")
artistReader = csv.reader(artistFile, delimiter=',',)

# Count rows in file, initialize data structure
artistCount = sum(1 for row in artistReader) - 1
summary  = []
followers = []
mentions = []
artistFile.seek(0)

# Get artist names from second column in file
i = 0
api = API("nbsmobile")
for artist in artistReader:
 
    # Get chart date, tracking start and end dates, artist name
    startDate = datetime.strptime('2018-08-14', '%Y-%m-%d') 
    endDate = datetime.strptime('2018-11-09', '%Y-%m-%d') 
    #startDate = datetime.strptime(sys.argv[2], '%Y-%m-%d')    
    #endDate = datetime.strptime(sys.argv[3], '%Y-%m-%d') 
    name = str(artist[0])
        
    # Get artist info
    try:
        artistInfo = json.loads(api.artistSearch(name.replace("_",",")))
        nbsId = list(artistInfo.keys())[0]
    except: # If artist doesn't exist in NBS
        print(datetime.now().strftime("%H:%M:%S") + "> artist " + str(i+1) + " of " + str(artistCount) + " not found on NBS: " + str(artist[0]))       
        i += 1
        continue
        
    # Get all NBS data for artist
    socialMediaData = json.loads(api.metricsArtist(nbsId, opt=[startDate,endDate,None]))
    
    # Get Twitter data
    for platform in list(socialMediaData):
        if platform['Service']['name'] == 'Twitter':              
            # Grab data from API response
            if type(platform['Metric']['fans']) is not list:
                for k in list(platform['Metric']['fans'].keys()):
                    followers.append([name, int(nbsId), datetime(year=1970,month=1,day=1) + timedelta(days=int(k)), platform['Metric']['fans'][k]])

            if type(platform['Metric']['mentions']) is not list:
                for k in list(platform['Metric']['mentions'].keys()):
                    mentions.append([name, int(nbsId), datetime(year=1970,month=1,day=1) + timedelta(days=int(k)), platform['Metric']['mentions'][k]])
       
    print(datetime.now().strftime("%H:%M:%S") + "> saved data for artist " + str(i+1) + " of " + str(artistCount) + ": " + str(artist[0]))
    i += 1
        
# Save detail data in CSVs
if not os.path.exists('detail'):
    os.makedirs('detail')
with open('detail/followers ' + startDate.strftime("%Y-%m-%d") + ' - ' + endDate.strftime("%Y-%m-%d") + '.csv', 'w+', newline='') as followerFile:
    followerWriter = csv.writer(followerFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    followerWriter.writerow(["Name","NbsId","MetricDate","Followers"])
    followerWriter.writerows(followers)
with open('detail/mentions ' + startDate.strftime("%Y-%m-%d") + ' - ' + endDate.strftime("%Y-%m-%d") + '.csv', 'w+', newline='') as mentionFile:
    mentionWriter = csv.writer(mentionFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    mentionWriter.writerow(["Name","NbsId","MetricDate","Mentions"])
    mentionWriter.writerows(mentions)