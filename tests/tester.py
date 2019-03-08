from visma.io.tokenize import tokenizer, getLHSandRHS, removeSpaces
from visma.io.checks import checkTypes

# TODO: Categorize all test cases into COVERAGE and BASIS


def quickTest(inp, operation, wrtVar=None):
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
    output = removeSpaces(token_string)
    return output


def getTokens(eqString):
    tokens = tokenizer(eqString)
    if len(tokens) == 1:
        tokens = tokens[0]
    return tokens
