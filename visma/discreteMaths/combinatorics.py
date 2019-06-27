'''This module is supposed to contain all the combinatorics related stuff which can be performed by VisualMath (VisMa)

Note: Please try to maintain proper documentation
'''

from visma.io.tokenize import tokenizer
from visma.simplify.simplify import simplify
from visma.io.parser import tokensToString
from visma.functions.constant import Constant


def factorial(tokens):
    '''Used to get factorial of tokens provided

    Argument:
        tokens {list} -- list of tokens

    Returns:
        result {list} -- list of result tokens
        {empty list}
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    '''
    tokens, _, _, _, _ = simplify(tokens)
    animation = []
    comments = []
    if (isinstance(tokens[0], Constant) & len(tokens) == 1):
        value = int(tokens[0].calculate())
        if value == 0:
            result = [Constant(1)]
        else:
            resultString = ''
            for i in range(1, value + 1):
                resultString += (str(i) + '*')
            resultString = resultString[:-1]
            resultTokens = tokenizer(resultString)
            result, _, _, _, _ = simplify(resultTokens)
        token_string = tokensToString(result)
    return result, [], token_string, animation, comments


def permutation(nTokens, rTokens):
    '''Used to get Permutation (nPr)

    Argument:
        nTokens {list} -- list of tokens of "n" in nPr
        rTokens {list} -- list of tokens of "r" in nPr

    Returns:
        result {list} -- list of result tokens
        {empty list}
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    '''
    nTokens, _, _, _, _ = simplify(nTokens)
    rTokens, _, _, _, _ = simplify(rTokens)
    animation = []
    comments = []
    if (isinstance(nTokens[0], Constant) & len(nTokens) == 1) & (isinstance(rTokens[0], Constant) & len(rTokens) == 1):
        numerator, _, _, _, _ = factorial(nTokens)
        denominator = nTokens[0] - rTokens[0]
        denominator, _, _, _, _ = factorial([denominator])
        result = [numerator[0] / denominator[0]]
    token_string = tokensToString(result)
    return result, [], token_string, animation, comments


def combination(nTokens, rTokens):
    '''Used to get Combination (nCr)

    Argument:
        nTokens {list} -- list of tokens of "n" in nCr
        rTokens {list} -- list of tokens of "r" in nCr

    Returns:
        result {list} -- list of result tokens
        {empty list}
        token_string {string} -- final result stored in a string
        animation {list} -- list of equation solving process
        comments {list} -- list of comments in equation solving process
    '''
    nTokens, _, _, _, _ = simplify(nTokens)
    rTokens, _, _, _, _ = simplify(rTokens)
    animation = []
    comments = []
    if (isinstance(nTokens[0], Constant) & len(nTokens) == 1) & (isinstance(rTokens[0], Constant) & len(rTokens) == 1):
        numerator, _, _, _, _ = factorial(nTokens)
        denominator1 = nTokens[0] - rTokens[0]
        denominator1, _, _, _, _ = factorial([denominator1])
        denominator2, _, _, _, _ = factorial([rTokens[0]])
        denominator = denominator1[0] * denominator2[0]
        result = [numerator[0] / denominator]
    token_string = tokensToString(result)
    return result, [], token_string, animation, comments
