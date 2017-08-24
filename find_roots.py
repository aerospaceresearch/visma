import solve
import math

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
	lTokens, rTokens, avaiableOperations, token_string, animation = solve.simplify_equation(lTokens, rTokens)
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
			imaginary = [-(coeffs[1]/(2 * coeffs[2])), d, (2 * coeffs[2])]
			roots = imaginary
	return roots
	
def quadratic_roots(lTokens, rTokens):
	lTokens, rTokens, availableOperations, token_string, animation = solve.simplify_equation(lTokens, rTokens)
	roots, variable = find_quadratic_roots(lTokens, rTokens)
	if len(roots) == 1:		
		tokens = []
		expression = {}
		expression["type"] = 'expression'
		expression["coefficient"] = 1
		expression["power"] = 2
 		variable = {}
		variable["type"] = 'variable'
		variable["value"] = variable
		variable["power"] = [1]
		variable["coefficient"] = 1
		tokens.append(variable)
		binary = {}
		binary["type"] = 'binary'
		if roots[0] < 0:
			binary["value"] = '+'
		else:
			binary["value"] = '-'	
		tokens.append(binary)
		constant = {}
		constant["type"] = 'constant'
		constant["value"] = roots[0]
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
		variable["value"] = variable
		variable["power"] = [1]
		variable["coefficient"] = 1
		tokens.append(variable)
		binary = {}
		binary["type"] = 'binary'
		if roots[0] < 0:
			binary["value"] = '+'
		else:
			binary["value"] = '-'	
		tokens.append(binary)
		constant = {}
		constant["type"] = 'constant'
		constant["value"] = roots[0]
		constant["power"] = 1
		tokens.append(constant)

		tokens2 = []
		expression2 = {}
		expression2["type"] = 'expression'
		expression2["coefficient"] = 1
		expression2["power"] = 1
 		variable2 = {}
		variable2["type"] = 'variable'
		variable2["value"] = variable
		variable2["power"] = [1]
		variable2["coefficient"] = 1
		tokens2.append(variable)
		binary2 = {}
		binary2["type"] = 'binary'
		if roots[1] < 0:
			binary2["value"] = '+'
		else:
			binary2["value"] = '-'	
		tokens.append(binary2)
		constant2 = {}
		constant2["type"] = 'constant'
		constant2["value"] = roots[1]
		constant2["power"] = 1
		tokens2.append(constant2)

		binary3 = {}
		binary3["type"] = 'binary'
		binary3["value"] = '*'
		lTokens = [expression, binary, expression2]
	
	elif len(roots) == 3:
		sqrtPow = {}
		sqrtPow["type"] = 'constant'
		sqrtPow["value"] = 2
		sqrtPow["power"] = 1
		tokens = []
		expression = {}
		expression["type"] = 'expression'
		expression["coefficient"] = 1
		expression["power"] = 1
 		variable = {}
		variable["type"] = 'variable'
		variable["value"] = variable
		variable["power"] = [1]
		variable["coefficient"] = 1
		tokens.append(variable)
		binary = {}
		binary["type"] = 'binary'
		binary["value"] = '+'
		tokens.append(binary)
		constant = {}
		constant["type"] = 'constant'
		constant["value"] = roots[1]
		constant["power"] = 1
		sqrt = {}
		sqrt["type"] = 'sqrt'
		sqrt["power"] = sqrtPow
		sqrt["expression"] = constant 
		tokens.append(constant)

		tokens2 = []
		expression2 = {}
		expression2["type"] = 'expression'
		expression2["coefficient"] = 1
		expression2["power"] = 1
 		variable2 = {}
		variable2["type"] = 'variable'
		variable2["value"] = variable
		variable2["power"] = [1]
		variable2["coefficient"] = 1
		tokens2.append(variable)
		binary2 = {}
		binary2["type"] = 'binary'
		binary2["value"] = '-'	
		tokens.append(binary2)
		constant2 = {}
		constant2["type"] = 'constant'
		constant2["value"] = roots[1]
		constant2["power"] = 1
		tokens2.append(constant2)

		binary3 = {}
		binary3["type"] = 'binary'
		binary3["value"] = '*'
		lTokens = [expression, binary, expression2]
	
	zero = {}
	zero["type"] = 'constant'
	zero["value"] = 0
	zero["power"] = 1
	rTokens = [zero] 

def find_quadratic_roots(lTokens, rTokens):
	roots = []
	if len(rTokens) > 0:
		lTokens, rTokens = move_rTokens_to_lTokens(lTokens, rTokens)
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
				return roots

	return get_roots(coeffs), avaiable_variables(lTokens)				

if __name__ == '__main__':
	pass
