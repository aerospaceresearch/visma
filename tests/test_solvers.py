from visma.solvers.polynomial.roots import quadraticRoots
from visma.solvers.simulEqn import simulSolver
from visma.solvers.solve import solveFor
from tests.tester import quickTest

############################
# solvers.polynomial.roots #
############################


def test_quadraticRoots():

    assert quickTest("x^2 + 2x + 1 = 0", quadraticRoots) == "(x+1.0)^(2)=0"
    assert quickTest("x^2 + 2x = - 1", quadraticRoots) == "(x+1.0)^(2)=0"
    assert quickTest("x^2 = - 2x - 1", quadraticRoots) == "(x+1.0)^(2)=0"
    assert quickTest("0 = x^2 + 2x + 1", quadraticRoots) == "(x+1.0)^(2)=0"

    assert quickTest("x^2 + 1 - 2x = 0", quadraticRoots) == "(x-1.0)^(2)=0"
    assert quickTest("x^2 + 1 = 2x", quadraticRoots) == "(x-1.0)^(2)=0"
    assert quickTest("x^2 = 2x - 1", quadraticRoots) == "(x-1.0)^(2)=0"
    assert quickTest("-2x = - x^2 - 1", quadraticRoots) == "(x-1.0)^(2)=0"
    # FIXME: assert quickTest("0 = 2x - x^2 - 1", quadraticRoots) == "(x-1.0)^(2)=0"

    assert quickTest("2x^2 - 4x - 6 = 0", quadraticRoots) == "(x+1.0)*(x-3.0)=0"
    assert quickTest("3x^2 + 7x + 1 = 0", quadraticRoots) == "(x+2.18)*(x+0.15)=0"
    assert quickTest("3x^2 - 7x + 1 = 0", quadraticRoots) == "(x-0.15)*(x-2.18)=0"

    assert quickTest("x^2 + x + 1 = 0", quadraticRoots) == "(x+0.5+0.87*sqrt[2](-1))*(x+0.5-0.87*sqrt[2](-1))=0"
    assert quickTest("x^2 - x + 1 = 0", quadraticRoots) == "(x-0.5+0.87*sqrt[2](-1))*(x-0.5-0.87*sqrt[2](-1))=0"


###############################
# solvers.simulEqn #
###############################

def test_simulSolvers():
    assert quickTest("1000x + 2y + 3z = 4; 5x + 6y + 7z = 8; 9x + 10y + 1100z = 12", simulSolver, 'x') == "x=0.0"
    assert quickTest("1000x + 2y + 3z = 4; 5x + 6y + 7z = 8; 9x + 10y + 1100z = 12", simulSolver, 'y') == "y=1.33"
    assert quickTest("1000x + 2y + 3z = 4; 5x + 6y + 7z = 8; 9x + 10y + 1100z = 12", simulSolver, 'z') == "z=-0.0"

    assert quickTest("1000x + 2y + 3z = 4; 5x + 6y + 7z = 8; 9x + 10y + 11z = 12", simulSolver, 'x') == "x=-0.0"
    assert quickTest("1000x + 2y + 3z = 4; 5x + 6y + 7z = 8; 9x + 10y + 11z = 12", simulSolver, 'y') == "y=-1.0"
    assert quickTest("1000x + 2y + 3z = 4; 5x + 6y + 7z = 8; 9x + 10y + 11z = 12", simulSolver, 'z') == "z=2.0"

    assert quickTest("1x + 2y + 3z = 4; 5x + 6y + 7z = 8; 9x + 10y + 11z = 12", simulSolver, 'x') == "NoTrivialSolution"
    assert quickTest("1x + 2y + 3z = 4; 5x + 6y + 7z = 8; 9x + 10y + 11z = 12", simulSolver, 'y') == "NoTrivialSolution"
    assert quickTest("1x + 2y + 3z = 4; 5x + 6y + 7z = 8; 9x + 10y + 11z = 12", simulSolver, 'z') == "NoTrivialSolution"

    assert quickTest("1000a + 2y + 3w = 4; 5a + 6y + 7w = 8; 9a + 10y + 1100w = 12", simulSolver, 'a') == "a=0.0"
    assert quickTest("1000a + 2y + 3w = 4; 5a + 6y + 7w = 8; 9a + 10y + 1100w = 12", simulSolver, 'y') == "y=1.33"
    assert quickTest("1000a + 2y + 3w = 4; 5a + 6y + 7w = 8; 9a + 10y + 1100w = 12", simulSolver, 'w') == "w=-0.0"

    assert quickTest("1000a + 2y + 3w = 4; 5a + 6y + 7w = 8; 10y = 12", simulSolver, 'a') == "a=0.0"
    assert quickTest("1000a + 2y + 3w = 4; 5a + 6y + 7w = 8; 10y = 12", simulSolver, 'y') == "y=1.2"
    assert quickTest("1000a + 2y + 3w = 4; 5a + 6y + 7w = 8; 10y = 12", simulSolver, 'w') == "w=0.11"


#################
# solvers.solve #
#################


def test_solveFor():

    assert quickTest("x - 1 + 2 = 0", solveFor, 'x') == "x=(-1.0)"
    assert quickTest("1 + y^2 = 0", solveFor, 'y') == "y=(-1.0)^(0.5)"
    assert quickTest("x^2 - 1 = 0", solveFor, 'x') == "x=(1.0)^(0.5)"

    assert quickTest("x - yz + 1= 0", solveFor, 'x') == "x=(-1.0+yz)"
    assert quickTest("x - 2yz + 1= 0", solveFor, 'y') == "y=-0.5*((-1.0-x)/z)"
    assert quickTest("x - 5yz + 1= 0", solveFor, 'z') == "z=-0.2*((-1.0-x)/y)"

    assert quickTest("w + x^2 + yz^3 = 1", solveFor, 'w') == "w=(-x^(2.0)-yz^(3.0)+1.0)"
    assert quickTest("w + x^2 + yz^3 = 1", solveFor, 'x') == "x=(-w-yz^(3.0)+1.0)^(0.5)"
    assert quickTest("w + x^2 + yz^3 = 1", solveFor, 'y') == "y=((-w-x^(2.0)+1.0)/z^(3.0))"
    assert quickTest("w + x^2 + yz^3 = 1", solveFor, 'z') == "z=((-w-x^(2.0)+1.0)/y)^(0.3333333333333333)"
