
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

	def get_level_variables():
		variables = []
		for i, term in enumerate(self.tokens):
			if term["type"] = 'variable':
				skip = False
				for var in variables:
					if var["value"] == term["value"]:
						var["power"].append(term["power"])
						if i != 0:
							if tokens[i-1]["type"] == 'binary':
								var["before"].append(tokens[i-1]["value"])
							else:
								var["before"].append('')
						else:
							var["before"].append('')

						if i+1 < len(self.tokens):
							if tokens[i+1]["type"] == 'binary':
								var["after"].append(tokens[i-1]["value"])
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
					var["power"].append(term["power"])
					if i != 0:
						if tokens[i-1]["type"] == 'binary':
							var["before"].append(tokens[i-1]["value"])
						else:
							var["before"].append('')
					else:
						var["before"].append('')

					if i+1 < len(self.tokens):
						if tokens[i+1]["type"] == 'binary':
							var["after"].append(tokens[i-1]["value"])
						else:
							var["after"].append('')
					else:
						var["after"].append('')


			
		
def check_types(lTokens, rTokens = 0):
	if len(rTokens) != 0:
		equationCompatibile = EquationCompatibility(lTokens, rTokens)
	else:
		expressionCompatible = ExpressionCompatibility(tokens)		

if __name__ == '__main__':
			check_types([])		