import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.linear_model import Perceptron
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn import tree
from sklearn import ensemble
from sklearn.model_selection import train_test_split
from itertools import combinations
from sklearn.metrics import mean_squared_error
import math
import numpy as np
import csv
from os import listdir
from os.path import isfile, join
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import random

####################################################################################################################
# 1) DATA LOADING
#Load feature vector data into dataframe
path = 'Feature Vectors - in.csv' # In-domain experiment
#path = 'Feature Vectors - out.csv' # Out-of-domain experiment
feature_vectors = pd.read_csv(path)

dataByArtist = {}
previous_artist = ""

#Create dictionary of data for each individual artist
for index, row in feature_vectors.iterrows():
    #trend = -(row['LastPosition'] - previous)
    artist = row['ArtistName']
    try:
        if row['Position'] == 101:
            weeksonchart = 0
        else:
            weeksonchart = row['WeeksOnChart']
        if row['DailyMentionsMult'] > 1:
            row['DailyMentionsMult'] = 1
        if row['DailyFollowersMult'] > 1:
            row['DailtFollowersMult'] = 1
        dataByArtist[artist].append([row['ChartDate'],row['LastPosition'],weeksonchart,row['DailyMentionsMult'],row['DailyFollowersMult'],row['Position'], row['PositionTrend']])
    except KeyError:
        if row['Position'] == 101:
            weeksonchart = 0
        else:
            weeksonchart = row['WeeksOnChart']
        if row['DailyMentionsMult'] > 1:
            row['DailyMentionsMult'] = 1
        if row['DailyFollowersMult'] > 1:
            row['DailtFollowersMult'] = 1
        dataByArtist[artist] = []
        dataByArtist[artist].append([row['ChartDate'],row['LastPosition'],weeksonchart,row['DailyMentionsMult'],row['DailyFollowersMult'],row['Position'], row['PositionTrend']])
    #previous = row['Position']

#Takes 2 artists and dictionary of features for all artists and return X and Y lists to train and test classifiers on
def getData(artist1, artist2, dataByArtist):
    X = []
    Y = []
    iter = 0
    artist1_data = dataByArtist[artist1]
    artist2_data = dataByArtist[artist2]
    while iter < len(artist1_data) - 1: # Leave out most recent week for testing
        # print(artist1_data[iter])
        # Check whether chart position of artist 1 is greater than artist 2
        position1 = int(artist1_data[iter][5])
        position2 = int(artist2_data[iter][5])
        #print(artist1 + ': ' + str(position1) + "  " + artist2 + ": " + str(position2))    
        
        X_list = [artist1_data[iter][1], artist1_data[iter][2], artist1_data[iter][3], artist1_data[iter][4], artist1_data[iter][6],
                  artist2_data[iter][1], artist2_data[iter][2],
                  artist2_data[iter][3], artist2_data[iter][4], artist2_data[iter][6]]
        X.append(X_list)
        if position1 < position2:
            # print(artist1 + " higher than " + artist2)
            Y.append(-1)
        elif position1 > position2:
            # print(artist2 + " higher than " + artist1)
            Y.append(1)
        else:
            # print(artist1 + " and " + artist 2 + " did not chart")
            Y.append(0)            
        iter += 1

    return X, Y

#Takes 2 artists and dictionary of features for all artists and return X and Y lists to train and test classifiers on for only most recent week of data
def getMostRecentData(artist1, artist2, dataByArtist):
    X = []
    Y = []
    artist_pair = (artist1, artist2)
    artist1_data = dataByArtist[artist1]
    artist2_data = dataByArtist[artist2]
    iter = len(artist1_data)-1
    while iter < len(artist1_data):
        # print(artist1_data[iter])
        # Check whether chart position of artist 1 is greater than artist 2
        position1 = int(artist1_data[iter][5])
        position2 = int(artist2_data[iter][5])
        # print(artist1 + ': ' + str(position1) + "  " + artist2 + ": " + str(position2))
        
        X_list = [artist1_data[iter][1], artist1_data[iter][2], artist1_data[iter][3], artist1_data[iter][4], artist1_data[iter][6],
                  artist2_data[iter][1], artist2_data[iter][2],
                  artist2_data[iter][3], artist2_data[iter][4], artist2_data[iter][6]]
        X.append(X_list)
        if position1 < position2:
            # print(artist1 + " higher than " + artist2)
            Y.append(-1)
        elif position1 > position2:
            # print(artist2 + " higher than " + artist1)
            Y.append(1)
        else:
            # print(artist1 + " and " + artist 2 + " did not chart")
            Y.append(0)
        iter += 1

    return X, Y, artist_pair

####################################################################################################################
# 2) TRAIN/TEST CLASSIFIER
artistList = [artist for artist in dataByArtist]
random.shuffle(artistList) # Shuffle artists since they'll be in order of latest chart

