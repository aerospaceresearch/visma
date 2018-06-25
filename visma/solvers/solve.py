from visma.functions.structure import Function, Expression
from visma.functions.variable import Variable
from visma.functions.constant import Constant
from visma.functions.operator import Operator, Plus, Minus, EqualTo
from visma.simplify.simplify import simplify, simplifyEquation

##########################
# Simple Solver(for now) #
##########################


def solveFor(lTokens, rTokens, wrtVar):

    ltokens, rtokens, availableOperations, token_string, animation, comments = simplifyEquation(lTokens, rTokens)

    tokens, animNew, commentsNew = (solveTokens(lTokens, rTokens, wrtVar))

    animation.append(animNew)
    comments.append(commentsNew)

    return tokens, availableOperations, token_string, animation, comments


def solveTokens(lTokens, rTokens, wrtVar):
    animNew = []
    commentsNew = ["Solving with respect to " + r"$" + wrtVar + r"$" + "\n"]
    animNew.extend()
    return lTokens, rTokens, animNew, commentsNew


def funcInverse(lTokens, rTokens, wrtVar):
    pass


def moveToRHS(lTokens, rTokens, wrtVar):
    comment = "Moving "
    lTokensCopy = lTokens
    for i, token in enumerate(lTokensCopy):
        if isinstance(token, Function) and not checkVarInToken(token, wrtVar):
            if i-1 > 0 and isinstance(lTokensCopy[i-1], Operator):
                if token.value == '-':
                    rTokens.append(Plus())
                else:
                    rTokens.append(Minus())
                comment += r"$" + lTokensCopy[i-1].__str__() + r"$"
                lTokens.pop(i-1)
            elif i == 0 and not checkVarInToken(token, wrtVar):
                rTokens.append(Minus())
            rTokens.append(token)
            lTokens.pop(i)
            comment += r"$" + token.__str__() + r"$" + " "
    comment += "to RHS"
    lTokens, _, _, _, _ = simplify(lTokens)
    rTokens, _, _, _, _ = simplify(rTokens)
    animation = lTokens
    animation.append(EqualTo())
    animation.extend(rTokens)
    return lTokens, rTokens, animation, comment


def checkVarInTokensList(tokens, wrtVar):
    for token in tokens:
        return checkVarInToken(token, wrtVar)


def checkVarInToken(token, wrtVar):
    if isinstance(token, Constant):
        return False
    elif isinstance(token, Variable):
        if wrtVar in token.value:
            return True
    elif isinstance(token, Expression):
        return checkVarInTokensList(token.tokens, wrtVar)
    else:
        return True


def ifOnlyVarTermsInList(tokens, wrtVar):  # Rename func
    for token in tokens:
        if checkVarInToken(token, wrtVar) is False:
            return False
    return True
