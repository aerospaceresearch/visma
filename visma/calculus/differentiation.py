import copy

from visma.functions.structure import Function
from visma.functions.constant import Constant, Zero
from visma.functions.operator import Operator
from visma.simplify.simplify import simplify


###################
# Differentiation #
###################


def differentiate(tokens, wrtVar):
    """Simplifies and then differentiates given tokens wrt given variable

    Arguments:
        tokens {list} -- list of function tokens
        wrtVar {string} -- with respect to variable

    Returns:
        tokens {list} -- list of differentiated tokens
        availableOperations {list} -- list of operations
        token_string {string} -- output equation string
        animation {list} -- equation tokens for step-by-step
        comments {list} -- comments for step-by-step
    """

    tokens, availableOperations, token_string, animation, comments = simplify(tokens)

    tokens, animNew, commentsNew = (differentiateTokens(tokens, wrtVar))

    animation.append(animNew)
    comments.append(commentsNew)

    tokens, availableOperations, token_string, animation2, comments2 = simplify(tokens)

    animation2.pop(0)
    comments2.pop(0)
    animation.extend(animation2)
    comments.extend(comments2)

    return tokens, availableOperations, token_string, animation, comments


def differentiateTokens(funcList, wrtVar):
    """Differentiates given tokens wrt given variable

    Arguments:

        funclist {list} -- list of function tokens
        wrtVar {string} -- with respect to variable

    Returns:
        diffFunc {list} -- list of differentiated tokens
        animNew {list} -- equation tokens for step-by-step
        commentsNew {list} -- comments for step-by-step
    """
    diffFunc = []
    animNew = []
    commentsNew = ["Differentiating with respect to " + r"$" + wrtVar + r"$" + "\n"]
    for func in funcList:
        if isinstance(func, Operator):
            diffFunc.append(func)
        else:
            newFunc = []
            while isinstance(func, Function):
                commentsNew[0] += r"$" + "\\frac{d}{d" + wrtVar + "} ( " + func.__str__() + ")" + r"$"
                funcCopy = copy.deepcopy(func)
                if wrtVar in funcCopy.functionOf():
                    if not isinstance(funcCopy, Constant):
                        for i, var in enumerate(funcCopy.value):
                            if var == wrtVar:
                                funcCopy.coefficient *= funcCopy.power[i]
                                funcCopy.power[i] -= 1
                                if funcCopy.power[i] == 0:
                                    del funcCopy.power[i]
                                    del funcCopy.value[i]
                                    if not funcCopy.value:
                                        funcCopy.__class__ = Constant
                                        funcCopy.value = funcCopy.coefficient
                                        funcCopy.coefficient = 1
                                        funcCopy.power = 1
                        commentsNew[0] += r"$" + r"= " + funcCopy.__str__() + r"\ ;\ " + r"$"  """" Was getting a Warning of *DeprecationWarning: invalid escape sequence* 
                                                                                                   solved by changing the string into a raw string. """
                        newFunc.append(funcCopy)
                    func.differentiate()
                    if not (isinstance(func, Constant) and func.value == 1):
                        newFunc.append(func)
                else:
                    funcCopy = (Zero())
                    newFunc.append(funcCopy)
                    commentsNew[0] += r"$" + r"= " + funcCopy.__str__() + r"\ ;\ " + r"$"

                if func.operand is None:
                    break
                else:
                    func = func.operand
                    if isinstance(func, Constant):
                        diffFunc = Zero()
                        break

            diffFunc.extend(newFunc)

    animNew.extend(diffFunc)
    return diffFunc, animNew, commentsNew
