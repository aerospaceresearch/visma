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
            comments += [['Factorial of ZERO is defined to be 1']]
            animation += [tokenizer('f = ' + str(1))]
        else:
            resultString = ''
            for i in range(1, value + 1):
                resultString += (str(i) + '*')
            resultString = resultString[:-1]
            resultTokens = tokenizer(resultString)
            comments += [['Expanding the factorial as']]
            animation += [resultTokens]
            result, _, _, _, _ = simplify(resultTokens)
        token_string = tokensToString(result)
        comments += [['Hence result: ']]
        animation += [tokenizer('f = ' + token_string)]
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
        comments += [['nCr is defined as (n!)/(r!)*(n-r)!']]
        animation += [[]]
        comments += [['Solving for n!']]
        animation += [[]]
        numerator, _, _, animNew1, commentNew1 = factorial(nTokens)
        commentNew1[1] = ['(n)! is thus solved as: ']
        animation.extend(animNew1)
        comments.extend(commentNew1)
        denominator = nTokens[0] - rTokens[0]
        comments += [['Solving for (n - r)!']]
        animation += [[]]
        denominator, _, _, animNew2, commentNew2 = factorial([denominator])
        commentNew2[1] = ['(n - r)! is thus solved as: ']
        comments.extend(commentNew2)
        animation.extend(animNew2)
        result = [numerator[0] / denominator[0]]
        comments += [['On placing values in (n!)/(n-r)!']]
        animation += [tokenizer('r = ' + tokensToString(result))]
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
        comments += [['nCr is defined as (n!)/(r!)*(n-r)!']]
        animation += [[]]
        comments += [['Solving for n!']]
        animation += [[]]
        numerator, _, _, animNew1, commentNew1 = factorial(nTokens)
        commentNew1[1] = ['(n)! is thus solved as: ']
        animation.extend(animNew1)
        comments.extend(commentNew1)
        denominator1 = nTokens[0] - rTokens[0]
        comments += [['Solving for (n - r)!']]
        animation += [[]]
        denominator1, _, _, animNew2, commentNew2 = factorial([denominator1])
        commentNew2[1] = ['(n - r)! is thus solved as: ']
        comments.extend(commentNew2)
        animation.extend(animNew2)
        comments += [['Solving for r!']]
        animation += [[]]
        denominator2, _, _, animNew3, commentNew3 = factorial([rTokens[0]])
        commentNew3[1] = ['r! is thus solved as: ']
        comments.extend(commentNew3)
        animation.extend(animNew3)
        denominator = denominator1[0] * denominator2[0]
        result = [numerator[0] / denominator]
        comments += [['On placing values in (n!)/(r!)*(n-r)!']]
        animation += [tokenizer('r = ' + tokensToString(result))]
    token_string = tokensToString(result)
    return result, [], token_string, animation, comments
