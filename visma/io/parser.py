def resultLatex(operation, equations, comments):

    equationLatex = []
    for eqTokens in equations:
        equationLatex.append(tokensToLatex(eqTokens))

    finalSteps = "INPUT: " + r"$" + equationLatex[0] + r"$" + "\n"
    finalSteps += "OPERATION: " + operation + "\n"
    finalSteps += "OUTPUT: " + r"$" + equationLatex[-1] + r"$" + "\n"*2

    for i in xrange(len(equationLatex)):
        if comments[i] != []:
            finalSteps += comments[i][0] + "\n"
        finalSteps += r"$" + equationLatex[i] + r"$" + "\n"*2

    return finalSteps


def tokensToLatex(eqTokens):
    eqLatex = ""
    for token in eqTokens:
        eqLatex += token.__str__()
    return eqLatex
