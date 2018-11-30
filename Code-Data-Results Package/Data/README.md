This directory contains 1 subdirectory and 5 other files:
- The Charts directory contains all the chart data used in the experiments. 
	* For the in-domain experiments, charts for 2018-08-25 - 2018-11-03 were used for training, and the chart for 2018-11-10 was used for testing.
	* For the out-of-domain experiments, charts for 2018-08-25 - 2018-11-10 were used for training, and the chart for 2018-11-17 was used for testing.
- Artists.csv is a list of 568 artists who appeared on the Artist 100 between 2017-08-05 and 2018-11-10. It was produced by the getArtist100Pool.py script. This list serves as the domain of artists which our classifier is guaranteed to have seen in training, and has data for.
- Followers.csv is a list of artist-date-Twitter followers triples collected from Next Big Sound through the getNbsData.py script. Each artist's Next Big Sound ID is also included, but this is never used. Data from 2018-08-14 through 2018-11-09 collected.
- Mentions.csv is a list of artist-date-Twitter mentions triples collected from Next Big Sound through the getNbsData.py script. Each artist's Next Big Sound ID is also included, but this is never used. Data from 2018-08-14 through 2018-11-09 collected.
- Feature Vectors - in.csv is a list of feature vectors from the featureVectorGenerator.py script for the chart weeks of 2018-08-25 - 2018-11-10. This file was used for the in-domain experiments.
- Feature Vectors - out.csv is a list of feature vectors from the featureVectorGenerator.py script for the chart weeks of 2018-08-25 - 2018-11-17. This file was used for the out-of-domain experiments, as the Artist 100 chart for 2018-11-17 may list artists which are not included in the domain of artists specified by Artists.csv.

In both feature vector files, there is a feature vector per artist in Artists.csv per Artist 100 chart. Feature vectors each contain the following fields which are extracted or aggregated from other files:
- ChartDate: date of the associated Artist 100 chart
- Position: position on the Artist 100 chart; if not charted, 101
- LastPosition: previous position on the Artist 100 chart, as dictated by the chart data; if not charted, 101
- PositionChange: LastPosition - Position; as such, negative values are associated with increasing chart position, i.e., "falling down" the chart
- WeeksOnChart: Total number of weeks on the Artist 100 chart, as dictated by the chart data
- DailyMentions: Average number of Twitter mentions artist accumulated per day THROUGH the tracking week of the associated chart
- TrackingWeekDailyMentions: Average number of Twitter mentions artist accumulated per day DURING the tracking week of the associated chart
- DailyMentionsDiff: TrackingWeekDailyMentions - DailyMentions
- DailyMentionsMult: TrackingWeekDailyMentions/DailyMentions, or 0 if DailyMentions = 0
- AvgFollowers: Average number of Twitter followers artist has each day THROUGH the tracking week of the associated chart
- MaxFollowers: Maximum number of Twitter followers artist has for a particular day THROUGH the tracking week of the associated chart
- DailyFollowers: Average number of Twitter followers artist gains each day THROUGH the tracking week of the associated chart
- TrackingWeekDailyFollowers: Average number of Twitter followers artist gains each day DURING the tracking week of the associated chart
- DailyFollowersDiff: TrackingWeekDailyFollowers - DailyFollowers
- DailyFollowersMult: TrackingWeekDailyFollowers/DailyFollowers, or 0 if DailyFollowers = 0