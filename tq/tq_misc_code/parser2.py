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


def get_movieSet():
    path = 'movies.csv'
    file = open(path)
    with file:
        reader = csv.reader(file, delimiter=',')
        next(reader)
        for row in reader:
            genres = row[2]
            movieSet[row[1]] = genres.split('|')

    file.close()
    return movieSet


def get_length_movieSet(movieSet):
    return len(movieSet)


# totalMovies = len(movieSet)

# Start asking the questions


def get_questions(totalMovies, errorBoundary, questionsAsked,
                  totalQuestions, selectedMovie):
    for i in range(0, totalQuestions):

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
                if((amount > lowerBoundary) & (amount < higherBoundary)):
                    selectedFeature = feature
                    break

        questionsAsked += 1
        response = raw_input("Is the movie " + selectedFeature + "? ")

        for movie, genres in list(movieSet.items()):
            if(selectedFeature in genres):
                # Remove movie from dictionary if
                # the feature is in the movie but the
                # user requests for movies without this feature
                if response == "no":
                    movieSet.pop(movie, None)
                    totalMovies -= 1
            else:
                # Remove movie from dictionary if
                # the feature is not in the movie but the
                # user requests for movies with this feature
                if response == "yes":
                    movieSet.pop(movie, None)
                    totalMovies -= 1

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
        elif not bool(movieSet):
            questionsAsked = 20
            break

    # This algorithm can be slightly optimized
    for movie in list(movieSet.keys())[:totalQuestions - questionsAsked]:
        # Just pick the first movie in the set because
        # all these movies contain the same features
        finalResponse = raw_input("Is the name of the movie " + movie + "? ")

        if(finalResponse == "yes"):
            selectedMovie = movie
            break
        elif(totalMovies == 1):
            break
        elif(finalResponse == "no"):
            totalMovies -= 1

    if(selectedMovie == "none"):
        return "Unable to find movie. Sorry"
    else:
        return "Found movie: " + selectedMovie
