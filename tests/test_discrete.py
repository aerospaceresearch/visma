from tests.tester import quickTest
from visma.discreteMaths.combinatorics import factorial, permutation, combination


def test_factorial():

    assert quickTest("5", factorial) == "120.0"
    assert quickTest("0", factorial) == "1"
    assert quickTest("11", factorial) == "39916800.0"
    assert quickTest("11 - 11", factorial) == "1"


def test_permutation():

    assert quickTest("5;2", permutation) == "20.0"
    assert quickTest("12;3", permutation) == "1320.0"
    assert quickTest("10 + 2;5 - 2", permutation) == "1320.0"
    assert quickTest("11;11", permutation) == "39916800.0"


def test_combination():

    assert quickTest("5;2", combination) == "10.0"
    assert quickTest("2;2", permutation) == "2.0"
    assert quickTest("11;0", permutation) == "1.0"
    assert quickTest("11;11 - 11", permutation) == "1.0"
