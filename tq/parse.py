import csv
import collections

# Create a dictionary where the keys are the genres and 
# the values correspond to the number of times these genres occur
features = collections.Counter()
# Create a dictionary where the keys are the name of the movie
# and values is the list of features
movieSet = {}
totalMovies = 0 
errorBoundary = 0.1

with open('movies.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    reader.next()
    for row in reader:
        genres = row[2]
        movieSet[row[1]] = genres.split("|")

totalMovies = len(movieSet)

# Set up boundary of when to capture feature
halfBoundary = totalMovies / 2
lowerBoundary = halfBoundary - (totalMovies * errorBoundary)
higherBoundary = halfBoundary + (totalMovies * errorBoundary)
selectedFeature = "none"

# Figure out how many times a feature occurs
for movie, genres in movieSet.items():
    for genre in genres:
        features[genre] += 1

# Algorithm to determine optimal feature
for feature, amount in features.items():
    if( (amount > lowerBoundary) & (amount < higherBoundary) ) :
        selectedFeature = feature 
        break

print "Is the movie " + selectedFeature + "?"

