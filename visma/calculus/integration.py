import copy
from visma.functions.constant import Constant
from visma.functions.variable import Variable
from visma.functions.operator import Operator
from visma.simplify.simplify import simplify
from visma.functions.trigonometry import Sine, Cosine, Tangent, Cosecant, Secant, Cotangent

###############
# Integration #
###############


def integrate(tokens, wrtVar):
    """Simplifies and then integrates given tokens wrt given variable

    Arguments:
        tokens {list} -- list of function tokens
        wrtVar {string} -- with respect to variable

    Returns:
        tokens {list} -- list of integrated tokens
        availableOperations {list} -- list of operations
        token_string {string} -- output equation string
        animation {list} -- equation tokens for step-by-step
        comments {list} -- comments for step-by-step
    """

    tokens, availableOperations, token_string, animation, comments = simplify(tokens)
    tokens, animNew, commentsNew = (integrateTokens(tokens, wrtVar))
    animation.append(animNew)
    comments.append(commentsNew)
    tokens, availableOperations, token_string, animation2, comments2 = simplify(tokens)
    animation2.pop(0)
    comments2.pop(0)
    animation.extend(animation2)
    comments.extend(comments2)
    return tokens, availableOperations, token_string, animation, comments


# This is only applicable to Variable and Constant type
# Kind of hacky as of now
# Must be modified to accomodate other function types
# Have to add integrate class method to individual functions

def integrateTokens(funclist, wrtVar):
    """Integrates given tokens wrt given variable

    Arguments:
        funclist {list} -- list of function tokens
        wrtVar {string} -- with respect to variable

    Returns:
        intFunc {list} -- list of integrated tokens
        animNew {list} -- equation tokens for step-by-step
        commentsNew {list} -- comments for step-by-step
    """
    intFunc = []
    animNew = []
    commentsNew = ["Integrating with respect to " + r"$" + wrtVar + r"$" + "\n"]
    for func in funclist:
        if isinstance(func, Operator):  # add isfunctionOf
            intFunc.append(func)
        else:
            newfunc = []
            commentsNew[0] += r"$" + r"\int \ " + r"( " + func.__str__() + ")" + r" d" + wrtVar + r"$"
            funcCopy = copy.deepcopy(func)
            if wrtVar in funcCopy.functionOf():
                if isinstance(funcCopy, Variable):
                    log = False
                    funcCopy, log = funcCopy.integrate(wrtVar)
                    if log:
                        commentsNew[0] += r"$" + r"= " + funcCopy[0].__str__() + r"*" + funcCopy[2].__str__() + r"\ ;\ " + r"$"
                        newfunc.extend(funcCopy)
                    else:
                        commentsNew[0] += r"$" + r"= " + funcCopy.__str__() + r"\ ;\ " + r"$"
                        newfunc.append(funcCopy)
                elif isinstance(funcCopy, Sine) or isinstance(funcCopy, Cosine) or isinstance(funcCopy, Tangent) or isinstance(funcCopy, Cosecant) or isinstance(funcCopy, Secant) or isinstance(funcCopy, Cotangent):
                    funcCopy = funcCopy.integrate(wrtVar)
                    newfunc.append(funcCopy)
                    commentsNew[0] += r"$" + r"= " + funcCopy.__str__() + r"\ ;\ " + r"$"
            else:
                if isinstance(funcCopy, Variable):
                    funcCopy.value.append(wrtVar)
                    funcCopy.power.append(1)
                if isinstance(funcCopy, Constant):
                    coeff = funcCopy.value
                    funcCopy = Variable()
                    funcCopy.coefficient = coeff
                    funcCopy.value.append(wrtVar)
                    funcCopy.power.append(1)
                newfunc.append(funcCopy)
                commentsNew[0] += r"$" + r"= " + funcCopy.__str__() + r"\ ;\ " + r"$"
            intFunc.extend(newfunc)
    animNew.extend(intFunc)
    return intFunc, animNew, commentsNew
