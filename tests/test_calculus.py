from visma.calculus.differentiation import differentiate
from visma.calculus.integration import integrate
from tests.tester import quickTest

############################
# calculus.differentiation #
############################


def test_differentiate():

    assert quickTest("x^2 + x", differentiate, 'x') == "2.0x+1"

    assert quickTest("xy + xy^2 + xyz", differentiate, 'x') == "y+y^(2.0)+yz"
    assert quickTest("xy + xy^2 + xyz", differentiate, 'y') == "x+2.0xy+xz"
    assert quickTest("xy + xy^2 + xyz", differentiate, 'z') == "+xy"


########################
# calculus.integration #
########################


def test_integrate():

    assert quickTest("x + 1", integrate, 'x') == "0.5x^(2)+x"

    assert quickTest("xyz + xy/z + x + 1", integrate, 'x') == "0.5x^(2)yz+0.5x^(2)yz^(-1)+0.5x^(2)+x"
    assert quickTest("xyz + xy/z + x + 1", integrate, 'y') == "0.5xy^(2)z+0.5xy^(2)z^(-1)+xy+y"
    assert quickTest("xyz + xy/z + x + 1", integrate, 'z') == "0.5xyz^(2)+xy*log(z)+xz+z"
