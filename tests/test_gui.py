from visma.gui.qsolver import quickSimplify

##############
# gui.logger #
##############


###############
# gui.plotter #
###############


###############
# gui.qsolver #
###############

def test_quickSimplify():
    # returns LaTeX output
    assert quickSimplify("") == ""
    assert quickSimplify("1+1") == "$ = \ {2.0} $"
    assert quickSimplify("x+") == "Invalid Expression"
    assert quickSimplify("x+(x") == "Too many '('"
    assert quickSimplify("x+(x)=y") == "$ \Rightarrow \ 2{x}-{y}={0} $"
