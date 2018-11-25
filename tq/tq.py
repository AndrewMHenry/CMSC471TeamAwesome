from __future__ import print_function
from sklearn.cluster import KMeans
import collections
import csv
import itertools
import numpy as np
import os
import pdb
import random
import re

from sklearn.cluster import KMeans

"""Parameter definitions"""

NUM_QUESTIONS = 20
NUM_DISCRETE_QUESTIONS = 15 

RELATIVE_ERROR = 0.1
MIN_COUNT_SCALE = 0.5 - RELATIVE_ERROR
HALF_COUNT_SCALE = 0.5
MAX_COUNT_SCALE = 0.5 + RELATIVE_ERROR

DUMMY_QUESTIONS = [
    'Do you know the muffin man?',
    'Do you want to be my Battle Buddy?',
    'Are you SURE the object is a movie?',
    'Did you bring the merchandise?'
]

MOVIE_CSV = os.path.join(os.path.dirname(__file__), 'movies.csv')
IMDB_MOVIE_CSV = os.path.join(os.path.dirname(__file__), 'imdbmovie.csv')

"""Generic helpers"""


def ask_question(question, expression):
    """Interactively ask question to user, returning boolean answer."""
    return input(question + ' ').upper().startswith('Y')


"""Discrete phase helpers"""


def generate_discrete_pair(things, discrete_features):
    """Create a feature-value pair to ask about.

    TODO: Currently, we keep track of the most recent
    feature-value pair and return it at the end if
    nothing falls in the target range.  In the future,
    we should add logic to keep track of the BEST
    feature-value pair and return that.

    NOTE: We assume that things is nonempty and well-formed,
    in the sense that the "value" (feature dict) for
    each thing it contains has an entry for each of the
    discrete_features.  Under these assumptions, we must
    process at least one pair, so we will have something
    to return.

    """
    min_count = len(things) * MIN_COUNT_SCALE
    half_count = len(things) * HALF_COUNT_SCALE
    max_count = len(things) * MAX_COUNT_SCALE

    best_count = 0
    best_pair = None

    for feature in discrete_features:

        counts = collections.Counter(itertools.chain.from_iterable([
            fdict[feature] for fdict in things.values()]))

        if len(counts) == 0:
            raise RuntimeError('counts is empty!')

        for value, count in counts.items():
            pair = (feature, value)

            diff = abs(count - half_count)
            best_diff = abs(best_count - half_count)

            # return current value if count in range
            if min_count < count < max_count:
                return pair

            # set new best value if new smallest difference
            elif best_pair is None or diff < best_diff:
                best_pair = pair

    return best_pair


def ask_discrete_question(things, discrete_features):
    """Ask a discrete question, returning filtered things."""
    discrete_pair = generate_discrete_pair(things, discrete_features)
    if discrete_pair is None:
        print(things)
        print(discrete_features)
        raise RuntimeError('discrete_pair is None!')
    feature, value = discrete_pair

    result = ask_question(
            'Is ' + value + ' among its ' + feature + '?',
            '"{}" in features["{}"]'.format(value, feature))

    return {thing: features
            for thing, features in things.items()
            if (value in features[feature]) == result}


"""Continuous phase helpers"""

# Assign weights to how often the continuous feature should
# be selected. In this case, 0th genre has a 25% chance of being chosen
def pick_continuous_feature(): 
    continuous_feature_weight = [0] * 50 + [1] * 25 + [2] * 25 
    return random.choice(continuous_feature_weight)

def ask_continuous_question(things, continuous_features):
    """Ask a continuous question, returning filtered things."""
    num_clusters = 2

    points = collections.OrderedDict({
            thing: get_point(features, continuous_features)
            for thing, features in things.items()})

    array = np.array(list(points.values()))

    #Apply k means algorithm
    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(array)

    #We can improve on this, but the easiest implementation is randomly
    #selecting the continuous feature to ask about.
    selected_continuous_feature = pick_continuous_feature() 

    #Used for testing, but can delete this code
    #if not continuous_features:
    #    ask_question(random.choice(DUMMY_QUESTIONS), 'True')
    #    return things

    #Right now, kmeans does not return the size of each cluster.
    #However because there are only two clusters, picking
    #one cluster over the other doesn't matter since whatever
    #the user answers, either cluster will be chosen.
    feature = continuous_features[selected_continuous_feature]
    
    centers = [center[selected_continuous_feature] for center in kmeans.cluster_centers_]
    value = int(sum(centers) / len(centers))

    result = ask_question(
            'Is its ' + feature + ' greater than ' + str(value) + '?',
            'features["{}"] > {}'.format(feature, value))

    return {thing: features
            for thing, features in things.items()
            if (features[feature] > value) == result}


"""Final Guess phase helpers."""

def get_point(features, continuous_features):
    """Create point based on continous features of thing."""
    point = []
    for feature in continuous_features:
        try:
            value = features[feature]
        except KeyError as e:
            pdb.set_trace()
            raise e
        else:
            point.append(value)
    return point


