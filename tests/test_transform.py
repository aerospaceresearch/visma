from visma.transform.factorization import factorize
from visma.transform.substitution import substitute
from visma.io.parser import tokensToString
from visma.functions.structure import Expression
from tests.tester import quickTest, getTokens

###########################
# transform.factorization #
###########################


def test_factorize():
    assert quickTest("x", factorize) == "x"
    assert quickTest("x^2 + 2x + 1", factorize) == "(x+1.0)*(x+1.0)"
    assert quickTest("2x^2 - 4x + 2", factorize) == "2.0*(x-1.0)*(x-1.0)"
    assert quickTest("x^4 - 1", factorize) == "(x+1.0)*(x-1.0)*(x^(2)+1.0)"
    assert quickTest("1 - x^3", factorize) == "(x-1.0)*(-x^(2)-x-1.0)"
    assert quickTest("x^4 - 5x^2 + 4", factorize) == "(x+2.0)*(x+1.0)*(x-1.0)*(x-2.0)"


##########################
# transform.substitution #
##########################


def test_substitute():

    init_tok = getTokens("x")
    subs_tok = getTokens("2")
    tok_list = getTokens("3zx^2 + x^3 + 5x")
    assert tokensToString(substitute(init_tok, subs_tok, tok_list)) == "12.0z + 8.0 + 10.0"

    init_tok = getTokens("2x")
    subs_tok = getTokens("4yz^2")
    tok_list = getTokens("3 + 2x + zx^4 + 3xyz")
    assert tokensToString(substitute(init_tok, subs_tok, tok_list)) == "3.0 + 4.0yz^(2.0) + 16.0z^(9.0)y^(4.0) + 6.0y^(2.0)z^(3.0)"

    init_tok = getTokens("4x^2")
    subs_tok = getTokens("9yz")
    tok_list = getTokens("2x + zx^3 + 3xyz")
    assert tokensToString(substitute(init_tok, subs_tok, tok_list)) == "3.0y^(0.5)z^(0.5) + 3.375z^(2.5)y^(1.5) + 4.5y^(1.5)z^(1.5)"

    init_tok = getTokens("2xy^3")
    subs_tok = getTokens("4z")
    tok_list = getTokens("3 + 2xy^3 + z + 3x^(2)y^(6)z")
    assert tokensToString(substitute(init_tok, subs_tok, tok_list)) == "3.0 + 4.0z + z + 12.0z^(3.0)"

    init_tok = getTokens("5x")
    subs_tok = Expression(getTokens("y + 2"))
    tok_list = getTokens("3 + 4x + 2xy^3 + 3x^(2)y^(3)z")
    assert tokensToString(substitute(init_tok, subs_tok, tok_list)) == "3.0 + 0.8*(y + 2.0) + (0.4y^(3.0) * (y + 2.0)) + (0.12y^(3.0)z * (y + 2.0)^(2.0))"
