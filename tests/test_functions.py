from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.functions.structure import Expression


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

    constant1 = Constant(2)
    constant2 = Constant(7)
    constant3 = constant1 + constant2
    assert constant3.__str__() == "{9}"

    constant1 = Constant(2)
    constant2 = Constant(7)
    constant3 = constant1 - constant2
    assert constant3.__str__() == "{-5}"

    constant1 = Constant(5)
    variable1 = Variable(5, 'x', 3)
    summation = constant1 + variable1
    assert summation.__str__() == "{({5}+5{x}^{3})}"

    constant1 = Constant(5)
    variable1 = Variable(5, 'x', 3)
    summation = constant1 - variable1
    assert summation.__str__() == "{({5}-5{x}^{3})}"

    constant1 = Constant(5)
    constant2 = Constant(5)
    summation = constant1 * constant2
    assert summation.__str__() == "{25}"

    constant1 = Constant(5)
    variable1 = Variable(5, 'x', 3)
    summation = constant1 * variable1
    assert summation.__str__() == "25{x}^{3}"

    constant1 = Constant(5)
    exp1 = constant1 + Variable(5, 'x', 3)
    constant2 = Constant(10)
    summation = constant2 * exp1
    assert summation.__str__() == "{({50}+50{x}^{3})}"

    constant1 = Constant(5)
    constant2 = Constant(5)
    summation = constant1 / constant2
    assert summation.__str__() == "{1.0}"

    constant1 = Constant(5)
    variable1 = Variable(5, 'x', 3)
    summation = constant1 / variable1
    assert summation.__str__() == "{x}^{-3}"

    constant1 = Constant(5)
    exp1 = constant1 + Variable(5, 'x', 3)
    constant2 = Constant(10)
    summation = constant2 / exp1
    assert summation.__str__() == "10.0*{({5}+5{x}^{3})}^{-1}"

######################
# functions.variable #
######################


def test_Variable():

    variable1 = Variable(2, 'x', 3)
    assert variable1.__str__() == "2{x}^{3}"
    variable1.integrate('x')
    assert variable1.__str__() == "0.5{x}^{4}"

    constant = Constant(3)
    variable = Variable(2, 'x', 3)
    add = variable + constant
    assert add.__str__() == "{(2{x}^{3}+{3})}"

    variable1 = Variable(2, 'x', 3)
    variable2 = Variable(4, 'x', 3)
    variable3 = Variable(2, 'x', 4)
    add1 = variable1 + variable2
    add2 = variable1 + variable3
    assert add1.__str__() == "6{x}^{3}"
    assert add2.__str__() == "{(6{x}^{3}+2{x}^{4})}"

    variable1 = Variable(2, 'x', 3)
    constant = Constant(3)
    exp1 = Expression([variable1, '+', constant])
    variable2 = Variable(4, 'x', 3)
    add2 = variable2 + exp1
    assert add2.__str__() == "{(6{x}^{3}+{3})}"

    constant = Constant(3)
    variable = Variable(2, 'x', 3)
    add = variable - constant
    assert add.__str__() == "{(2{x}^{3}-{3})}"

    variable1 = Variable(2, 'x', 3)
    variable2 = Variable(4, 'x', 3)
    variable3 = Variable(2, 'x', 4)
    variable4 = Variable(2, 'x', 3)
    add1 = variable1 - variable2
    add2 = variable3 - variable4
    assert add1.__str__() == "-2{x}^{3}"
    assert add2.__str__() == "{(2{x}^{4}-2{x}^{3})}"

    variable1 = Variable(2, 'x', 3)
    constant = Constant(3)
    exp1 = variable1 - constant
    variable2 = Variable(4, 'x', 3)
    add2 = variable2 - exp1
    assert add2.__str__() == "{(2{x}^{3}-{-3})}"

    # FIXME: Optimize integrate
    '''
    variable2 = Variable(3, 'x', -1)
    variable2.integrate('x')
    assert isinstance(variable2, Expression)
    assert variable2.__str__() == '{3log{x}}'
    '''
