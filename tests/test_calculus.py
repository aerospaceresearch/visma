from visma.calculus.differentiation import differentiate
from visma.calculus.integration import integrate
from tests.tester import quickTest

############################
# calculus.differentiation #
############################


def test_differentiate():

    assert quickTest("x^2 + x", differentiate, 'x') == "2.0x+1.0"

    assert quickTest("x + 2y + 3z + 4", differentiate, 'x') == "1.0"
    assert quickTest("x + 2y + 3z + 4", differentiate, 'y') == "2.0"
    # FIXME: add module is simplify not giving correct result for (0 + 0 + 0 + ...)
    # assert quickTest("x + 2y + 3z + 4", differentiate, 'z') == "3.0"

    assert quickTest("xy + xy^2 + xyz", differentiate, 'x') == "y+y^(2.0)+yz"
    assert quickTest("xy + xy^2 + xyz", differentiate, 'y') == "x+2.0xy+xz"
    assert quickTest("xy + xy^2 + xyz", differentiate, 'z') == "xy"

    assert quickTest("xy + z", differentiate, 'z') == "1.0"
    assert quickTest("z + xy", differentiate, 'z') == "1.0"
    assert quickTest("z - xy", differentiate, 'z') == "1.0"
    assert quickTest("xy - z", differentiate, 'z') == "-1.0"
########################
# calculus.integration #
########################


def test_integrate():

    assert quickTest("x + 1", integrate, 'x') == "0.5x^(2.0)+x"

    assert quickTest("xyz + xy/z + x + 1 + 1/x", integrate, 'x') == "0.5x^(2.0)yz+0.5x^(2.0)yz^(-1.0)+0.5x^(2.0)+x+1.0*log(x)"  # FIXME(integration.py): Ignore coeff if 1
    assert quickTest("xyz + xy/z + x + 1 + 1/x", integrate, 'y') == "0.5xy^(2.0)z+0.5xy^(2.0)z^(-1.0)+xy+y+x^(-1.0)y"
    assert quickTest("xyz + xy/z + x + 1 + 1/x", integrate, 'z') == "0.5xyz^(2.0)+xy*log(z)+xz+z+x^(-1.0)z"
