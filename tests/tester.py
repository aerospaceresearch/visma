from visma.io.tokenize import tokenizer, getLHSandRHS, removeSpaces
from visma.io.checks import checkTypes

# TODO: Categorize all test cases into COVERAGE and BASIS


def quickTest(input, operation, wrtVar=None):
    lhs, rhs = getLHSandRHS(tokenizer(input))
    _, type = checkTypes(lhs, rhs)
    if type == "equation":
        if wrtVar is not None:
            _, _, _, token_string, _, _ = operation(lhs, rhs, wrtVar)
        else:
            _, _, _, token_string, _, _ = operation(lhs, rhs)
    elif type == "expression":
        if wrtVar is not None:
            _, _, token_string, _, _ = operation(lhs, wrtVar)
        else:
            _, _, token_string, _, _ = operation(lhs)
    output = removeSpaces(token_string)
    return output
