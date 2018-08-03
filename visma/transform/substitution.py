import copy
from visma.functions.operator import Multiply
from visma.functions.structure import Expression
from visma.functions.variable import Variable
from visma.functions.constant import Constant
from visma.io.checks import isTokenInToken, getVariables


def substitute(init_tok, subs_tok, toklist):
    """Substitute given token in token list
    
    [description]
    
    Arguments:
        init_tok {[type]} -- [description]
        subs_tok {[type]} -- [description]
        toklist {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    
    for i, token in enumerate(toklist):
        if isTokenInToken(init_tok, token):
            toklist[i] = substituteTokens(init_tok, subs_tok, token)
    return toklist


def substituteTokens(init_tok, subs_tok, given_tok):
    """Substitute some init_tok with subs_tok in a given_tok.
    
    For example: substitute x(init_tok) with wyz^2(subs_tok) in xyz(given_tok)
    i.e. final_tok will be wy^2z^3
    
    Arguments:
        init_tok {[type]} -- [description]
        subs_tok {[type]} -- [description]
        given_tok {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    
    if isinstance(given_tok, Variable):
        if isinstance(init_tok, Variable):
            power = getPowerRatio(init_tok, given_tok)
            if isinstance(subs_tok, Constant):
                given_tok = removeValues(init_tok, given_tok)
                if len(given_tok.value) == 0:
                    given_tok = Constant((subs_tok.value**power)*given_tok.coefficient)
                else:
                    given_tok.coefficient *= subs_tok.value**power
            elif isinstance(subs_tok, Variable):

                given_tok.coefficient /= init_tok.coefficient**power
                given_tok.coefficient *= subs_tok.coefficient**power
                given_tok = replaceValues(init_tok, subs_tok, given_tok, power)
            elif isinstance(subs_tok, Expression):
                subs_copy = copy.deepcopy(subs_tok)
                given_tok.coefficient /= init_tok.coefficient**power
                given_tok.coefficient *= subs_copy.coefficient**power
                subs_copy.coefficient = 1
                subs_copy.power = power
                given_tok = removeValues(init_tok, given_tok)
                if len(given_tok.value) == 0:
                    subs_copy.coefficient = given_tok.coefficient
                    given_tok = subs_copy
                else:
                    given_tok = Expression([given_tok, Multiply(), subs_copy])

    elif isinstance(given_tok, Expression):
        substitute(init_tok, subs_tok, Expression.toklist)

    return given_tok


def getPowerRatio(init_tok, given_tok):
    """returns given_tok.power / init_tok.power
    
    [description]
    
    Arguments:
        init_tok {[type]} -- [description]
        given_tok {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    
    if isinstance(init_tok, Variable) and isinstance(given_tok, Variable):
        varA = getVariables([init_tok])
        varB = getVariables([given_tok])
        if all(var in varB for var in varA):
            ratios = []
            for i, valA in enumerate(init_tok.value):
                for j, valB in enumerate(given_tok.value):
                    if valA == valB:
                        ratios.append(given_tok.power[j]/init_tok.power[i])
                        break
            if all(ratio == ratios[0] for ratio in ratios):
                return ratios[0]
    return 1


def removeValues(init_tok, given_tok):
    """[summary]
    
    [description]
    
    Arguments:
        init_tok {[type]} -- [description]
        given_tok {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    for valI in init_tok.value:
        for i, valG in enumerate(given_tok.value):
            if valI == valG:
                given_tok.value.pop(i)
                given_tok.power.pop(i)
                break
    return given_tok


def replaceValues(init_tok, subs_tok, given_tok, power):
    """[summary]
    
    [description]
    
    Arguments:
        init_tok {[type]} -- [description]
        subs_tok {[type]} -- [description]
        given_tok {[type]} -- [description]
        power {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    given_tok = removeValues(init_tok, given_tok)
    subs_copy = copy.deepcopy(subs_tok)
    subs_copy.power = [pow * power for pow in subs_copy.power]
    for val, pow in zip(subs_copy.value, subs_copy.power):
        if val in given_tok.value:
            valIndex = given_tok.value.index(val)
            given_tok.power[valIndex] += pow
        else:
            given_tok.value.append(val)
            given_tok.power.append(pow)
    return given_tok
