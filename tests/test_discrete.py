from tests.tester import quickTest
from visma.discreteMaths.combinatorics import factorial, permutation, combination
from visma.discreteMaths.statistics import ArithemeticMean, Mode, Median


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


def test_statistics():

    assert quickTest([12, 1, -12, -1, 0], ArithemeticMean) == "0.0"
    assert quickTest([11, 1, -2, -1, 0], ArithemeticMean) == "1.8"

    assert quickTest([12, 12, 12, 12, 1, -12, -1, 0], Mode) == "Mode=12;ModeFrequency=4"
    assert quickTest([-1, -1, 2, 3, 4, 5, 6], Mode) == "Mode=-1;ModeFrequency=2"

    assert quickTest([1, 2, 3, 4, 5], Median) == "3"
    assert quickTest([1, 2, 3, 4, 5, 12], Median) == "3.5"
