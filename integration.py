import solve

def integrate_variable(coefficient, power):
	if solve.is_number(power):
		power += 1
		coefficient /= power
	return coefficient, power

def integrate_constant(constant, var):
	variable = {}
	variable["scope"] = constant["scope"]
	variable["coefficient"] = solve.evaluate_constant(constant)
	variable["value"] = [var]
	variable["power"] = [1]
	return variable

def integrate_tokens(tokens):
	for token in tokens:
		pass

def integrate(lTokens, rTokens):
	integratedLTokens = integrate_tokens(lTokens)
	integratedRTokens = integrate_tokens(rTokens)

	
if __name__ == '__main__':
	pass