import numpy as np
import matplotlib.pyplot as plt

# TODO: Use matplotlib to plot graphs(use openGL if possible)


def plotthis(result):
    from visma.input.tokenize import check_result_type, tokenizer, get_variables_value, get_lhs_rhs
    resulttokens = tokenizer(result)
    LHS, RHS = get_lhs_rhs(resulttokens)
    variables = get_variables_value(resulttokens)
    type = check_result_type(result)
    variables = varArrays(variables, result)
    plot(variables, LHS, RHS, type)


def plot(varDict, lhstok, rhstok, type):
    LHS = 0
    RHS = 0
    coeff = 1
    for token in lhstok:
        if token['type'] == 'variable':
            LHS += coeff*token['coefficient']*(varDict[token['coefficient'][0]]**token['power'])
        elif token['type'] == 'constant':
            LHS += coeff*token['value']
        elif token['type'] == 'binary':
            if token['value'] == '+':
                coeff = 1
            elif token['value'] == '-':
                coeff = -1
    for token in rhstok:
        if token['type'] == 'variable':
            RHS += coeff*token['coefficient']*(varDict[token['coefficient'][0]]**token['power'])
        elif token['type'] == 'constant':
            RHS += coeff*token['value']
        elif token['type'] == 'binary':
            if token['value'] == '+':
                coeff = 1
            elif token['value'] == '-':
                coeff = -1
    if rhstok == []:
        RHS = varDict['ex']

    plt.contour(varDict['x'], varDict['y'], (LHS - RHS), [0])
    plt.grid()
    plt.show()


def varArrays(varDict, type, limits=np.arange(-50, 50, 1)):
    if type == 'expression':
        varDict['ex'] = None
    # FIXME: Assign different limit range to different variables
    # xrange = np.arange(-20, 20.0, 0.1)
    # yrange = np.arange(-20, 20.0, 0.1)
    for key in varDict:
        varDict[key] = np.meshgrid(limits)
    return varDict


'''
def plot():
    delta = 0.1
    xrange = np.arange(-20, 20.0, delta)
    yrange = np.arange(-20, 20.0, delta)
    X, Y = np.meshgrid(xrange, yrange)

    # F is one side of the equation, G is the other
    LHS = X**2
    RHS = Y

    plt.contour(X, Y, (LHS - RHS), [0])
    plt.grid()
    plt.show()
'''

if __name__ == '__main__':
    plotthis("x = y")
