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
			d = math.sqrt(-d)
			imaginary = [-(coeffs[1]/(2 * coeffs[2])), d/(2 * coeffs[2])]
			roots.append(imaginary)
	return roots
	
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
							coeffs[token["power"][0]] += var
						else:
							return roots	
					else:
						return roots
			else:
				return roots

	return get_roots(coeffs), avaiable_variables(lTokens)				

if __name__ == '__main__':
	pass
