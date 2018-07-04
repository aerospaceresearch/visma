from visma.io.checks import findWRTVariable, areTokensEqual, isTokenInToken
from visma.io.tokenize import getTerms
from visma.functions.operator import Operator, Plus
from visma.functions.structure import Expression
from tests.tester import getTokens

#############
# io.checks #
#############


def test_findWRTVariable():

    varA = getTokens("x")
    assert findWRTVariable([varA]) == ['x']

    varB = getTokens("xy+ xy^2 +yz^3")
    assert findWRTVariable(varB) == ['x', 'y', 'z']


def test_areTokensEqual():

    varA = getTokens("3xy")
    varB = getTokens("3yx")
    varC = getTokens("3yz")
    assert areTokensEqual(varA, varB)
    assert not areTokensEqual(varA, varC)

    opA = Operator()
    opA.value = '+'
    opB = Plus()
    assert areTokensEqual(opA, opB)


def test_isTokenInToken():

    varA = getTokens("x^3")
    varB = getTokens("xy^2")
    varC = Expression(getTokens("1 + w + x"))
    varD = Expression(getTokens("w + y"))
    assert isTokenInToken(varA, varB)
    assert isTokenInToken(varA, varC)
    assert not isTokenInToken(varA, varD)

    varA = getTokens("xy^2")
    varB = getTokens("x^(2)y^(4)z")
    varC = getTokens("yx^0.5")
    varD = getTokens("xy^(3)z")
    varE = getTokens("2")
    assert isTokenInToken(varA, varB)
    assert isTokenInToken(varA, varC)
    assert not isTokenInToken(varA, varD)
    assert not isTokenInToken(varA, varE)


#############
# io.parser #
#############


###############
# io.tokenize #
###############


def test_getTerms():

    assert getTerms("1 + 2 * 3 - sqrt(2) / 5") == ['1', '+', '2', '*', '3', '-', 'sqrt', '(', '2', ')', '/', '5']
    assert getTerms("x + x^2*y + y^2 + y/z = -z") == ['x', '+', 'x', '^', '2', '*', 'y', '+', 'y', '^', '2', '+', 'y', '/', 'z', '=', '-', 'z']

    assert getTerms("sin^2(x) + cos^2(x) = 1") == ['sin', '^', '2', '(', 'x', ')', '+', 'cos', '^', '2', '(', 'x', ')', '=', '1']
    assert getTerms("1 + tan^2(x) = sec^2(x)") == ['1', '+', 'tan', '^', '2', '(', 'x', ')', '=', 'sec', '^', '2', '(', 'x', ')']
    assert getTerms("1 + cot^2(x) = csc^2(x)") == ['1', '+', 'cot', '^', '2', '(', 'x', ')', '=', 'csc', '^', '2', '(', 'x', ')']

    assert getTerms("cosh^2(x)-sinh^2(x)=1") == ['cosh', '^', '2', '(', 'x', ')', '-', 'sinh', '^', '2', '(', 'x', ')', '=', '1']
    assert getTerms("1 - tanh^2(x) = sech^2(x)") == ['1', '-', 'tanh', '^', '2', '(', 'x', ')', '=', 'sech', '^', '2', '(', 'x', ')']
    assert getTerms("coth^2(x)-csch^2(x)=1") == ['cot', 'h', '^', '2', '(', 'x', ')', '-', 'csch', '^', '2', '(', 'x', ')', '=', '1']

    assert getTerms("e = 2.71828") == ['exp', '=', '2.71828']
    assert getTerms("log(e) = 1") == ['log', '(', 'exp', ')', '=', '1']
    assert getTerms("e^(i*pi)=1") == ['exp', '^', '(', 'iota', '*', 'pi', ')', '=', '1']
