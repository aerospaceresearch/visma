from visma.io.tokenize import tokenizer


def simpleProbability(sampleSpace, requiredEvent=None):
    """Implements simple probability

    Arguments:
        sampleSpace -- {visma.discreteMaths.statistics.ArithemeticMean}
        requiredEvent -- {Event whose probability is to be calculated}

    Returns:
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    """

    animations = []
    comments = []
    events = []
    token_string = ''
    if sampleSpace.values is not []:
        events.extend(sampleSpace.values)
        totalOccurances = len(events)
        animations += [[]]
        comments += [['The total occurances are ' + str(totalOccurances)]]
        requiredOccurances = events.count(requiredEvent)
        animations += [[]]
        comments += [['The occurances of required event are ' + str(requiredOccurances)]]
        probability = requiredOccurances/totalOccurances
        comments += [['Hence, Required probability is: ']]
        animations += [tokenizer('P = ' + str(probability))]
        token_string = 'P = ' + str(probability)
        return token_string, animations, comments
    else:
        return '', [], []
