import numpy as np
import matplotlib.pyplot as plt
from visma.input.tokenize import tokenizer, get_variables_value, get_lhs_rhs

# TODO: Use matplotlib to plot graphs(use openGL if possible)


def plotthis(result):
    resultTokens = tokenizer(result)
    LHS, RHS = get_lhs_rhs(resultTokens)
    varDict = get_variables_value(resultTokens)
    varDict = varNumpyArrays(varDict, LHS, RHS)
    plot(varDict, LHS, RHS)
    return None


def plot(varDict, lhstok, rhstok):
    LHS = 0
    RHS = 0
    coeff = 1
    for token in lhstok:
        if token['type'] == 'variable':
            LHS += coeff*token['coefficient']*((varDict[token['value'][0]])**token['power'][0])
        elif token['type'] == 'constant':
            LHS += coeff*token['value']
        elif token['type'] == 'binary':
            if token['value'] == '+':
                coeff = 1
            elif token['value'] == '-':
                coeff = -1
    for token in rhstok:
        if token['type'] == 'variable':
            RHS += coeff*token['coefficient']*((varDict[token['value'][0]])**token['power'][0])
        elif token['type'] == 'constant':
            RHS += coeff*token['value']
        elif token['type'] == 'binary':
            if token['value'] == '+':
                coeff = 1
            elif token['value'] == '-':
                coeff = -1
    if rhstok == []:
        RHS += varDict['y']

    plt.contour(varDict['x'], varDict['y'], (LHS - RHS), [0])
    plt.grid()
    plt.show()
    return None


def varNumpyArrays(varDict, LHS, RHS):
    delta = 1
    if RHS == []:
        varDict['y'] = None
    # FIXME: Assign limit range dynamically to different variables
    # xrange = np.arange(-20, 20.0, 0.1)
    # yrange = np.arange(-20, 20.0, 0.1)
    for key in varDict:
        limits = np.arange(-20.0, 20.0, delta)
        varDict[key] = np.meshgrid(limits)
        varDict[key] = np.asarray(varDict[key])
    return varDict


'''
def plot():
    delta = 0.1
    xrange = np.arange(-20, 20.0, delta)
    yrange = np.arange(-20, 20.0, delta)
    X, Y = np.meshgrid(xrange, yrange)

    LHS = X**2
    RHS = Y

    plt.contour(X, Y, (LHS - RHS), [0])
    plt.grid()
    plt.show()
'''

if __name__ == '__main__':
    plotthis("x = y")
