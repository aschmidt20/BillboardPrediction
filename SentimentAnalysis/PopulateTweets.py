import pandas as pd
import twitter
import mysql.connector
import time

ts = time.time()

mydb = mysql.connector.connect(
    host="160.153.71.229",
    user="schmi651",
    password="######",
    database='nsinvestmentledger'
)


add_tweet = ("INSERT INTO Tweets "
               "(artistName, timestamp, content) "
               "VALUES (%s, %s, %s)")

cursor = mydb.cursor()

api = twitter.Api(consumer_key='Vf2Gyh18iHFBURb21bbzpw432',
                      consumer_secret='FmIwnAp6yVrpimTDvWs3mrTzO4n6YpkKMyiXuOsVMm9bjptxVT',
                      access_token_key='2600508180-4UoJ9ssATc73oOCuV1fMkNOlQR3Y9Io0qZzbjqA',
                      access_token_secret='yDoyTgmTu1KbLukEAEgehwKe67s7wHmpDsEYezpTUqASu', sleep_on_rate_limit=True)

#Take in list of top 100 artists twitter handles from last week, get tweets and add to database
artist_list = ['QueenWillRock', 'kanebrown', 'Imaginedragons', 'ArianaGrande', 'Drake', 'PostMalone', 'ladygaga', 'xxxtentacion', 'BTS_twt', 'thebeatles', 'halsey', 'iamcardib', 'JuiceWorlddd', 'Lilpeep', 'trvisXX', 'trippieredd', 'PanicAtTheDisco', 'thegreatkhalid', 'lukecombs', 'BradleyC_Fan', 'Lauren_Daigle', 'edsheeran', 'muse', 'ellamai', 'DanAndShay', 'LilTunechi', 'weareoneEXO', 'Eminem', 'maroon5', 'lilbaby4PF', 'ChrisStapleton', '5SOS', 'ShawnMendes', 'marshmellomusic', 'BrunoMars', 'billieeilish', 'jonbellion', 'Camila_Cabello', 'MetroBoomin', 'taylorswift13', 'KodakBlack1k', 'twentyonepilots', 'PTXofficial', 'CovingtonQ', 'ImBadBunny', 'ThomasRhett', 'BebeRexha', 'bastilledan', 'Jason_Aldean', 'nfrealmusic', 'BrettYoungMusic', 'FLAGALine', 'MariahCarey', 'kendricklamar', 'bazzi', 'lovelytheband', 'DUALIPA', 'djsnake', '1GunnaGunna', '6ix9ine', 'JimmieAllen', 'selenagomez', 'TheChainsmokers', 'Pink', 'goSwaeLee', 'scrowder', 'NICKIMINAJ', 'Tyga', 'SarahBrightman', 'lauvsongs', 'carrieunderwood', 'AndreaBocelli', 'MarenMorris', 'ThePianoGuys', 'Disturbed', 'backstreetboys', 'Metallica', 'ElvisPresley', 'LukeBryanOnline', 'm10penny', 'zacbrownband', 'joshgroban', 'DierksBentley', 'blakeshelton', 'ericchurch', 'johnlegend', 'Zedd', 'Normani', 'FlippDinero', 'Migos', 'theweeknd', 'OffsetYRN', 'KeithUrban', 'JBALVIN', 'kelly_clarkson', 'BarbraStreisand', 'gucci1017', 'rihanna', 'daddy_yankee', 'OldDominion']


for artist in artist_list:

    query = '@' + artist
    #tweets = api.GetSearch(raw_query=query)
    tweets = api.GetSearch(term=query, since='2018-11-10')
    tweet_list = []
    print(artist)
    for tweet in tweets:
        content = tweet.text
        tweet_insert = (artist, ts, content)
        tweet_list.append(tweet_insert)

    cursor.executemany(add_tweet, tweet_list)


# Make sure data is committed to the database
mydb.commit()

cursor.close()
mydb.close()

