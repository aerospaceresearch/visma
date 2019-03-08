from visma.functions.structure import Function, Expression
from visma.functions.variable import Variable
from visma.functions.constant import Constant
from visma.functions.operator import Operator, Minus, EqualTo
from visma.simplify.simplify import simplify, simplifyEquation
from visma.io.parser import tokensToString
import copy

##########################
# Simple Solver(for now) #
##########################

# FIXME: try-catch ValueError: negative number cannot be raised to a fractional power
# FIXME: Only single variable in LHS after moveToRHS


def solveFor(lTokens, rTokens, wrtVar):
    """Solve the input equation wrt to selected variable

    Arguments:
        lTokens {list} -- LHS tokens list
        rTokens {list} -- RHS tokens list
        wrtVar {string} -- variable to be solved

    Returns:
        lTokens {list} -- LHS tokens list
        rTokens {list} -- RHS tokens list
        availableOperations {list} -- list of operations
        token_string {string} -- final result in string
        animation {list} -- list of equation solving progress
        comments {list} -- list of solution steps
    """

    lTokens, rTokens, availableOperations, token_string, animation, comments = simplifyEquation(lTokens, rTokens)

    lTokens, rTokens, animNew, commentsNew = solveTokens(lTokens, rTokens, wrtVar)

    tokenToStringBuilder = copy.deepcopy(lTokens)
    tokenToStringBuilder.append(EqualTo())
    tokenToStringBuilder.extend(rTokens)
    token_string = tokensToString(tokenToStringBuilder)

    animation.extend(animNew)
    comments.extend(commentsNew)

    return lTokens, rTokens, availableOperations, token_string, animation, comments


def solveTokens(lTokens, rTokens, wrtVar):
    """Solve the input equation wrt to selected variable after equation simplification

    Arguments:
        lTokens {list} -- LHS tokens list
        rTokens {list} -- RHS tokens list
        wrtVar {string} -- variable to be solved

    Returns:
        lTokens {list} -- LHS tokens list
        rTokens {list} -- RHS tokens list
        animNew {list} -- list of equation solving progress
        commentsNew {list} -- list of solution steps
    """
    animNew = []
    commentsNew = []

    lTokens, rTokens, animation1, comment1 = moveToRHS(lTokens, rTokens, wrtVar)

    if checkOnlyVarTermsInList(lTokens, wrtVar):
        if len(lTokens) == 1:
            lTokens, rTokens, animation2, comment2 = funcInverse(lTokens, rTokens, wrtVar)
        else:
            animation2 = []
            comment2 = [""]
    else:
        animation2 = []
        comment2 = [""]

    animNew.extend([animation1, animation2])
    commentsNew.extend([comment1, comment2])
    return lTokens, rTokens, animNew, commentsNew


def moveToRHS(lTokens, rTokens, wrtVar):
    """Moves all variables which are not equal to wrtVar to RHS

    Arguments:
        lTokens {list} -- LHS tokens list
        rTokens {list} -- RHS tokens list
        wrtVar {string} -- variable to be solved

    Returns:
        lTokens {list} -- LHS tokens list
        rTokens {list} -- RHS tokens list
        animation {list} -- list of equation solving progress
        comments {list} -- list of solution steps
    """

    comment = "Moving "
    i = 0
    while i < len(lTokens):
        if isinstance(lTokens[i], Function) and not isVarInToken(lTokens[i], wrtVar):
            if i-1 >= 0 and isinstance(lTokens[i-1], Operator):
                comment += r"$" + lTokens[i-1].__str__() + r"$"
                if lTokens[i-1].value == '-':
                    lTokens[i-1].value = '+'
                    rTokens.append(lTokens.pop(i-1))
                elif lTokens[i-1].value == '+':
                    lTokens[i-1].value = '-'
                    rTokens.append(lTokens.pop(i-1))
                i -= 1
            elif i == 0:
                rTokens.append(Minus())
            comment += r"$" + lTokens[i].__str__() + r"$"
            rTokens.append(lTokens.pop(i))
            i -= 1
        i += 1
    comment += " to RHS"
    if isinstance(lTokens[0], Operator):
        if lTokens[0].value == '+':
            lTokens.pop(0)
        elif lTokens[0].value == '-':
            lTokens.pop(0)
            lTokens[0].coefficient *= -1
    lTokens, _, _, _, _ = simplify(lTokens)
    rTokens, _, _, _, _ = simplify(rTokens)
    animation = copy.deepcopy(lTokens)
    animation.append(EqualTo())
    animation.extend(rTokens)
    return lTokens, rTokens, animation, [comment]


def funcInverse(lTokens, rTokens, wrtVar):
    """Applies inverse of function of wrtVar to RHS

    Arguments:
        lTokens {list} -- LHS tokens list
        rTokens {list} -- RHS tokens list
        wrtVar {string} -- variable to be solved

    Returns:
        lTokens {list} -- LHS tokens list
        rTokens {list} -- RHS tokens list
        animation {list} -- list of equation solving progress
        comments {list} -- list of solution steps
    """
    if len(lTokens) == 1:
        rExpr = Expression()
        rExpr.tokens.extend(rTokens)
        lToken, rToken, comment = lTokens[0].inverse(rExpr, wrtVar)
    animation = copy.deepcopy(lTokens)
    animation.append(EqualTo())
    animation.append(rToken)
    return [lToken], [rToken], animation, [comment]


def isVarInTokensList(tokens, wrtVar):
    for token in tokens:
        if isVarInToken(token, wrtVar) is True:
            return True
    return False


def checkOnlyVarTermsInList(tokens, wrtVar):  # Rename func
    for token in tokens:
        if isVarInToken(token, wrtVar) is False:
            return False
    return True


def isVarInToken(token, wrtVar):
    if isinstance(token, Constant):
        return False
    elif isinstance(token, Variable):
        if wrtVar in token.value:
            return True
    elif isinstance(token, Expression):
        return isVarInTokensList(token.tokens, wrtVar)
    else:
        return True
