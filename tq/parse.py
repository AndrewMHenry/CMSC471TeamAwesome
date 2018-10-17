import csv

# Create a dictionary where the keys are the name of the movie
# and values is the list of features
movieSet = {}
featureSet = {}
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
# by populating a feature as the key
# and a list of movie names as the value
for movie, genres in movieSet.items():
    for genre in genres:
        if featureSet.has_key(genre):
            featureSet[genre].append(movie)
        else:
            featureSet[genre] = [movie]

# Algorithm to determine optimal feature
for feature, movies in featureSet.items():
    amount = len(movies)
    if( (amount > lowerBoundary) & (amount < higherBoundary) ) :
        selectedFeature = feature 
        break

response = input("Is the movie " + selectedFeature + "? ")

if response == "yes":
    tmpFeatureSet = {}
    tmpFeatureSet[selectedFeature] = featureSet[selectedFeature]
    featureSet = tmpFeatureSet
    totalMovies = len(featureSet[selectedFeature])
else:
    featureSet.pop(selectedFeature, None)
    totalMovies = totalMovies - len(featureSet[selectedFeature])
 
