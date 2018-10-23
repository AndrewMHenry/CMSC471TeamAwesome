from tq import tq

class Player(object):

    def __init__(self, movie, features):
        """Create player thinking of movie with features."""
        self.movie = movie
        self.features = features

    def ask_question(self, question):
        print('Answering question "{}" with `False`...'.format(question))
        return False



def create_callback(movie, features, discrete_features, continuous_features):
    """Create an ask_question override for particular movie."""

    def ask_question(question, expression):
        """Behave like tq.ask_question."""
        namespace = {
                'name': movie,
                'features': features}
        answer = eval(expression, namespace, namespace)
        print('Answering question "{}" with `{}`...'.format(question, answer))
        return answer

    return ask_question


def main():
    """Run main from tq."""
    for movie, features in tq.MOVIE_THINGS.items():
        if 'Money Train (1995)' not in movie:
            pass
        tq.ask_question = create_callback(
                movie, features,
                tq.MOVIE_DISCRETE_FEATURES, tq.MOVIE_CONTINUOUS_FEATURES)
        print('[Selected movie {}]'.format(movie))
        tq.main()

