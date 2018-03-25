"""
This file is to differentiate a function and is made along similar lines to that of integration.py
"""
import solve

def differntiate_variable(variable):
	if len(variable["value"]) == 1:
		if solve.is_number(variable["power"][0]):
			if variable["power"][0] != 0:
				variable["coefficient"] *= variable["power"][0]
				variable["power"][0] -= 1
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
			var["coefficient"] *= var["power"][i]
			var["power"][i] -= 1
			tokens.append(var)
		return tokens

def trigonometry(variable):
	if variable["type"] == 'cos':
		variable["type"] = 'sin'
		variable["coefficient"] *= -1
		return variable
	elif variable["type"] == 'sin':
		variable["type"] = 'cos'
		return variable
	elif variable["type"] == 'tan':
		if variable["power"] == 1:
			variable["power"] = 2
			variable["type"] = 'sec'
			return variable
	elif variable["type"] == 'cot':
		if variable["power"] == 1:
			variable["power"] = 2
			variable["type"] = 'cosec'
			variable["coefficient"] *= -1
			return variable
	return variable				

def differentiate_tokens(tokens):
	for token in tokens:
		pass

def differentiate(lTokens, rTokens):
	integratedLTokens = differentiate_tokens(lTokens)
	integratedRTokens = differentiate_tokens(rTokens)

	
if __name__ == '__main__':
	pass