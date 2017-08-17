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

def check_for_square_roots(lTokens, rTokens):
	lVariables = avaiable_variables(lTokens)
	rVariables = avaiable_variables(rTokens)
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

if __name__ == '__main__':
	pass