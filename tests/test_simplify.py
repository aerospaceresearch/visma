from visma.simplify.simplify import simplify, simplifyEquation
from visma.simplify.addsub import addition, additionEquation, subtraction, subtractionEquation
from visma.simplify.muldiv import multiplication, division
from tests.tester import quickTest

#####################
# simplify.simplify #
#####################


def test_simplify():

    assert quickTest("1 + 2 - 3", simplify) == "0"
    assert quickTest("1 + 2 - 4", simplify) == "-1.0"

    assert quickTest("3*2 + 4*2 - 3*4", simplify) == "2.0"
    assert quickTest("3*x + 4*x - 2*y", simplify) == "7.0x-2.0y"
    assert quickTest("x*y + x*x + x*x^2 + x^2*x + x*y^2 + x^2*y", simplify) == "xy+x^(2)+2x^(3.0)+xy^(2.0)+x^(2.0)y"

    assert quickTest("3/2 + 4/2 - 2/4", simplify) == "3.0"
    assert quickTest("x/5 + x/4 - 2/y", simplify) == "0.45x-2.0y^(-1)"
    assert quickTest("x/y + x/x + x/x^2 + x^2/x + x/y^2 + x^2/y + x + 1", simplify) == "xy^(-1)+x^(-1.0)+xy^(-2.0)+x^(2.0)y^(-1)+2.0x+2.0"

    assert quickTest("1 + 2 = 3", simplifyEquation) == "=0"  # FIXME: Vanishing zero
    assert quickTest("1 + 2 = 4", simplifyEquation) == "-1.0=0"  # FIXME: Exclude these cases, raise math error

    assert quickTest("3*2 + 4*2 = 3*4", simplifyEquation) == "2.0=0"  # FIXME: Exclude these cases, raise math error
    assert quickTest("3*x = 4*x + 2*y", simplifyEquation) == "-x-2.0y=0"
    assert quickTest("1 - 1 = 3*x + 4*x + 2*y", simplifyEquation) == "7.0x+2.0y=0"

    assert quickTest("x = y --1 --x^2", simplifyEquation) == "x-y-1.0-x^(2.0)=0"  # FIXME: Valid but silly input case

    assert quickTest("4 = 3x - 4x - 1 + 2", simplifyEquation) == "3.0+x=0"
    assert quickTest("z = x^2 - x + 1 - 2", simplifyEquation) == "z-x^(2.0)+x+1.0=0"
    assert quickTest("x = -1 + 2", simplifyEquation) == "x+1.0-2.0=0"  # FIXME: Further simplification required (simplification in RHS)
    assert quickTest("x*y + x*x + x*x^2 = x^2*x + x*y^2 + x^2*y", simplifyEquation) == "xy+x^(2)-xy^(2.0)-x^(2.0)y=0"

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

    assert quickTest("1 - 2 = x - 3x", subtractionEquation) == "-1.0=-2.0x"
    assert quickTest("y + 2 = -x - x", subtractionEquation) == "y+2.0=-2.0x"


def test_muldiv():

    assert quickTest("3*y + x*2", multiplication) == "3.0y+2.0x"
    assert quickTest("x^3 * x^2", multiplication) == "x^(5.0)"
    assert quickTest("x^(-1)y^2 * zx^2", multiplication) == "xy^(2.0)z"

    assert quickTest("x^2 / x^2", division) == "1.0"
    assert quickTest("x^2 / x^4", division) == "x^(-2.0)"
    assert quickTest("x^(-1)y^2 / zx^2", division) == "x^(-3.0)y^(2.0)z^(-1)"
