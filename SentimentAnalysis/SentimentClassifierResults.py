import math
from sklearn.metrics import mean_squared_error

with open('sentiment100.txt') as sentiment:
    sentiment_list = sentiment.readlines()
    sentiment_list = [entry.rstrip('\n') for entry in sentiment_list]

with open('top100.txt') as top100:
    actual_list = top100.readlines()
    actual_list = [entry.rstrip('\n') for entry in actual_list]

with open('prevtop100.txt') as prevtop100:
    prev_list = prevtop100.readlines()
    prev_list = [entry.rstrip('\n') for entry in prev_list]

print(sentiment_list)
print(actual_list)
print(prev_list)

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

    rmse = math.sqrt(mean_squared_error(actualRanks, predRanks))
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
        rmse = math.sqrt(mean_squared_error(actualRanks, predRanks))
    return rmse


# Calculates proportion of chart entries shared between predicted and actual chart
def chartOverlap(actualChart, predChart):
    overlap = list(set(actualChart).intersection(set(predChart)))
    prop = float(len(overlap)) / len(actualChart)
    return prop


# Evaluate predicted chart
predRMSE = chartRMSE(sentiment_list, actual_list)
predRMSEMatchesOnly = chartRMSE_matchesOnly(sentiment_list, actual_list)
predOverlap = chartOverlap(sentiment_list, actual_list)

predRMSETop10 = chartRMSE(sentiment_list[:10], actual_list[:10])
predRMSETop10MatchesOnly = chartRMSE_matchesOnly(sentiment_list[:10], actual_list[:10])
predOverlapTop10 = chartOverlap(sentiment_list[:10], actual_list[:10])

print("Predicted Chart Results")
print('Chart RMSE: ' + str(predRMSE))
print('Chart RMSE (matches only): ' + str(predRMSEMatchesOnly))
print('Overlap with actual chart: ' + str(predOverlap) + '\n')

print('Top 10 RMSE: ' + str(predRMSETop10))
print('Top 10 RMSE (matches only): ' + str(predRMSETop10MatchesOnly))
print('Overlap with actual top 10: ' + str(predOverlapTop10) + '\n')


# Evaluate previous chart baseline
prevRMSE = chartRMSE(actual_list, prev_list)
prevRMSEMatchesOnly = chartRMSE_matchesOnly(actual_list, prev_list)
prevOverlap = chartOverlap(actual_list, prev_list)

prevRMSETop10 = chartRMSE(actual_list[:10], prev_list[:10])
prevRMSETop10MatchesOnly = chartRMSE_matchesOnly(actual_list[:10], prev_list[:10])
prevOverlapTop10 = chartOverlap(actual_list[:10], prev_list[:10])

print("Baseline Results (Uses last weeks chart)")
print('Chart RMSE: ' + str(prevRMSE))
print('Chart RMSE (matches only): ' + str(prevRMSEMatchesOnly))
print('Overlap with actual chart: ' + str(prevOverlap) + '\n')

print('Top 10 RMSE: ' + str(prevRMSETop10))
print('Top 10 RMSE (matches only): ' + str(prevRMSETop10MatchesOnly))
print('Overlap with actual top 10: ' + str(prevOverlapTop10)  + '\n')






