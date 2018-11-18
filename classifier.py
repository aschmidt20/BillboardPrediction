import pandas as pd
from matplotlib import pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from itertools import combinations
from sklearn.metrics import mean_squared_error

#Load feautre vector data into dataframe
path = 'featurevectors.csv'
feature_vectors = pd.read_csv(path)

dataByArtist = {}
previous_artist = ""
#Create dictionary of data for each individual artist
for index, row in feature_vectors.iterrows():
    artist = row['ArtistName']
    if row['Position'] < 101:
        onList = True
    else:
        onList = False
    try:
        dataByArtist[artist].append([row['ChartDate'],row['LastPosition'],row['WeeksOnChart'],row['DailyMentions'],row['DailyMentionsDiff'],row['DailyFollowers'],row['DailyFollowersDiff'],row['Position'],onList])
    except KeyError:
        dataByArtist[artist] = []
        dataByArtist[artist].append([row['ChartDate'],row['LastPosition'],row['WeeksOnChart'],row['DailyMentions'],row['DailyMentionsDiff'],row['DailyFollowers'],row['DailyFollowersDiff'],row['Position'],onList])

#Takes 2 artists and dictionary of features for all artists and return X and Y lists to train and test classifiers on
def getData(artist1, artist2, dataByArtist):
    X = []
    Y = []
    iter = 0
    artist1_data = dataByArtist[artist1]
    artist2_data = dataByArtist[artist2]
    while iter < len(artist1_data):
        # print(artist1_data[iter])
        # Check whether chart position of artist 1 is greater than artist 2
        position1 = int(artist1_data[iter][7])
        position2 = int(artist2_data[iter][7])
        #print(artist1 + ': ' + str(position1) + "  " + artist2 + ": " + str(position2))
        if position1 < position2:
            #print(artist1 + " higher than " + artist2)
            X_list = [artist1_data[iter][1], artist1_data[iter][2], artist1_data[iter][3], artist1_data[iter][4],
                      artist1_data[iter][5], artist1_data[iter][6], artist2_data[iter][1], artist2_data[iter][2],
                      artist2_data[iter][3], artist2_data[iter][4], artist2_data[iter][5], artist2_data[iter][6]]
            X.append(X_list)
            Y.append(True)
        elif position1 > position2:
            # print(artist2 + " higher than " + artist1)
            X_list = [artist1_data[iter][1], artist1_data[iter][2], artist1_data[iter][3], artist1_data[iter][4],
                      artist1_data[iter][5], artist1_data[iter][6], artist2_data[iter][1], artist2_data[iter][2],
                      artist2_data[iter][3], artist2_data[iter][4], artist2_data[iter][5], artist2_data[iter][6]]
            X.append(X_list)
            Y.append(False)
        iter += 1

    return X, Y


artistList = [artist for artist in dataByArtist]

# Generate all possible combinations of artist comparisons
combinations = list(combinations(artistList, 2))

X = []
Y = []
#Generate training and test sets of X and Y for classifier training
for entry in combinations:
    artist1 = entry[0]
    artist2 = entry[1]
    individualX, individualY = getData(artist1, artist2, dataByArtist)
    if len(individualX) > 0:
        #print("X " + artist1 + " and " + artist2)
        #print(individualX)
        #print("Y " + artist1 + " and " + artist2)
        #print(individualY)
        iter = 0
        while iter < len(individualX):
            X.append(individualX[iter])
            Y.append(individualY[iter])
            iter += 1

print(len(X))
print(len(Y))

X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.2)

classifier = LogisticRegression()
classifier.fit(X_train, y_train)

y_pred = classifier.predict(X_test)

iter = 0
correct = 0
total = 0
while iter < len(y_pred):
    if y_pred[iter] == y_test[iter]:
        correct += 1
    total += 1
    iter += 1
percentage = (correct / total) * 100
print("Correct: " + str(correct))
print("Total: " + str(total))
print("Percentage Predicted: " + str(percentage) + "%")

