from visma.calculus.differentiation import differentiate, differentiationProductRule
from visma.calculus.integration import integrate
from tests.tester import quickTest

############################
# calculus.differentiation #
############################


def test_differentiate():

    assert quickTest("x^2 + x", differentiate, 'x') == "2.0x+1.0"

    assert quickTest("x + 2y + 3z + 4", differentiate, 'x') == "1.0"
    assert quickTest("x + 2y + 3z + 4", differentiate, 'y') == "2.0"
    assert quickTest("x + 2y + 3z + 4", differentiate, 'z') == "3.0"

    assert quickTest("xy + xy^2 + xyz", differentiate, 'x') == "y+y^(2.0)+yz"
    assert quickTest("xy + xy^2 + xyz", differentiate, 'y') == "x+2.0xy+xz"
    assert quickTest("xy + xy^2 + xyz", differentiate, 'z') == "xy"

    assert quickTest("xy + z", differentiate, 'z') == "1.0"
    assert quickTest("z + xy", differentiate, 'z') == "1.0"
    assert quickTest("z - xy", differentiate, 'z') == "1.0"
    assert quickTest("xy - z", differentiate, 'z') == "-1.0"

    assert quickTest("sin(x)", differentiate, 'x') == "cos(x)*1.0"
    assert quickTest("sin(x)", differentiate, 'y') == "0.0"
    assert quickTest("sin(xxx)", differentiate, 'x') == "cos(x^(3.0))*3.0x^(2.0)"
    assert quickTest("sin(log(xx))", differentiate, 'x') == "cos(log(x^(2.0)))*x^(-1.0)*2.0x"

    assert quickTest("cos(x)", differentiate, 'x') == "-1.0*sin(x)*1.0"
    assert quickTest("cos(x)", differentiate, 'y') == "0.0"
    assert quickTest("cos(xxx)", differentiate, 'x') == "-1.0*sin(x^(3.0))*3.0x^(2.0)"
    assert quickTest("cos(log(xx))", differentiate, 'x') == "-1.0*sin(log(x^(2.0)))*x^(-1.0)*2.0x"

    assert quickTest("tan(x)", differentiate, 'x') == "sec(x)*1.0"
    # FIXME: Simplify module simplifies sec^2(x) as sec(x) and cosec^2(x) as cosec(x), however differentiation modules give correct output
    assert quickTest("tan(x)", differentiate, 'y') == "0.0"

    assert quickTest("cot(x)", differentiate, 'x') == "-1.0*csc(x)*1.0"
    # FIXME: Simplify module simplifies sec^2(x) as sec(x) and cosec^2(x) as cosec(x), however differentiation modules give correct output
    assert quickTest("cot(x)", differentiate, 'y') == "0.0"

    assert quickTest("csc(x)", differentiate, 'x') == "-1.0*csc(x)*cot(x)*1.0"
    assert quickTest("csc(x)", differentiate, 'y') == "0.0"

    assert quickTest("sec(x)", differentiate, 'x') == "sec(x)*tan(x)*1.0"
    assert quickTest("sec(x)", differentiate, 'y') == "0.0"

    assert quickTest("log(x)", differentiate, 'x') == "x^(-1.0)"
    assert quickTest("log(xx)", differentiate, 'x') == "2.0"

    # Tests for Product Rule of Differentiation.
    assert quickTest("sin(x)*cos(x)", differentiationProductRule, 'x') == "(cos(x)*1.0)*cos(x)+sin(x)*(-1.0*sin(x)*1.0)"
    assert quickTest("sin(x)*x", differentiationProductRule, 'x') == "(cos(x)*1.0)*x+sin(x)*(1.0)"
    assert quickTest("sin(x)*y", differentiationProductRule, 'x') == "(cos(x)*1.0)*y+sin(x)*(0.0)"
    assert quickTest("sin(x)*cos(x)*sec(x)", differentiationProductRule, 'x') == "(cos(x)*1.0)*cos(x)*sec(x)+sin(x)*(-1.0*sin(x)*1.0)*sec(x)+sin(x)*cos(x)*(sec(x)*tan(x)*1.0)"


########################
# calculus.integration #
########################


def test_integrate():

    assert quickTest("x + 1", integrate, 'x') == "0.5x^(2.0)+x"

    assert quickTest("xyz + xy/z + x + 1 + 1/x", integrate, 'x') == "0.5x^(2.0)yz+0.5x^(2.0)yz^(-1.0)+0.5x^(2.0)+x+1.0*log(x)"  # FIXME(integration.py): Ignore coeff if 1
    assert quickTest("xyz + xy/z + x + 1 + 1/x", integrate, 'y') == "0.5xy^(2.0)z+0.5xy^(2.0)z^(-1.0)+xy+y+x^(-1.0)y"
    assert quickTest("xyz + xy/z + x + 1 + 1/x", integrate, 'z') == "0.5xyz^(2.0)+xy*log(z)+xz+z+x^(-1.0)z"

    assert quickTest("sin(x)", integrate, 'x') == "-1.0*cos(x)"
    assert quickTest("cos(x)", integrate, 'x') == "sin(x)"
    assert quickTest("tan(x)", integrate, 'x') == "-1.0*ln(cos(x))"
    assert quickTest("csc(x)", integrate, 'x') == "-1.0*ln((csc(x)+cot(x)))"
    assert quickTest("sec(x)", integrate, 'x') == "ln((sec(x)+tan(x)))"
    assert quickTest("cot(x)", integrate, 'x') == "ln(sin(x))"
