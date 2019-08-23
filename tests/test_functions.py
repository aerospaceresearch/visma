from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.functions.structure import Expression
from visma.functions.operator import Plus, Minus
from visma.io.parser import tokensToString

######################
# functions.constant #
######################


def test_Constant():

    # Tests for Calculus operations for Constant Class.

    constant1 = Constant(10)
    assert constant1.__str__() == "{10}"
    constant1.differentiate()
    assert constant1.value == 0

    constant2 = Constant(5, 2)
    constant2.integrate('x')
    assert isinstance(constant2, Variable)
    assert constant2.__str__() == "25{x}"

    # Tests for Add/Sub operations (using Overloading) for Constant Class.

    constant4 = Constant(2, 2)
    constant5 = Constant(7)
    constant3 = constant4 - constant5
    assert constant3.__str__() == "{-3}"

    constant4 = Constant(7, 2)
    constant0 = Constant(5)
    constant6 = constant4 - constant3 - constant5 + constant0
    assert constant6.__str__() == "{50}"

    constant0 = Constant(5, 2, 2)
    constant2 = constant0
    variable0 = Variable(5, 'X', 3)
    summation0 = constant0 - variable0 + constant2
    assert summation0.__str__() == "{({100}-5{X}^{3})}"

    constant0 = Constant(5, 2, 2)
    constant2 = constant0
    variable0 = Variable(5, 'X', 3)
    summation0 = constant0 + variable0 + constant2
    assert summation0.__str__() == "{({100}+5{X}^{3})}"

    var1 = Variable(3, 'x', 3)
    const1 = Constant(5)
    expr1 = Expression([var1, Minus(), const1])
    constant2 = Constant(2, 2)
    sub1 = constant2 - expr1
    assert sub1.__str__() == "{({9}-3{x}^{3})}"

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

# Tests for Add/Sub operations (using Overloading) for Constant Class.

    constant0 = Constant(0, 2)
    constant1 = Constant(5)
    mul1 = constant0 * constant1
    assert mul1.calculate() == 0
    mul1 = constant1 * constant0
    assert mul1.calculate() == 0
    mul1 = constant1 * constant1 + constant0 * constant1 + constant0 * constant1
    assert mul1.calculate() == 25

    constant1 = Constant(5, 2)
    constant2 = Constant(4, 2)
    variable0 = Variable(3, 'X', 3)
    mul3 = constant1 * (constant2 + variable0)
    assert mul3.__str__() == "{({400}+75{X}^{3})}"

    constant1 = Constant(5, 2)
    constant2 = Constant(4, 2)
    variable0 = Variable(3, 'X', 3)
    mul3 = constant1 / (constant2 + variable0)
    assert mul3.__str__() == "{25}*{({16}+3{X}^{3})}^{-1}"

    constant1 = Constant(5)
    constant2 = Constant(4)
    div1 = constant1 / constant2
    assert div1.__str__() == "{1.25}"

    constant1 = Constant(3, 2)
    constant2 = Constant(4, 2)
    variable0 = Variable(3, 'X', 3)
    mul3 = constant1 - constant1/(constant2/variable0 + constant1)
    assert mul3.__str__() == "{({9}-{9}*{(5.333333333333333{X}^{-3}+{9})}^{-1})}"

    constant1 = Constant(2, 2)
    constant2 = Constant(2, 2)
    mul3 = constant1 ** constant2
    assert mul3.__str__() == "{256}"

    constant1 = Constant(5)
    constant2 = Constant(5)
    summation = constant1 * constant2
    assert summation.__str__() == "{25}"

    constant1 = Constant(5)
    variable1 = Variable(5, 'x', 3)
    exp1 = Expression([constant1, Plus(), variable1])
    constant2 = Constant(10)
    summation = constant2 + exp1
    assert summation.__str__() == "{({15}+5{x}^{3})}"

    constant1 = Constant(5)
    variable1 = Variable(5, 'x', 3)
    exp1 = Expression([constant1, Plus(), variable1])
    constant2 = Constant(10)
    summation = constant2 - exp1
    assert summation.__str__() == "{({5}-5{x}^{3})}"

    constant1 = Constant(5)
    variable1 = Variable(5, 'x', 3)
    exp1 = Expression([constant1, Plus(), variable1])
    constant2 = Constant(10)
    summation = exp1 - constant2
    assert summation.__str__() == "{({-5}+5{x}^{3})}"

    constant1 = Constant(5)
    variable1 = Variable(5, 'x', 3)
    summation = constant1 * variable1
    assert summation.__str__() == "25{x}^{3}"

    constant1 = Constant(5)
    variable1 = Variable(5, 'x', 3)
    exp1 = Expression([constant1, Plus(), variable1])
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
    variable1 = Variable(5, 'x', 3)
    exp1 = Expression([constant1, Plus(), variable1])
    constant2 = Constant(10)
    summation = constant2 / exp1
    assert summation.__str__() == "{10}*{({5}+5{x}^{3})}^{-1}"

    constant1 = Constant(5)
    variable1 = Variable(5, 'x', 3)
    exp1 = Expression([constant1, Plus(), variable1])
    constant2 = Constant(10)
    summation = exp1 / constant2
    assert summation.__str__() == "{({0.5}+0.5{x}^{3})}"


