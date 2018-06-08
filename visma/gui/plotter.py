from visma.io.tokenize import get_lhs_rhs
import numpy as np
from visma.functions.variable import Variable
from visma.functions.constant import Constant
from visma.functions.operator import Binary
from visma.io.checks import is_equation


def plotThis(equationTokens):

    # FIXME: Quite basic right now. Need fix for multi-variables

    LHStok, RHStok = get_lhs_rhs(equationTokens)

    varDict = {}
    delta = 0.1
    xrange = np.arange(-20, 20.0, delta)
    yrange = np.arange(-20, 20.0, delta)
    varDict['x'], varDict['y'] = np.meshgrid(xrange, yrange)

    LHS = 0
    coeff = 1
    for token in LHStok:
        if isinstance(token, Variable):
            LHS += coeff*token.coefficient
            for eachValue, eachPower in zip(token.value, token.power):
                LHS *= (varDict[eachValue]**eachPower)
        elif isinstance(token, Binary) and token.value == '-':
            coeff = -1
        elif isinstance(token, Constant):
            LHS += coeff*token.value
    RHS = varDict['y']
    if(is_equation(LHStok, RHStok)):
        RHS = 0

    return varDict['x'], varDict['y'], LHS, RHS
