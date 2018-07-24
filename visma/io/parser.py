from visma.functions.structure import Expression
from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.functions.operator import Binary, Sqrt
from visma.functions.exponential import Logarithm
from visma.io.checks import isNumber


def resultLatex(operation, equations, comments, wrtVar=None):

    equationLatex = []
    for eqTokens in equations:
        equationLatex.append(tokensToLatex(eqTokens))

    finalSteps = "INPUT: " + r"$" + equationLatex[0] + r"$" + "\n"
    finalSteps += "OPERATION: " + operation
    if wrtVar is not None:
        finalSteps += " with respect to " + r"$" + wrtVar + r"$"
    finalSteps += "\n"
    finalSteps += "OUTPUT: " + r"$" + equationLatex[-1] + r"$" + "\n"*2

    for i in range(len(equationLatex)):
        if comments[i] != []:
            finalSteps += str(comments[i][0]) + "\n"
        finalSteps += r"$" + equationLatex[i] + r"$" + "\n"*2

    return finalSteps


def tokensToLatex(eqTokens):
    eqLatex = ""
    for token in eqTokens:
        eqLatex += token.__str__()
    return eqLatex


def tokensToString(tokens):
    # FIXME: tokensToString method
    tokenString = ''
    for token in tokens:
        if isinstance(token, Constant):
            if isinstance(token.value, list):
                for j, val in token.value:
                    if token['power'][j] != 1:
                        tokenString += (str(val) + '^(' + str(token.power[j]) + ')')
                    else:
                        tokenString += str(val)
            elif isNumber(token.value):
                if token.power != 1:
                    tokenString += (str(token.value) + '^(' + str(token.power) + ')')
                else:
                    tokenString += str(token.value)
        elif isinstance(token, Variable):
            if token.coefficient == 1:
                pass
            elif token.coefficient == -1:
                tokenString += '-'
            else:
                tokenString += str(token.coefficient)
            for j, val in enumerate(token.value):
                if token.power[j] != 1:
                    tokenString += (str(val) + '^(' + str(token.power[j]) + ')')
                else:
                    tokenString += str(val)
        elif isinstance(token, Binary):
            tokenString += ' ' + str(token.value) + ' '
        elif isinstance(token, Expression):
            if token.coefficient != 1:
                tokenString += str(token.coefficient) + '*'
            tokenString += '('
            tokenString += tokensToString(token.tokens)
            tokenString += ')'
            if token.power != 1:
                tokenString += '^(' + str(token.power) + ')'
        elif isinstance(token, Sqrt):
            tokenString += 'sqrt['
            if isinstance(token.power, Constant):
                tokenString += tokensToString([token.power])
            elif isinstance(token.power, Variable):
                tokenString += tokensToString([token.power])
            elif isinstance(token.power, Expression):
                tokenString += tokensToString(token.power.tokens)
            tokenString += ']('
            if isinstance(token.operand, Constant):
                tokenString += tokensToString([token.operand])
            elif isinstance(token.operand, Variable):
                tokenString += tokensToString([token.operand])
            elif isinstance(token.operand, Expression):
                tokenString += tokensToString(token.operand.tokens)

            tokenString += ')'
        elif isinstance(token, Logarithm):
            if token.coefficient == 1:
                pass
            elif token.coefficient == -1:
                tokenString += '-'
            else:
                tokenString += str(token.coefficient)
            if token.operand is not None:
                tokenString += token.value
                if token.power != 1:
                    tokenString += "^" + "(" + str(token.power) + ")"
                tokenString += "(" + tokensToString([token.operand]) + ")"

    return tokenString
