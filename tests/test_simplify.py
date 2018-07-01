from visma.simplify.simplify import simplify, simplifyEquation
from visma.simplify.addsub import addition, additionEquation, subtraction
from tests.tester import quickTest

#####################
# simplify.simplify #
#####################


def test_simplify():

    assert quickTest("1 + 2 - 3", simplify) == ""  # FIXME: Vanishing zero
    assert quickTest("1 + 2 - 4", simplify) == "-1.0"

    assert quickTest("3*2 + 4*2 - 3*4", simplify) == "2.0"
    assert quickTest("3*x + 4*x - 2*y", simplify) == "7.0x-2.0y"
    assert quickTest("x*y + x*x + x*x^2 + x^2*x + x*y^2 + x^2*y", simplify) == "xy+x^(2)+xx^(2.0)+x^(2.0)x+xy^(2.0)+x^(2.0)y"  # FIXME: Simplify further

    assert quickTest("3/2 + 4/2 - 2/4", simplify) == "3.0"
    assert quickTest("x/5 + x/4 - 2/y", simplify) == "0.45x-2.0y^(-1)"
    assert quickTest("x/y + x/x + x/x^2 + x^2/x + x/y^2 + x^2/y + x + 1", simplify) == "xy^(-1)+x^(-1.0)+xy^(-2.0)+x^(2.0)y^(-1)+2x+2.0"

    assert quickTest("1 + 2 = 3", simplifyEquation) == "=0"  # FIXME: Vanishing zero
    assert quickTest("1 + 2 = 4", simplifyEquation) == "-1.0=0"  # FIXME: Exclude these cases, raise math error

    assert quickTest("3*2 + 4*2 = 3*4", simplifyEquation) == "2.0=0"  # FIXME: Exclude these cases, raise math error
    assert quickTest("3*x = 4*x + 2*y", simplifyEquation) == "-x-2.0y=0"
    assert quickTest("x*y + x*x + x*x^2 = x^2*x + x*y^2 + x^2*y", simplifyEquation) == "xy+x^(2)+xx^(2.0)-x^(2.0)x-xy^(2.0)-x^(2.0)y=0"  # FIXME: Simplify further

    assert quickTest("3/2 + 4/2 = 2/4", simplifyEquation) == "3.0=0"  # FIXME: Exclude these cases, raise math error
    assert quickTest("x/5 + x/4 = 2/y", simplifyEquation) == "0.45x-2.0y^(-1)=0"
    assert quickTest("x/y + x/x + x/x^2 + x^2/x = x/y^2 + x^2/y + x - 1", simplifyEquation) == "xy^(-1)+2.0+x^(-1.0)-xy^(-2.0)-x^(2.0)y^(-1)=0"


def test_addsub():

    assert quickTest("1 + 2", addition) == "3.0"
    assert quickTest("x + 2x", addition) == "3.0x"
    assert quickTest("xy^2 + 2xy^2", addition) == "3.0xy^(2.0)"
    assert quickTest("-1 + 2", addition) == "1.0"
    assert quickTest("-x + 2x", addition) == "x"
    assert quickTest("-xy^2 + 3xy^2", addition) == "2.0xy^(2.0)"
    assert quickTest("1 + 0", addition) == "1.0"
    assert quickTest("1 + 2 + 3", addition) == "6.0"
    assert quickTest("1 + 2 + x + 3x", addition) == "3.0+4.0x"

    assert quickTest("1 + 2 = x + 3x", additionEquation) == "3.0=4.0x"
    assert quickTest("y + 2 = -x + x", additionEquation) == "y+2.0=0"

    assert quickTest("1 - 2", subtraction) == "-1.0"
    assert quickTest("x - 2x", subtraction) == "-x"
    assert quickTest("xy^2 - 3xy^2", subtraction) == "-2.0xy^(2.0)"