# Generate all possible combinations of artist comparisons
combinations = list(combinations(artistList, 2))

X = []
Y = []
# Generate training set (includes all chart weeks from the feature vectors except the last one)
for entry in combinations:
    artist1 = entry[0]
    artist2 = entry[1]
    individualX, individualY = getData(artist1, artist2, dataByArtist)
    if len(individualX) > 0:
        iter = 0
        while iter < len(individualX):
            X.append(individualX[iter])
            Y.append(individualY[iter])
            iter += 1

X_test = []
Y_test = []
artist_pairs = []
ranking = []
# Generate test set (includes only last week of feature vectors)
for entry in combinations:
    artist1 = entry[0]
    artist2 = entry[1]
    individualX, individualY, artists = getMostRecentData(artist1, artist2, dataByArtist)
    if len(individualX) > 0:
        iter = 0
        while iter < len(individualX):
            X_test.append(individualX[iter])
            Y_test.append(individualY[iter])
            artist_pairs.append(artists)
            iter += 1

# Create, train, and test classifier
# LOGISTIC REGRESSION
#classifier = LogisticRegression(solver='liblinear')
#classifierName = "LogisticRegression"

# DECISION TREE
#classifier = DecisionTreeClassifier(max_depth=7)
#classifierName = "DecisionTree"

# DECISION TREE ENSEMBLE WITH BAGGING
classifier = ensemble.BaggingClassifier(DecisionTreeClassifier(max_depth=4), n_estimators=50)
classifierName = "BaggingDecisionTree"

# DECISION TREE ENSEMBLE WITH ADABOOST
#classifier = ensemble.AdaBoostClassifier(DecisionTreeClassifier(max_depth=4), n_estimators=50)
#classifierName = "AdaBoostDecisionTree"

# NAIVE BAYES
#classifier = GaussianNB()
#classifierName = "NaiveBayes"


classifier.fit(X, Y)
y_pred = classifier.predict(X_test)

# Export logistic regression coefficients/decision tree
#print("LogisticRegression classes/coefficients:")
#print(classifier.classes_)
#print(classifier.coef_)
#tree.export_graphviz(classifier, out_file='DecisionTree.dot')

# Use classifier predictions for testing feature vectors to generate Artist 100

# First, populate list with all unique artists
iter = 0
while iter < len(artist_pairs):
    pair = artist_pairs[iter]
    artist1 = pair[0]
    artist2 = pair[1]
    
    if artist1 not in ranking:
        ranking.append(artist1)
    if artist2 not in ranking:
        ranking.append(artist2)
    
    iter += 1

random.shuffle(ranking) # Shuffle artists randomly

# Second, compare each pair and swap based on predictions - perform swapping until convergence or 100 swaps are done (should only have to do two iterations for convergence)
swaps = 0
convergence = False
prevRanking = None

iter = 0
while convergence == False and swaps < 100:
    while iter < len(artist_pairs):
        pair = artist_pairs[iter]
        artist1 = pair[0]
        artist2 = pair[1]
        
        pred = y_pred[iter]
        pos1 = ranking.index(artist1)
        pos2 = ranking.index(artist2)
        #if artist1 is predicted to be higher on the list then artist2
        if pred == -1:
            #swap artist1 and artist2 on the ranking if the order is not already correct
            if pos1 > pos2:
                ranking[pos2], ranking[pos1] = ranking[pos1], ranking[pos2]
                
        #if artist2 is predicted to be higher on the list than artist1
        elif pred == 1:
            #swap artist1 and artist2 on the ranking if the order is not already correct
            if pos2 > pos1:
                ranking[pos2], ranking[pos1] = ranking[pos1], ranking[pos2]
                  
        #if artists tied, i.e., neither charted, then move both to the end of the ranking
        elif pred == 0:
            ranking.remove(artist1)
            ranking.remove(artist2)
            ranking.append(artist1)
            ranking.append(artist2)
                
        iter += 1
        
    if prevRanking != None:
        sameAsPrev = True
        
        i = 0
        for artist in ranking:
            if (prevRanking[i] != ranking[i]):
                sameAsPrev = False
        
        if sameAsPrev == True:
            convergence = True
            
    prevRanking = ranking.copy()
    swaps += 1

iter = 1
top100list = []
ranking = ranking[:100]
while (iter-1) < 100:
    top100list.append(ranking[iter-1])
    iter += 1


####################################################################################################################
# 3) EVALUATION
# Calculates RMSE based on distances of artist rankings between an actual and predicted chart - pass in arrays of artist names sorted by rank
def chartRMSE(actualChart, predChart):
    actualRanks = []
    predRanks = []
    
    iter = 1
    for artist in actualChart:      
        try:
            predRank = predChart.index(artist) + 1
        except:
            predRank = 101
        
        actualRanks.append(iter)
        predRanks.append(predRank)
        
        iter += 1
        
    iter = 1
    for artist in predChart:
        if artist not in actualChart:
            actualRanks.append(101)
            predRanks.append(iter)
    iter += 1
    
    rmse = math.sqrt(mean_squared_error(actualRanks,predRanks))
    return rmse

