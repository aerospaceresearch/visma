def is_number(term):
	if isinstance(term, int) or isinstance(term, float):
		return True
	else:	
	    x = 0
	    while x < len(term):
	        if term[x] < '0' or term[x] > '9':
	            return False
	        x += 1  
	    return True

class Linear(object):
	def __init__(self, tokens):
		super(ExpressionCompatibility, self).__init__()
		self.tokens = tokens


class EqautionCompatibility(object):
	def __init__(self, lTokens, rTokens):
		super(EquationCompatibility, self).__init__()
		self.lTokens = lTokens
		self.rTokens = rTokens

class ExpressionCompatibility(object):
	"""docstring for ExpressionCompatibility"""
	def __init__(self, tokens):
		super(ExpressionCompatibility, self).__init__()
		self.tokens = tokens
		self.variables = []
		self.variables.extend(self.get_level_variables(self.tokens))

	def get_level_variables(self, tokens):
		variables = []
		for i, term in enumerate(tokens):
			if term["type"] == 'variable':
				skip = False
				for var in variables:
					if var["value"] == term["value"]:
						var["power"].append(term["power"])
						if i != 0:
							if tokens[i-1]["type"] == 'binary':
								var["before"].append(tokens[i-1]["value"])
								var["before_scope"].append(tokens[i-1]["scope"])
							else:
								var["before"].append('')
								var["before_scope"].append('')
						else:
							var["before"].append('')
							var["before_scope"].append('')

						if i+1 < len(tokens):
							if tokens[i+1]["type"] == 'binary':
								var["after"].append(tokens[i+1]["value"])
								var["after_scope"].append(tokens[i+1]["scope"])
							else:
								var["after"].append('')
								var["after_scope"].append('')
						else:
							var["after"].append('')
							var["after_scope"].append('')
						skip = True
						break
				if not skip: 
					variable = {}
					variable["type"] = "variable"
					variable["value"] = term["value"]
					variable["power"] = []
					variable["before"] = []
					variable["before_scope"] = []
					variable["after"] = []
					variable["after_scope"] = []

					variable["power"].append(term["power"])
					if i != 0:
						if tokens[i-1]["type"] == 'binary':
							variable["before"].append(tokens[i-1]["value"])
							variable["before_scope"].append(tokens[i-1]["scope"])
						else:
							variable["before"].append('')
							variable["before_scope"].append('')
					else:
						variable["before"].append('')
						variable["before_scope"].append('')

					if i+1 < len(tokens):
						if tokens[i+1]["type"] == 'binary':
							variable["after"].append(tokens[i+1]["value"])
							variable["after_scope"].append(tokens[i+1]["scope"])
						else:
							variable["after"].append('')
							variable["after_scope"].append('')
					else:
						variable["after"].append('')
						variable["after_scope"].append('')
					variables.append(variable)
			elif term["type"] == 'constant':
				skip = False
				for var in variables:
					if isinstance(var["value"], list) and is_number(var["value"][0]):
						var["value"].append(term["value"])
						var["power"].append(1)
						if i != 0:
							if tokens[i-1]["type"] == 'binary':
								var["before"].append(tokens[i-1]["value"])
								var["before_scope"].append(tokens[i-1]["scope"])
							else:
								var["before"].append('')
								var["before_scope"].append('')
						else:
							var["before"].append('')
							var["before_scope"].append('')

						if i+1 < len(tokens):
							if tokens[i+1]["type"] == 'binary':
								var["after"].append(tokens[i+1]["value"])
								var["after_scope"].append(tokens[i+1]["scope"])
							else:
								var["after"].append('')
								var["after_scope"].append('')
						else:
							var["after"].append('')
							var["after_scope"].append('')
						skip = True
						break
				if not skip: 
					variable = {}
					variable["type"] = "constant"
					variable["value"] = [term["value"]]
					variable["power"] = []
					variable["before"] = []
					variable["before_scope"] = []
					variable["after"] = []
					variable["after_scope"] = []
					variable["power"].append(1)
					if i != 0:
						if tokens[i-1]["type"] == 'binary':
							variable["before"].append(tokens[i-1]["value"])
							variable["before_scope"].append(tokens[i-1]["scope"])
						else:
							variable["before"].append('')
							variable["before_scope"].append('')
					else:
						variable["before"].append('')
						variable["before_scope"].append('')

					if i+1 < len(tokens):
						if tokens[i+1]["type"] == 'binary':
							variable["after"].append(tokens[i+1]["value"])
							variable["after_scope"].append(tokens[i+1]["scope"])
						else:
							variable["after"].append('')
							variable["after_scope"].append('')
					else:
						variable["after"].append('')
						variable["after_scope"].append('')
					variables.append(variable)
			elif term["type"] == "expression":
				variable = {}
				variable["type"] = "expression"
				variable["value"] = self.get_level_variables(term["tokens"]) 

		print variables							
		return variables
			
		
def check_types(lTokens=[{'coefficient': 1, 'scope': [0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [1], 'type': 'binary', 'value': '+'}, {'scope': [2], 'type': 'constant', 'value': 6}, {'scope': [3], 'type': 'binary', 'value': '/'}, {'scope': [4], 'type': 'constant', 'value': 3}, {'scope': [5], 'type': 'binary', 'value': '-'}, {'coefficient': 2, 'scope': [6], 'type': 'variable', 'power': [1], 'value': ['x']}], rTokens = []):
	if len(rTokens) != 0:
		equationCompatibile = EquationCompatibility(lTokens, rTokens)
	else:
		expressionCompatible = ExpressionCompatibility(lTokens)		

if __name__ == '__main__':
			check_types()		