from visma.io.tokenize import tokenizer, getLHSandRHS, removeSpaces
from visma.io.checks import checkTypes
from visma.discreteMaths.statistics import sampleSpace


# TODO: Categorize all test cases into COVERAGE and BASIS
def quickTest(inp, operation, wrtVar=None):
    if operation.__name__ not in ['ArithemeticMean', 'Mode', 'Median']:
        if (inp.count(';') == 2):
            afterSplit = inp.split(';')
            eqStr1 = afterSplit[0]
            eqStr2 = afterSplit[1]
            eqStr3 = afterSplit[2]
            tokens = [tokenizer(eqStr1), tokenizer(eqStr2), tokenizer(eqStr3)]
            token_string, _, _ = operation(tokens[0], tokens[1], tokens[2], wrtVar)
            return removeSpaces(token_string)
        elif (inp.count(';') == 1):
            afterSplit = inp.split(';')
            eqStr1 = afterSplit[0]
            eqStr2 = afterSplit[1]
            tokens = [tokenizer(eqStr1), tokenizer(eqStr2)]
            _, _, token_string, _, _ = operation(tokens[0], tokens[1])
            return removeSpaces(token_string)
        else:
            lhs, rhs = getLHSandRHS(tokenizer(inp))
            _, inpType = checkTypes(lhs, rhs)
            if inpType == "equation":
                if wrtVar is not None:
                    _, _, _, token_string, _, _ = operation(lhs, rhs, wrtVar)
                else:
                    _, _, _, token_string, _, _ = operation(lhs, rhs)
            elif inpType == "expression":
                if wrtVar is not None:
                    _, _, token_string, _, _ = operation(lhs, wrtVar)
                else:
                    _, _, token_string, _, _ = operation(lhs)
    else:
        sampleSpaceObject = sampleSpace(inp)
        token_string, _, _ = operation(sampleSpaceObject)
    output = removeSpaces(token_string)
    return output


def getTokens(eqString):
    tokens = tokenizer(eqString)
    if len(tokens) == 1:
        tokens = tokens[0]
    return tokens
