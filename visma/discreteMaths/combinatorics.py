from visma.io.tokenize import tokenizer
from visma.simplify.simplify import simplify
from visma.io.parser import tokensToString
from visma.functions.constant import Constant


def factorial(tokens):
    tokens, _, _, _, _ = simplify(tokens)
    availableOperation = ''
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
    return result, availableOperation, token_string, animation, comments


def permutation(nTokens, rTokens):
    nTokens, _, _, _, _ = simplify(nTokens)
    rTokens, _, _, _, _ = simplify(rTokens)
    availableOperation = ''
    animation = []
    comments = []
    if (isinstance(nTokens[0], Constant) & len(nTokens) == 1) & (isinstance(rTokens[0], Constant) & len(rTokens) == 1):
        numerator, _, _, _, _ = factorial(nTokens)
        denominator = nTokens[0] - rTokens[0]
        denominator, _, _, _, _ = factorial([denominator])
        result = [numerator[0] / denominator[0]]
    token_string = tokensToString(result)
    return result, availableOperation, token_string, animation, comments


def combination(nTokens, rTokens):
    nTokens, _, _, _, _ = simplify(nTokens)
    rTokens, _, _, _, _ = simplify(rTokens)
    availableOperation = ''
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
    return result, availableOperation, token_string, animation, comments
