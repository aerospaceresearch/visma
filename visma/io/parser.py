from visma.functions.structure import Expression
from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.functions.operator import Binary, Sqrt
from visma.functions.exponential import Logarithm
from visma.io.checks import isNumber, mathError
from visma.matrix.structure import Matrix


def resultLatex(operation, equations, comments, wrtVar=None):
    """Converts tokens to LaTeX format for displaying in step-by-step solution figure

    Arguments:
        operation {string} -- operation performed on input
        equations {list} -- list of tokens list
        comments {list} -- list of comments

    Keyword Arguments:
        wrtVar {string} -- with respect to variable (default: {None})

    Returns:
        finalSteps {string} -- final result in LaTeX
    """

    equationLatex = []
    for eqTokens in equations:
        equationLatex.append(tokensToLatex(eqTokens))

    finalSteps = "INPUT: " + r"$" + equationLatex[0] + r"$" + "\n"
    finalSteps += "OPERATION: " + operation
    if wrtVar is not None:
        finalSteps += " with respect to " + r"$" + wrtVar + r"$"
    finalSteps += "\n"
    finalSteps += "OUTPUT: " + r"$" + equationLatex[-1] + r"$" + "\n"*2

    for i, _ in enumerate(equationLatex):
        if comments[i] != []:
            finalSteps += str(comments[i][0]) + "\n"
        finalSteps += r"$" + equationLatex[i] + r"$" + "\n"*2

    return finalSteps


def resultStringCLI(equationTokens, operation, comments, solutionType, simul):
    """Converts tokens to final string format for displaying in terminal in CLI

    Arguments:
        equationTokens {list} -- list of animations or step by step tokens
        operation {string} -- operation performed on input
        comments {list} -- list of comments
        solutionType {string} -- type of solution expression/equation
        simul{bool} -- True indicates user has entered simultaneous equation

    Returns:
        finalSteps {string} -- final result to be displayed in CLI
    """

    equationString = []
    for x in equationTokens:
        equationString.append(tokensToString(x))

    commentsString = []
    for x in comments:
        if not x:
            commentsString.append([])
        else:
            for y in x:
                commentsString.append([y.translate({ord(c): None for c in '${\}'})])

    finalSteps = ''
    finalSteps = 'INPUT: ' + equationString[0] + '\n'
    finalSteps += 'OPERATION: ' + operation + '\n'
    finalSteps += 'OUTPUT: ' + equationString[-1] + 2*'\n'
    finalSteps += 'STEP-BY-STEP SOLUTION: ' + '\n'

    for i, _ in enumerate(equationString):
        if comments[i] != [] and equationString[i] != '':
            finalSteps += '(' + str(commentsString[i][0]) + ')' + '\n'
            finalSteps += equationString[i] + 2*"\n"
        elif comments[i] != [] and equationString[i] == '':
            finalSteps += '\n' + '[' + str(commentsString[i][0]) + ']' + '\n'
        elif comments[i] == [] and equationString[i] != '':
            finalSteps += '\n' + equationString[i] + 2*'\n'

    if mathError(equationTokens[-1]) and (not simul):
        finalSteps += 'Math Error: LHS not equal to RHS' + "\n"

    return finalSteps


def tokensToLatex(eqTokens):
    """Converts tokens to LaTeX string

    Arguments:
        eqTokens {list} -- list of function tokens

    Returns:
        eqLatex {string} -- equation string in LaTeX
    """
    eqLatex = ""
    for token in eqTokens:
        eqLatex += token.__str__()
    return eqLatex


def latexToTerms(terms):

    for index, term in enumerate(terms):
        if term == 'frac':
            terms.remove(terms[index])
            if index < len(terms):
                terms.remove(terms[index])
                j = index
                while j < len(terms) and terms[j] != '}':
                    j += 1
                if j < len(terms):
                    terms.remove(terms[j])
                    terms.insert(j, '/')
                if j+1 < len(terms):
                    terms.remove(terms[j+1])
                while j < len(terms) and terms[j] != '}':
                    j += 1
                if j < len(terms):
                    terms.remove(terms[j])

    return terms


def tokensToString(tokens):
    """Converts tokens to text string

    Arguments:
        tokens {list} -- list of function tokens

    Returns:
        tokenString {string} -- equation string
    """
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
        elif isinstance(token, Matrix):
            tokenString += "["
            for i in range(token.dim[0]):
                for j in range(token.dim[1]):
                    tokenString += tokensToString(token.value[i][j])
                    tokenString += ","
                tokenString = tokenString[:-1] + ";"
            tokenString = tokenString[:-1] + "]"

    return tokenString
