"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors: 
Owner: AerospaceResearch.net
About: Module is still under development. It aims at integrating the input, will only take care of simple cases in starting.
Note: Please try to maintain proper documentation
Logic Description:
"""
import solve

def integrate_variable(variable):
	if len(variable["value"]) == 1:
		if solve.is_number(variable["power"][0]):
			if variable["power"][0] != -1:
				variable["power"][0] += 1
				variable["coefficient"] /= variable["power"][0]
				return variable
			else:
				#log
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

def hyperbolic(variable):
	if variable["type"] == 'sinh':
		variable["type"] = 'cosh'
		return variable
	elif variable["type"] == 'cosh':
		variable["type"] = 'sinh'
		return variable
	return variable

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
