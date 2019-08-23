"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors:
Owner: AerospaceResearch.net
About: This module's basic purpose is to be able to tokenize every possible input given by the user into a consistent key-value pair format for each equation/expression. Redundant data has been provided with the tokens on purpose, to make the job of future developers easier.
Still far from perfect and requires a bit of clean up.
Note: Please try to maintain proper documentation
-1 -> power
-2 -> value
-3 -> sqrt expression
-4 -> sqrt power
Logic Description:
"""

import math
import copy
from visma.io.checks import isNumber, isVariable, getNumber, checkEquation, funcs, funcSyms
from visma.functions.structure import Function, Equation, Expression
from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.functions.exponential import Logarithm, NaturalLog, Exponential
from visma.functions.hyperbolic import Sinh, Cosh, Tanh, ArcSinh, ArcCosh, ArcTanh
from visma.functions.trigonometry import Sine, Cosine, Tangent, Cotangent, Cosecant, Secant, ArcSin, ArcCos, ArcTan
from visma.functions.operator import Binary, Sqrt
from visma.matrix.structure import Matrix
from visma.matrix.checks import isMatrix
from visma.io.parser import latexToTerms
# from visma.gui import logger

symbols = ['+', '-', '*', '/', '(', ')', '{', '}', '[', ']', '^', '=', '<', '>', '<=', '>=', ',', ';', '$']
greek = [u'\u03B1', u'\u03B2', u'\u03B3']
constants = [u'\u03C0', 'e', 'i']

funcFourLetters = ["sinh", "sqrt", "sech", "csch", "cosh", "coth", "frac", "iota", "tanh", "log_"]
funcThreeLetters = ["tan", "sin", "cos", "sec", "log", "exp", "csc", "cot"]
funcTwoLetters = ["ln", "pi"]

# TODO: Add module for different inputs(ex: LaTeX)
inputLaTeX = ['\\times', '\\div', '+', '-', '=', '^', '\\sqrt']
inputGreek = ['*', '/', '+', '-', '=', '^', 'sqrt']

funcTokens = [Logarithm(), Logarithm(), NaturalLog(), Exponential(), Sine(), Cosine(), Tangent(), Cosecant(), Secant(), Cotangent(), ArcSin(), ArcCos(), ArcTan(), Sinh(), Cosh(), Tanh(), ArcSinh(), ArcCosh(), ArcTanh()]


def removeSpaces(eqn):
    """Gets rid of whitespaces from the input equation

    Arguments:
        eqn {string} -- input equation string

    Returns:
        cleanEqn {string} -- equation string without spaces
    """
    cleanEqn = ''.join(i for i in eqn.split())
    return cleanEqn


def getTerms(eqn):
    """Separate terms of the input equation into a list

    Arguments:
        eqn {string} -- equation string

    Returns:
        terms {list} -- list of terms{strings}
    """
    x = 0
    terms = []
    while x < len(eqn):

        if ('a' <= eqn[x] <= 'z') or ('A' <= eqn[x] <= 'Z') or eqn[x] in greek:

            buf = eqn[x]
            if x + 3 < len(eqn):
                for i in range(1, 4):
                    buf += eqn[x+i]
            if len(buf) == 4:
                if buf in funcFourLetters:
                    terms.append(buf)
                    x += 4
                    continue

            buf = eqn[x]
            if x + 2 < len(eqn):
                for i in range(1, 3):
                    buf += eqn[x + i]
            if len(buf) == 3:
                if buf in funcThreeLetters:
                    terms.append(buf)
                    x += 3
                    continue

            buf = eqn[x]
            if x + 1 < len(eqn):
                buf += eqn[x + 1]
            if len(buf) == 2:
                if buf in funcTwoLetters:
                    terms.append(buf)
                    x += 2
                    continue

            if eqn[x] == 'e':   # Special Cases: e , i
                terms.append("exp")
                x += 1
                continue
            elif eqn[x] == 'i':
                terms.append("iota")
                x += 1
                continue

            terms.append(eqn[x])
            x += 1

        elif '0' <= eqn[x] <= '9':
            buf = eqn[x]
            x += 1
            while x < len(eqn):
                if '0' <= eqn[x] <= '9' or eqn[x] == '.':
                    buf += eqn[x]
                    x += 1
                else:
                    break
            terms.append(buf)

        elif eqn[x] in symbols:
            if eqn[x] == '<':
                i = x
                buf = eqn[x]
                while (i - x) < len("="):
                    i += 1
                    if i < len(eqn):
                        buf += eqn[i]
                if buf == '<=':
                    terms.append(buf)
                    x = i + 1
                    continue
                terms.append(eqn[x])
            elif eqn[x] == '>':
                i = x
                buf = eqn[x]
                while (i - x) < len("="):
                    i += 1
                    if i < len(eqn):
                        buf += eqn[i]
                if buf == '>=':
                    terms.append(buf)
                    x = i + 1
                    continue
                terms.append(eqn[x])
            else:
                terms.append(eqn[x])
            x += 1
        else:
            x += 1
    return terms


def normalize(terms):
    """Replace input terms of LaTeX to Greek

    Arguments:
        terms {list} -- LaTeX/Greek input terms

    Returns:
        terms {list} -- Greek input terms
    """
    for term in terms:
        for i, x in enumerate(inputLaTeX):
            if x == term:
                term = inputGreek[i]

    terms = latexToTerms(terms)

    return terms


def tokenizeSymbols(terms):
    """Assigns a token symbol to some items in terms list

    Arguments:
        terms {list} -- input terms

    Returns:
        symTokens {list} -- symbol tokens for input terms
    """

    symTokens = []
    for i, term in enumerate(terms):
        symTokens.append('')
        if term in symbols:
            if term == '^':
                if i + 1 < len(terms) and not isVariable(terms[i - 1]):
                    symTokens[-1] = 'Binary'
                else:
                    symTokens[-1] = False
            elif term == '*' or term == '/':
                if i + 1 < len(terms):
                    if (isVariable(terms[i - 1]) or isNumber(terms[i - 1]) or terms[i - 1] == ')' or terms[i - 1] == ']') and (isVariable(terms[i + 1]) or isNumber(terms[i + 1]) or terms[i + 1] == '(' or terms[i + 1] == '[' or ((terms[i + 1] == '-' or terms[i + 1] == '+') and (isVariable(terms[i + 2]) or isNumber(terms[i + 2])))):
                        symTokens[-1] = 'Binary'
                    else:
                        symTokens[-1] = False
                else:
                    symTokens[-1] = False
            elif term == '+' or term == '-':
                if i == 0:
                    symTokens[-1] = 'Unary'
                elif terms[i - 1] in ['-', '+', '*', '/', '=', '<', '>', '<=', '>=', '^', '(', '[', ',', ';']:
                    symTokens[-1] = 'Unary'
                elif i + 1 < len(terms):
                    if (isVariable(terms[i - 1]) or isNumber(terms[i - 1]) or terms[i - 1] == ')' or terms[i - 1] == ']') and (isVariable(terms[i + 1]) or isNumber(terms[i + 1]) or terms[i + 1] == '(' or terms[i + 1] == '[' or terms[i + 1] in funcs or ((terms[i + 1] == '-' or terms[i + 1] == '+') and (isVariable(terms[i + 2]) or isNumber(terms[i + 2]) or terms[i + 2] in funcs))):
                        symTokens[-1] = 'Binary'
                    else:
                        symTokens[-1] = False
                else:
                    symTokens[-1] = False
                    # print(terms[i - 1], terms[i], isNumber(terms[i + 1]))
            elif term in ['=', '<', '>', '<=', '>=']:
                symTokens[-1] = 'Binary'
        elif term in funcs:
            symTokens[-1] = funcSyms[funcs.index(term)]
    return symTokens


def removeUnary(terms, symTokens):
    """Removes unary tokens from terms

    Example:
        -x --> ['-', 'x']
        after removeUnary -x --> ['-x']

    Arguments:
        terms {list} -- input terms
        symTokens {list} -- symbol tokens for terms

    Returns:
        terms {list} -- input terms
        symTokens {list} -- symbol tokens for terms
    """
    for i, symToken in enumerate(symTokens):
        if symToken == 'Unary':
            if i + 1 < len(terms):
                if isNumber(terms[i + 1]):
                    if terms[i] == '-':
                        terms[i + 1] = terms[i] + terms[i + 1]
                    terms.pop(i)
                    symTokens.pop(i)
                elif isVariable(terms[i + 1]):
                    terms[i] = terms[i] + '1'
                    symTokens[i] = ''
    return terms, symTokens


def getVariable(terms, symTokens, scope, coeff=1):

    variable = Variable()
    value = []
    coefficient = coeff
    power = []
    x = 0
    level = 0
    while x < len(terms):
        if isVariable(terms[x]):
            if terms[x] in value:
                for i, term in enumerate(value):
                    if term == terms[x]:
                        power[i] += 1
            else:
                value.append(terms[x])
                power.append(1)
            level += 1
            x += 1
        elif isNumber(terms[x]):
            if x + 1 < len(terms) and terms[x + 1] != '^':
                coefficient *= getNumber(terms[x])
            else:
                value.append(getNumber(terms[x]))
                power.append(1)
            level += 1
            x += 1
        elif symTokens[x] == 'Unary':
            if terms[x] == '-':
                coefficient *= -1
            x += 1
        elif terms[x] == '^':
            x += 1
            if x < len(terms):
                if terms[x] == '(':
                    x += 1
                    binary = 0
                    nSqrt = 0
                    varTerms = []
                    varSymTokens = []
                    brackets = 0
                    while x < len(terms):
                        if terms[x] != ')' or brackets != 0:
                            if symTokens[x] == 'Binary':
                                if brackets == 0:
                                    binary += 1
                            elif terms[x] == '(':
                                brackets += 1
                            elif terms[x] == ')':
                                brackets -= 1
                            elif symTokens[x] == 'Sqrt':
                                if brackets == 0:
                                    nSqrt += 1
                            varTerms.append(terms[x])
                            varSymTokens.append(symTokens[x])
                            x += 1
                        else:
                            break
                    if x + 1 < len(terms) and terms[x + 1] == '^':
                        x += 2
                        binary2 = 0
                        nSqrt2 = 0
                        brackets2 = 0
                        varSymTokens2 = []
                        varTerms2 = []
                        power2 = []
                        while x < len(terms):
                            if symTokens[x] != 'Binary' or brackets != 0:
                                if symTokens[x] == 'Binary':
                                    if brackets2 == 0:
                                        binary2 += 1
                                elif terms[x] == '(':
                                    brackets2 += 1
                                elif terms[x] == ')':
                                    brackets2 -= 1
                                elif symTokens[x] == 'Sqrt':
                                    if nSqrt2 == 0:
                                        nSqrt2 += 1
                                varTerms2.append(terms[x])
                                varSymTokens2.append(symTokens[x])
                                x += 1
                            else:
                                break
                        if len(varTerms2) == 1:
                            if isVariable(terms[x - 1]):
                                variable = Variable()
                                variable.value = [terms[x - 1]]
                                variable.power = [1]
                                variable.coefficient = 1
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tempScope.append(-1)
                                variable.scope = tempScope
                                power2.append(variable)
                            elif isNumber(terms[x - 1]):
                                variable = Constant()
                                variable.value = getNumber(terms[x - 1])
                                variable.power = 1
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tempScope.append(-1)
                                variable.scope = tempScope
                                power2.append(variable)
                        else:
                            if binary2 == 0 and nSqrt2 == 0:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tempScope.append(-1)
                                power2.append(getVariable(varTerms2, varSymTokens2, tempScope))
                            else:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tempScope.append(-1)
                                power2.append(getToken(varTerms2, varSymTokens2, tempScope))
                        if len(varTerms) == 1:
                            if isVariable(varTerms[-1]):
                                variable = Variable()
                                variable.value = [varTerms[-1]]
                                variable.power = power2
                                variable.coefficient = coeff
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                variable.scope = tempScope
                                power[-1] = variable
                            elif isNumber(varTerms[-1]):
                                variable = Constant()
                                variable.value = getNumber(varTerms[-1])
                                variable.power = power2
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                variable.scope = tempScope
                                power[-1] = variable
                        else:
                            if binary == 0 and nSqrt == 0:
                                variable = Variable()
                                variable.power = power2
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                variable.value = getVariable(varTerms, varSymTokens, tempScope)
                                variable.coefficient = 1
                                power[-1] = variable
                            else:
                                variable = Equation()
                                variable.power = power2
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                variable.value = getToken(varTerms, varSymTokens, tempScope)
                                variable.coefficient = 1
                                power[-1] = variable
                    else:
                        if len(varTerms) == 1:
                            if isVariable(varTerms[0]):
                                power[-1] = varTerms[0]
                            elif isNumber(varTerms[0]):
                                power[-1] *= getNumber(varTerms[0])
                        else:
                            if binary == 0 and nSqrt == 0:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                power[-1] = getVariable(varTerms, varSymTokens, tempScope)
                            else:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                power[-1] = getToken(varTerms, varSymTokens, tempScope)
                    x += 1
                elif isVariable(terms[x]) or isNumber(terms[x]):
                    if x + 1 < len(terms):
                        if terms[x + 1] == '^' or isNumber(terms[x]) or isVariable(terms[x]):
                            varTerms = []
                            varSymTokens = []
                            brackets = 0
                            nSqrt = 0
                            binary = 0
                            while x < len(terms):
                                if symTokens[x] != 'Binary' or brackets != 0:
                                    if terms[x] == '(':
                                        brackets += 1
                                    elif terms[x] == ')':
                                        brackets -= 1
                                    elif symTokens[x] == 'Binary':
                                        if brackets == 0:
                                            binary += 1
                                    elif symTokens[x] == 'Sqrt':
                                        if brackets == 0:
                                            nSqrt += 1
                                    varTerms.append(terms[x])
                                    varSymTokens.append(symTokens[x])
                                    x += 1
                                else:
                                    break
                            if binary != 0 or nSqrt != 0:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                power[-1] = getToken(varTerms, varSymTokens, tempScope)
                            else:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                power[-1] = getVariable(varTerms, varSymTokens, tempScope)

                        else:
                            if isNumber(terms[x]):
                                power[-1] = getNumber(terms[x])
                            else:
                                power[-1] = terms[x]
                            x += 1
                    else:
                        if isNumber(terms[x]):
                            power[-1] = getNumber(terms[x])
                        else:
                            power[-1] = terms[x]
                        x += 1
                elif symTokens[x] == 'Unary':
                    coeff = 1
                    if terms[x] == '-':
                        coeff = -1
                    x += 1
                    if terms[x] == '(':
                        x += 1
                        binary = 0
                        varTerms = []
                        varSymTokens = []
                        brackets = 0
                        nSqrt = 0
                        while x < len(terms):
                            if terms[x] != ')' or brackets != 0:
                                if symTokens[x] == 'Binary':
                                    if brackets == 0:
                                        binary += 1
                                if terms[x] == '(':
                                    brackets += 1
                                elif terms[x] == ')':
                                    brackets -= 1
                                elif symTokens[x] == 'Sqrt':
                                    if brackets == 0:
                                        nSqrt += 1
                                varTerms.append(terms[x])
                                varSymTokens.append(symTokens[x])
                                x += 1
                            else:
                                break
                        if x + 1 < len(terms):
                            if terms[x + 1] == '^':
                                x += 2
                                binary2 = 0
                                nSqrt2 = 0
                                brackets2 = 0
                                varSymTokens2 = []
                                varTerms2 = []
                                power2 = []
                                while x < len(terms):
                                    if symTokens[x] != 'Binary' or brackets != 0:
                                        if symTokens[x] == 'Binary':
                                            if brackets2 == 0:
                                                binary2 += 1
                                        elif terms[x] == '(':
                                            brackets2 += 1
                                        elif terms[x] == ')':
                                            brackets2 -= 1
                                        elif symTokens[x] == 'Sqrt':
                                            if nSqrt2 == 0:
                                                nSqrt2 += 1
                                        varTerms2.append(terms[x])
                                        varSymTokens2.append(symTokens[x])
                                        x += 1
                                    else:
                                        break
                                if len(varTerms2) == 1:
                                    if isVariable(terms[x - 1]):
                                        variable = Variable()
                                        variable.value = terms[x - 1]
                                        variable.power = [1]
                                        variable.coefficient = 1
                                        tempScope = []
                                        tempScope.extend(scope)
                                        tempScope.append(level)
                                        tempScope.append(-1)
                                        variable.scope = tempScope
                                        power2.append(variable)
                                    elif isNumber(terms[x - 1]):
                                        variable = Constant()
                                        variable.value = getNumber(terms[x - 1])
                                        variable.power = 1
                                        tempScope = []
                                        tempScope.extend(scope)
                                        tempScope.append(level)
                                        tempScope.append(-1)
                                        variable.scope = tempScope
                                        power2.append(variable)
                                else:
                                    if binary2 == 0 and nSqrt2 == 0:
                                        tempScope = []
                                        tempScope.extend(scope)
                                        tempScope.append(level)
                                        tempScope.append(-1)
                                        power2.append(getVariable(
                                            varTerms2, varSymTokens2, tempScope))
                                    else:
                                        tempScope = []
                                        tempScope.extend(scope)
                                        tempScope.append(level)
                                        tempScope.append(-1)
                                        power2.append(
                                            getToken(varTerms2, varSymTokens2, tempScope))
                                if len(varTerms) == 1:
                                    if isVariable(varTerms[-1]):
                                        variable = Variable()
                                        variable.value = [varTerms[-1]]
                                        variable.power = power2
                                        variable.coefficient = coeff
                                        power[-1] = variable
                                    elif isNumber(varTerms[-1]):
                                        variable = Constant()
                                        variable.value = coeff * \
                                            getNumber(varTerms[-1])
                                        variable.power = power2
                                        power[-1] = variable
                                else:
                                    if binary == 0 and nSqrt == 0:
                                        variable = Variable()
                                        variable.power = power2
                                        tempScope = []
                                        tempScope.extend(scope)
                                        tempScope.append(level)
                                        variable.value = getVariable(varTerms, varSymTokens, tempScope)
                                        variable.coefficient = coeff
                                        power[-1] = variable
                                    else:
                                        variable = Equation()
                                        variable.power = power2
                                        tempScope = []
                                        tempScope.extend(scope)
                                        tempScope.append(level)
                                        variable.value = getToken(varTerms, varSymTokens, tempScope)
                                        variable.coefficient = coeff
                                        variable.type = "equation"
                                        power[-1] = variable
                            else:
                                if len(varTerms) == 1:
                                    if isVariable(terms[x - 1]):
                                        variable = Variable()
                                        variable.value = [terms[x - 1]]
                                        variable.power = power2
                                        variable.coefficient = coeff
                                        power[-1] = variable
                                    elif isNumber(terms[x - 1]):
                                        power[-1] *= (coeff * getNumber(terms[x - 1]))
                                else:
                                    if binary == 0 and nSqrt == 0:
                                        tempScope = []
                                        tempScope.extend(scope)
                                        tempScope.append(level)
                                        power[-1] = getVariable(varTerms, varSymTokens, tempScope, coeff)
                                    else:
                                        tempScope = []
                                        tempScope.extend(scope)
                                        tempScope.append(level)
                                        power[-1] = getToken(varTerms, varSymTokens, tempScope, coeff)

                        else:
                            if len(varTerms) == 1:
                                if isVariable(terms[x - 1]):
                                    variable = Variable()
                                    variable.value = [terms[x - 1]]
                                    variable.power = power2
                                    variable.coefficient = coeff
                                    power[-1] = variable
                                elif isNumber(terms[x - 1]):
                                    power[-1] *= (coeff * getNumber(terms[x - 1]))
                            else:
                                if binary == 0 and nSqrt == 0:
                                    tempScope = []
                                    tempScope.extend(scope)
                                    tempScope.append(level)
                                    power[-1] = getVariable(varTerms, varSymTokens, tempScope, coeff)
                                else:
                                    tempScope = []
                                    tempScope.extend(scope)
                                    tempScope.append(level)
                                    power[-1] = getToken(varTerms, varSymTokens, tempScope, coeff)
                        x += 1

                    elif isVariable(terms[x]) or isNumber(terms[x]):

                        if x + 1 < len(terms):
                            if terms[x + 1] == '^' or isNumber(terms[x]) or isVariable(terms[x]):
                                varTerms = []
                                varSymTokens = []
                                brackets = 0
                                binary = 0
                                nSqrt = 0
                                while x < len(terms):
                                    if symTokens[x] != 'Binary' or brackets != 0:
                                        if terms[x] == '(':
                                            brackets += 1
                                        elif terms[x] == ')':
                                            brackets -= 1
                                        elif symTokens[x] == 'Binary':
                                            if brackets == 0:
                                                binary += 1
                                        elif symTokens[x] == 'Sqrt':
                                            if brackets == 0:
                                                nSqrt += 1
                                        varTerms.append(terms[x])
                                        varSymTokens.append(symTokens[x])
                                        x += 1
                                    else:
                                        break
                                if binary != 0 or nSqrt != 0:
                                    tempScope = []
                                    tempScope.extend(scope)
                                    tempScope.append(level)
                                    power[-1] = getToken(varTerms, varSymTokens, tempScope, coeff)
                                else:
                                    tempScope = []
                                    tempScope.extend(scope)
                                    tempScope.append(level)
                                    power[-1] = getVariable(varTerms, varSymTokens, tempScope, coeff)

                            else:
                                if isNumber(terms[x]):
                                    power[-1] = getNumber(terms[x])
                                else:
                                    power[-1] = terms[x]
                                x += 1
                        else:
                            if isNumber(terms[x]):
                                power[-1] = getNumber(terms[x])
                            else:
                                power[-1] = terms[x]
                            x += 1
    variable.scope = scope
    variable.value = value
    variable.power = power
    variable.coefficient = coefficient
    return variable


def getToken(terms, symTokens, scope=None, coeff=1):
    """Returns equation tokens for the given input terms and symtokens

    Arguments:
        terms {list} -- equation terms
        symTokens {list} -- symtoken for terms

    Keyword Arguments:
        scope {int} -- token scope (default: {None})
        coeff {int} -- coefficient (default: {1})

    Returns:
        eqn {list} -- equation tokens list
    """
    if scope is None:
        scope = []
    eqn = Expression()
    tokens = []
    x = 0
    level = 0
    while x < len(terms):
        if terms[x] == '$':
            symTokens.pop(x)
            terms.pop(x)
            symTokens.pop()
            terms.pop()
        if isVariable(terms[x]) and symTokens[x] not in funcSyms:
            varTerms = []
            varSymTokens = []
            brackets = 0
            nSqrt = 0
            binary = 0
            while x < len(terms) and (symTokens[x] != 'Binary' or brackets != 0) and terms[x] != ',':
                if terms[x] == '(':
                    brackets += 1
                elif terms[x] == ')':
                    brackets -= 1
                elif symTokens[x] == 'Sqrt':
                    if brackets == 0:
                        nSqrt += 1
                varTerms.append(terms[x])
                varSymTokens.append(symTokens[x])
                x += 1
            x -= 1
            tempScope = []
            tempScope.extend(scope)
            tempScope.append(level)
            if nSqrt != 0:
                termToken = getToken(varTerms, varSymTokens, tempScope)
            else:
                termToken = getVariable(varTerms, varSymTokens, tempScope)
            level += 1
            tokens.append(termToken)
        elif isNumber(terms[x]):
            if x + 1 < len(terms) and (terms[x + 1] == '^' or isVariable(terms[x + 1])):
                varTerms = []
                brackets = 0
                nSqrt = 0
                varSymTokens = []
                while x < len(terms):
                    if symTokens[x] != 'Binary' or brackets != 0:
                        if terms[x] == ')':
                            brackets += 1
                        elif terms[x] == '(':
                            brackets -= 1
                        elif symTokens == 'Sqrt':
                            nSqrt += 1
                        varTerms.append(terms[x])
                        varSymTokens.append(symTokens[x])
                    else:
                        break
                    x += 1
                x -= 1
                if nSqrt != 0:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    termToken = getToken(varTerms, varSymTokens, tempScope)
                else:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    termToken = getVariable(
                        varTerms, varSymTokens, tempScope)
                level += 1
                tokens.append(termToken)
            else:
                termToken = Constant()
                tempScope = []
                tempScope.extend(scope)
                tempScope.append(level)
                termToken.scope = tempScope
                termToken.power = 1
                termToken.value = getNumber(terms[x])
                level += 1
                tokens.append(termToken)
        elif symTokens[x] == 'Binary':
            operator = Binary()
            operator.value = terms[x]
            tempScope = []
            tempScope.extend(scope)
            tempScope.append(level)
            operator.scope = tempScope
            level += 1
            tokens.append(operator)
        elif terms[x] == '(':
            x += 1
            binary = 0
            varTerms = []
            varSymTokens = []
            brackets = 0
            nSqrt = 0
            while x < len(terms) and (brackets != 0 or terms[x] != ')'):
                if symTokens[x] == 'Binary':
                    if brackets == 0:
                        binary += 1
                if terms[x] == '(':
                    brackets += 1
                elif terms[x] == ')':
                    brackets -= 1
                elif symTokens[x] == 'Sqrt':
                    if brackets == 0:
                        nSqrt += 1
                varTerms.append(terms[x])
                varSymTokens.append(symTokens[x])
                x += 1
            expression = Expression(getToken(varTerms, varSymTokens).tokens)
            if len(expression.tokens) == 1:
                expression = expression.tokens[0]
            # TODO: Add code for case ()^()
            level += 1
            if tokens != []:
                if isinstance(tokens[-1], Function) and not isinstance(tokens[-1], Variable) and not isinstance(tokens[-1], Constant):
                    tokens[-1].operand = expression
                else:
                    tokens.append(expression)
            else:
                tokens.append(expression)
        elif terms[x] == '[':
            x += 1
            matrixTok = Matrix()
            while x < len(terms) and terms[x] != ']':
                rowToks = []
                while x < len(terms) and terms[x] != ';' and terms[x] != ']':
                    eleTerms = []
                    eleSymTokens = []
                    while x < len(terms) and terms[x] != ',' and terms[x] != ';' and terms[x] != ']':
                        eleTerms.append(terms[x])
                        eleSymTokens.append(symTokens[x])
                        x += 1
                    eleToks = getToken(eleTerms, eleSymTokens)
                    rowToks.append(eleToks.tokens)
                    if terms[x] != ']' and terms[x] != ';':
                        x += 1
                matrixTok.value.append(rowToks)
                if terms[x] != ']':
                    x += 1
            if isMatrix(matrixTok):
                tokens.append(matrixTok)
            else:
                pass
                # logger.error('Invalid Matrix')
        elif symTokens[x] == 'Unary':
            coeff = 1
            if terms[x] == '-':
                coeff *= -1
            x += 1
            if terms[x] == '(':
                x += 1
                binary = 0
                varTerms = []
                varSymTokens = []
                brackets = 0
                nSqrt = 0
                while x < len(terms):
                    if terms[x] != ')' or brackets != 0:
                        if symTokens[x] == 'Binary':
                            if brackets == 0:
                                binary += 1
                        if terms[x] == '(':
                            brackets += 1
                        elif terms[x] == ')':
                            brackets -= 1
                        elif symTokens[x] == 'Sqrt':
                            if brackets == 0:
                                nSqrt += 1
                        varTerms.append(terms[x])
                        varSymTokens.append(symTokens[x])
                        x += 1
                    else:
                        break
                if x + 1 < len(terms):
                    if terms[x + 1] == '^':
                        x += 2
                        binary2 = 0
                        nSqrt2 = 0
                        brackets2 = 0
                        varSymTokens2 = []
                        varTerms2 = []
                        power2 = []
                        while x < len(terms):
                            if symTokens[x] != 'Binary' or brackets != 0:
                                if symTokens[x] == 'Binary':
                                    if brackets2 == 0:
                                        binary2 += 1
                                elif terms[x] == '(':
                                    brackets2 += 1
                                elif terms[x] == ')':
                                    brackets2 -= 1
                                elif symTokens[x] == 'Sqrt':
                                    if nSqrt2 == 0:
                                        nSqrt2 += 1
                                varTerms2.append(terms[x])
                                varSymTokens2.append(symTokens[x])
                                x += 1
                            else:
                                break
                        if len(varTerms2) == 1:
                            if isVariable(terms[x - 1]):
                                termToken = Variable
                                termToken.value = terms[x - 1]
                                termToken.power = [1]
                                termToken.coefficient = 1
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tempScope.append(-1)
                                termToken.scope = tempScope
                                power2.append(termToken)
                            elif isNumber(terms[x - 1]):
                                termToken = Constant()
                                termToken.value = getNumber(terms[x - 1])
                                termToken.power = 1
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tempScope.append(-1)
                                termToken.scope = tempScope
                                power2.append(termToken)
                        else:
                            if binary2 == 0 and nSqrt2 == 0:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tempScope.append(-1)
                                power2.append(getVariable(
                                    varTerms2, varSymTokens2, tempScope))
                            else:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tempScope.append(-1)
                                power2.append(
                                    getToken(varTerms2, varSymTokens2, tempScope))
                        if len(varTerms) == 1:
                            if isVariable(varTerms[-1]):
                                termToken = Variable()
                                termToken.value = [varTerms[-1]]
                                termToken.power = power2
                                termToken.coefficient = coeff
                                tokens.append(termToken)
                            elif isNumber(varTerms[-1]):
                                termToken = Constant
                                # CHECKME:
                                termToken.value = coeff * \
                                    getNumber(varTerms[-1])
                                termToken.power = power2
                                tokens.append(termToken)
                        else:
                            if binary == 0 and nSqrt == 0:
                                termToken = Variable()
                                termToken.power = power2
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                termToken.value = getVariable(
                                    varTerms, varSymTokens, tempScope)
                                termToken.coefficient = coeff
                                tokens.append(termToken)
                            else:
                                termToken = Expression()
                                termToken.power = power2
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                termToken.value = getToken(
                                    varTerms, varSymTokens, tempScope)
                                termToken.coefficient = coeff
                                tokens.append(termToken)
                    else:
                        if len(varTerms) == 1:
                            if isVariable(terms[x - 1]):
                                termToken = Variable()
                                termToken.value = [terms[x - 1]]
                                termToken.power = power2
                                termToken.coefficient = coeff
                                tokens.append(termToken)
                            elif isNumber(terms[x - 1]):
                                tokens.append(coeff * getNumber(terms[x - 1]))
                        else:
                            if binary == 0 and nSqrt == 0:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tokens.append(getVariable(
                                    varTerms, varSymTokens, tempScope,  coeff))
                            else:
                                tempScope = []
                                tempScope.extend(scope)
                                tempScope.append(level)
                                tokens.append(
                                    getToken(varTerms, varSymTokens, tempScope, coeff))

                else:
                    if len(varTerms) == 1:
                        if isVariable(terms[x - 1]):
                            termToken = Variable()
                            termToken.value = [terms[x - 1]]
                            termToken.power = power2
                            termToken.coefficient = coeff
                            tokens.append(termToken)
                        elif isNumber(terms[x - 1]):
                            tokens.append((coeff * getNumber(terms[x - 1])))
                    else:
                        if binary == 0 and nSqrt == 0:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tokens.append(getVariable(
                                varTerms, varSymTokens, tempScope, coeff))
                        else:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            tokens.append(
                                getToken(varTerms, varSymTokens, tempScope, coeff))
                x += 1
                level += 1
            elif isVariable(terms[x]):
                varTerms = []
                varSymTokens = []
                brackets = 0
                binary = 0
                nSqrt = 0
                while x < len(terms):
                    if symTokens[x] != 'Binary' or brackets != 0:
                        if terms[x] == '(':
                            brackets += 1
                        elif terms[x] == ')':
                            brackets -= 1
                        elif symTokens[x] == 'Sqrt':
                            nSqrt += 1
                        elif symTokens[x] == 'Binary':
                            if brackets == 0:
                                binary += 1
                        varTerms.append(terms[x])
                        varSymTokens.append(symTokens[x])
                        x += 1
                    else:
                        break
                x -= 1
                if nSqrt != 0 or binary != 0:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    termToken = getToken(
                        varTerms, varSymTokens, tempScope, coeff)
                else:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    termToken = getVariable(
                        varTerms, varSymTokens, tempScope, coeff)
                level += 1
                tokens.append(termToken)

            elif isNumber(terms[x]):
                if x + 1 < len(terms):
                    if terms[x + 1] == '^' or isVariable(terms[x + 1]):
                        varTerms = []
                        varSymTokens = []
                        brackets = 0
                        binary = 0
                        nSqrt = 0
                        while x < len(terms):
                            if symTokens[x] != 'Binary' or brackets != 0:
                                if terms[x] == ')':
                                    brackets += 1
                                elif terms[x] == '(':
                                    brackets -= 1
                                elif symTokens[x] == 'Sqrt':
                                    nSqrt += 1
                                elif symTokens[x] == 'Binary':
                                    if brackets == 0:
                                        binary += 1
                                varTerms.append(terms[x])
                                varSymTokens.append(symTokens[x])
                            else:
                                break
                            x += 1
                        x -= 1
                        if nSqrt != 0 or binary != 0:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            termToken = getToken(
                                varTerms, varSymTokens, tempScope, coeff)
                        else:
                            tempScope = []
                            tempScope.extend(scope)
                            tempScope.append(level)
                            termToken = getVariable(
                                varTerms, varSymTokens, tempScope, coeff)
                        level += 1
                        tokens.append(termToken)
                    else:
                        termToken = Constant()
                        termToken.value = coeff * getNumber(terms[x])
                        termToken.power = 1
                        tempScope = []
                        tempScope.extend(scope)
                        tempScope.append(level)
                        termToken.scope = tempScope
                        level += 1
                        tokens.append(termToken)
                else:
                    # SIMPLIFY:
                    termToken = Constant()
                    termToken.value = coeff * getNumber(terms[x])
                    termToken.power = 1
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    termToken.scope = tempScope
                    level += 1
                    tokens.append(termToken)
        elif symTokens[x] == 'Sqrt':
            x += 2
            binary = 0
            brackets = 0
            sqrBrackets = 0
            nSqrt = 0
            varTerms = []
            varSymTokens = []
            while x < len(terms):
                if terms[x] != ']' or sqrBrackets != 0 or brackets != 0:
                    if terms[x] == '(':
                        brackets += 1
                    elif terms[x] == ')':
                        brackets -= 1
                    elif symTokens[x] == 'Binary':
                        binary += 1
                    elif terms[x] == '[':
                        sqrBrackets += 1
                    elif terms[x] == ']':
                        sqrBrackets -= 1
                    elif symTokens[x] == 'Sqrt':
                        nSqrt += 1
                    varTerms.append(terms[x])
                    varSymTokens.append(symTokens[x])
                    x += 1
                else:
                    break
            operator = Sqrt()
            if len(varTerms) == 1:
                if isNumber(terms[x - 1]):
                    termToken = Constant()
                    termToken.value = getNumber(terms[x - 1])
                    termToken.power = 1
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(0)
                    termToken.scope = tempScope
                    operator.power = termToken
                elif isVariable(terms[x - 1]):
                    termToken = Variable()
                    termToken.value = [terms[x - 1]]
                    termToken.power = [1]
                    termToken.coefficient = 1
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(0)
                    termToken.scope = tempScope
                    operator.power = termToken
            else:
                if binary != 0 or nSqrt != 0:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(0)
                    operator.power = getToken(varTerms, varSymTokens, tempScope)
                else:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(0)
                    operator.power = getVariable(varTerms, varSymTokens, tempScope)
            x += 2

            binary = 0
            brackets = 0
            nSqrt = 0
            varTerms = []
            varSymTokens = []
            while x < len(terms):
                if terms[x] != ')' or brackets != 0:
                    if terms[x] == '(':
                        brackets += 1
                    elif terms[x] == ')':
                        brackets -= 1
                    elif symTokens[x] == 'Binary':
                        if brackets == 0:
                            binary += 1
                    elif symTokens[x] == 'Sqrt':
                        nSqrt += 1
                    varTerms.append(terms[x])
                    varSymTokens.append(symTokens[x])
                    x += 1
                else:
                    break
            if len(varTerms) == 1:
                if isNumber(terms[x - 1]):
                    termToken = Constant()
                    termToken.value = getNumber(terms[x - 1])
                    termToken.power = 1
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(1)
                    termToken.scope = tempScope
                    operator.tokens = termToken
                elif isVariable(terms[x - 1]):
                    termToken = Variable()
                    termToken.value = [terms[x - 1]]
                    termToken.power = [1]
                    termToken.coefficient = 1
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(1)
                    termToken.scope = tempScope
                    operator.tokens = termToken
            else:
                if binary == 0 and nSqrt == 0:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(1)
                    operator.tokens = getVariable(
                        varTerms, varSymTokens, tempScope)
                else:
                    tempScope = []
                    tempScope.extend(scope)
                    tempScope.append(level)
                    tempScope.append(1)
                    operator.tokens = getToken(
                        varTerms, varSymTokens, tempScope)
            level += 1
            tokens.append(operator)
        elif symTokens[x] in funcSyms:
            operator = copy.deepcopy(funcTokens[funcSyms.index(symTokens[x])])
            tokens.append(operator)
        x += 1
    eqn.scope = scope
    eqn.coefficient = coeff
    eqn.tokens = tokens
    return eqn


def preprocess(eqn):
    """Processes input equation string and returns equation tokens

    Arguments:
        eqn {string} -- input equation string

    Returns:
        tokens {list} -- equation tokens if valid input string
    """
    cleanEqn = removeSpaces(eqn)
    terms = getTerms(cleanEqn)
    normalizedTerms = normalize(terms)
    symTokens = tokenizeSymbols(normalizedTerms)
    normalizedTerms, symTokens = removeUnary(normalizedTerms, symTokens)
    if checkEquation(normalizedTerms, symTokens):
        tokens = getToken(normalizedTerms, symTokens)
        return tokens.tokens


def constantVariable(variable):

    constant = True

    for var in variable.value:
        if isinstance(var, Function):
            if isinstance(var, Expression):
                result, _ = constantConversion(var.tokens)
                if not result:
                    constant = False
            elif isinstance(var, Variable):
                if not constantVariable(var):
                    constant = False
        elif not isNumber(var):
            constant = False

    for p in variable.power:
        if isinstance(p, Function):
            if isinstance(p, Expression):
                result, _ = constantConversion(p.tokens)
                if not result:
                    constant = False
            elif isinstance(p, Variable):
                if not constantVariable(p):
                    constant = False
        elif not isNumber(p):
            constant = False

    return constant


def evaluateConstant(constant):
    """Returns constant value for a given visma.functions.Function or constant term

    Arguments:
        constant {visma.functions.Function/string} -- input term

    Returns:
       constant value -- value of input term
    """
    if isinstance(constant, Function):
        if isinstance(constant.value, list):
            val = 1
            if constant.coefficient is not None:
                val *= constant.coefficient
            for i, c_val in enumerate(constant.value):
                val *= math.pow(c_val, constant.power[i])
            return val
        elif isNumber(constant.value):
            return math.pow(constant.value[0], constant.power[0])
    elif isNumber(constant):
        return constant


def constantConversion(tokens):

    constantExpression = True
    for token in tokens:
        if isinstance(token, Variable):
            constant = True
            if not constantVariable(token):
                constant = False
                constantExpression = False
            if constant:
                token.__class__ = Constant
                token.value = evaluateConstant(token)
                token.power = 1

        elif isinstance(token, Binary):
            constantExpression = False

        elif isinstance(token, Expression):
            result, _ = constantConversion(token.tokens)
            if not result:
                constantExpression = False
    return constantExpression, tokens


def tokenizer(eqnString):
    """Generates tokens for input string

    Keyword Arguments:
        eqn {str} -- input equation string

    Returns:
        list -- function tokens list
    """
    _, tokens = constantConversion(preprocess(eqnString))
    return tokens


def changeToken(tokens, variables, scope_times=0):

    if len(variables) != 0:
        for changeVariable in variables:
            for token in tokens:
                if isinstance(token, Constant):
                    if token.scope == changeVariable.scope:
                        if changeVariable.coefficient is not None:
                            token.coefficient = changeVariable.coefficient
                        token.power = changeVariable.power
                        token.value = changeVariable.value
                        break
                elif isinstance(token, Variable):
                    if token.scope == changeVariable.scope:
                        token.coefficient = changeVariable.coefficient
                        token.power = changeVariable.power
                        token.value = changeVariable.value
                        break
                elif isinstance(token, Binary):
                    if token.scope == changeVariable.scope:
                        token.value = changeVariable.value
                elif isinstance(token, Expression):
                    if scope_times + 1 == len(changeVariable.scope):
                        if token.scope == changeVariable.scope:
                            break
                    elif token.scope == changeVariable.scope[0:(scope_times + 1)]:
                        token.tokens = changeToken(
                            token.tokens, token.scope, scope_times + 1)
                        break
    return tokens


def removeToken(tokens, scope, scope_times=0):
    """Removes a token given scope from tokens list

    Arguments:
        tokens {list} -- list of function tokens
        scope {int} -- scope number of token to be removed

    Keyword Arguments:
        scope_times {number} -- (default: {0})

    Returns:
        tokens {list} -- list of function tokens after removing token
    """
    for remScope in scope:
        for i, token in enumerate(tokens):
            if isinstance(token, Constant) or isinstance(token, Variable):
                if token.scope == remScope:
                    tokens.pop(i)
                    break
            elif isinstance(token, Binary):
                if token.scope == remScope:
                    tokens.pop(i)
                    break
            elif isinstance(token, Expression):
                if scope_times + 1 == len(remScope):
                    if token.scope == remScope:
                        tokens.pop(i)
                        break
                elif token.scope == remScope[0:(scope_times + 1)]:
                    token.tokens = removeToken(
                        token.tokens, scope, scope_times + 1)
                    break

    return tokens


def getLHSandRHS(tokens):
    """Returns LHS and RHS tokens

    Arguments:
        tokens {list} -- list of function tokens

    Returns:
        lhs {list} -- list of lhs function tokens
        rhs {list} -- list of rhs function tokens
        or
        bool -- False if not tokens list
    """
    lhs = []
    rhs = []
    eqn = False
    if not isinstance(tokens, list):
        return False, False
    for token in tokens:
        if isinstance(token, Binary):
            if token.value == '=':
                eqn = True
            elif not eqn:
                lhs.append(token)
            else:
                rhs.append(token)
        elif not eqn:
            lhs.append(token)
        else:
            rhs.append(token)
    return lhs, rhs


if __name__ == "__main__":
    pass
    # logger.setLevel = 0
    # logger.setLogName = 'tokenize'
    # print(getLHSandRHS(tokenizer('0.2x^(2.0)+ 7.0x - 34.0')))

# -xy^22^22^-z^{s+y}^22=sqrt[x+1]{x}
# x+y=2^-{x+y}
# x + 6.00 / 3 + 2 - 2x
# x^{1} - x^{-1}
