
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
		self.variables.extend(self.get_level_variables())

	def get_level_variables(self):
		variables = []
		for i, term in enumerate(self.tokens):
			if term["type"] == 'variable':
				skip = False
				for var in variables:
					if var["value"] == term["value"]:
						var["power"].append(term["power"])
						if i != 0:
							if self.tokens[i-1]["type"] == 'binary':
								var["before"].append(self.tokens[i-1]["value"])
							else:
								var["before"].append('')
						else:
							var["before"].append('')

						if i+1 < len(self.tokens):
							if self.tokens[i+1]["type"] == 'binary':
								var["after"].append(self.tokens[i+1]["value"])
							else:
								var["after"].append('')
						else:
							var["after"].append('')
						skip = True
						break
				if not skip: 
					variable = {}
					variable["value"] = term["value"]
					variable["power"] = []
					variable["before"] = []
					variable["after"] = []
					variable["power"].append(term["power"])
					if i != 0:
						if self.tokens[i-1]["type"] == 'binary':
							variable["before"].append(self.tokens[i-1]["value"])
						else:
							variable["before"].append('')
					else:
						variable["before"].append('')

					if i+1 < len(self.tokens):
						if self.tokens[i+1]["type"] == 'binary':
							variable["after"].append(self.tokens[i+1]["value"])
						else:
							variable["after"].append('')
					else:
						variable["after"].append('')
					variables.append(variable)	
		print variables
		return variables
			
		
def check_types(lTokens=[{'coefficient': 1, 'scope': [0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [1], 'type': 'binary', 'value': '+'}, {'scope': [2], 'type': 'constant', 'value': 6}, {'scope': [3], 'type': 'binary', 'value': '/'}, {'scope': [4], 'type': 'constant', 'value': 3}, {'scope': [5], 'type': 'binary', 'value': '-'}, {'coefficient': 2, 'scope': [6], 'type': 'variable', 'power': [1], 'value': ['x']}], rTokens = []):
	if len(rTokens) != 0:
		equationCompatibile = EquationCompatibility(lTokens, rTokens)
	else:
		expressionCompatible = ExpressionCompatibility(lTokens)		

if __name__ == '__main__':
			check_types()		