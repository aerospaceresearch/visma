from visma.functions.constant import Constant
from visma.functions.variable import Variable
from tests.tester import getTokens


######################
# functions.constant #
######################


def test_Constant():

    constant1 = Constant(10)
    assert constant1.__str__() == "{10}"
    constant1.differentiate()
    assert constant1.value == 0

    constant2 = Constant(5)
    constant2.integrate('x')
    assert isinstance(constant2, Variable)
    assert constant2.__str__() == "5{x}"


######################
# functions.variable #
######################


def test_Variable():

    variable1 = Variable(2, 'x', 3)
    assert variable1.__str__() == "2{x}^{3}"
    variable1.integrate('x')
    assert variable1.__str__() == "0.5{x}^{4}"

    # FIXME: Optimize integrate
    '''
    variable2 = Variable(3, 'x', -1)
    variable2.integrate('x')
    assert isinstance(variable2, Expression)
    assert variable2.__str__() == '{3log{x}}'
    '''


#######################
# functions.structure #
#######################


def test_reduce():

    expr = getTokens("(2x+x)")
    assert str(expr) == "3.0{x}"
    assert expr.type == "Variable"

    expr = getTokens("(3x+4*(x+(2x))+2y)")
    assert str(expr) == "{(15.0{x}+2.0{y})}"

    expr = getTokens("((2x+4x)+(2y+4y))")
    assert str(expr) == "{(6.0{x}+6.0{y})}"
