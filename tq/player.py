import collections
import contextlib
import os
import json

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
    parser.add_argument(
            'reduction_factor', type=int,
            default=REDUCTION_FACTOR, nargs='?')
    parser.add_argument(
            '-d', type=int, dest='discrete', help='Integer number of discrete questions',
            default=tq.NUM_DISCRETE_QUESTIONS)
    parser.add_argument(
            '-w', dest='weight', help='File name to continuous json weight',
            default=None)
    parser.add_argument(
            '--train',dest='training', help='Flag to determine if the game is ran using training data',
            default=False, action='store_true'
            )
    parser.add_argument(
            '--test',dest='testing', help='Flag to determine if the game is ran using test data',
            default=False, action='store_true'
            )

    args = parser.parse_args()

    log_file = open(args.log_file, 'w')
    isTraining = args.training
    isTesting = args.testing
    num_discrete_questions = args.discrete
    continuous_weight_file = args.weight
    continuous_weight = {}

    if continuous_weight_file is not None:
        continuous_weight_json = open(continuous_weight_file)
        continuous_weight_string = continuous_weight_json.read()
        continuous_weight = json.loads(continuous_weight_string)
        continuous_weight_json.close()
    else:
        continuous_weight = tq.MOVIE_CONTINUOUS_FEATURES

    if isTraining:
        things = tq.MOVIE_THINGS_TRAINING
    elif isTesting:
        things = tq.MOVIE_THINGS_TESTING
    else:
        things = tq.MOVIE_THINGS

    num_successes = 0
    num_attempts = 0

    for index, (movie, features) in enumerate(things.items()):
        if index % args.reduction_factor != 0:
            continue
        answerer = Answerer(
                movie, features,
                tq.MOVIE_DISCRETE_FEATURES, tq.MOVIE_CONTINUOUS_FEATURES)
        tq.ask_question = answerer.ask_question

        with open(os.devnull, 'w') as output_stream:
            with contextlib.redirect_stdout(output_stream):
                tq.main(num_discrete_questions, continuous_weight, isTraining, isTesting)

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
