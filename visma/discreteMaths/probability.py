from visma.io.tokenize import tokenizer


def simpleProbability(sampleSpace, requiredEvent=None):
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
