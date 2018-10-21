from __future__ import print_function
import collections
import csv
import itertools
import os
import pdb
import random


"""Parameter definitions"""

NUM_QUESTIONS = 20
NUM_DISCRETE_QUESTIONS = NUM_QUESTIONS / 2

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


"""Generic helpers"""


def ask_question(question):
    """Interactively ask question to user, returning boolean answer."""
    return input(question + ' ') == 'yes'


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

        counts = collections.Counter([
            fdict[feature] for fdict in things.values()])

        for value, count in counts.items():
            pair = (feature, value)
            if min_count < count < max_count:
                return pair
            elif abs(count - half_count) < abs(best_count - half_count):
                best_pair = pair

    return best_pair


def ask_discrete_question(things, discrete_features):
    """Ask a discrete question, returning filtered things."""
    feature, value = generate_discrete_pair(things, discrete_features)

    if isinstance(value, bool):
        result = ask_question('Is it ' + feature + '?')
        value = True
    else:
        result = ask_question('Is its ' + feature + ' ' + str(value) + '?')

    return {thing: features
            for thing, features in things.items()
            if (features[feature] == value) == result}


"""Continuous phase helpers"""


def ask_continuous_question(things, continuous_features):
    """Ask a continuous question, returning filtered things."""
    ask_question(random.choice(DUMMY_QUESTIONS))
    return things


"""Final Guess phase helpers."""


def make_final_guess(things, discrete_features, continuous_features):
    """Ask identity of object, returning filtered things.

    TODO: Implement the strategy given in the updated proposal
    instead of just making a random choice!

    """
    guess = random.choice(things.keys())
    result = ask_question('Is it ' + guess + '?')

    if result:
        return {guess: things[guess]}
    else:
        return {thing: features
                for thing, features in things.items()
                if thing != guess}


"""Main gameplay function"""


def play_game(things, discrete_features, continuous_features):
    """Play Twenty Questions."""
    for qnum in range(NUM_QUESTIONS):

        if len(things) <= 1:
            break

        print('[{} things left...]'.format(len(things)), end=' ')

        if qnum == NUM_DISCRETE_QUESTIONS:
            print('\n'.join(sorted(things)))
        if qnum < NUM_DISCRETE_QUESTIONS:
            things = ask_discrete_question(things, discrete_features)
        else:
            things = ask_continuous_question(things, continuous_features)

    if len(things) > 1:
        print('Hmm... too many options.')
    elif len(things) == 1:
        print('AHA! It must be ' + list(things)[0] + '!')
    else:
        print('Idk')


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
    with open(MOVIE_CSV, 'r') as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        return {name: create_movie_attributes(genres.split('|'))
                for number, name, genres in reader}


"""Program entry point"""


def main():
    # pdb.set_trace()
    things = create_movie_things()
    discrete_features = set(itertools.chain.from_iterable(things.values()))
    continuous_features = []
    play_game(things, discrete_features, continuous_features)
