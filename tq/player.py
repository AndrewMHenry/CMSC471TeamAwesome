import collections
import contextlib
import os

from tq import tq

class Player(object):

    def __init__(self, movie, features):
        """Create player thinking of movie with features."""
        self.movie = movie
        self.features = features

    def ask_question(self, question):
        print('Answering question "{}" with `False`...'.format(question))
        return False


num_questions = None
success = None


class Answerer(object):

    def __init__(self, movie, features, discrete_features, continuous_features):
        """ """
        self.movie = movie
        self.features = features
        self.discrete_features = discrete_features
        self.continuous_features = continuous_features

        self.num_questions = 0
        self.success = False

    def ask_question(self, question, expression):
        """Behave like tq.ask_question."""

        # register that another question was asked
        self.num_questions += 1

        namespace = {
                'name': self.movie,
                'features': self.features}
        answer = eval(expression, namespace, namespace)
        print('Answering question "{}" with `{}`...'.format(question, answer))

        # register a win if answered "yes" to movie guess
        if 'name' in expression and answer:
            self.success = True

        return answer

def create_callback(
        movie, features,
        discrete_features, continuous_features,
        result):
    """Create an ask_question override for particular movie.

    The result dict should have keys 'success' and 'num_questions'.
    The ask_question function will modify these values as necessary,
    so the caller of create_callback can retrieve these values at
    the end of the game.

    expression = 'name == "{}"'.format(movie)
    """

    def ask_question(question, expression):
        """Behave like tq.ask_question."""

        nonlocal result
        # register that another question was asked
        result['num_questions'] += 1

        namespace = {
                'name': movie,
                'features': features}
        answer = eval(expression, namespace, namespace)
        print('Answering question "{}" with `{}`...'.format(question, answer))

        # register a win if answered "yes" to movie guess
        if 'name' in expression and answer:
            result['success'] = True

        return answer

    return ask_question


def main():
    """Run main from tq."""
    report = ''
    for movie, features in tq.MOVIE_THINGS.items():
        result = {
                'success': False,
                'num_questions': 0
                }

        answerer = Answerer(
                movie, features,
                tq.MOVIE_DISCRETE_FEATURES, tq.MOVIE_CONTINUOUS_FEATURES)
        tq.ask_question = answerer.ask_question

        with open(os.devnull, 'w') as output_stream:
            with contextlib.redirect_stdout(output_stream):
                tq.main()

        print('{},{},{}'.format(
            movie,
            'SUCCESS' if answerer.success else 'FAILURE',
            answerer.num_questions))

