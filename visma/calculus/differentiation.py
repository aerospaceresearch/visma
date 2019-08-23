import copy

from visma.functions.structure import Function, Expression
from visma.functions.constant import Constant, Zero
from visma.functions.operator import Operator, Multiply, Plus
from visma.simplify.simplify import simplify
from visma.functions.variable import Variable
from visma.functions.exponential import Logarithm, Exponential
from visma.functions.trigonometry import Trigonometric
from visma.io.parser import tokensToString

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
    animation = []
    comments = []
    tokens, availableOperations, token_string, animation, comments = simplify(tokens)
    tokens, animNew, commentsNew = differentiateTokens(tokens, wrtVar)
    animation.append(animNew)
    comments.append(commentsNew)
    tokens, availableOperations, token_string, animation2, comments2 = simplify(tokens)
    animation2.pop(0)
    comments2.pop(0)
    animation.extend(animation2)
    comments.extend(comments2)
    return tokens, availableOperations, token_string, animation, comments


def differentiateTokens(funclist, wrtVar):
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
    for func in funclist:
        if isinstance(func, Operator):
            diffFunc.append(func)
        else:
            newExpression = Expression()
            newfunc = []
            while(isinstance(func, Function)):
                commentsNew[0] += r"$" + "\\frac{d}{d" + wrtVar + "} ( " + func.__str__() + ")" + r"$"
                funcCopy = copy.deepcopy(func)
                if wrtVar in funcCopy.functionOf():
                    if isinstance(funcCopy, Trigonometric) or isinstance(funcCopy, Logarithm) or isinstance(funcCopy, Variable) or isinstance(funcCopy, Exponential):
                        funcCopy = funcCopy.differentiate(wrtVar)
                        newfunc.append(funcCopy)
                        commentsNew[0] += r"$" + r"= " + funcCopy.__str__() + r"\ ;\ " + r"$"
                else:
                    funcCopy = Zero()
                    newfunc.append(funcCopy)
                    commentsNew[0] += r"$" + r"= " + funcCopy.__str__() + r"\ ;\ " + r"$"
                newfunc.append(Multiply())
                if func.operand is None:
                    break
                else:
                    func = func.operand
                    if isinstance(func, Constant):
                        diffFunc = Zero()
                        break
            newfunc.pop()
            newExpression.tokens = newfunc
            diffFunc.extend([newExpression])
    animNew.extend(diffFunc)
    return diffFunc, animNew, commentsNew


def differentiationProductRule(tokens, wrtVar):
    resultTokens = []
    for i in range(0, len(tokens), 2):
        currentDiff = Expression()
        currentDiffTokens, _, _, _, _ = differentiate([tokens[i]], wrtVar)
        currentDiff.tokens = currentDiffTokens
        tempTokens = copy.deepcopy(tokens)
        tempTokens[i] = currentDiff
        resultTokens.extend(tempTokens)
        resultTokens.append(Plus())
    resultTokens.pop()
    token_string = tokensToString(resultTokens)
    # TODO: Make simplify module to simplify expressions involving Trigonometric Expressions (to some extent)
    # resultTokens, _, token_string, _, _ = simplify(resultTokens)
    return tokens, [], token_string, [], []
