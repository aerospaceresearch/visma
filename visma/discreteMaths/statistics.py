from collections import Counter
from visma.io.tokenize import tokenizer
from visma.simplify.simplify import simplify
from visma.io.parser import tokensToString
from visma.functions.constant import Constant

# TODO: Implement this module in GUI/CLI


class sampleSpace(object):
    """Class used to represent sample space of a data.
    """
    values = []
    size = 0

    def __init__(self, values):
        if values is not None:
            self.values = values
            self.size = len(values)


def ArithemeticMean(sampleSpace):
    """Implements arithemetic mean

    Arguments:
        sampleSpace -- {visma.discreteMaths.statistics.ArithemeticMean}

    Returns:
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    """
    animations = []
    comments = []
    if sampleSpace.values is not []:
        sm = sum(sampleSpace.values)
        animations += [[]]
        comments += [['Sum of all the values of the sample space provided by user: ' + str(sm)]]
        summationString = ''
        for val in sampleSpace.values:
            summationString += str(val) + '+'
        summationString = summationString[:-1]
        summationTokens = tokenizer(summationString)
        resultTokens, _, _, _, _ = simplify(summationTokens)
        if len(resultTokens) == 1 and isinstance(resultTokens[0], Constant):
            ArithemeticMean = resultTokens[0]/Constant(len(sampleSpace.values))
        animations += [[]]
        comments += [['Considering ' + str(len(sampleSpace.values)) + ' values.']]
        animations += [[tokenizer('mean = ' + str(ArithemeticMean.calculate))]]
        token_string = tokensToString([ArithemeticMean])
        return token_string, animations, comments
    else:
        return '', [], []


def Mode(sampleSpace):
    """Implements Mode

    Arguments:
        sampleSpace -- {visma.discreteMaths.statistics.ArithemeticMean}

    Returns:
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    """

    animations = []
    comments = []
    token_string = ''
    if sampleSpace.values is not []:
        mode, frequency = Counter(sampleSpace.values).most_common(1)[0]
        comments += [['The mode refers to the most occuring element']]
        animations += [[]]
        comments += [['Mode = ' + str(mode) + '; Mode Frequency = ' + str(frequency)]]
        animations += [[]]
        token_string = 'Mode = ' + str(mode) + '; Mode Frequency = ' + str(frequency)
        return token_string, animations, comments
    else:
        return '', [], []


def Median(sampleSpace):
    """Implements Median

    Arguments:
        sampleSpace -- {visma.discreteMaths.statistics.ArithemeticMean}

    Returns:
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    """

    animations = []
    comments = []
    token_string = ''
    if sampleSpace.values is not []:
        sizeSampleSpace = sampleSpace.size
        if sizeSampleSpace % 2 == 1:
            medianValue = sorted(sampleSpace.values)[sizeSampleSpace//2]
        else:
            medianValue = sum(sorted(sampleSpace.values)[sizeSampleSpace//2-1: sizeSampleSpace//2+1])/2.0
        comments += [['The median refers to the middle element in sorted sample space']]
        animations += [[]]
        comments += [['Median = ' + str(medianValue)]]
        animations += [[]]
        token_string = str(medianValue)
        return token_string, animations, comments
    else:
        return '', [], []