def cluster_things(things, continuous_features):
    """Return list of lists, representing clusters of things."""
    num_clusters = 2

    points = collections.OrderedDict({
            thing: get_point(features, continuous_features)
            for thing, features in things.items()})

    array = np.array(list(points.values()))

    kmeans = KMeans(n_clusters=num_clusters, random_state=0).fit(array)
    indices = kmeans.predict(array)

    clusters = [[] for i in range(num_clusters)]
    for thing, index in zip(points, indices):
        clusters[index].append(thing)

    return [cluster for cluster in clusters if cluster]


def ask_guess_question(guess):
    """Ask question guessing that the thing is guess."""
    ask_question(
            'Are you thinking of "{}"?'.format(guess),
            'name == "{}"'.format(guess))


def make_final_guess(things, discrete_features, continuous_features):
    """Ask identity of object, returning filtered things.

    TODO: Implement the strategy given in the updated proposal
    instead of just making a random choice!

    """
    if not continuous_features:
        return random.choice(list(things))

    while len(things) > 1:
        clusters = cluster_things(things, continuous_features)
        if len(clusters) <= 1:
            break

        max_size = 0
        biggest_cluster = None
        for cluster in clusters:
            size = len(cluster)
            if size > max_size:
                max_size = size
                biggest_cluster = cluster

        things = {thing: things[thing] for thing in biggest_cluster}

    ask_guess_question(list(things)[0])

"""Main gameplay function"""


def play_game(
        things, discrete_features, continuous_features,
        num_discrete_questions=NUM_DISCRETE_QUESTIONS):
    """Play Twenty Questions."""
    questions_asked = 0
    for qnum in range(NUM_QUESTIONS - 1):

        if len(things) <= 1:
            break

        if not discrete_features:
            raise RuntimeError('discrete_features empty!')
        print('[{} things left...]'.format(len(things)), end=' ')

        if qnum < num_discrete_questions:
            things = ask_discrete_question(things, discrete_features)
        else:
            things = ask_continuous_question(things, continuous_features)

        questions_asked += 1
   
    """No more movies in the dictionary to guess from."""
    if not things:
        print('Sorry, we were unable to guess your movie.')
        return

    for thing, number in zip(things, range(NUM_QUESTIONS - questions_asked)):
        print('Attempting final guess {}'.format(number))
        make_final_guess(things, discrete_features, continuous_features)


"""Movie data"""


def create_movie_attributes(genres):
    """Create attribute "dict" for movie with given genres.

    For each possible movie genre, a particular movie either is
    or is not that genre.  The created attribute dict maps each
    passed genre to True, and any other genre to False.  That is,
    each possible movie genre is its own discrete genre.

    """
    return collections.defaultdict(
        lambda: False,
        {genre: True for genre in genres})


# Parse csv file into movieSet format
def create_movie_things():
    """Create the things dict needed by play_game from movie data."""

    things = {}
    """Map movie id to movie name."""
    movieMap = {}

    """Load data from our original csv file."""
    with open(MOVIE_CSV, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for number, name, genres in reader:
            features = {'genres': tuple(sorted(genres.split('|')))}
            mo = re.search(r'(?<=\()\d\d\d\d(?=\))', name)
            if mo:
                year = int(mo.group(0))
            else:
                year = 1985
            features['year'] = year
            things[name] = features
            movieMap[number] = name

    """Append to our current data structures using extended data from imdb."""
    with open(IMDB_MOVIE_CSV, 'r') as f:
        imdb_reader = csv.reader(f, delimiter=',')
        next(imdb_reader)
        for movie_line in imdb_reader:
            if(len(movie_line) == 5) :
                movieId = movie_line[0]
                cast = movie_line[1]
                director = movie_line[2]
                runtime = movie_line[3]
                rating = movie_line[4]
                features = things[movieMap.get(movieId)]; 
                features['runtime'] = int(runtime) 
                features['rating'] = float(rating) 
                things[movieMap.get(movieId)] = features

    return things

MOVIE_THINGS = create_movie_things()
MOVIE_ALL_FEATURES = set(
        itertools.chain.from_iterable(MOVIE_THINGS.values()))
MOVIE_CONTINUOUS_FEATURES = ['year', 'runtime', 'rating']
MOVIE_DISCRETE_FEATURES = MOVIE_ALL_FEATURES - set(MOVIE_CONTINUOUS_FEATURES)

"""
Filter MOVIE_THINGS by movies with all features.
(This avoids movies that don't have values for some features.)
"""
MOVIE_THINGS = {
        movie: features
        for movie, features in MOVIE_THINGS.items()
        if set(features) == MOVIE_ALL_FEATURES}

"""Program entry point"""

def main(num_discrete_questions=NUM_DISCRETE_QUESTIONS):
    things = MOVIE_THINGS
    discrete_features = MOVIE_DISCRETE_FEATURES
    continuous_features = MOVIE_CONTINUOUS_FEATURES
    play_game(things, discrete_features, continuous_features, num_discrete_questions)

if __name__ == '__main__':
    main()

