import copy

from visma.functions.structure import Function
from visma.functions.constant import Constant, Zero
from visma.functions.variable import Variable
from visma.functions.operator import Operator
from visma.solvers.solve import simplify_equation, tokens_to_string

###################
# Differentiation #
###################


def differentiate(lTokens, rTokens, wrtVar):

    lTokens, rTokens, availableOperations, \
      token_string, animation, comments \
      = simplify_equation(lTokens, rTokens)

    print animation
    print comments

    lTokens = (differentiateTokens(lTokens, wrtVar))

    tokenToStringBuilder = copy.deepcopy(lTokens)
    animation.append(copy.deepcopy(tokenToStringBuilder))
    token_string = tokens_to_string(tokenToStringBuilder)
    comments.append([])
    for token in lTokens:
        print token
    return lTokens, rTokens, [], token_string, animation, comments


def differentiateTokens(funclist, wrtVar):
    difffunc = []
    for func in funclist:
        if isinstance(func, Operator):  # add isFuntionOf
            difffunc.append(func)
        else:
            newfunc = []
            while(isinstance(func, Function)):
                funcCopy = copy.deepcopy(func)
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
                    newfunc.append(funcCopy)
                func.differentiate()
                if not(isinstance(func, Constant) and func.value == 1):
                    newfunc.append(func)

                # TODO: Send each of these steps to animator

                if func.operand is None:
                    break
                else:
                    func = func.operand
                    if isinstance(func, Constant):
                        func = Zero()
                        newfunc = [func]
                        break

            difffunc.extend(newfunc)

        # The differentiated function list has been generated in difffunc
        # FIXME: Find workaround for differentiating func1(func2+func3)
    return difffunc
