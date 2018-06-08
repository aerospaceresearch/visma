from visma.functions.structure import Expression
from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.functions.operator import Binary, Sqrt
from visma.functions.exponential import Logarithm
from visma.io.checks import isNumber


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
        eqLatex += token.__str__()
    return eqLatex


def tokensToString(tokens):
    token_string = ''
    for token in tokens:
        if isinstance(token, Constant):
            if isinstance(token.value, list):
                for j, val in token.value:
                    if token['power'][j] != 1:
                        token_string += (str(val) + '^(' + str(token.power[j]) + ') ')
                    else:
                        token_string += str(val)
            elif isNumber(token.value):
                if token.power != 1:
                    token_string += (str(token.value) + '^(' + str(token.power) + ') ')
                else:
                    token_string += str(token.value)
        elif isinstance(token, Variable):
            if token.coefficient == 1:
                pass
            elif token.coefficient == -1:
                token_string += ' -'
            else:
                token_string += str(token.coefficient)
            for j, val in enumerate(token.value):
                if token.power[j] != 1:
                    token_string += (str(val) + '^(' + str(token.power[j]) + ') ')
                else:
                    token_string += str(val)
        elif isinstance(token, Binary):
            token_string += ' ' + str(token.value) + ' '
        elif isinstance(token, Expression):
            token_string += ' ( '
            token_string += tokensToString(token.tokens)
            token_string += ' ) '
            if token.power != 1:
                token_string += '^(' + str(token.power) + ') '
        elif isinstance(token, Sqrt):
            token_string += 'sqrt['
            if isinstance(token.power, Constant):
                token_string += tokensToString([token.power])
            elif isinstance(token.power, Variable):
                token_string += tokensToString([token.power])
            elif isinstance(token.power, Expression):
                token_string += tokensToString(token.power.tokens)
            token_string += ']('
            if isinstance(token.expression, Constant):
                token_string += tokensToString([token.expression])
            elif isinstance(token.expression, Variable):
                token_string += tokensToString([token.expression])
            elif isinstance(token.expression, Expression):
                token_string += tokensToString(token.expression.tokens)

            token_string += ') '
        elif isinstance(token, Logarithm):
            if token.coefficient == 1:
                pass
            elif token.coefficient == -1:
                token_string += ' -'
            else:
                token_string += str(token.coefficient)
            if token.operand is not None:
                for eachOperand in token.operand:
                    token_string += token.value
                    if token.power != 1:
                        token_string += "^" + "(" + str(token.power) + ")"
                    token_string += "(" + tokensToString([eachOperand]) + ")"

    return token_string
