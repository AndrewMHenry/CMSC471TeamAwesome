import csv
import collections

# Create a dictionary where the keys are the name of the movie
# and values is the list of features
movieSet = {}
# Keep track of how many movies exist
totalMovies = 0
# Define an error boundary when selecting feature
errorBoundary = 0.1

# Keep track of questions asked
questionsAsked = 0
totalQuestions = 20

# Store the result if there is one
selectedMovie = "none"

# Parse csv file into movieSet format
with open('movies.csv', 'rb') as f:
    reader = csv.reader(f, delimiter=',')
    reader.next()
    for row in reader:
        genres = row[2]
        movieSet[row[1]] = genres.split("|")

totalMovies = len(movieSet)

# Start asking the questions
for i in range(0,totalQuestions):

    # Set up boundary of when to capture feature
    halfBoundary = totalMovies / 2
    lowerBoundary = halfBoundary
    higherBoundary = halfBoundary
    selectedFeature = "none"
    features = collections.Counter()

    # Figure out how many times a feature occurs
    # by populating a feature as the key
    # and value is number of times feature occurs 
    for movie, genres in movieSet.items():
        for genre in genres:
            features[genre] += 1


    # print(features)

    # Algorithm to determine optimal feature
    while(selectedFeature == "none"):
        lowerBoundary = lowerBoundary - (totalMovies * errorBoundary)
        higherBoundary = higherBoundary + (totalMovies * errorBoundary)
        # print(lowerBoundary)
        # print(higherBoundary)
        for feature, amount in features.items():
            if( (amount > lowerBoundary) & (amount < higherBoundary) ) :
                selectedFeature = feature 
                break

    questionsAsked += 1
    response = input("Is the movie " + selectedFeature + "? ")
   
    for movie, genres in movieSet.items():
        if(selectedFeature in genres):
            # Remove movie from dictionary if
            # the feature is in the movie but the
            # user requests for movies without this feature
            if response == "no":
                movieSet.pop(movie, None)
                totalMovies -= 1;
        else:
            # Remove movie from dictionary if
            # the feature is not in the movie but the
            # user requests for movies with this feature
            if response == "yes":
                movieSet.pop(movie, None)
                totalMovies -= 1;
 
    # If the total number of movies is 1, then
    # that is the only option left
    if(totalMovies == 1):
        break
    # If all the remaining movies have the same
    # features that occur the same amount of times
    # then we can't pick the optimal feature anymore
    elif(len(set(features.values())) == 1):
        break
    # There are no more movies available, game immediately ends
    elif not bool(movieSet) :
        questionsAsked = 20
        break

# This algorithm can be slightly optimized
for j in range(0, totalQuestions - questionsAsked):
    # Just pick the first movie in the set because
    # all these movies contain the same features
    finalResponse = input("Is the name of the movie " + movieSet.keys()[j] + "? ")
    
    if(finalResponse == "yes"):
        selectedMovie = movieSet.keys()[j]; 
        break
    elif(totalMovies == 1):
        break
    elif(finalResponse == "no"):
        totalMovies -= 1

if(selectedMovie == "none"):
    print("Unable to find movie. Sorry")
else:
    print("Found movie: " + selectedMovie)
