import sys
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn import ensemble
from sklearn.metrics import accuracy_score

# Load pre-labeled data from lesley2958 on Github
trainTweets = []
trainLabels = []
with open("pos_tweets.txt", encoding="utf8") as file:
    for i in file: 
        trainTweets.append(i) 
        trainLabels.append('pos')

with open("neg_tweets.txt", encoding="utf8") as file:
    for i in file: 
        trainTweets.append(i)
        trainLabels.append('neg')
    
# Extract word features from tweets    
vectorizer = CountVectorizer(analyzer='word',lowercase=False)
features = vectorizer.fit_transform(trainTweets)
featureArray = features.toarray()

## DEVELOPMENT CODE #################################################################################
## Split data into train/test
#trainData, testData, trainLabel, testLabel = train_test_split(featureArray, tweetLabels, train_size=0.80, test_size=0.20, random_state=0)
#
## Train/test model
#model = LogisticRegression().fit(X=trainData, y=trainLabel)
##model = GaussianNB().fit(X=trainData, y=trainLabel)
##model = DecisionTreeClassifier().fit(X=trainData, y=trainLabel)
##model = SVC(kernel='linear').fit(X=trainData, y=trainLabel)
##model = SVC(kernel='rbf').fit(X=trainData, y=trainLabel)
##model = ensemble.BaggingClassifier(DecisionTreeClassifier(max_depth=20), n_estimators=100).fit(X=trainData, y=trainLabel)
##model = ensemble.AdaBoostClassifier(DecisionTreeClassifier(max_depth=10), n_estimators=100).fit(X=trainData, y=trainLabel)
#
#
#predLabel = model.predict(testData)
#print(accuracy_score(testLabel,predLabel))
#####################################################################################################

# Train model with labeled data
model = LogisticRegression().fit(X=trainTweets, y=trainLabels)

# Classify tweets in file specified by command-line arg
tweets = []
with open(sys.argv[1], encoding="utf8") as file:
    for i in file: 
        tweets.append(i) 

predLabels = model.predict(tweets)
print(accuracy_score(testLabel,predLabel))


