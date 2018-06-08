import copy

from visma.functions.structure import Function
from visma.functions.constant import Constant, Zero
from visma.functions.operator import Operator
from visma.simplify.simplify import simplify

###################
# Differentiation #
###################


def differentiate(tokens, wrtVar):

    tokens, availableOperations, token_string, animation, comments = simplify(tokens)

    tokens, animNew, commentsNew = (differentiateTokens(tokens, wrtVar))

    animation.append(animNew)
    comments.append(commentsNew)

    tokens, availableOperations, token_string, animation2, comments2 = simplify(tokens)

    return tokens, availableOperations, token_string, animation, comments


def differentiateTokens(funclist, wrtVar):
    diffFunc = []
    animNew = []
    commentsNew = ["Differentiating with respect to " + r"$" + wrtVar + r"$" + "\n"]
    for func in funclist:
        if isinstance(func, Operator):  # add isFuntionOf
            diffFunc.append(func)
        else:
            newfunc = []
            while(isinstance(func, Function)):
                commentsNew[0] += r"$" + "\\frac{d}{d" + wrtVar + "} ( " + func.__str__() + ")" + r"$"
                funcCopy = copy.deepcopy(func)
                if wrtVar in funcCopy.functionOf():
                    if not isinstance(funcCopy, Constant):
                        for i, var in enumerate(funcCopy.value):
                            if var == wrtVar:
                                funcCopy.coefficient *= funcCopy.power[i]
                                funcCopy.power[i] -= 1
                                if(funcCopy.power[i] == 0):
                                    del funcCopy.power[i]
                                    del funcCopy.value[i]
                                    if funcCopy.value == []:
                                        funcCopy.__class__ = Constant
                                        funcCopy.value = funcCopy.coefficient
                                        funcCopy.coefficient = 1
                                        funcCopy.power = 1
                        commentsNew[0] += r"$" + "= " + funcCopy.__str__() + "\ ;\ " + r"$"
                        newfunc.append(funcCopy)
                    func.differentiate()
                    if not(isinstance(func, Constant) and func.value == 1):
                        newfunc.append(func)
                else:
                    funcCopy = (Zero())
                    newfunc.append(funcCopy)
                    commentsNew[0] += r"$" + "= " + funcCopy.__str__() + "\ ;\ " + r"$"

                if func.operand is None:
                    break
                else:
                    func = func.operand
                    if isinstance(func, Constant):
                        diffFunc = Zero()
                        break

            diffFunc.extend(newfunc)

    animNew.extend(diffFunc)
    return diffFunc, animNew, commentsNew
