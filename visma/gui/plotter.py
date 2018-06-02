from visma.io.tokenize import get_lhs_rhs
import numpy as np
from visma.functions.variable import Variable, Constant
from visma.functions.operator import Binary
from visma.solvers.solve import is_equation


def plotThis(equationTokens):
    LHStok, RHStok = get_lhs_rhs(equationTokens)

    varDict = {}
    delta = 0.1
    xrange = np.arange(-20, 20.0, delta)
    yrange = np.arange(-20, 20.0, delta)
    varDict['x'], varDict['y'] = np.meshgrid(xrange, yrange)

    LHS = 0
    coeff = 1
    for token in LHStok:
        if token.__class__ == Variable:
            LHS += coeff*token.coefficient*(varDict['x']**token.power[0])
        elif token.__class__ == Binary and token.value == '-':
            coeff = -1
        elif token.__class__ == Constant:
            LHS += coeff*token.value
    RHS = varDict['y']
    if(is_equation(LHStok, RHStok)):
        RHS = 0

    return varDict['x'], varDict['y'], LHS, RHS
