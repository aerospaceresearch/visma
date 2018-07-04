from visma.functions.structure import Expression
from visma.functions.variable import Variable
from visma.functions.constant import Constant
from visma.io.checks import isTokenInToken, findWRTVariable


def substitute(init_tok, subs_tok, toklist):
    """Substitute given token in token list
    """
    for i, token in enumerate(toklist):
        if isTokenInToken(init_tok, token):
            toklist[i] = substituteTokens(init_tok, subs_tok, token)
    return toklist


def substituteTokens(init_tok, subs_tok, given_tok):
    """Substitute some init_tok with subs_tok in a given_tok.
    For example: substitute x(init_tok) with ab^2(subs_tok) in xyz(given_tok)
    i.e. final_tok will be ab^2yz
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
                pass
            elif isinstance(subs_tok, Expression):
                pass

    elif isinstance(given_tok, Expression):
        pass

    return given_tok


def getPowerRatio(init_tok, given_tok):
    """returns given_tok.power / init_tok.power
    """
    if isinstance(init_tok, Variable) and isinstance(given_tok, Variable):
        varA = findWRTVariable([init_tok])
        varB = findWRTVariable([given_tok])
        if all(var in varB for var in varA):
            ratios = []
            for i, valA in enumerate(init_tok.value):
                for j, valB in enumerate(given_tok.value):
                    if valA == valB:
                        ratios.append(given_tok.power[j]/init_tok.power[i])
                        break
            if all(ratio == ratios[0] for ratio in ratios):
                return ratios[0]


def removeValues(init_tok, given_tok):
    for valI in init_tok.value:
        for i, valG in enumerate(given_tok.value):
            if valI == valG:
                given_tok.value.pop(i)
                given_tok.power.pop(i)
                break
    return given_tok
