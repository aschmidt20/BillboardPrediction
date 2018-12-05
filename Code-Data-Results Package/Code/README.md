This directory contains 6 subdirectories, each pertaining to one or more Python scripts we wrote for the project:
- getArtist100Pool: Contains a script which collects and writes to a .csv file all artists which appear on the Artist 100 for a specified date range. To generate the Artists.csv file (in Data directory) which defines our domain of artists, we specified the date range 2018-08-25 - 2018-11-10.
- getArtist100: Contains a script which collects and writes to several .csv files all Artist 100 chart data for a specified date range. Our collected chart data includes charts in the date range 2018-08-25 - 2018-11-17.
- getNbsData: Contains a script which collects and writes to two .csv files Twitter mention and follower statistics from Next Big Sound (NBS) for a specified .csv file containing a list of artists and a specified date range. Limited by the time range that NBS keeps their data, we collected data for the date range 2018-08-14 - 2018-11-09 on artists listed in Artists.csv.
- featureVectorGenerator: Given output files from the previous three scripts, generates and writes to a .csv file feature vectors per artist (in Artists.csv) per chart. Performs all necessary preprocessing on chart and NBS data to make it usable by our classifier.
- Ranking Classifier: Contains a script which performs the training, testing, and evaluation for all experiments. Required input files are also included there for easy reproducibility. See line 23 to switch between in-domain and out-of-domain data, and line 160 to change the model being used to perform artist pair classifications.
- SentimentAnalysis: Contains several code and data files related to the sentiment analysis experiment.
	* PopulateTweets.py: Collects tweets about artists in a given list over the past week.
	* positive.txt: list of positive words used to score sentiment of tweets.
	* negative.txt: list of negative words used to score sentiment of tweets.
	* ScoreSentiment.py: Scores sentiment of all tweets given the positive.txt and negative.txt word lists.
	* SentimentClassifierResults.py: Generates and evaluates a predicted chart based on sentiment scores.
	* ClassifyTweets.py: Converts sentiment scores to positive, negative, and neutral class labels based on the sign or zero-value of the scores.

Note: getArtist100Pool.py and getArtist100.py use an API for Billboard charts created by Allen Guo (@guoguo12 on Github).
	  getNbsData.py uses a Python API wrapper for the NBS API created by Buck Heroux (@buckhx on Github).
	  populateTweets.py in the SentimentAnalysis folder uses the Twitter API from Twitter.
	  
Note: ScoreSentiment.py uses positive and negative word lists obtained from ____ to make predictions. These files required no preprocessing, so we did not include them with the rest of our data, rather we only included them here.