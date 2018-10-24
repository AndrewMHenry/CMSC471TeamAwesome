import collections
import contextlib
import os

from tq import tq


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


LOG_FILE = 'report.txt'
REDUCTION_FACTOR = 100

def main():
    """Run main from tq."""
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('log_file', default=LOG_FILE, nargs='?')
    parser.add_argument('reduction_factor', type=int, default=REDUCTION_FACTOR, nargs='?')
    args = parser.parse_args()

    log_file = open(args.log_file, 'w')

    num_successes = 0
    num_attempts = 0

    for index, (movie, features) in enumerate(tq.MOVIE_THINGS.items()):
        if index % args.reduction_factor != 0:
            continue
        answerer = Answerer(
                movie, features,
                tq.MOVIE_DISCRETE_FEATURES, tq.MOVIE_CONTINUOUS_FEATURES)
        tq.ask_question = answerer.ask_question

        with open(os.devnull, 'w') as output_stream:
            with contextlib.redirect_stdout(output_stream):
                tq.main(19)

        log_file.write('{},{},{}\n'.format(
            movie,
            'SUCCESS' if answerer.success else 'FAILURE',
            answerer.num_questions))

        num_attempts += 1
        num_successes += int(answerer.success)

    log_file.close()

    success_rate = num_successes / num_attempts
    print('SUCCESSES: {} / {} ({}%)'.format(
        num_successes, num_attempts, 100.0 * success_rate))
