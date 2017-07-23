"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors: 
Owner: AerospaceResearch.net
About: This module aims to create a sort of middleware module to call other modules which can handle/solve different types of equations and 
	expressions.
Note: Please try to maintain proper documentation
Logic Description:
"""

import math

def is_number(term):
	if isinstance(term, int) or isinstance(term, float):
		return True
	else:
	    x = 0
	    dot = 0
	    while x < len(term):
			if (term[x] < '0' or term[x] > '9') and (dot!= 0 or term[x] != '\.'):
				return False
			if term[x] == '.':
				dot += 1
			x += 1
	    return True
	return False

def get_num(term):
	return float(term)

def is_variable(term):
	if term in greek: 
		return True
	elif (term[0] >= 'a' and term[0] <= 'z') or (term[0] >= 'A' and term[0] <= 'Z'):
		x = 0
		while x < len(term):
			if term[x] < 'A' or (term[x] > 'Z' and term[x] < 'a') or term[x] > 'z':
				return False
			x += 1
		return True


class EqautionCompatibility(object):
	def __init__(self, lTokens, rTokens):
		super(EquationCompatibility, self).__init__()
		self.lTokens = lTokens
		self.rTokens = rTokens


class Expression(object):
	"""docstring for Expression"""
	def __init__(self, tokens, variables):
		super(Expression, self).__init__()
		self.tokens = tokens
		self.variables = variables

	
class ExpressionCompatibility(object):
	"""docstring for ExpressionCompatibility"""
	def __init__(self, tokens):
		super(ExpressionCompatibility, self).__init__()
		self.tokens = tokens
		self.variables = []
		self.variables.extend(get_level_variables(self.tokens))
		self.availableOperations = get_available_operations(self.variables, self.tokens)


def tokens_to_string(tokens):
	token_string = ''
	for i, token in tokens:
		if token["type"] == 'constant':
			if isinstance(token["value"], list):
				for j, val in token["value"]:
					token_string += (str(val) + '^{' + token["power"][j] + '} ')
			elif is_number(token["value"]):
				token_string += (str(token["value"]) + ' ^{' + token["power"] + '} ') 		
		elif token["type"] == 'variable':
			if token["coefficient"] == 1:
				pass
			elif token["coefficient"] == -1:
				token_string += ' -'
			else:
				token_string += str(token["coefficient"])	
			for j, val in token["value"]:
				token_string += (str(val) + '^{' + token["power"][j] + '} ')
		elif token["type"] == 'binary':
			token_string += str(token["value"])
		elif token["type"] == 'expression':
			token_string += tokens_to_string(token["tokens"])
	return token_string					 		

def test():
	tokens = [{'coefficient': 1, 'scope': [0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [1], 'type': 'binary', 'value': '+'}, {'scope': [2], 'type': 'constant', 'value': 6.0, 'power': 1}, {'scope': [3], 'type': 'binary', 'value': '/'}, {'scope': [4], 'type': 'constant', 'value': 3.0, 'power': 1}, {'scope': [5], 'type': 'binary', 'value': '+'}, {'scope': [6], 'type': 'constant', 'value': 2.0, 'power': 1}, {'scope': [7], 'type': 'binary', 'value': '-'}, {'coefficient': 2.0, 'scope': [8], 'type': 'variable', 'power': [1], 'value': ['x']}]
	variables = []
	variables.extend(get_level_variables(tokens))
	availableOperations = get_available_operations(variables, tokens)
	print variables, availableOperations
	var, tok, rem = expression_division(variables, tokens)
	print expression_addition(get_level_variables (remove_token(tok, rem)), tok)


def remove_token(tokens, scope, scope_times=0):
	for remScope in scope:
		for i, token in enumerate(tokens):
			if token["type"] == 'constant' or token["type"] == 'variable':
				if token["scope"] == remScope:
					tokens.pop(i)
					break
			elif token["type"] == 'binary':
				if token["scope"] == remScope:
					tokens.pop(i)
					break
			elif token["type"] == 'expression':
				if scope_times + 1 == len(remScope):
					if token["scope"] == remScope:
						tokens.pop(i)
						break
				elif token["scope"] == remScope[0:(scope_times+1)]:
					token["tokens"] = remove_token(token["tokens"], scope, scope_times + 1)
					break			
	return tokens

def change_token(tokens, variables, scope_times=0):
	for changeVariable in variables:
		for i, token in enumerate(tokens):
			if token["type"] == 'constant':
				if token["scope"] == changeVariable["scope"]:
					if "coefficient" in changeVariable:
						token["coefficient"] = changeVariable["coefficient"]
					token["power"] = changeVariable["power"]
					token["value"] = changeVariable["value"]
					break
			elif  token["type"] == 'variable':
				if token["scope"] == changeVariable["scope"]:
					token["coefficient"] = changeVariable["coefficient"]
					token["power"] = changeVariable["power"]
					token["value"] = changeVariable["value"]
					break		
			elif token["type"] == 'expression':
				if scope_times + 1 == len(changeVariable["scope"]):
					if token["scope"] == changeVariable["scope"]:
						break
				elif token["scope"] == changeVariable["scope"][0:(scope_times+1)]:
					token["tokens"] = change_token(token["tokens"], scope, scope_times + 1)
					break			
	return tokens

def expression_addition(variables, tokens):
	changeScopes = []
	removeScopes = []
	change = {}
	for i, variable in enumerate(variables):
		if variable["type"] == "constant":
			if len(variable["value"]) > 1:
				constantAdd = []
				constant = []
				for j in xrange(len(variable["value"])):
					if variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+']:
						constantAdd.append(j)
					elif variable["after"][j] in ['+','-',''] and variable["before"][j] in ['', '-']:
						constant.append(j)
				if len(constant) > 0 and len(constantAdd) > 0:
					i = 0
					while i < len(constantAdd):
						for const in constant:
							if variable["power"][constantAdd[i]] == variable["power"][const]:
								if variable["before"][const] == '-':
									variable["value"][const] -= variable["value"][constantAdd[i]]
								else:
									variable["value"][const] += variable["value"][constantAdd[i]]
								changeScopes.append(variable["scope"][const])
								change["power"] = variable["power"][const]
								change["value"] = variable["value"][const]
								removeScopes.append(variable["scope"][constantAdd[i]])
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								#TODO re-evaluate variable and tokens?
								return variables, tokens, removeScopes, changeScopes, change
						for const in constantAdd:
							if variable["power"][constantAdd[i]] == variable["power"][const]:
								variable["value"][const] += variable["value"][constantAdd[i]]
								changeScopes.append(variable["scope"][const])
								change["power"] = variable["power"][const]
								change["value"] = variable["value"][const]
								removeScopes.append(variable["scope"][constantAdd[i]])
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								return variables, tokens, removeScopes, changeScopes, change
						i += 1	
				elif len(constant) == 0 and len(constantAdd) > 1:
					i = 0
					while i < len(constantAdd):
						for j, const in enumerate(constantAdd):
							if i !=j:
								if variable["power"][constantAdd[i]] == variable["power"][const]:
									variable["value"][const] += variable["value"][constantAdd[i]]
									changeScopes.append(variable["scope"][const])
									change["power"] = variable["power"][const]
									change["value"] = variable["value"][const]
									removeScopes.append(variable["scope"][constantAdd[i]])
									removeScopes.append(variable["before_scope"][constantAdd[i]])
									return variables, tokens, removeScopes, changeScopes, change
						i += 1	

		elif variable["type"] == "variable":
			if len(variable["power"]) > 1:
				constantAdd = []
				constant = []
				for j in xrange(len(variable["value"])):
					if variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+']:
						constantAdd.append(j)
					elif variable["after"][j] in ['+','-',''] and variable["before"][j] in ['', '-']:
						constant.append(j)
				if len(constant) > 0 and len(constantAdd) > 0:
					i = 0
					while i < len(constantAdd):
						for const in constant:
							if variable["power"][constantAdd[i]] == variable["power"][const]:
								if variable["before"][const] == '-':
									variable["coefficient"][const] -= variable["coefficient"][constantAdd[i]]
								else:
									variable["coefficient"][const] += variable["coefficient"][constantAdd[i]]
								changeScopes.append(variable["scope"][const])
								change["power"] = variable["power"][const]
								change["value"] = variable["value"][const]
								change["coefficient"] = variable["coefficient"][const]
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								removeScopes.append(variable["scope"][constantAdd[i]])
								return variables, tokens, removeScopes, changeScopes, change
						for const in constantAdd:
							if variable["power"][constantAdd[i]] == variable["power"][const]:
								variable["coefficient"][const] += variable["coefficient"][constantAdd[i]]
								changeScopes.append(variable["scope"][const])
								change["power"] = variable["power"][const]
								change["value"] = variable["value"][const]
								change["coefficient"] = variable["coefficient"][const]
								removeScopes.append(variable["scope"][constantAdd[i]])
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								return variables, tokens, removeScopes, changeScopes, change		
						i += 1	
				elif len(constant) == 0 and len(constantAdd) > 1:
					i = 0
					while i < len(constantAdd):
						for j, const in enumerate(constantAdd):
							if i !=j:
								if variable["power"][constantAdd[i]] == variable["power"][const]:
									variable["value"][const] += variable["value"][constantAdd[i]]
									changeScopes.append(variable["scope"][const])
									change["power"] = variable["power"][const]
									change["value"] = variable["value"][const]
									change["coefficient"] = variable["coefficient"][const]
									removeScopes.append(variable["scope"][constantAdd[i]])
									removeScopes.append(variable["before_scope"][constantAdd[i]])
									return variables, tokens, removeScopes, changeScopes, change
						i += 1

		elif variable["type"] == "expression":
			pass
			

	return variables, tokens, removeScopes, changeScopes, change					

def expression_subtraction(variables, tokens):
	changeScopes = []
	removeScopes = []
	for i, variable in enumerate(variables):
		if variable["type"] == "constant":
			if len(variable["value"]) > 1:
				constantAdd = []
				constant = []
				for j in xrange(len(variable["value"])):
					if variable["after"][j] in ['+','-',''] and variable["before"][j] in ['-']:
						constantAdd.append(j)
					elif variable["after"][j] in ['+','-',''] and variable["before"][j] in ['', '+']:
						constant.append(j)
				if len(constant) > 0 and len(constantAdd) > 0:
					i = 0
					while i < len(constantAdd):
						for const in constant:
							if variable["power"][constantAdd[i]] == variable["power"][const]:
								variable["value"][const] -= variable["value"][constantAdd[i]]
								changeScopes.append(variable["scope"][const])
								change["power"] = variable["power"][const]
								change["value"] = variable["value"][const]
								removeScopes.append(variable["scope"][constantAdd[i]])
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								return variables, tokens, removeScopes, changeScopes, change
						for const in constantAdd:
							if variable["power"][constantAdd[i]] == variable["power"][const]:
								variable["value"][const] += variable["value"][constantAdd[i]]
								changeScopes.append(variable["scope"][const])
								change["power"] = variable["power"][const]
								change["value"] = variable["value"][const]
								removeScopes.append(variable["scope"][constantAdd[i]])
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								return variables, tokens, removeScopes, changeScopes, change
						i += 1	
				elif len(constant) == 0 and len(constantAdd) > 1:
					i = 0
					while i < len(constantAdd):
						for j, const in enumerate(constantAdd):
							if i !=j:
								if variable["power"][constantAdd[i]] == variable["power"][const]:
									variable["value"][const] += variable["value"][constantAdd[i]]
									changeScopes.append(variable["scope"][const])
									change["power"] = variable["power"][const]
									change["value"] = variable["value"][const]
									removeScopes.append(variable["scope"][constantAdd[i]])
									removeScopes.append(variable["before_scope"][constantAdd[i]])
									return variables, tokens, removeScopes, changeScopes, change
						i += 1	
							

		elif variable["type"] == "variable":
			if len(variable["power"]) > 1:
				constantAdd = []
				constant = []
				for j in xrange(len(variable["value"])):
					if variable["after"][j] in ['+','-',''] and variable["before"][j] in ['-']:
						constantAdd.append(j)
					elif variable["after"][j] in ['+','-',''] and variable["before"][j] in ['', '+']:
						constant.append(j)
				if len(constant) > 0 and len(constantAdd) > 0:
					i = 0
					while i < len(constantAdd):
						for const in constant:
							if variable["power"][constantAdd[i]] == variable["power"][const]:
								variable["coefficient"][const] -= variable["coefficient"][constantAdd[i]]
								changeScopes.append(variable["scope"][const])
								change["power"] = variable["power"][const]
								change["value"] = variable["value"][const]
								change["coefficient"] = variable["coefficient"][const]
								removeScopes.append(variable["scope"][constantAdd[i]])
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								return variables, tokens, removeScopes, changeScopes, change
						for const in constantAdd:
							if variable["power"][constantAdd[i]] == variable["power"][const]:
								variable["coefficient"][const] += variable["coefficient"][constantAdd[i]]
								changeScopes.append(variable["scope"][const])
								change["power"] = variable["power"][const]
								change["value"] = variable["value"][const]
								change["coefficient"] = variable["coefficient"][const]
								removeScopes.append(variable["scope"][constantAdd[i]])
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								return variables, tokens, removeScopes, changeScopes, change		
						i += 1	
				elif len(constant) == 0 and len(constantAdd) > 1:
					i = 0
					while i < len(constantAdd):
						for j, const in enumerate(constantAdd):
							if i !=j:
								if variable["power"][constantAdd[i]] == variable["power"][const]:
									variable["value"][const] += variable["value"][constantAdd[i]]
									changeScopes.append(variable["scope"][const])
									change["power"] = variable["power"][const]
									change["value"] = variable["value"][const]
									change["coefficient"] = variable["coefficient"][const]
									removeScopes.append(variable["scope"][constantAdd[i]])
									removeScopes.append(variable["before_scope"][constantAdd[i]])
									return variables, tokens, removeScopes, changeScopes, change
						i += 1
		elif variable["type"] == "expression":
			pass

	return variables, tokens, removeScopes, changeScopes, change					


def expression_multiplication(variables, tokens):
	changeScopes = []
	removeScopes = []
	for i, token in enumerate(tokens):
		if token["type"] == 'binary':
			if token["value"] in ['*']:
				prev = False
				nxt = False
				if i != 0:
					if tokens[i-1]["type"] in ["variable", "constant"]:
						prev = True
				if i+1 < len(tokens):
					if tokens[i+1]["type"] in ["variable", "constant"]:
						nxt = True
				if nxt and prev:
					if tokens[i+1]["type"] == "constant" and tokens[i-1]["type"] == "constant":
						no_1 = False
						no_2 = False
						if is_number(tokens[i-1]["value"]):
							no_1 = True
						if is_number(tokens[i+1]["value"]):
							no_2 = True
						if no_1 and no_2:
							tokens[i+1]["value"] = evaluate_constant(tokens[i-1]) * evaluate_constant(tokens[i+1]) 
							tokens[i+1]["power"] = 1
							removeScopes.append(tokens[i]["scope"])
							removeScopes.append(tokens[i-1]["scope"])
						elif no_1 and not no_2:
							tokens[i+1]["value"].append(tokens[i-1]["value"])
							tokens[i+1]["power"].append(tokens[i-1]["power"])
							removeScopes.append(tokens[i]["scope"])
							removeScopes.append(tokens[i-1]["scope"])
						elif not no_1 and no_2:	
							tokens[i-1]["value"].append(tokens[i+1]["value"])
							tokens[i-1]["power"].append(tokens[i+1]["power"])
							removeScopes.append(tokens[i]["scope"])
							removeScopes.append(tokens[i+1]["scope"])
						elif not no_1 and not no_2:
							for vals in tokens[i-1]["value"]:
								tokens[i+1]["value"].append(vals)
							for pows in tokens[i-1]["power"]:
								tokens[i+1]["power"].append(pows)
							removeScopes.append(tokens[i]["scope"])
							removeScopes.append(tokens[i-1]["scope"])	
						
						return variables, tokens, removeScopes

					elif tokens[i+1]["type"] == "variable" and tokens[i-1]["type"] == "variable":
						for j, var in enumerate(tokens[i+1]["value"]):
							found = False
							for k, var2 in enumerate(tokens[i-1]["value"]):
								if var == var2:
									if tokens[i+1]["power"][j] == tokens[i-1]["power"][k]:
										if is_number(tokens[i+1]["power"][j])  and is_number(tokens[i-1]["power"][k]):
											tokens[i-1]["power"][k] += tokens[i+1]["power"][j]
											found = True
											break
							if not found:
								tokens[i-1]["value"].append(tokens[i+1]["value"][j])				
								tokens[i-1]["power"].append(tokens[i+1]["power"][j])				
						removeScopes.append(tokens[i]["scope"])
						removeScopes.append(tokens[i+1]["scope"])
						return variables, tokens, removeScopes
					
					elif (tokens[i+1]["type"] == "variable" and tokens[i-1]["type"] == "constant"):
						tokens[i+1]["coefficient"] +=  evaluate_constant(tokens[i-1])
						removeScopes.append(tokens[i]["scope"])
						removeScopes.append(tokens[i-1]["scope"])
						return variables, tokens, removeScopes

					elif (tokens[i-1]["type"] == "variable" and tokens[i+1]["type"] == "constant"):
						tokens[i-1]["coefficient"] += evaluate_constant(tokens[i+1])
						removeScopes.append(tokens[i]["scope"])
						removeScopes.append(tokens[i+1]["scope"])
						return variables, tokens, removeScopes

	return variables, tokens, removeScopes


def expression_division(variables, tokens):
	changeScopes = []
	removeScopes = []
	for i, token in enumerate(tokens):
		if token["type"] == 'binary':
			if token["value"] in ['/']:
				prev = False
				nxt = False
				if i != 0:
					if tokens[i-1]["type"] in ["variable", "constant"]:
						prev = True
				if i+1 < len(tokens):
					if tokens[i+1]["type"] in ["variable", "constant"]:
						nxt = True		
				if nxt and prev:
					if tokens[i+1]["type"] == "constant" and tokens[i-1]["type"] == "constant":
						no_1 = False
						no_2 = False
						if is_number(tokens[i-1]["value"]):
							no_1 = True
						if is_number(tokens[i+1]["value"]):
							no_2 = True
						if no_1 and no_2:
							tokens[i+1]["value"] = evaluate_constant(tokens[i-1]) / evaluate_constant(tokens[i+1]) 
							tokens[i+1]["power"] = 1
							removeScopes.append(tokens[i]["scope"])
							removeScopes.append(tokens[i-1]["scope"])
						elif no_1 and not no_2:
							value = tokens[i-1]["value"]
							power = tokens[i-1]["power"]
							tokens[i-1]["value"] = [value]
							tokens[i-1]["power"] = [power]
							for val in tokens[i+1]["value"]:
								tokens[i-1]["value"].append(val)
							for pows in tokens[i+1]["power"]:
								tokens[i-1]["power"].append(-pows)
							removeScopes.append(tokens[i]["scope"])
							removeScopes.append(tokens[i+1]["scope"])	
						elif not no_1 and no_2:	
							tokens[i-1]["value"].append(tokens[i+1]["value"])
							tokens[i-1]["power"].append(-tokens[i+1]["power"])
							removeScopes.append(tokens[i]["scope"])
							removeScopes.append(tokens[i+1]["scope"])
						elif not no_1 and not no_2:
							for vals in tokens[i+1]["value"]:
								tokens[i-1]["value"].append(vals)
							for pows in tokens[i+1]["power"]:
								tokens[i-1]["power"].append(pows)
							removeScopes.append(tokens[i]["scope"])
							removeScopes.append(tokens[i+1]["scope"])	
						return variables, tokens, removeScopes

					elif tokens[i+1]["type"] == "variable" and tokens[i-1]["type"] == "variable":
						for j, var in enumerate(tokens[i+1]["value"]):
							found = False
							for k, var2 in enumerate(tokens[i-1]["value"]):
								if var == var2:
									if tokens[i+1]["power"][j] == tokens[i-1]["power"][k]:
										if is_number(tokens[i+1]["power"][j])  and is_number(tokens[i-1]["power"][k]):
											tokens[i-1]["power"][k] -= tokens[i+1]["power"][j]
											found = True
											break
							if not found:
								tokens[i-1]["value"].append(tokens[i+1]["value"][j])				
								tokens[i-1]["power"].append(-tokens[i+1]["power"][j])				

							removeScopes.append(tokens[i]["scope"])
							removeScopes.append(tokens[i+1]["scope"])
							return variables, tokens, removeScopes

					elif (tokens[i+1]["type"] == "variable" and tokens[i-1]["type"] == "constant"):
						val = evaluate_constant(tokens[i-1])
						scope = tokens[i-1]["scope"]
						tokens[i-1] = {}
						tokens[i-1]["value"] = tokens[i+1]["value"]
						tokens[i-1]["coefficient"] = tokens[i+1]["coefficient"]/val
						tokens[i-1]["power"] = []
						for pows in tokens[i+1]["power"]:
							tokens[i-1]["power"].append(pows)

						removeScopes.append(tokens[i]["scope"])
						removeScopes.append(tokens[i+1]["scope"])	
						return variables, tokens, removeScopes

					elif (tokens[i-1]["type"] == "variable" and tokens[i+1]["type"] == "constant"):
						tokens[i-1]["coefficient"] /= evaluate_constant(tokens[i+1])
						removeScopes.append(tokens[i]["scope"])
						removeScopes.append(tokens[i+1]["scope"])
						return variables, tokens, removeScopes
	return variables, tokens, removeScopes						

def evaluate_constant(constant):
	if is_number(constant["value"]):
		return math.pow(constant["value"], constant["power"])
	elif isinstance(constant["value"], list):
		val = 1
		if "coefficient" in constant:
			val*= constant["coefficient"]
		for i, c_val in enumerate(constant["value"]):
			val *= math.pow(c_val, constant["power"][i])
		return val		

def get_available_operations(variables, tokens):
	operations = []
	for i, token in enumerate(tokens):
		if token["type"] == 'binary':
			if token["value"] in ['*', '/']:
				prev = False
				nxt = False
				if i != 0:
					if tokens[i-1]["type"] in ["variable", "constant"]:
						prev = True
				if i+1 < len(tokens):
					if tokens[i+1]["type"] in ["variable", "constant"]:
						nxt = True
				if nxt and prev:
					op = token["value"]
					if not op in operations:
						operations.append(op)
	for i, variable in enumerate(variables):
		if variable["type"] == "constant":
			if len(variable["value"]) > 1:
				count = 0
				ops = []
				for j in xrange(len(variable["value"])):
					if variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+', '-']:
						count += 1
						if not (variable["before"][j] in ops):
							ops.append(variable["before"][j])
				if count > 1:
					for op in ops:
						if not op in operations:
							operations.append(op)			
		elif variable["type"] == "variable":
			if len(variable["power"]) > 1:
				count = 0
				ops = []
				power = []
				scope = []
				for j in xrange(len(variable["power"])):
					if variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+', '-']:
						count += 1
						if not (variable["before"][j] in ops):
							ops.append(variable["before"][j])
							power.append(variable["power"][j])		
				for i, op in enumerate(ops):
					if not (op in operations):
						operations.append(op)
								

		elif variable["type"] == "expression":
			ops = get_available_operations(variable["value"], variable["tokens"])
			for op in ops:
				if not op in operations:
					operations.append(op)			
	return operations								

def get_level_variables(tokens):
	variables = []
	for i, term in enumerate(tokens):
		if term["type"] == 'variable':
			skip = False
			for var in variables:
				if var["value"] == term["value"]:
					var["power"].append(term["power"])
					var["scope"].append(term["scope"])
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
				variable["scope"] = [term["scope"]]
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
					if var["power"][0] == term["power"]:
						var["value"].append(term["value"])
						var["power"].append(term["power"])
						var["scope"].append(term["scope"])
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
				variable["scope"] = [term["scope"]]
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
			var = get_level_variables(term["tokens"])
			retType, val = extract_expression(var)
			if retType == "expression":
				variable = {}
				variable["type"] = "expression"
				variable["value"] = val
				variable["tokens"] = term["tokens"]
				variables.append(variable)
			elif retType == "constant":
				skip = False
				for var in variables:
					if isinstance(var["value"], list) and is_number(var["value"][0]):
						if var["power"] == val["power"]:
							var["value"].append(val["value"])
							var["power"].append(val["power"])
							var["scope"].append(val["scope"])
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
					var["scope"] = [val["scope"]]
					var["before"] = [val["before"]]
					var["before_scope"] = [val["before_scope"]]
					var["after"] = []
					var["after_scope"] = ['']
					variables.append(var)
			elif retType == "variable":
				skip = False
				for var in variables:
					if var["value"] == val["value"]:
						var["power"].append(val["power"])
						var["before"].append('')
						var["before_scope"].append('')
						var["after"].append('')
						var["after_scope"].append('')
						var["coefficient"].append(val["coefficient"])
						var["scope"].append(val["scope"])
						skip = True
						break
				if not skip: 
					var = {}
					var["type"] = "variable"
					var["coefficient"] = [val["coefficient"]]
					var["value"] = val["value"]
					var["power"] = [val["power"]]
					var["scope"] = [val["scope"]]
					var["before"] = ['']
					var["before_scope"] = ['']
					var["after"] = ['']
					var["after_scope"] = ['']
					variables.append(var)
			elif retType == "mixed":
				for v in val:
					if v["type"] == "variable":
						for var in variables:
							if var["value"] == v["value"]:
								var["power"].extend(v["power"])
								var["before"].extend(v["before"])
								var["before_scope"].extend(v["before_scope"])
								var["after"].extend(v["after"])
								var["after_scope"].extend(v["after_scope"])
								var["coefficient"].extend(v["coefficient"])
								var["scope"].extend(v["scope"])
								skip = True
								break
						if not skip: 
							var = {}
							var["type"] = "variable"
							var["coefficient"] = [v["coefficient"]]
							var["value"] = v["value"]
							var["power"] = [v["power"]]
							var["scope"] = [v["scope"]]
							var["before"] = [v["before"]]
							var["before_scope"] = [v["before_scope"]]
							var["after"] = [v["after"]]
							var["after_scope"] = [v["after_scope"]]
							variables.append(var)
					elif v["type"] == "constant":
						for var in variables:
							if isinstance(var["value"], list) and is_number(var["value"][0]):
								if var["power"] == v["power"]:
									var["value"].extend(v["value"])
									var["power"].extend(v["power"])
									var["before"].extend(v["before"])
									var["before_scope"].extend(v["before_scope"])
									var["after"].extend(v["after"])
									var["after_scope"].extend(v["after_scope"])
									var["coefficient"].extend(v["coefficient"])
									var["scope"].extend(v["scope"])
									skip = True
									break
						if not skip: 
							var = {}
							var["type"] = "constant"
							var["coefficient"] = [v["coefficient"]]
							var["value"] = [v["value"]]
							var["power"] = [v["power"]]
							var["scope"] = [v["scope"]]
							var["before"] = [v["before"]]
							var["before_scope"] = [v["before_scope"]]
							var["after"] = [v["after"]]
							var["after_scope"] = [v["after_scope"]]
							variables.append(var)
					elif v["type"] == "expression":
						variables.append(v)		
					
	return variables

def extract_expression(variable):
	retType = ''
	if len(variable) == 1:
		if variable[0]["type"] == "expression":
			retType, variable = extract_expression(variable[0]["value"])
		elif variable[0]["type"] == "constant":
			return "constant", variable[0]
		elif variable[0]["type"] == "variable":
			return "variable", variable[0]
	else:
		val = []
		if not eval_expressions(variable):
			return "expression", get_level_variables(variable)
		else:
			return "mixed", get_level_variables(variable)

def eval_expressions(variables):
	constantCount = 0
	var = []
	varPowers = []
	for variable in variables:
		if variable["type"] == "expression":
			if eval_expressions(variable["tokens"]):
				return False
		elif variable["type"] == "variable":
			prev = False
			nxt = False
			if i != 0:
				if tokens[i-1]["type"] == 'binary':
					if tokens[i-1]["value"] in ['-', '+']:
						prev = True
				else:
					print tokens[i-1]
			else:
				prev = True
			
			if i+1 < len(tokens):
				if tokens[i+1]["type"] == 'binary':
					if tokens[i+1]["value"] in ['-', '+']:
						nxt = True
				else:
					print tokens[i+1]
			else:
				nxt = True
			if nxt and prev:
				match = False	
				for i, v in enumerate(var):
					if variable["value"] == v:
						for j, p in enumerate(varPowers[i]):
							if variable["power"] == p:
								return False
						varPowers[i].append(variable["power"])
						match = True
						break
				if not match:	
					var.append(variable["value"])
					varPowers.append([variable["power"]])
		elif variable["type"] == "constant":
			prev = False
			nxt = False
			if i != 0:
				if tokens[i-1]["type"] == 'binary':
					if tokens[i-1]["value"] in ['-', '+']:
						prev = True
				else:
					print tokens[i-1]
			else:
				prev = True
			
			if i+1 < len(tokens):
				if tokens[i+1]["type"] == 'binary':
					if tokens[i+1]["value"] in ['-', '+']:
						nxt = True
				else:
					print tokens[i+1]
			else:
				nxt = True
			if nxt and prev:
				match = False
				for i, v in enumerate(var):
					if isinstance(v["value"], list) and is_number(v["value"][0]):
						for j, p in enumerate(varPowers[i]):
							if variable["power"] == p:
								return False
						varPowers[i].append(variable["power"])
						match = True
						break
				if not match:	
					var.append([variable["value"]])			
					varPowers.append([variable["power"]])
	for i, variable in enumerate(variables):
		if variable["type"] == 'binary':
			prev = False
			nxt = False
			if variable["value"] in ['*', '/']:
				if i != 0:
					if variables[i-1]["type"] in ["variable", "constant"]:
						prev = True
				if i+1 < len(variables):
					if variables[i+1]["type"] in ["variable", "constant"]:
						nxt = True
				if prev and nxt:
					return False

	return True

def check_types(lTokens=[{'coefficient': 1, 'scope': [0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [1], 'type': 'binary', 'value': '+'}, {'scope': [2], 'type': 'constant', 'power': 1, 'value': 6}, {'scope': [3], 'type': 'binary', 'value': '/'}, {'scope': [4], 'type': 'constant', 'power': 1, 'value': 3}, {'scope': [5], 'type': 'binary', 'value': '-'}, {'coefficient': 2, 'scope': [6], 'type': 'variable', 'power': [1], 'value': ['x']}], rTokens = []):
	if len(rTokens) != 0:
		equationCompatibile = EquationCompatibility(lTokens, rTokens)
	else:
		expressionCompatible = ExpressionCompatibility(lTokens)
		return expressionCompatible.availableOperations

if __name__ == '__main__':
			#check_types()
			test()