# Calculates chart RMSE but only considering artists which are correctly predicted to be on the chart (no big penalties for missing artists or charting uncharted artists)
def chartRMSE_matchesOnly(actualChart, predChart):
    actualRanks = []
    predRanks = []
    
    iter = 1
    for artist in actualChart:      
        try:
            predRank = predChart.index(artist) + 1
        except:
            continue
        
        actualRanks.append(iter)
        predRanks.append(predRank)
              
        iter += 1
            
    rmse = None
    if len(actualRanks) > 0:
        rmse = math.sqrt(mean_squared_error(actualRanks,predRanks))
    return rmse

# Calculates proportion of chart entries shared between predicted and actual chart
def chartOverlap(actualChart, predChart):
    overlap = list(set(actualChart).intersection(set(predChart)))
    prop = float(len(overlap))/len(actualChart)
    return prop

# Evaluation, comparison of charts
feature_vectors['ChartDate'] = pd.to_datetime(feature_vectors['ChartDate'])    

chartDate = max(feature_vectors['ChartDate'])
actualChart = ((feature_vectors.loc[(feature_vectors['ChartDate'] == chartDate)].sort_values('Position'))[['ChartDate','ArtistName','Position']])[:100]

prevChartDate = chartDate + np.timedelta64(-7,'D')
prevChart = ((feature_vectors.loc[(feature_vectors['ChartDate'] == prevChartDate)].sort_values('Position'))[['ChartDate','ArtistName','Position']])[:100]

# Evaluate predicted chart
predRMSE = chartRMSE(actualChart['ArtistName'].tolist(), ranking)
predRMSEMatchesOnly = chartRMSE_matchesOnly(actualChart['ArtistName'].tolist(), ranking)
predOverlap = chartOverlap(actualChart['ArtistName'].tolist(), ranking)

predRMSETop10 = chartRMSE(actualChart['ArtistName'].tolist()[:10], ranking[:10])
predRMSETop10MatchesOnly = chartRMSE_matchesOnly(actualChart['ArtistName'].tolist()[:10], ranking[:10])
predOverlapTop10 = chartOverlap(actualChart['ArtistName'].tolist()[:10], ranking[:10])

# Evaluate previous chart baseline
prevRMSE = chartRMSE(actualChart['ArtistName'].tolist(), prevChart['ArtistName'].tolist())
prevRMSEMatchesOnly = chartRMSE_matchesOnly(actualChart['ArtistName'].tolist(), prevChart['ArtistName'].tolist())
prevOverlap = chartOverlap(actualChart['ArtistName'].tolist(), prevChart['ArtistName'].tolist())

prevRMSETop10 = chartRMSE(actualChart['ArtistName'].tolist()[:10], prevChart['ArtistName'].tolist()[:10])
prevRMSETop10MatchesOnly = chartRMSE_matchesOnly(actualChart['ArtistName'].tolist()[:10], prevChart['ArtistName'].tolist()[:10])
prevOverlapTop10 = chartOverlap(actualChart['ArtistName'].tolist()[:10], prevChart['ArtistName'].tolist()[:10])

print(classifierName + " Results")
print('Chart RMSE: ' + str(predRMSE))
print('Chart RMSE (matches only): ' + str(predRMSEMatchesOnly))
print('Overlap with actual chart: ' + str(predOverlap) + '\n')

print('Top 10 RMSE: ' + str(predRMSETop10))
print('Top 10 RMSE (matches only): ' + str(predRMSETop10MatchesOnly))
print('Overlap with actual top 10: ' + str(predOverlapTop10)  + '\n')

# Score accuracy of each pairwise prediction
iter = 0
correct = 0
total = 0
while iter < len(y_pred):
    if y_pred[iter] == Y_test[iter]:
        correct += 1
    total += 1
    iter += 1
percentage = (correct / total) * 100

print("Pairwise classification accuracy: " + str(percentage) + "%\n")  

print("Baseline Results")
print('Chart RMSE: ' + str(prevRMSE))
print('Chart RMSE (matches only): ' + str(prevRMSEMatchesOnly))
print('Overlap with actual chart: ' + str(prevOverlap)  + '\n')

print('Top 10 RMSE: ' + str(prevRMSETop10))
print('Top 10 RMSE (matches only): ' + str(prevRMSETop10MatchesOnly))
print('Overlap with actual top 10: ' + str(prevOverlapTop10)  + '\n')

with open(classifierName + ' predicted chart.csv', 'w+', newline='') as outputFile:
    outputWriter = csv.writer(outputFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for entry in top100list:
        outputWriter.writerow([entry])




