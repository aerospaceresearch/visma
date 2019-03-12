from visma.io.checks import getVariables, areTokensEqual, isTokenInToken, checkSyntax
from visma.io.parser import tokensToString
from visma.io.tokenize import getTerms, normalize
from visma.functions.operator import Operator, Plus
from visma.functions.structure import Expression
from tests.tester import getTokens

#############
# io.checks #
#############


def test_getVariables():

    varA = getTokens("x")
    assert getVariables([varA]) == ['x']

    varB = getTokens("xy+ xy^2 +yz^3")
    assert getVariables(varB) == ['x', 'y', 'z']


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


def test_checkSyntax():
    test1 = False
    test2 = False
    test3 = False
    test4 = False
    test5 = False
    eqn1 = "2 + sin(2)"
    boolean, log = checkSyntax(eqn1)
    if (boolean is True and log == "Standard syntax is followed"):
        test1 = True
    assert test1
    eqn2 = "2 + (log2)^(e+2) + sinh(x + x^2)"
    boolean, log = checkSyntax(eqn2)
    if (boolean is False and log == "For function 'log', arguments are not enclosed within parentheses"):
        test2 = True
    assert test2
    eqn3 = "0.2 + .5"
    boolean, log = checkSyntax(eqn3)
    if (boolean is False and log == "Decimal point must be between two integers"):
        test3 = True
    assert test3
    eqn4 = "2 + (x+2)(x+3)"
    boolean, log = checkSyntax(eqn4)
    if (boolean is False and log == "There must be an operator between close parenthesis and open parenthesis"):
        test4 = True
    assert test4
    eqn5 = "2 + (x+2)*(x+3)"
    boolean, log = checkSyntax(eqn5)
    if (boolean is True and log == "Standard syntax is followed"):
        test5 = True
    assert test5


#############
# io.parser #
#############


def test_tokensToString():

    # Matrix token to string
    mat = getTokens("[1+x, 2; \
                      3  , 4]")
    assert tokensToString([mat]) == "[1.0 + x,2.0;3.0,4.0]"

    mat = getTokens("[1+x, 2] + [1, y + z^2]")
    assert tokensToString(mat) == "[1.0 + x,2.0] + [1.0,y + z^(2.0)]"


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
    assert getTerms("coth^2(x)-csch^2(x)=1") == ['coth', '^', '2', '(', 'x', ')', '-', 'csch', '^', '2', '(', 'x', ')', '=', '1']

    assert getTerms("e = 2.71828") == ['exp', '=', '2.71828']
    assert getTerms("log_10(100) = 2") == ['log_', '10', '(', '100', ')', '=', '2']
    assert getTerms("ln(e) = 1") == ['ln', '(', 'exp', ')', '=', '1']
    assert getTerms("e^(i*pi)=1") == ['exp', '^', '(', 'iota', '*', 'pi', ')', '=', '1']

    assert getTerms("a = b") == ['a', '=', 'b']
    assert getTerms("a < b") == ['a', '<', 'b']
    assert getTerms("a > b") == ['a', '>', 'b']
    assert getTerms("a <= b") == ['a', '<=', 'b']
    assert getTerms("a >= b") == ['a', '>=', 'b']

    assert getTerms("[1,0;0,1]") == ['[', '1', ',', '0', ';', '0', ',', '1', ']']
    assert getTerms("2*[2,3;2,3]+[1,2;1,2]") == ['2', '*', '[', '2', ',', '3', ';', '2', ',', '3', ']', '+', '[', '1', ',', '2', ';', '1', ',', '2', ']']

    assert getTerms(r"$\frac {3}{x}-\frac{x}{y}$") == ['$', 'frac', '{', '3', '}', '{', 'x', '}', '-', 'frac', '{', 'x', '}', '{', 'y', '}', '$']


def test_normalize():

    assert normalize(['$', 'frac', '{', '3', '}', '{', 'x', '}', '-', 'frac', '{', 'x', '}', '{', 'y', '}', '$']) == ['$', '3', '/', 'x', '-', 'x', '/', 'y', '$']