######################
# functions.variable #
######################


def test_Variable():

    variable1 = Variable(2, 'x', 3)
    assert variable1.__str__() == "2{x}^{3}"
    variable1, _ = variable1.integrate('x')
    assert variable1.__str__() == "0.5{x}^{4}"

    constant = Constant(3)
    variable = Variable(2, 'x', 3)
    add = variable + constant
    assert add.__str__() == "{(2{x}^{3}+{3})}"

    variable1 = Variable(2, 'x', 3)
    variable2 = Variable(4, 'x', 3)
    add1 = variable1 + variable2
    assert add1.__str__() == "6{x}^{3}"

    variable1 = Variable(2, 'x', 3)
    constant = Constant(3)
    exp1 = Expression([variable1, Plus(), constant])
    variable2 = Variable(4, 'x', 3)
    add2 = variable2 + exp1
    assert add2.__str__() == "{(6{x}^{3}+{3})}"

    variable1 = Variable(2, 'x', 3)
    constant = Constant(3)
    exp1 = variable1 + constant
    variable2 = Variable(4, 'x', 3)
    add2 = variable2 - exp1
    assert add2.__str__() == "{(2{x}^{3}-{3})}"

    variable1 = Variable(2, 'x', 3)
    constant = Constant(3)
    exp1 = Expression([variable1, Plus(), constant])
    variable2 = Variable(4, 'x', 3)
    add2 = exp1 - variable2
    assert add2.__str__() == "{(-2{x}^{3}+{3})}"

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

    constant = Constant(3)
    variable = Variable(2, 'x', 3)
    add = variable * constant
    assert add.__str__() == "6{x}^{3}"

    variable1 = Variable(2, 'x', 3)
    variable2 = Variable(4, 'x', 3)
    add2 = variable1 * variable2
    assert add2.__str__() == "8{x}^{6}"

    variable1 = Variable(2, 'x', 3)
    variable2 = Variable(4, 'y', 3)
    add2 = variable1 * variable2
    assert add2.__str__() == "8{x}^{3}{y}^{3}"

    variable1 = Variable(2, 'x', 3)
    variable2 = Variable(4, 'y', 4)
    add1 = variable1 / variable2
    assert add1.__str__() == "0.5{x}^{3}{y}^{-4}"

    variable1 = Variable(2, 'x', 3)
    constant = Constant(3)
    exp1 = variable1 - constant
    variable2 = Variable(4, 'x', 3)
    add2 = variable2 / exp1
    assert add2.__str__() == "{(4.0{x}^{3}*{(2{x}^{3}-{3})}^{-1})}"

    variable1 = Variable(2, 'x', 3)
    constant = Constant(3)
    exp1 = variable1 - constant
    variable2 = Variable(4, 'x', 3)
    add2 = variable2 * exp1
    assert add2.__str__() == "{(8{x}^{6}-12{x}^{3})}"

    variable1 = Variable(2, 'x', 3)
    constant1 = Constant(3)
    exp1 = variable1 - constant1
    variable2 = Variable(4, 'x', 3)
    constant2 = Constant(4)
    exp2 = variable2 - constant2
    add2 = exp1 * exp2
    assert add2.__str__() == "{({(8{x}^{6}-8{x}^{3})}-{(12{x}^{3}-{12})})}"

    variable2 = Variable(3, 'x', -1)
    variable2, _ = variable2.integrate('x')
    assert tokensToString(variable2) == '3 * log(x)'
