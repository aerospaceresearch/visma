from visma.functions.structure import Expression
from visma.functions.variable import Variable, Constant
from visma.functions.operator import Binary, Sqrt


def resultLatex(operation, equations, comments):

    equationLatex = []
    for eqTokens in equations:
        equationLatex.append(tokensToLatex(eqTokens))

    finalSteps = "INPUT: " + r"$" + equationLatex[0] + r"$" + "\n"
    finalSteps += "OPERATION: " + operation + "\n"
    finalSteps += "OUTPUT: " + r"$" + equationLatex[-1] + r"$" + "\n"*2

    for i in xrange(len(equationLatex)):
        if comments[i] != []:
            finalSteps += comments[i][0] + "\n"
        finalSteps += r"$" + equationLatex[i] + r"$" + "\n"*2

    return finalSteps


def tokensToLatex(eqTokens):
    eqLatex = ""
    for token in eqTokens:
        if token.__class__ == Binary:
            eqLatex += str(token.value)
        elif token.__class__ == Constant:
            eqLatex += str(token.value)
        elif token.__class__ == Variable:
            if token.coefficient != 1:
                eqLatex += str(token.coefficient)
            eqLatex += "{" + token.value[0] + " }"
            if token.power != [1]:
                eqLatex += "^{" + str(token.power[0]) + " }"
        elif token.__class__ == Expression:
            if token.coefficient != 1:
                eqLatex += str(token.coefficient) + "*"
            eqLatex += "{ (" + tokensToLatex(token.tokens) + ") }"
            if token.power != 1:
                eqLatex += "^{" + str(token.power) + " }"
        elif token.__class__ == Sqrt:
            if token.expression.value == -1:
                eqLatex += "\iota "
            else:
                eqLatex += "\sqrt { { (" + tokensToLatex(token.expression) + ") }^" + str(token.expression.power) + " }"
    return eqLatex
