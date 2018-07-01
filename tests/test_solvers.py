from visma.solvers.polynomial.roots import quadraticRoots
from visma.solvers.solve import solveFor
from tests.tester import quickTest

############################
# solvers.polynomial.roots #
############################


def test_quadraticRoots():

    assert quickTest("x^2 + 2x + 1 = 0", quadraticRoots) == "(x+1.0)^(2)=0"
    assert quickTest("x^2 + 1 = 2x", quadraticRoots) == "(x-1.0)^(2)=0"

    assert quickTest("2x^2 - 4x - 6 = 0", quadraticRoots) == "(x+1.0)*(x-3.0)=0"
    assert quickTest("3x^2 + 7x + 1 = 0", quadraticRoots) == "(x+2.18)*(x+0.15)=0"
    assert quickTest("3x^2 - 7x + 1 = 0", quadraticRoots) == "(x-0.15)*(x-2.18)=0"

    assert quickTest("x^2 + x + 1 = 0", quadraticRoots) == "(x+0.5+0.87*sqrt[2](-1.0))*(x+0.5-0.87*sqrt[2](-1.0))=0"
    assert quickTest("x^2 - x + 1 = 0", quadraticRoots) == "(x-0.5+0.87*sqrt[2](-1.0))*(x-0.5-0.87*sqrt[2](-1.0))=0"


#################
# solvers.solve #
#################


def test_solveFor():

    assert quickTest("x - 1 + 2 = 0", solveFor, 'x') == "x=(-1.0)"
    assert quickTest("1 + y^2 = 0", solveFor, 'y') == "y=(-1.0)^(0.5)"
    assert quickTest("x^2 - 1 = 0", solveFor, 'x') == "x=(1.0)^(0.5)"

    assert quickTest("x - yz + 1= 0", solveFor, 'x') == "x=(-1.0+yz)"
    assert quickTest("x - yz + 1= 0", solveFor, 'y') == "y=((-1.0-x)/z)"
    assert quickTest("x - yz + 1= 0", solveFor, 'z') == "z=((-1.0-x)/y)"

    assert quickTest("w + x^2 + yz^3 = 1", solveFor, 'w') == "w=(-x^(2.0)-yz^(3.0)+1.0)"
    assert quickTest("w + x^2 + yz^3 = 1", solveFor, 'x') == "x=(-w-yz^(3.0)+1.0)^(0.5)"
    assert quickTest("w + x^2 + yz^3 = 1", solveFor, 'y') == "y=((-w-x^(2.0)+1.0)/z^(3.0))"
    assert quickTest("w + x^2 + yz^3 = 1", solveFor, 'z') == "z=((-w-x^(2.0)+1.0)/y)^(0.333333333333)"
