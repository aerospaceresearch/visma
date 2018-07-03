from visma.io.tokenize import getTerms

###############
# io.checks #
###############


###############
# io.parser #
###############


###############
# io.tokenize #
###############

def test_getTerms():

    assert getTerms("1 + 2 * 3 - sqrt(2) / 5") == ['1', '+', '2', '*', '3', '-', 'sqrt', '(', '2', ')', '/', '5']
    assert getTerms("x + x^2*y + y^2 + y/z = -z") == ['x', '+', 'x', '^', '2', '*', 'y', '+', 'y', '^', '2', '+', 'y', '/', 'z', '=', '-', 'z']

    assert getTerms("sin^2(x) + cos^2(x) = 1") == ['sin', '^', '2', '(', 'x', ')', '+', 'cos', '^', '2', '(', 'x', ')', '=', '1']
    assert getTerms("1 + tan^2(x) = sec^2(x)") == ['1', '+', 'tan', '^', '2', '(', 'x', ')', '=', 'sec', '^', '2', '(', 'x', ')']
    assert getTerms("1 + cot^2(x) = csc^2(x)") == ['1', '+', 'cot', '^', '2', '(', 'x', ')', '=', 'csc', '^', '2', '(', 'x', ')']

    assert getTerms("cosh^2(x)-sinh^2(x)=1") == ['cosh', '^', '2', '(', 'x', ')', '-', 'sinh', '^', '2', '(', 'x', ')', '=', '1']
    assert getTerms("1 - tanh^2(x) = sech^2(x)") == ['1', '-', 'tanh', '^', '2', '(', 'x', ')', '=', 'sech', '^', '2', '(', 'x', ')']
    assert getTerms("coth^2(x)-csch^2(x)=1") == ['cot', 'h', '^', '2', '(', 'x', ')', '-', 'csch', '^', '2', '(', 'x', ')', '=', '1']

    assert getTerms("e = 2.71828") == ['exp', '=', '2.71828']
    assert getTerms("log(e) = 1") == ['log', '(', 'exp', ')', '=', '1']
    assert getTerms("e^(i*pi)=1") == ['exp', '^', '(', 'iota', '*', 'pi', ')', '=', '1']
