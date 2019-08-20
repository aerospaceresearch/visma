from visma.simplify.simplify import simplify
from visma.functions.constant import Constant
from visma.io.tokenize import tokenizer

# TODO: Test cases.
# TODO: Implement GUI/CLI.


def logicalAND(token1, token2):
    """Implements Bitwise AND
    Arguments:
        token1 -- {list} -- List of tokens of a constant number
        token2 -- {list} -- List of tokens of a constant number

    Returns:
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    """

    comments = []
    animations = []
    token1, _, _, _, _ = simplify(token1)
    token2, _, _, _, _ = simplify(token2)
    if isinstance(token1, Constant) and isinstance(token2, Constant):
        comments += [['Converting numbers to Binary Illustrations: ']]
        animations += [[]]
        binaryValue1 = token1.binary()
        binaryValue2 = token2.binary()
        comments += [[]]
        animations += [[tokenizer('a = ' + str(binaryValue1))]]
        comments += [[]]
        animations += [[tokenizer('b = ' + str(binaryValue2))]]
        comments += [['Doing AND operation for each of the consecutive bit']]
        animations += [[]]
        resultValue = token1.calculate() & token2.calculate()
        comments += [['Final result is']]
        animations += [[tokenizer('r = ' + str(resultValue))]]
        token_string = 'r = ' + str(resultValue)
        return token_string, animations, comments
    else:
        return '', [], []


def logicalOR(token1, token2):
    """Implements Bitwise OR
    Arguments:
        token1 -- {list} -- List of tokens of a constant number
        token2 -- {list} -- List of tokens of a constant number

    Returns:
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    """

    comments = []
    animations = []
    token1, _, _, _, _ = simplify(token1)
    token2, _, _, _, _ = simplify(token2)
    if isinstance(token1, Constant) and isinstance(token2, Constant):
        comments += [['Converting numbers to Binary Illustrations: ']]
        animations += [[]]
        binaryValue1 = token1.binary()
        binaryValue2 = token2.binary()
        comments += [[]]
        animations += [[tokenizer('a = ' + str(binaryValue1))]]
        comments += [[]]
        animations += [[tokenizer('b = ' + str(binaryValue2))]]
        comments += [['Doing OR operation for each of the consecutive bit']]
        animations += [[]]
        resultValue = token1.calculate() | token2.calculate()
        comments += [['Final result is']]
        animations += [[tokenizer('r = ' + str(resultValue))]]
        token_string = 'r = ' + str(resultValue)
        return token_string, animations, comments
    else:
        return '', [], []


def logicalNOT(token1):
    """Implements Bitwise NOT
    Arguments:
        token1 -- {list} -- List of tokens of a constant number

    Returns:
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    """

    comments = []
    animations = []
    token1, _, _, _, _ = simplify(token1)
    if isinstance(token1, Constant):
        comments += [['Converting numbers to Binary Illustrations: ']]
        animations += [[]]
        binaryValue1 = token1.binary()
        comments += [[]]
        animations += [[tokenizer('a = ' + str(binaryValue1))]]
        resultValueBinary = bin((1 << 8) - 1 - int(binaryValue1, 2))
        resultValue = int(resultValueBinary, 2)
        comments += [['Final binary is']]
        animations += [[tokenizer('r = ' + str(resultValueBinary))]]
        comments += [['Final result is']]
        animations += [[tokenizer('r = ' + str(resultValue))]]
        token_string = 'r = ' + str(resultValue)
        return token_string, animations, comments
    else:
        return '', [], []
