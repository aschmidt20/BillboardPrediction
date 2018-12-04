import mysql.connector
from pandas import ExcelWriter
import pandas as pd

mydb = mysql.connector.connect(
    host="160.153.71.229",
    user="schmi651",
    password="######",
    database='nsinvestmentledger'
)

cursor = mydb.cursor()

#Generate lists of positive and negative words
with open('positive.txt') as p:
    positive = p.readlines()
positive = [entry.rstrip('\n') for entry in positive]
p.close()

with open('negative.txt') as n:
    negative = n.readlines()
negative = [entry.rstrip('\n') for entry in negative]
n.close()

#Given a tweet, assign a score based on occurences of positive and negative sentiments
def Score(tweet):
    score = 0
    for word in positive:
        if word in tweet:
            score += 1
    for word in negative:
        if word in tweet:
            score -= 1
    return score


#Use list of artists from most recent week to pull tweets stored in db
#Database indexes tweets by artists twitter username, use this list to store artist twitter handles
artists = ['QueenWillRock', 'kanebrown', 'Imaginedragons', 'ArianaGrande', 'Drake', 'PostMalone', 'ladygaga', 'xxxtentacion', 'BTS_twt', 'thebeatles', 'halsey', 'iamcardib', 'JuiceWorlddd', 'Lilpeep', 'trvisXX', 'trippieredd', 'PanicAtTheDisco', 'thegreatkhalid', 'lukecombs', 'BradleyC_Fan', 'Lauren_Daigle', 'edsheeran', 'muse', 'ellamai', 'DanAndShay', 'LilTunechi', 'weareoneEXO', 'Eminem', 'maroon5', 'lilbaby4PF', 'ChrisStapleton', '5SOS', 'ShawnMendes', 'marshmellomusic', 'BrunoMars', 'billieeilish', 'jonbellion', 'Camila_Cabello', 'MetroBoomin', 'taylorswift13', 'KodakBlack1k', 'twentyonepilots', 'PTXofficial', 'CovingtonQ', 'ImBadBunny', 'ThomasRhett', 'BebeRexha', 'bastilledan', 'Jason_Aldean', 'nfrealmusic', 'BrettYoungMusic', 'FLAGALine', 'MariahCarey', 'kendricklamar', 'bazzi', 'lovelytheband', 'DUALIPA', 'djsnake', '1GunnaGunna', '6ix9ine', 'JimmieAllen', 'selenagomez', 'TheChainsmokers', 'Pink', 'goSwaeLee', 'scrowder', 'NICKIMINAJ', 'Tyga', 'SarahBrightman', 'lauvsongs', 'carrieunderwood', 'AndreaBocelli', 'MarenMorris', 'ThePianoGuys', 'Disturbed', 'backstreetboys', 'Metallica', 'ElvisPresley', 'LukeBryanOnline', 'm10penny', 'zacbrownband', 'joshgroban', 'DierksBentley', 'blakeshelton', 'ericchurch', 'johnlegend', 'Zedd', 'Normani', 'FlippDinero', 'Migos', 'theweeknd', 'OffsetYRN', 'KeithUrban', 'JBALVIN', 'kelly_clarkson', 'BarbraStreisand', 'gucci1017', 'rihanna', 'daddy_yankee', 'OldDominion']
#Stores artist names corresponding to the above twitter usernames
artist_names = ['Queen', 'Kane Brown', 'Imagine Dragons', 'Ariana Grande', 'Drake', 'Post Malone', 'Lady Gaga', 'XXXTENTACION', 'BTS', 'The Beatles', 'Halsey', 'Cardi B', 'Juice WRLD', 'Lil Peep', 'Travis Scott', 'Trippie Redd', 'Panic! At The Disco', 'Khalid', 'Luke Combs', 'Bradley Cooper', 'Lauren Daigle', 'Ed Sheeran', 'Muse', 'Ella Mai', 'Dan + Shay', 'Lil Wayne', 'EXO', 'Eminem', 'Maroon 5', 'Lil Baby', 'Chris Stapleton', '5 Seconds Of Summer', 'Shawn Mendes', 'Marshmello', 'Bruno Mars', 'Billie Eilish', 'Jon Bellion', 'Camila Cabello', 'Metro Boomin', 'Taylor Swift', 'Kodak Black', 'twenty one pilots', 'Pentatonix', 'Sheck Wes', 'Bad Bunny', 'Thomas Rhett', 'Bebe Rexha', 'Bastille', 'Jason Aldean', 'NF', 'Brett Young', 'Florida Georgia Line', 'Mariah Carey', 'Kendrick Lamar', 'Bazzi', 'lovelytheband', 'Dua Lipa', 'DJ Snake', 'Gunna', '6ix9ine', 'Jimmie Allen', 'Selena Gomez', 'The Chainsmokers', 'P!nk', 'Swae Lee', 'Crowder', 'Nicki Minaj', 'Tyga', 'Sarah Brightman', 'Lauv', 'Carrie Underwood', 'Andrea Bocelli', 'Maren Morris', 'The Piano Guys', 'Disturbed', 'Backstreet Boys', 'Metallica', 'Elvis Presley', 'Luke Bryan', 'Mitchell Tenpenny', 'Zac Brown Band', 'Josh Groban', 'Dierks Bentley', 'Blake Shelton', 'Eric Church', 'John Legend', 'Zedd', 'Normani', 'Flipp Dinero', 'Migos', 'The Weeknd', 'Offset', 'Keith Urban', 'J Balvin', 'Kelly Clarkson', 'Barbra Streisand', 'Gucci Mane', 'Rihanna', 'Daddy Yankee', 'Old Dominion']
iter = 0
rows_list = []
while iter < len(artists):
    artist = artists[iter]
    query = "SELECT * FROM Tweets WHERE artistName ='" + artist + "'"
    cursor.execute(query)
    total_score = 0
    num_tweets = 0
    for (artistName, timestamp, content) in cursor:
        score = Score(content)
        total_score += score
        num_tweets += 1
    avg_score = total_score / num_tweets
    print('Score for ' + artist_names[iter] + ': ' + str(avg_score) + '\n')
    entry_dict = {}
    entry_dict['Artist'] =  artist_names[iter]
    entry_dict['Sentiment Score'] = avg_score
    rows_list.append(entry_dict)
    iter += 1

sentiment = pd.DataFrame(rows_list)


writer = ExcelWriter('sentment.xlsx')
sentiment.to_excel(writer,'Sheet1')
writer.save()