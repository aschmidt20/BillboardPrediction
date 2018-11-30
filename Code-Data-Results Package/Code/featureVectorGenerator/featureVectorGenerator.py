import sys
import csv
import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join
from datetime import datetime
from datetime import timedelta
from datetime import date

# Load data files
allArtists = pd.read_csv('artists.csv', delimiter=',', header=None)

#followersData = pd.read_csv(sys.argv[1], delimiter=',', header=0)
followersData = pd.read_csv('followers.csv', delimiter=',', header=0)

#mentionsData = pd.read_csv(sys.argv[2], delimiter=',', header=0)
mentionsData = pd.read_csv('mentions.csv', delimiter=',', header=0)

chartFiles = [f for f in listdir('Charts') if isfile(join('Charts/', f))]
charts = pd.DataFrame()
for chart in chartFiles:
    newChart = pd.read_csv('Charts/' + chart, delimiter=',', header=0)
    charts = charts.append(newChart)
charts['ChartDate'] = pd.to_datetime(charts['ChartDate'])

featureVectors = []

# For each artist - TODO: get names from artist pool
for artist in allArtists[0].unique():
    # Get all NBS data for artist and do some data type conversion
    allMentions = mentionsData.loc[mentionsData['Name'] == artist]
    allMentions['MetricDate'] = pd.to_datetime(allMentions['MetricDate'])
    allMentions['Mentions'] = pd.to_numeric(allMentions['Mentions'])
    
    allFollowers = followersData.loc[followersData['Name'] == artist]
    allFollowers['MetricDate'] = pd.to_datetime(allFollowers['MetricDate'])
    allFollowers['Followers'] = pd.to_numeric(allFollowers['Followers'])
        
    lastPosition = 0
    # For each chart   
    for chartDate in charts['ChartDate'].unique():
        # Get chart for the date
        chart = charts.loc[charts['ChartDate'] == chartDate]
        
        # Get chart date and tracking period of chart
        trackingStart = chartDate + np.timedelta64(-15,'D')
        trackingEnd = chartDate + np.timedelta64(-9,'D')

        # Extract overall features from mentions and followers from NBS data before/during tracking period
        mentions = allMentions.loc[allMentions['MetricDate'] <= trackingEnd]
        followers = allFollowers.loc[allFollowers['MetricDate'] <= trackingEnd]       
        
        if len(mentions['MetricDate']) > 0:
            overallAvgMentions = float(sum(mentions['Mentions']))/len(mentions['Mentions'])
        else:
            overallAvgMentions = 0
            
        if len(followers['MetricDate']) > 0:
            overallAvgFollowers = float(sum(followers['Followers']))/len(followers['Followers'])
            
            minFollowers = min(followers['Followers'])
            maxFollowers = max(followers['Followers'])
            followersGained = maxFollowers - minFollowers
            dayCount = len(followers['MetricDate'].unique())
            
            overallMaxFollowers = maxFollowers          
            overallAvgFollowersGained = float(followersGained)/dayCount
        else:
            overallAvgFollowers = 0
            overallMaxFollowers = 0       
            overallAvgFollowersGained = 0

        # Get tracking week of mentions and extract features - NBS could be missing some days so don't count on it being 7 days
        trackedMentions = mentions.loc[(mentions['MetricDate'] >= trackingStart) & (mentions['MetricDate'] <= trackingEnd)]
        if len(trackedMentions['MetricDate']) > 0:
            weekAvgMentions = float(sum(trackedMentions['Mentions']))/len(trackedMentions['MetricDate'])
        else:
            weekAvgMentions = 0
        
        # Get tracking week of followers and extract features - NBS could be missing some days so don't count on it being 7 days
        trackedFollowers = followers.loc[(followers['MetricDate'] >= trackingStart) & (followers['MetricDate'] <= trackingEnd)]
        if len(trackedFollowers['MetricDate']) > 0:
            weekMinFollowers = min(trackedFollowers['Followers'])
            weekMaxFollowers = max(trackedFollowers['Followers'])
            weekFollowersGained = weekMaxFollowers - weekMinFollowers
            
            weekAvgFollowersGained = float(weekFollowersGained)/len(trackedFollowers['MetricDate'])
        else:
            weekAvgFollowersGained = 0

        # Compare overall social media data to this week and generate more features
        avgMentionsChange = weekAvgMentions - overallAvgMentions
        if (overallAvgMentions != 0):
            avgMentionsRate = float(weekAvgMentions)/overallAvgMentions       
        else:
            avgMentionsRate = 0
        
        avgFollowersGainedChange = weekAvgFollowersGained - overallAvgFollowersGained
        if (overallAvgFollowersGained != 0):
            avgFollowersGainedRate = float(weekAvgFollowersGained)/overallAvgFollowersGained
        else:
            avgFollowersGainedRate = 0
                
        # Get features from chart data
        artistEntry = chart.loc[chart['Artist'] == artist]
        
        # If artist charted, get latest chart info
        if len(artistEntry) == 1:
            position = int(artistEntry['CurrentPosition'].iloc[0])
            # If this is the first chart we're looking at
            if lastPosition == 0: 
                # Only trust the chart's last position if we're on the first chart; it can often be wrong for the #1 spot
                lastPosition = int(artistEntry['LastPosition'].iloc[0])
            positionChange = lastPosition - position
            weeksOnChart = int(artistEntry['WeeksOnChart'].iloc[0]) - 1 # Weeks on chart BEFORE this chart (that way we aren't "cheating" if using vectors for test data)
        
        # If artist didn't chart, see if they've charted before in our data
        else:
            position = 101 # Assign 101 as "off chart" position
            if lastPosition == 0: 
                # If this is our first chart, assume they didn't chart previous week either
                lastPosition = 101
            positionChange = lastPosition - 101

            pastCharts = charts.loc[(charts['Artist'] == artist) & (charts['ChartDate'] < chartDate)].sort_values('ChartDate', ascending=False)
            futureCharts = charts.loc[(charts['Artist'] == artist) & (charts['ChartDate'] > chartDate)].sort_values('ChartDate')
            
            # If past chart entries found, get weeks on chart from most recent one
            if len(pastCharts) > 0:
                weeksOnChart = int(pastCharts['WeeksOnChart'].iloc[0])
            else:
                # If future chart entries found, get weeks on chart from soonest one (this is not "cheating" since we subtract 1, and we should have access to this number anyway)
                if len(futureCharts) > 0:
                    weeksOnChart = int(futureCharts['WeeksOnChart'].iloc[0]) - 1
            
                # If not, zero for weeks on chart (this case shouldn't happen for anyone important because all of our artists charted in the past year)
                else:
                    weeksOnChart = 0
        
        # Add feature vector and set last position to whatever chart position got chosen here
        featureVectors.append([chartDate, artist, position, lastPosition, positionChange, weeksOnChart, overallAvgMentions, weekAvgMentions, avgMentionsChange, avgMentionsRate, overallAvgFollowers, overallMaxFollowers, overallAvgFollowersGained, weekAvgFollowersGained, avgFollowersGainedChange, avgFollowersGainedRate])
        lastPosition = position
        
    print("Feature vectors for " + artist + " generated.")
        
with open('output/feature vectors.csv', 'w+', newline='') as outputFile:
    outputWriter = csv.writer(outputFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    outputWriter.writerow(["ChartDate","ArtistName","Position","LastPosition","PositionChange","WeeksOnChart","DailyMentions", "TrackingWeekDailyMentions", "DailyMentionsDiff", "DailyMentionsMult", "AvgFollowers", "MaxFollowers", "DailyFollowers", "TrackingWeekDailyFollowers", "DailyFollowersDiff", "DailyFollowersMult"])
    outputWriter.writerows(featureVectors)
    
# TODO: Add sentiment score feature when we have it
