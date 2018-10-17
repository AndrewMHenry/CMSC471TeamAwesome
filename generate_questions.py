import collections

"""Parameters"""
NUM_QUESTIONS = 20
NUM_DISCRETE_QUESTIONS = NUM_QUESTIONS / 2

RELATIVE_ERROR = 0.1
MIN_COUNT_SCALE = 0.5 - RELATIVE_ERROR
MAX_COUNT_SCALE = 0.5 + RELATIVE_ERROR


def ask_question(question):
    """Interactively ask question to user, returning boolean answer."""
    return input(question + ' ') == 'yes'



def get_count_range(num_things):
    """Return range ((lower, upper)) of acceptable discrete value counts."""
    return (num_things * MIN_COUNT_SCALE, num_things * MAX_COUNT_SCALE)


def generate_discrete_pair(things, discrete_features):
    """Create a feature-value pair to ask about."""
    min_count, max_count = get_count_range(len(things))
    for feature in discrete_features:

        counts = collections.Counter([
            fdict[feature] for fdict in things.values()])

        for value, count in counts:
            if min_count < count < max_count:
                return (feature, value)


def filter_things_discrete(things, feature, value, result):
    """Filter things that don't match result for feature and value."""
    return {thing: features
            for thing, features in things.items()
            if (features[feature] == value) == result}


def ask_discrete_questions(things, discrete_features):
    """Ask discrete questions, returning filtered set of things."""
    for i in range(NUM_DISCRETE_QUESTIONS):
        feature, value = generate_discrete_question(things, discrete_features)
        result = ask_question('Is its ' + feature + ' ' + value + '?')
        things = filter_things_discrete(things, feature, value, result)

    return things


def ask_continuous_questions(things, continuous_features):
    """Ask continuous questions, returning filtered set of things."""
    return things


def play_game(things, discrete_features, continuous_features):
    """Play Twenty Questions."""
    things = ask_discrete_questions(things, discrete_features)
    things = ask_continuous_questions(things, continuous_features)
