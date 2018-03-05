"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors:
Owner: AerospaceResearch.net
About: This module is aimed at first checking if quadratic roots can be found for the given equation, and then in the next step find the quadratic roots and display them.

Note: Please try to maintain proper documentation
Logic Description:
"""

from __future__ import division
import solve
import math
import copy

ROUND_OFF = 3

def avaiable_variables(tokens):
	variables = []
	for token in tokens:
		if token["type"] == 'variable':
			for val in token["value"]:
				if val not in variables:
					variables.append(val)
	return variables

def highest_power(tokens, variable):
	maxPow = 0
	for token in tokens:
		if token["type"] == 'variable':
			for i, val in enumerate(token["value"]):
				if val == variable:
					if token["power"][i] > maxPow:
						maxPow = token["power"][i]
	return maxPow

def preprocess_check_quadratic_roots(lTokens, rTokens):
	lTokens, rTokens, avaiableOperations, token_string, animation, comments = solve.simplify_equation(lTokens, rTokens)
	return check_for_quadratic_roots(lTokens, rTokens)

def check_for_quadratic_roots(lTokens, rTokens):
	lVariables = avaiable_variables(lTokens)
	rVariables = avaiable_variables(rTokens)
	for token in lTokens:
		if token["type"] == 'binary':
			if token["value"] in ['*', '/']:
				return False
	for token in rTokens:
		if token["type"] == 'binary':
			if token["value"] in ['*', '/']:
				return False

	if len(lVariables) == 1 and len(rVariables) == 1:
		if lVariables[0] == rVariables[0]:
			if highest_power(lTokens, lVariables[0]) == 2 or highest_power(rTokens, rVariables[0]) == 2:
				return True
	elif len(lVariables) == 1 and len(rVariables) == 0:
		if highest_power(lTokens, lVariables[0]) == 2:
			return True

	elif len(lVariables) == 0 and len(rVariables) == 1:
		if highest_power(lTokens, lVariables[0]) == 2:
			return True

	return False

def get_roots(coeffs):
	roots = []
	if len(coeffs) == 3:
		d = (coeffs[1] * coeffs[1]) - (4 * coeffs[0] * coeffs[2])
		if d == 0:
			roots.append(-(coeffs[1]/(2 * coeffs[2])))
		elif d > 0:
			d = math.sqrt(d)
			roots.append(-(coeffs[1] + d)/(2*coeffs[2]))
			roots.append(-(coeffs[1] - d)/(2*coeffs[2]))
		else:
			imaginary = [-(coeffs[1]/(2 * coeffs[2])), -1, (math.sqrt(-d))/(2 * coeffs[2])]
			roots = imaginary
	return roots

def quadratic_roots(lTokens, rTokens):
	lTokens, rTokens, availableOperations, token_string, animation, comments = solve.simplify_equation(lTokens, rTokens)
	roots, var = find_quadratic_roots(lTokens, rTokens)
	if len(roots) == 1:
		tokens = []
		expression = {}
		expression["type"] = 'expression'
		expression["coefficient"] = 1
		expression["power"] = 2
		variable = {}
		variable["type"] = 'variable'
		variable["value"] = var
		variable["power"] = [1]
		variable["coefficient"] = 1
		tokens.append(variable)
		binary = {}
		binary["type"] = 'binary'
		if roots[0] < 0:
			roots[0] *= -1
			binary["value"] = '+'
		else:
			binary["value"] = '-'
		tokens.append(binary)
		constant = {}
		constant["type"] = 'constant'
		constant["value"] = round(roots[0],ROUND_OFF)
		constant["power"] = 1
		tokens.append(constant)
		expression["tokens"] = tokens
		lTokens = [expression]

	elif len(roots) == 2:
		tokens = []
		expression = {}
		expression["type"] = 'expression'
		expression["coefficient"] = 1
		expression["power"] = 1
		variable = {}
		variable["type"] = 'variable'
		variable["value"] = var
		variable["power"] = [1]
		variable["coefficient"] = 1
		tokens.append(variable)
		binary = {}
		binary["type"] = 'binary'
		if roots[0] < 0:
			roots[0] *= -1
			binary["value"] = '+'
		else:
			binary["value"] = '-'
		tokens.append(binary)
		constant = {}
		constant["type"] = 'constant'
		constant["value"] = round(roots[0],ROUND_OFF)
		constant["power"] = 1
		tokens.append(constant)
		expression["tokens"] = tokens

		tokens2 = []
		expression2 = {}
		expression2["type"] = 'expression'
		expression2["coefficient"] = 1
		expression2["power"] = 1
		variable2 = {}
		variable2["type"] = 'variable'
		variable2["value"] = var
		variable2["power"] = [1]
		variable2["coefficient"] = 1
		tokens2.append(variable)
		binary2 = {}
		binary2["type"] = 'binary'
		if roots[1] < 0:
			roots[1] *= -1
			binary2["value"] = '+'
		else:
			binary2["value"] = '-'
		tokens2.append(binary2)
		constant2 = {}
		constant2["type"] = 'constant'
		constant2["value"] = round(roots[1],ROUND_OFF)
		constant2["power"] = 1
		tokens2.append(constant2)
		expression2["tokens"] = tokens2

		binary3 = {}
		binary3["type"] = 'binary'
		binary3["value"] = '*'
		lTokens = [expression, binary3, expression2]

	elif len(roots) == 3:
		sqrtPow = {}
		sqrtPow["type"] = 'constant'
		sqrtPow["value"] = 2
		sqrtPow["power"] = 1

		binary4 = {}
		binary4["type"] = 'binary'
		if roots[0] < 0:
			roots[0] *= -1
			binary4["value"] = '+'
		else:
			binary4["value"] = '-'

		constant3 = {}
		constant3["type"] = 'constant'
		constant3["value"] = round(roots[0],ROUND_OFF)
		constant3["power"] = 1

		binary5 = {}
		binary5["type"] = 'binary'
		binary5["value"] = '*'

		constant2 = {}
		constant2["type"] = 'constant'
		constant2["value"] = round(roots[2],ROUND_OFF)
		constant2["power"] = 1

		tokens = []
		expression = {}
		expression["type"] = 'expression'
		expression["coefficient"] = 1
		expression["power"] = 1
		variable = {}
		variable["type"] = 'variable'
		variable["value"] = var
		variable["power"] = [1]
		variable["coefficient"] = 1
		tokens.append(variable)
		tokens.append(binary4)
		tokens.append(constant3)
		binary = {}
		binary["type"] = 'binary'
		binary["value"] = '+'
		tokens.append(binary)
		tokens.append(constant2)
		tokens.append(binary5)
		constant = {}
		constant["type"] = 'constant'
		constant["value"] = round(roots[1],ROUND_OFF)
		constant["power"] = 1
		sqrt = {}
		sqrt["type"] = 'sqrt'
		sqrt["power"] = sqrtPow
		sqrt["expression"] = constant
		tokens.append(sqrt)
		expression["tokens"] = tokens

		tokens2 = []
		expression2 = {}
		expression2["type"] = 'expression'
		expression2["coefficient"] = 1
		expression2["power"] = 1
		variable2 = {}
		variable2["type"] = 'variable'
		variable2["value"] = var
		variable2["power"] = [1]
		variable2["coefficient"] = 1
		tokens2.append(variable)
		tokens2.append(binary4)
		tokens2.append(constant3)
		binary2 = {}
		binary2["type"] = 'binary'
		binary2["value"] = '-'
		tokens2.append(binary2)
		tokens2.append(constant2)
		tokens2.append(binary5)
		tokens2.append(sqrt)
		expression2["tokens"] = tokens2

		binary3 = {}
		binary3["type"] = 'binary'
		binary3["value"] = '*'
		lTokens = [expression, binary3, expression2]

	zero = {}
	zero["type"] = 'constant'
	zero["value"] = 0
	zero["power"] = 1
	rTokens = [zero]
	comments.append([])
	tokenToStringBuilder = copy.deepcopy(lTokens)
	l = len(lTokens)
	tokenToStringBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
	if len(rTokens) == 0:
		zero = {}
		zero["type"] = 'constant'
		zero["value"] = 0
		zero["power"] = 1
		zero["scope"] = [l+1]
		tokenToStringBuilder.append(zero)
	else:
		tokenToStringBuilder.extend(rTokens)
	animation.append(copy.deepcopy(tokenToStringBuilder))
	token_string = solve.tokens_to_string(tokenToStringBuilder)
	return lTokens, rTokens, [], token_string, animation, comments

def find_quadratic_roots(lTokens, rTokens):
	roots = []
	if len(rTokens) > 0:
		lTokens, rTokens = solve.move_rTokens_to_lTokens(lTokens, rTokens)
	coeffs = [0, 0, 0]
	for i, token in enumerate(lTokens):
		if token["type"] == 'constant':
			cons = solve.evaluate_constant(token)
			if i != 0:
				if lTokens[i-1]["type"] == 'binary':
					if lTokens[i-1]["value"] in ['-', '+']:
						if lTokens[i-1]["value"] == '-':
							cons *= -1
			if (i+1) < len(lTokens):
				if lTokens[i+1]["type"] not in ['*', '/']:
					coeffs[0] += cons
				else:
					return roots
			else:
				coeffs[0] += cons
		if token["type"] == 'variable':
			if len(token["value"]) == 1:
				var = token["coefficient"]
				if i != 0:
					if lTokens[i-1]["type"] == 'binary':
						if lTokens[i-1]["value"] in ['-', '+']:
							if lTokens[i-1]["value"] == '-':
								var *= -1
				if (i+1) < len(lTokens):
					if lTokens[i+1]["type"] not in ['*', '/']:
						if token["power"][0] == 1 or token["power"][0] == 2:
							coeffs[int(token["power"][0])] += var
						else:
							return roots
					else:
						return roots
				else:
					if token["power"][0] == 1 or token["power"][0] == 2:
						coeffs[int(token["power"][0])] += var
					else:
						return roots
			else:
				return roots

	return get_roots(coeffs), avaiable_variables(lTokens)

if __name__ == '__main__':
	pass
