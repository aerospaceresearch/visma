from visma.transform.factorize import factorize
from tests.tester import quickTest

#######################
# transform.factorize #
#######################


def test_factorize():
    assert quickTest("x", factorize) == "x"
    assert quickTest("x^2 + 2x + 1", factorize) == "(x+1.0)*(x+1.0)"
    assert quickTest("2x^2 - 4x + 2", factorize) == "2.0*(x-1.0)*(x-1.0)"
    assert quickTest("x^4 - 1", factorize) == "(x-1.0)*(x+1.0)*(x^(2)+1.0)"
    assert quickTest("1 - x^3", factorize) == "(x-1.0)*(-x^(2)-x-1.0)"
