"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors:
Owner: AerospaceResearch.net
About: Module is still under development. It aims at integrating the input, will only take care of simple cases in starting.
Note: Please try to maintain proper documentation
Logic Description:
"""

import visma.simplify.simplify as ViSoSo
import copy


def integrate_variable(variable):
    if len(variable["value"]) == 1:
        if ViSoSo.isNumber(variable["power"][0]):
            if variable["power"][0] != -1:
                variable["power"][0] += 1
                variable["coefficient"] /= variable["power"][0]
                return variable
            else:
                variable["type"] = 'log'
                variable["power"] = 1
                return variable
    else:
        tokens = []
        for i in xrange(len(variable["value"])):
            if i != 0:
                binary = {}
                binary["type"] = 'binary'
                binary["value"] = '+'
                tokens.append(binary)
            var = copy.deepcopy(variable)
            var["power"][i] += 1
            var["coefficient"] /= var["power"][i]
            tokens.append(var)
        return tokens


def trigonometry(variable):
    if variable["type"] == 'cos':
        variable["type"] = 'sin'
        return variable
    elif variable["type"] == 'sin':
        variable["type"] = 'cos'
        variable["coefficient"] *= -1
        return variable
    elif variable["type"] == 'sec':
        if variable["power"] == 2:
            variable["power"] = 1
            variable["type"] = 'tan'
            return variable
    elif variable["type"] == 'cosec':
        if variable["power"] == 2:
            variable["power"] = 1
            variable["type"] = 'cot'
            variable["coefficient"] *= -1
        return variable


def hyperbolic(variable):
    if variable["type"] == 'sinh':
        variable["type"] = 'cosh'
        return variable
    elif variable["type"] == 'cosh':
        variable["type"] = 'sinh'
        return variable


def integrate_constant(constant, var):
    variable = {}
    variable["scope"] = constant["scope"]
    variable["coefficient"] = ViSoSo.evaluateConstant(constant)
    variable["value"] = [var]
    variable["power"] = [1]
    return variable


def integrate_tokens(tokens):
    # for token in tokens:
    # logic
    return tokens


def integrate(lTokens, rTokens):
    integratedLTokens = integrate_tokens(lTokens)
    integratedRTokens = integrate_tokens(rTokens)
    return integratedLTokens, integratedRTokens


if __name__ == '__main__':
    pass
