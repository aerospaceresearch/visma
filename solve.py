"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors: 
Owner: AerospaceResearch.net
About: This module aims to create a sort of middleware module to call other modules which can handle/solve different types of equations and 
	expressions.
Note: Please try to maintain proper documentation
Logic Description:
"""

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
		self.availableOperations = self.get_available_operations(self.variables)

	def get_available_operations(self, variables):
		operations = []


	def get_level_variables(self, tokens):
		variables = []
		for i, term in enumerate(tokens):
			if term["type"] == 'variable':
				skip = False
				for var in variables:
					if var["value"] == term["value"]:
						var["power"].append(term["power"])
						var["coefficient"].append(term["coefficient"])
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
					variable["coefficient"] = []
					variable["before"] = []
					variable["before_scope"] = []
					variable["after"] = []
					variable["after_scope"] = []
					variable["power"].append(term["power"])
					variable["coefficient"].append(term["coefficient"])
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
					variable["type"] = "constant"
					variable["value"] = [term["value"]]
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
			elif term["type"] == "expression":
				var = self.get_level_variables(term["tokens"])
				retType, val = self.extract_expression(var)
				if retType == "expression":
					variable = {}
					variable["type"] = "expression"
					variable["value"] = val
					variables.append(variable)
				elif retType == "constant":
					skip = False
					for var in variables:
						if isinstance(var["value"], list) and is_number(var["value"][0]):
							var["value"].append(val["value"])
							var["power"].append(val["power"])
							var["before"].append(val["before"])
							var["before_scope"].append(val["before_scope"])
							var["after"].append(val["after"])
							var["after_scope"].append(val["after_scope"])
							skip = True
							break
					if not skip: 
						var = {}
						var["type"] = "constant"
						var["value"] = [val["value"]]
						var["power"] = [val["power"]]
						var["before"] = [val["before"]]
						var["before_scope"] = [val["before_scope"]]
						var["after"] = [val["after"]]
						var["after_scope"] = [val["after_scope"]]
						variables.append(var)
				elif retType == "variable":
					skip = False
					for var in variables:
						if var["value"] == val["value"]:
							var["value"].append(val["value"])
							var["power"].append(val["power"])
							var["before"].append(val["before"])
							var["before_scope"].append(val["before_scope"])
							var["after"].append(val["after"])
							var["after_scope"].append(val["after_scope"])
							var["coefficient"].append(val["coefficient"])
							skip = True
							break
					if not skip: 
						var = {}
						var["type"] = "variable"
						var["coefficient"] = [val["coefficient"]]
						var["value"] = [val["value"]]
						var["power"] = [val["power"]]
						var["before"] = [val["before"]]
						var["before_scope"] = [val["before_scope"]]
						var["after"] = [val["after"]]
						var["after_scope"] = [val["after_scope"]]
						variables.append(var)


		print variables							
		return variables
			
	def extract_expression(self, variable):
		retType = ''
		if len(variable) == 1:
			if variable[0]["type"] == "expression":
				retType, variable = extract_expression(variable[0]["value"])
			elif variable[0]["type"] == "constant":
				return "constant", variable[0]
			elif variable[0]["type"] == "variable":
				return "variable", variable[0]
		else:
			retType = "mixed"


		
def check_types(lTokens=[{'coefficient': 1, 'scope': [0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [1], 'type': 'binary', 'value': '+'}, {'scope': [2], 'type': 'constant', 'power': 1, 'value': 6}, {'scope': [3], 'type': 'binary', 'value': '/'}, {'scope': [4], 'type': 'constant', 'power': 1, 'value': 3}, {'scope': [5], 'type': 'binary', 'value': '-'}, {'coefficient': 2, 'scope': [6], 'type': 'variable', 'power': [1], 'value': ['x']}], rTokens = []):
	if len(rTokens) != 0:
		equationCompatibile = EquationCompatibility(lTokens, rTokens)
	else:
		expressionCompatible = ExpressionCompatibility(lTokens)


if __name__ == '__main__':
			check_types()		