import copy
from visma.functions.operator import Multiply
from visma.functions.structure import Expression
from visma.functions.variable import Variable
from visma.functions.constant import Constant
from visma.io.checks import isTokenInToken, getVariables


def substitute(initTok, subsTok, toklist):
    """Substitute given token in token list

    Arguments:
        initTok {functions.structure.Function} -- token to be substituted
        subsTok {functions.structure.Function} -- substitute token
        toklist {list} -- token list

    Returns:
        toklist {list} -- token list
    """

    for i, token in enumerate(toklist):
        if isTokenInToken(initTok, token):
            toklist[i] = substituteTokens(initTok, subsTok, token)
    return toklist


def substituteTokens(initTok, subsTok, givenTok):
    """Substitute initTok with subsTok in a givenTok.

    For example: substitute x(initTok) with wyz^2(subsTok) in xyz(givenTok)
    i.e. final_tok will be wy^2z^3

    Arguments:
        initTok {functions.structure.Function} -- token to be substituted
        subsTok {functions.structure.Function} -- substitute token
        givenTok {functions.structure.Function} -- given token

    Returns:
        givenTok {functions.structure.Function} -- given token after substitution
    """

    if isinstance(givenTok, Variable):
        if isinstance(initTok, Variable):
            power = getPowerRatio(initTok, givenTok)
            if isinstance(subsTok, Constant):
                givenTok = removeValues(initTok, givenTok)
                if len(givenTok.value) == 0:
                    givenTok = Constant((subsTok.value**power)*givenTok.coefficient)
                else:
                    givenTok.coefficient *= subsTok.value**power
            elif isinstance(subsTok, Variable):

                givenTok.coefficient /= initTok.coefficient**power
                givenTok.coefficient *= subsTok.coefficient**power
                givenTok = replaceValues(initTok, subsTok, givenTok, power)
            elif isinstance(subsTok, Expression):
                subs_copy = copy.deepcopy(subsTok)
                givenTok.coefficient /= initTok.coefficient**power
                givenTok.coefficient *= subs_copy.coefficient**power
                subs_copy.coefficient = 1
                subs_copy.power = power
                givenTok = removeValues(initTok, givenTok)
                if len(givenTok.value) == 0:
                    subs_copy.coefficient = givenTok.coefficient
                    givenTok = subs_copy
                else:
                    givenTok = Expression([givenTok, Multiply(), subs_copy])

    elif isinstance(givenTok, Expression):
        substitute(initTok, subsTok, Expression.toklist)

    return givenTok


def getPowerRatio(initTok, givenTok):
    """Returns ratio of power of given token to power of token to be substituted

    Arguments:
        initTok {functions.structure.Function} -- token to be substituted
        givenTok {functions.structure.Function} -- given token

    Returns:
        ratio {float} -- ratio of givenTok.power to initTok.power
    """

    if isinstance(initTok, Variable) and isinstance(givenTok, Variable):
        varA = getVariables([initTok])
        varB = getVariables([givenTok])
        if all(var in varB for var in varA):
            ratios = []
            for i, valA in enumerate(initTok.value):
                for j, valB in enumerate(givenTok.value):
                    if valA == valB:
                        ratios.append(givenTok.power[j]/initTok.power[i])
                        break
            if all(ratio == ratios[0] for ratio in ratios):
                return ratios[0]
    return 1


def removeValues(initTok, givenTok):
    """Removes token to be substituted from given token

    Arguments:
        initTok {functions.structure.Function} -- token to be substituted
        givenTok {functions.structure.Function} -- given token

    Returns:
        givenTok {functions.structure.Function} -- given token after removing initTok
    """
    for valI in initTok.value:
        for i, valG in enumerate(givenTok.value):
            if valI == valG:
                givenTok.value.pop(i)
                givenTok.power.pop(i)
                break
    return givenTok


def replaceValues(initTok, subsTok, givenTok, poweratio):
    """Replaces a token with a substitute token

    Arguments:
        initTok {functions.structure.Function} -- token to be substituted
        subsTok {functions.structure.Function} -- substitute token
        toklist {list} -- token list
        poweratio {float} -- ratio of givenTok.power to initTok.power

    Returns:
        givenTok {functions.structure.Function} -- given token after replacing initTok with subsTok
    """
    givenTok = removeValues(initTok, givenTok)
    subs_copy = copy.deepcopy(subsTok)
    subs_copy.power = [powr * poweratio for powr in subs_copy.power]
    for val, powr in zip(subs_copy.value, subs_copy.power):
        if val in givenTok.value:
            valIndex = givenTok.value.index(val)
            givenTok.power[valIndex] += powr
        else:
            givenTok.value.append(val)
            givenTok.power.append(powr)
    return givenTok
