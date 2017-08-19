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
import copy

def is_number(term):
    if isinstance(term, int) or isinstance(term, float):
        return True
    else:
        x = 0
        dot = 0
        if term[0] == '-':
            x += 1
            while x < len(term):
                if (term[x] < '0' or term[x] > '9') and (dot!= 0 or term[x] != '.'):
                    return False
                if term[x] == '.':
                    dot += 1
                x += 1
            if x >= 2:
                return True
            else:
                    return False
        else:
            while x < len(term):
                if (term[x] < '0' or term[x] > '9') and (dot!= 0 or term[x] != '.'):
                    return False
                if term[x] == '.':
                    dot += 1
                x += 1  
        return True

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

def move_rTokens_to_lTokens(lTokens, rTokens):
	if len(lTokens) == 0 and len(rTokens) > 0:
		return rTokens, lTokens
	elif len(lTokens) != 0:
		for i, token in enumerate(rTokens):
			if i == 0:
				if token["type"] == 'binary':
					tempToken = copy.deepcopy(token)
					if token["value"] == '-':
						tempToken["value"] = '+'
					else: 
						tempToken["value"] = '-'
					lTokens.append(tempToken)		
				else:	
					binary = {}
					binary["type"] = 'binary'
					binary["value"] = '-'
					binary["scope"] = copy.copy(token["scope"])
					binary["scope"][-1] -= 1
					lTokens.append(binary)
					lTokens.append(token)
			else:
				if token["type"] == 'binary':
					if token["value"] in ['+', '-']:
						if token["value"] == '-':
							token["value"] = '+'
						else:
							token["value"] = '-'	
				lTokens.append(token)
									
	return lTokens, rTokens

class EquationCompatibility(object):
	def __init__(self, lTokens, rTokens):
		super(EquationCompatibility, self).__init__()
		self.lTokens = lTokens
		self.lVariables = []
		self.lVariables.extend(get_level_variables(self.lTokens))
		
		self.rTokens = rTokens
		self.rVariables = []
		self.rVariables.extend(get_level_variables(self.rTokens))
		self.availableOperations = []
		if check_solve_for(lTokens, rTokens):
			self.availableOperations.append('solve')
		self.availableOperations.extend(get_available_operations_equations(self.lVariables, self.lTokens, self.rVariables, self.rTokens))
		#print self.availableOperations
	
def find_solve_for(lTokens, rTokens=[], variables = []):	
	for i, token in enumerate(lTokens):
		if token["type"] == "variable":
			for val in token["value"]:
				if val not in variables:
					variables.append(val)
		elif token["type"] == "expression":
			variables.extend(find_solve_for(token["tokens"]))
	
	for i, token in enumerate(rTokens):
		if token["type"] == "variable":
			for val in token["value"]:
				if val not in variables:
					variables.append(val)
		elif token["type"] == "expression":
			variables.extend(find_solve_for(token["tokens"], [], variables))
	return variables

class ExpressionCompatibility(object):
	"""docstring for ExpressionCompatibility"""
	def __init__(self, tokens):
		super(ExpressionCompatibility, self).__init__()
		self.tokens = tokens
		self.variables = []
		self.variables.extend(get_level_variables(self.tokens))
		self.availableOperations = get_available_operations(self.variables, self.tokens)


def check_solve_for(lTokens, rTokens):
	for i, token in enumerate(lTokens):
		if token["type"] == 'variable':
			return True
		elif token["type"] == 'expression':
			if check_solve_for(token["tokens"]):
				return True	

	for i, token in enumerate(rTokens):
		if token["type"] == 'variable':
			return True
		elif token["type"] == 'expression':
			if check_solve_for(token["tokens"]):
				return True	

def tokens_to_string(tokens):
	token_string = ''
	for i, token in enumerate(tokens):
		if token["type"] == 'constant':
			if isinstance(token["value"], list):
				for j, val in token["value"]:
					token_string += (str(val) + '^{' + str(token["power"][j]) + '} ')
			elif is_number(token["value"]):
				token_string += (str(token["value"]) + '^{' + str(token["power"]) + '} ') 		
		elif token["type"] == 'variable':
			if token["coefficient"] == 1:
				pass
			elif token["coefficient"] == -1:
				token_string += ' -'
			else:
				token_string += str(token["coefficient"])	
			for j, val in enumerate(token["value"]):
				token_string += (str(val) + '^{' + str(token["power"][j]) + '} ')
		elif token["type"] == 'binary':
			token_string += ' ' + str(token["value"]) + ' '
		elif token["type"] == 'expression':
			token_string += tokens_to_string(token["tokens"])
	return token_string					 		

def test():
	tokens = [{'coefficient': 1, 'scope': [0], 'type': 'variable', 'power': [5.0], 'value': ['x']}, {'scope': [1], 'type': 'binary', 'value': '-'}, {'coefficient': 1, 'scope': [2], 'type': 'variable', 'power': [4.0], 'value': ['x']}]
	#tokens = [{'coefficient': 1, 'scope': [0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [1], 'type': 'binary', 'value': '+'}, {'scope': [2], 'type': 'constant', 'value': 6.0, 'power': 1}, {'scope': [3], 'type': 'binary', 'value': '/'}, {'scope': [4], 'type': 'constant', 'value': 3.0, 'power': 1}, {'scope': [5], 'type': 'binary', 'value': '+'}, {'scope': [6], 'type': 'constant', 'value': 2.0, 'power': 1}, {'scope': [7], 'type': 'binary', 'value': '-'}, {'coefficient': 2.0, 'scope': [8], 'type': 'variable', 'power': [1], 'value': ['x']}]
	variables = []
	variables.extend(get_level_variables(tokens))
	availableOperations = get_available_operations(variables, tokens)
	print variables, availableOperations
	#var, tok, rem, change = expression_subtraction(variables, tokens)
	#print tokens_to_string(change_token(remove_token(tok, rem), [change]))
	#print tokens_to_string(remove_token(tok, rem))


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

def simplify(tokens):
	tokens_orig = copy.deepcopy(tokens)
	animation = [tokens_orig]
	variables = []
	variables.extend(get_level_variables(tokens))
	availableOperations = get_available_operations(variables, tokens)
	while len(availableOperations)>0:
		if '/' in availableOperations:
			tokens_temp = copy.deepcopy(tokens)
			tokens, availableOperations, token_string, anim = division(tokens_temp)
			animation.pop(len(animation)-1)
			animation.extend(anim)
		elif '*' in availableOperations:
			tokens_temp = copy.deepcopy(tokens)
			tokens, availableOperations, token_string, anim = multiplication(tokens_temp)
			animation.pop(len(animation)-1)
			animation.extend(anim)
		elif '+' in availableOperations:
			tokens_temp = copy.deepcopy(tokens)
			tokens, availableOperations, token_string, anim = addition(tokens_temp)
			animation.pop(len(animation)-1)
			animation.extend(anim)
		elif '-' in availableOperations:
			tokens_temp = copy.deepcopy(tokens)
			tokens, availableOperations, token_string, anim = subtraction(tokens_temp)
			animation.pop(len(animation)-1)
			animation.extend(anim)
	token_string = tokens_to_string(tokens)
	return tokens, availableOperations, token_string, animation

def addition_equation(lToks, rToks):
	lTokens = copy.deepcopy(lToks)
	rTokens = copy.deepcopy(rToks)
	animation = []
	animBuilder = lToks
	l = len(lToks)
	animBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
	animBuilder.extend(rToks)
	animation.append(copy.deepcopy(animBuilder))
	lVariables = []
	lVariables.extend(get_level_variables(lTokens))
	rVariables = []
	rVariables.extend(get_level_variables(rTokens))
	availableOperations = get_available_operations(lVariables, lTokens)
	while '+' in availableOperations:
		var, tok, rem, change = expression_addition(lVariables, lTokens)
		lTokens = change_token(remove_token(tok, rem), [change])
		animBuilder = lTokens
		l = len(lTokens)
		animBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
		animBuilder.extend(rTokens)
		animation.append(copy.deepcopy(animBuilder))
		lVariables = get_level_variables(lTokens)
		availableOperations = get_available_operations(lVariables, lTokens)
	
	availableOperations = get_available_operations(rVariables, rTokens)
	while '+' in availableOperations:
		var, tok, rem, change = expression_addition(rVariables, rTokens)
		rTokens = change_token(remove_token(tok, rem), [change])
		animBuilder = lTokens
		l = len(lTokens)
		animBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
		animBuilder.extend(rTokens)
		animation.append(copy.deepcopy(animBuilder))
		rVariables = get_level_variables(rTokens)
		availableOperations = get_available_operations(rVariables, rTokens)

	#add function

	tokenToStringBuilder = lTokens
	l = len(lTokens)
	tokenToStringBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
	tokenToStringBuilder.extend(rTokens)
	token_string = tokens_to_string(tokenToStringBuilder)
	return	lTokens, rTokens, availableOperations, token_string, animation
			
def addition(tokens):
	animation = [copy.deepcopy(tokens)]
	variables = []
	variables.extend(get_level_variables(tokens))
	availableOperations = get_available_operations(variables, tokens)
	while '+' in availableOperations:
		var, tok, rem, change = expression_addition(variables, tokens)
		tokens = change_token(remove_token(tok, rem), [change])
		animation.append(tokens)
		variables = get_level_variables(tokens)
		availableOperations = get_available_operations(variables, tokens)
	token_string = tokens_to_string(tokens)
	return tokens, availableOperations, token_string, animation

def subtraction_equation(lToks, rToks):
	lTokens = copy.deepcopy(lToks)
	rTokens = copy.deepcopy(rToks)
	animation = []
	animBuilder = lToks
	l = len(lToks)
	animBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
	animBuilder.extend(rToks)
	animation.append(copy.deepcopy(animBuilder))
	lVariables = []
	lVariables.extend(get_level_variables(lTokens))
	rVariables = []
	rVariables.extend(get_level_variables(rTokens))
	availableOperations = get_available_operations(lVariables, lTokens)
	while '-' in availableOperations:
		var, tok, rem, change = expression_subtraction(lVariables, lTokens)
		lTokens = change_token(remove_token(tok, rem), [change])
		animBuilder = lTokens
		l = len(lTokens)
		animBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
		animBuilder.extend(rTokens)
		animation.append(copy.deepcopy(animBuilder))
		lVariables = get_level_variables(lTokens)
		availableOperations = get_available_operations(lVariables, lTokens)
	
	availableOperations = get_available_operations(rVariables, rTokens)
	while '-' in availableOperations:
		var, tok, rem, change = expression_subtraction(rVariables, rTokens)
		rTokens = change_token(remove_token(tok, rem), [change])
		animBuilder = lTokens
		l = len(lTokens)
		animBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
		animBuilder.extend(rTokens)
		animation.append(copy.deepcopy(animBuilder))
		rVariables = get_level_variables(rTokens)
		availableOperations = get_available_operations(rVariables, rTokens)

	#add function

	tokenToStringBuilder = lTokens
	l = len(lTokens)
	tokenToStringBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
	tokenToStringBuilder.extend(rTokens)
	token_string = tokens_to_string(tokenToStringBuilder)
	return	lTokens, rTokens, availableOperations, token_string, animation

def subtraction(tokens):
	animation = [copy.deepcopy(tokens)]
	variables = []
	variables.extend(get_level_variables(tokens))
	availableOperations = get_available_operations(variables, tokens)
	while '-' in availableOperations:
		var, tok, rem, change = expression_subtraction(variables, tokens)
		tokens = change_token(remove_token(tok, rem), [change])
		animation.append(tokens)
		variables = get_level_variables(tokens)
		availableOperations = get_available_operations(variables, tokens)
	token_string = tokens_to_string(tokens)	
	return tokens, availableOperations, token_string, animation

def division_equation(lToks, rToks):
	lTokens = copy.deepcopy(lToks)
	rTokens = copy.deepcopy(rToks)
	animation = []
	animBuilder = lToks
	l = len(lToks)
	animBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
	animBuilder.extend(rToks)
	animation.append(copy.deepcopy(animBuilder))
	lVariables = []
	lVariables.extend(get_level_variables(lTokens))
	rVariables = []
	rVariables.extend(get_level_variables(rTokens))
	availableOperations = get_available_operations(lVariables, lTokens)
	while '/' in availableOperations:
		var, tok, rem, change = expression_division(lVariables, lTokens)
		lTokens = change_token(remove_token(tok, rem), [change])
		animBuilder = lTokens
		l = len(lTokens)
		animBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
		animBuilder.extend(rTokens)
		animation.append(copy.deepcopy(animBuilder))
		lVariables = get_level_variables(lTokens)
		availableOperations = get_available_operations(lVariables, lTokens)
	
	availableOperations = get_available_operations(rVariables, rTokens)
	while '/' in availableOperations:
		var, tok, rem, change = expression_division(rVariables, rTokens)
		rTokens = change_token(remove_token(tok, rem), [change])
		animBuilder = lTokens
		l = len(lTokens)
		animBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
		animBuilder.extend(rTokens)
		animation.append(copy.deepcopy(animBuilder))
		rVariables = get_level_variables(rTokens)
		availableOperations = get_available_operations(rVariables, rTokens)

	#add function

	tokenToStringBuilder = lTokens
	l = len(lTokens)
	tokenToStringBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
	tokenToStringBuilder.extend(rTokens)
	token_string = tokens_to_string(tokenToStringBuilder)
	return	lTokens, rTokens, availableOperations, token_string, animation

def division(tokens):
	animation = [copy.deepcopy(tokens)]
	variables = []
	variables.extend(get_level_variables(tokens))
	availableOperations = get_available_operations(variables, tokens)
	while '/' in availableOperations:
		var, tok, rem = expression_division(variables, tokens)
		tokens = remove_token(tok, rem)
		animation.append(tokens)
		variables = get_level_variables(tokens)
		availableOperations = get_available_operations(variables, tokens)
	token_string = tokens_to_string(tokens)
	return tokens, availableOperations, token_string, animation

def multiplication_equation(lToks, rToks):
	lTokens = copy.deepcopy(lToks)
	rTokens = copy.deepcopy(rToks)
	animation = []
	animBuilder = lToks
	l = len(lToks)
	animBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
	animBuilder.extend(rToks)
	animation.append(copy.deepcopy(animBuilder))
	lVariables = []
	lVariables.extend(get_level_variables(lTokens))
	rVariables = []
	rVariables.extend(get_level_variables(rTokens))
	availableOperations = get_available_operations(lVariables, lTokens)
	while '*' in availableOperations:
		var, tok, rem, change = expression_multiplication(lVariables, lTokens)
		lTokens = change_token(remove_token(tok, rem), [change])
		animBuilder = lTokens
		l = len(lTokens)
		animBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
		animBuilder.extend(rTokens)
		animation.append(copy.deepcopy(animBuilder))
		lVariables = get_level_variables(lTokens)
		availableOperations = get_available_operations(lVariables, lTokens)
	
	availableOperations = get_available_operations(rVariables, rTokens)
	while '*' in availableOperations:
		var, tok, rem, change = expression_multiplication(rVariables, rTokens)
		rTokens = change_token(remove_token(tok, rem), [change])
		animBuilder = lTokens
		l = len(lTokens)
		animBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
		animBuilder.extend(rTokens)
		animation.append(copy.deepcopy(animBuilder))
		rVariables = get_level_variables(rTokens)
		availableOperations = get_available_operations(rVariables, rTokens)

	#add function

	tokenToStringBuilder = lTokens
	l = len(lTokens)
	tokenToStringBuilder.append({'scope': [l], 'type': 'binary', 'value': '='})
	tokenToStringBuilder.extend(rTokens)
	token_string = tokens_to_string(tokenToStringBuilder)
	return	lTokens, rTokens, availableOperations, token_string, animation

def multiplication(tokens):
	animation = [copy.deepcopy(tokens)]
	variables = []
	variables.extend(get_level_variables(tokens))
	availableOperations = get_available_operations(variables, tokens)
	while '*' in availableOperations:
		var, tok, rem = expression_multiplication(variables, tokens)
		tokens = remove_token(tok, rem)
		animation.append(tokens)
		variables = get_level_variables(tokens)
		availableOperations = get_available_operations(variables, tokens)
	token_string = tokens_to_string(tokens)
	return tokens, availableOperations, token_string, animation

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

def define_scope_variable(variable, scope):
	token = copy.deepcopy(variable)
	local_scope = copy.deepcopy(scope)
	if isinstance(token["value"], list):
		for j, val in enumerate(token["value"]):
			if val["type"] in ['binary', 'variable', 'constant', 'expression']:
				local_scope_value = copy.deepcopy(local_scope)
				local_scope_value.extend(-1)
				local_scope_value.extend(j)
				val["scope"] = local_scope_value

	if isinstance(token["power"], list):
		for j, val in enumerate(token["value"]):
			if val["type"] in ['binary', 'variable', 'constant', 'expression']:
				local_scope_value = copy.deepcopy(local_scope)
				local_scope_value.extend(-2)
				local_scope_value.extend(j)
				val["scope"] = local_scope_value

	return token

def define_scope_constant(constant, scope):
	token = copy.deepcopy(constant)
	local_scope = copy.deepcopy(scope)
	if isinstance(token["value"], list):
		for j, val in enumerate(token["value"]):
			if val["type"] in ['binary', 'variable', 'constant', 'expression']:
				local_scope_value = copy.deepcopy(local_scope)
				local_scope_value.extend(-1)
				local_scope_value.extend(j)
				val["scope"] = local_scope_value


	if isinstance(token["power"], list):
		for j, val in enumerate(token["value"]):
			if val["type"] in ['binary', 'variable', 'constant', 'expression']:
				local_scope_value = copy.deepcopy(local_scope)
				local_scope_value.extend(-2)
				local_scope_value.extend(j)
				val["scope"] = local_scope_value
	return token

def define_scope(tokens, scope=[]):
	i = 0
	for token in tokens:
		local_scope = copy.deepcopy(scope)
		local_scope.extend(i)
		token["scope"] = local_scope
		if token["type"] == 'variable':
			token = define_scope_variable(token, copy.deepcopy(local_scope))
		elif token["type"] == 'constant':
			token = define_scope_constant(token, copy.deepcopy(local_scope))
		elif token["type"] == 'expression':
			token["tokens"] = define_scope(token["tokens"], local_scope)
		elif token["type"] == 'binary':
			pass
		i += 1	
	return tokens				

def equation_addition(lVariables, lTokens, rVariables, rTokens):
	lRemoveScopes = []
	rRemoveScopes = []
	lChange = {}
	rChange = {}
	for i, variable in enumerate(lVariables):
		if variable["type"] == "constant":
			for j, val in enumerate(variable["value"]):
				if variable["before"][j] in ['-', '+'] and variable["after"][j] in ['+', '-','']:		
					for variable2 in rVariables:
						if variable2["type"] == 'constant':
							if variable2["power"][0] == variable["power"][0]:
								for k, val2 in enumerate(variable2["value"]):
									if variable2["before"][k] == '-' and variable2["after"][k] in ['-', '+', '']:
										if variable["before"][j] == '-':
											variable["value"][j] -= variable2["value"][k]
										else:
											variable["value"][j] += variable2["value"][k]
										if variable["value"][j] == 0:
											if variable["power"] == 0:
												variable["value"] = 1
												variable["power"] = 1
											else:
												lRemoveScopes.append(variable["scope"][j])
												lRemoveScopes.append(variable["before_scope"][j])
										else:
											lChange["scope"] = variable["scope"][j]
											lChange["power"] = variable["power"][j]
											lChange["value"] = variable["value"][j]

										rRemoveScopes.append(variable2["scope"][k])
										rRemoveScopes.append(variable2["before_scope"][k])
										return lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange											
		elif variable["type"] == "variable":
			for j, pow1 in enumerate(variable["power"]):
				if variable["before"][j] in ['-', '+'] and variable["after"][j] in ['+', '-','']:		
					for variable2 in rVariables:
						if variable2["type"] == 'variable':
							if variable2["power"][0] == variable["power"][0]:
								for k, pow2 in enumerate(variable2["value"]):
									if variable2["before"][k] == '-' and variable2["after"][k] in ['-', '+', '']:
										if variable["before"][j] == '-':
											variable["coefficient"][j] -= variable2["coefficient"][k]
										else:
											variable["coefficient"][j] += variable2["coefficient"][k]
										if variable["coefficient"][j] == 0:
											lRemoveScopes.append(variable["scope"][j])
											lRemoveScopes.append(variable["before_scope"][j])
										else:
											lChange["scope"] = variable["scope"][j]
											lChange["power"] = variable["power"][j]
											lChange["value"] = variable["value"][j]
											lChange["coefficient"] = variable["coefficient"][j]
										rRemoveScopes.append(variable2["scope"][k])
										rRemoveScopes.append(variable2["before_scope"][k])
										return lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange											


def expression_addition(variables, tokens):
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
								if variable["value"][const] == 0:
									if variable["power"][const] == 0:
										variable["value"][const] = 1
										variable["power"][const] = 1
										change["scope"] = variable["scope"][const]
										change["power"] = variable["power"][const]
										change["value"] = variable["value"][const]
									else:
										removeScopes.append(variable["scope"][const])
										removeScopes.append(variable["before_scope"][const])
								else:				
									change["scope"] = variable["scope"][const]
									change["power"] = variable["power"][const]
									change["value"] = variable["value"][const]
								removeScopes.append(variable["scope"][constantAdd[i]])
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								#TODO re-evaluate variable and tokens?
								return variables, tokens, removeScopes, change
						for const in constantAdd:
							if variable["power"][constantAdd[i]] == variable["power"][const]:
								variable["value"][const] += variable["value"][constantAdd[i]]
								if variable["value"][const] == 0:
									if variable["power"][const] == 0:
										variable["value"][const] = 1
										variable["power"][const] = 1
										change["scope"] = variable["scope"][const]
										change["power"] = variable["power"][const]
										change["value"] = variable["value"][const]
									else:
										removeScopes.append(variable["scope"][const])
										removeScopes.append(variable["before_scope"][const])
								else:
									change["scope"] = variable["scope"][const]
									change["power"] = variable["power"][const]
									change["value"] = variable["value"][const]
								removeScopes.append(variable["scope"][constantAdd[i]])
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								return variables, tokens, removeScopes, change
						i += 1	
				elif len(constant) == 0 and len(constantAdd) > 1:
					i = 0
					while i < len(constantAdd):
						for j, const in enumerate(constantAdd):
							if i !=j:
								if variable["power"][constantAdd[i]] == variable["power"][const]:
									variable["value"][const] += variable["value"][constantAdd[i]]
									if variable["value"][const] == 0:
										if variable["power"][const] == 0:
											variable["value"][const] = 1
											variable["power"][const] = 1
											change["scope"] = variable["scope"][const]
											change["power"] = variable["power"][const]
											change["value"] = variable["value"][const]
										else:
											removeScopes.append(variable["scope"][const])
											removeScopes.append(variable["before_scope"][const])
									else:
										change["scope"] = variable["scope"][const]
										change["power"] = variable["power"][const]
										change["value"] = variable["value"][const]
									removeScopes.append(variable["scope"][constantAdd[i]])
									removeScopes.append(variable["before_scope"][constantAdd[i]])
									return variables, tokens, removeScopes, change
						i += 1	

		elif variable["type"] == "variable":
			if len(variable["power"]) > 1:
				constantAdd = []
				constant = []
				for j in xrange(len(variable["power"])):
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
								if variable["coefficient"][const] == 0:
									removeScopes.append(variable["scope"][const])
									removeScopes.append(variable["before_scope"][const])
								else:
									change["scope"] = variable["scope"][const]
									change["power"] = variable["power"][const]
									change["value"] = variable["value"]
									change["coefficient"] = variable["coefficient"][const]
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								removeScopes.append(variable["scope"][constantAdd[i]])
								return variables, tokens, removeScopes, change
						for const in constantAdd:
							if variable["power"][constantAdd[i]] == variable["power"][const]:
								if variable["before"][const] == '-':
									variable["coefficient"][const] -= variable["coefficient"][constantAdd[i]]
								else:
									variable["coefficient"][const] += variable["coefficient"][constantAdd[i]]
								if variable["coefficient"][const] == 0:
									removeScopes.append(variable["scope"][const])
									removeScopes.append(variable["before_scope"][const])
								else:
									change["scope"] = variable["scope"][const]
									change["power"] = variable["power"][const]
									change["value"] = variable["value"]
									change["coefficient"] = variable["coefficient"][const]
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								removeScopes.append(variable["scope"][constantAdd[i]])
								return variables, tokens, removeScopes, change		
						i += 1	
				elif len(constant) == 0 and len(constantAdd) > 1:
					i = 0
					while i < len(constantAdd):
						for j, const in enumerate(constantAdd):
							if i !=j:
								if variable["power"][constantAdd[i]] == variable["power"][const]:
									variable["coefficient"][const] += variable["coefficient"][constantAdd[i]]
									if variable["coefficient"][const] == 0:
										removeScopes.append(variable["scope"][const])
										removeScopes.append(variable["before_scope"][const])
									else:
										change["scope"] = variable["scope"][const]
										change["power"] = variable["power"][const]
										change["value"] = variable["value"]
										change["coefficient"] = variable["coefficient"][const]
									removeScopes.append(variable["scope"][constantAdd[i]])
									removeScopes.append(variable["before_scope"][constantAdd[i]])
									return variables, tokens, removeScopes, change
						i += 1

		elif variable["type"] == "expression":
			pass

	return variables, tokens, removeScopes, change					

def equation_subtraction(lVariables, lTokens, rVariables, rTokens):
	lRemoveScopes = []
	rRemoveScopes = []
	lChange = {}
	rChange = {}
	for i, variable in enumerate(lVariables):
		if variable["type"] == "constant":
			for j, val in enumerate(variable["value"]):
				if variable["before"][j] in ['-', '+'] and variable["after"][j] in ['+', '-','']:		
					for variable2 in rVariables:
						if variable2["type"] == 'constant':
							if variable2["power"][0] == variable["power"][0]:
								for k, val2 in enumerate(variable2["value"]):
									if variable2["before"][k] in ['+', ''] and variable2["after"][k] in ['-', '+', '']:
										if variable["before"][j] == '-':
											variable["value"][j] += variable2["value"][k]
										else:
											variable["value"][j] -= variable2["value"][k]
										if variable["value"][j] == 0:
											if variable["power"] == 0:
												variable["value"] = 1
												variable["power"] = 1
											else:
												lRemoveScopes.append(variable["scope"][j])
												lRemoveScopes.append(variable["before_scope"][j])
										else:
											lChange["scope"] = variable["scope"][j]
											lChange["power"] = variable["power"][j]
											lChange["value"] = variable["value"][j]

										rRemoveScopes.append(variable2["scope"][k])
										rRemoveScopes.append(variable2["before_scope"][k])
										return lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange											
		elif variable["type"] == "variable":
			for j, pow1 in enumerate(variable["power"]):
				if variable["before"][j] in ['-', '+'] and variable["after"][j] in ['+', '-','']:		
					for variable2 in rVariables:
						if variable2["type"] == 'variable':
							if variable2["power"][0] == variable["power"][0]:
								for k, pow2 in enumerate(variable2["value"]):
									if variable2["before"][k] in ['+', ''] and variable2["after"][k] in ['-', '+', '']:
										if variable["before"][j] == '-':
											variable["coefficient"][j] += variable2["coefficient"][k]
										else:
											variable["coefficient"][j] -= variable2["coefficient"][k]
										if variable["coefficient"][j] == 0:
											lRemoveScopes.append(variable["scope"][j])
											lRemoveScopes.append(variable["before_scope"][j])
										else:
											lChange["scope"] = variable["scope"][j]
											lChange["power"] = variable["power"][j]
											lChange["value"] = variable["value"][j]
											lChange["coefficient"] = variable["coefficient"][j]
										rRemoveScopes.append(variable2["scope"][k])
										rRemoveScopes.append(variable2["before_scope"][k])
										return lVariables, lTokens, lRemoveScopes, lChange, rVariables, rTokens, rRemoveScopes, rChange											


def expression_subtraction(variables, tokens):
	removeScopes = []
	change = {}
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
								if variable["before"][const] == '+' or variable["before"][const] == '':
									variable["value"][const] -= variable["value"][constantAdd[i]]
								else:
									variable["value"][const] += variable["value"][constantAdd[i]]
								if variable["value"][const] == 0:
									if variable["power"][const] == 0:
										variable["value"][const] = 1
										variable["power"][const] = 1
									else:
										removeScopes.append(variable["scope"][const])
										removeScopes.append(variable["before_scope"][const])
								else:	
									change["scope"] = variable["scope"][const]
									change["power"] = variable["power"][const]
									change["value"] = variable["value"][const]
								removeScopes.append(variable["scope"][constantAdd[i]])
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								return variables, tokens, removeScopes, change
						for const in constantAdd:
							if variable["power"][constantAdd[i]] == variable["power"][const]:
								variable["value"][const] += variable["value"][constantAdd[i]]
								if variable["value"][const] == 0:
									if variable["power"][const] == 0:
										variable["value"][const] = 1
										variable["power"][const] = 1
									else:
										removeScopes.append(variable["scope"][const])
										removeScopes.append(variable["before_scope"][const])
								else:
									change["scope"] = variable["scope"][const]
									change["power"] = variable["power"][const]
									change["value"] = variable["value"][const]
								removeScopes.append(variable["scope"][constantAdd[i]])
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								return variables, tokens, removeScopes, change
						i += 1	
				elif len(constant) == 0 and len(constantAdd) > 1:
					i = 0
					while i < len(constantAdd):
						for j, const in enumerate(constantAdd):
							if i !=j:
								if variable["power"][constantAdd[i]] == variable["power"][const]:
									variable["value"][const] += variable["value"][constantAdd[i]]
									if variable["value"][const] == 0:
										if variable["power"][const] == 0:
											variable["value"][const] = 1
											variable["power"][const] = 1
										else:
											removeScopes.append(variable["scope"][const])
											removeScopes.append(variable["before_scope"][const])
									else:
										change["scope"] = variable["scope"][const]
										consthange["power"] = variable["power"][const]
										change["value"] = variable["value"][const]
									removeScopes.append(variable["scope"][constantAdd[i]])
									removeScopes.append(variable["before_scope"][constantAdd[i]])
									return variables, tokens, removeScopes, change
						i += 1	
							
		elif variable["type"] == "variable":
			if len(variable["power"]) > 1:
				constantAdd = []
				constant = []
				for j in xrange(len(variable["power"])):
					if variable["after"][j] in ['+','-',''] and variable["before"][j] in ['-']:
						constantAdd.append(j)
					elif variable["after"][j] in ['+','-',''] and variable["before"][j] in ['', '+']:
						constant.append(j)		
				if len(constant) > 0 and len(constantAdd) > 0:
					i = 0
					while i < len(constantAdd):
						for const in constant:
							if variable["power"][constantAdd[i]] == variable["power"][const]:
								if variable["before"][const] == '+' or variable["before"][const] == '':
									variable["coefficient"][const] -= variable["coefficient"][constantAdd[i]]
								else:
									variable["coefficient"][const] += variable["coefficient"][constantAdd[i]]
								if variable["coefficient"][const] == 0:
									removeScopes.append(variable["scope"][const])
									removeScopes.append(variable["before_scope"][const])
								else:
									change["scope"] = variable["scope"][const]
									change["power"] = variable["power"][const]
									change["value"] = variable["value"]
									change["coefficient"] = variable["coefficient"][const]
								removeScopes.append(variable["scope"][constantAdd[i]])
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								return variables, tokens, removeScopes, change
						for const in constantAdd:
							if variable["power"][constantAdd[i]] == variable["power"][const]:
								variable["coefficient"][const] += variable["coefficient"][constantAdd[i]]
								if variable["coefficient"][const] == 0:
									removeScopes.append(variable["scope"][const])
									removeScopes.append(variable["before_scope"][const])
								else:
									change["scope"] = variable["scope"][const]
									change["power"] = variable["power"][const]
									change["value"] = variable["value"]
									change["coefficient"] = variable["coefficient"][const]
								removeScopes.append(variable["scope"][constantAdd[i]])
								removeScopes.append(variable["before_scope"][constantAdd[i]])
								return variables, tokens, removeScopes, change		
						i += 1	
				elif len(constant) == 0 and len(constantAdd) > 1:
					i = 0
					while i < len(constantAdd):
						for j, const in enumerate(constantAdd):
							if i !=j:
								if variable["power"][constantAdd[i]] == variable["power"][const]:
									variable["coefficient"][const] += variable["coefficient"][constantAdd[i]]
									if variable["coefficient"][const] == 0:
										removeScopes.append(variable["scope"][const])
										removeScopes.append(variable["before_scope"][const])
									else:
										change["scope"] = variable["scope"][const]
										change["power"] = variable["power"][const]
										change["value"] = variable["value"]
										change["coefficient"] = variable["coefficient"][const]
									removeScopes.append(variable["scope"][constantAdd[i]])
									removeScopes.append(variable["before_scope"][constantAdd[i]])
									return variables, tokens, removeScopes, change
						i += 1
		elif variable["type"] == "expression":
			pass
	return variables, tokens, removeScopes, change					

def multiply_variables(variable1, variable2, coeff):
	variable = {}
	variable["value"] = []
	variable["value"].extend(variable1["value"])
	variable["power"] = []
	variable["power"].extend(variable1["power"])
	if is_number(variable1["coefficient"]):
		variable["coefficient"] = float(variable1["coefficient"])
	elif isinstance(variable1["coefficient"], dict):
		variable["coefficient"] = evaluate_constant(variable1["coefficient"])
	else:
		variable["coefficient"] = variable1["coefficient"]	
	removeScopes = []
	for j, var in enumerate(variable["value"]):
		found = False
		for k, var2 in enumerate(variable2["value"]):
			if var == var2:
				if is_number(variable["power"][j])  and is_number(variable2["power"][k]):
					variable["power"][j] += variable2["power"][k]
					found = True
					break
		if not found:
			variable["value"].append(variable2["value"][j])				
			variable["power"].append(variable2["power"][j])	
	variable["coefficient"] *= variable2["coefficient"]
	variable["coefficient"] *= coeff
	#removeScopes.append(tokens[i]["scope"])
	#removeScopes.append(tokens[i+1]["scope"])
	return variable

def multiply_constants(constant1, constant2, coeff):
	no_1 = False
	no_2 = False
	removeScopes = []
	constant = {}
	if is_number(constant1["value"]):
		no_1 = True
	if is_number(constant2["value"]):
		no_2 = True
	if no_1 and no_2:
		constant["value"] = evaluate_constant(constant1) * evaluate_constant(constant2) * coeff
		constant["power"] = 1
		#removeScopes.append(tokens[i]["scope"])
		#removeScopes.append(tokens[i-1]["scope"])
	elif no_1 and not no_2:
		constant["value"] = constant2["value"]
		constant["power"] = constant2["power"]
		done = False
		for i, val in enumerate(constant["value"]):
			if val == constant1["value"]:
				constant["power"][i] += constant1["power"]
				done = True
				break
		if not done:		
			constant["value"].append(constant1["value"])
			constant["power"].append(constant1["power"])
		constant["value"].append(coeff)
		constant["power"].append(1)
		#removeScopes.append(tokens[i]["scope"])
		#removeScopes.append(tokens[i-1]["scope"])
	elif not no_1 and no_2:	
		constant["value"] = constant1["value"]
		constant["power"] = constant1["power"]
		done = False
		for i, val in enumerate(constant["value"]):
			if val == constant2["value"]:
				constant["power"][i] += constant2["power"]
				done = True
				break
		if not done:		
			constant["value"].append(constant2["value"])
			constant["power"].append(constant2["power"])
		constant["value"].append(coeff)
		constant["power"].append(1)
		#removeScopes.append(tokens[i]["scope"])
		#removeScopes.append(tokens[i+1]["scope"])
	elif not no_1 and not no_2:
		constant["value"] = constant2["value"]
		constant["power"] = constant2["power"]
		for i, val in enumerate(constant1["value"]):
			done = False
			for j, val2 in enumerate(constant["value"]):
				if val == val2:
					constant["power"][j] += constant1["power"][i]
					done = True
					break
			if not done:
				constant["value"].append(val)
				constant["power"].append(constant1["power"][i])	 

		constant["value"].append(coeff)
		constant["power"].append(1)	
		#removeScopes.append(tokens[i]["scope"])
		#removeScopes.append(tokens[i-1]["scope"])	
	
	return constant

def multiply_variable_constant(constant, variable, coeff):	
	variable1 = {}
	variable1["value"] = []
	variable1["value"].extend(variable["value"])
	variable1["power"] = []
	variable1["power"].extend(variable["power"])
	if is_number(variable["coefficient"]):
		variable1["coefficient"] = float(variable["coefficient"])
	elif isinstance(variable["coefficient"], dict):
		variable1["coefficient"] = evaluate_constant(variable["coefficient"])
	else:
		variable["coefficient"] = variable1["coefficient"]	

	variable1["coefficient"] *=  evaluate_constant(constant)
	variable1["coefficient"] *= coeff
	#removeScopes.append(tokens[i]["scope"])
	#removeScopes.append(tokens[i-1]["scope"])
	return variable1

def multiply_expression_constant(constant, expression, coeff):
	tokens = copy.deepcopy(expression)
	tokens["coefficient"] *= (evaluate_constant(constant) * coeff)
	return tokens

def multiply_expression_variable(variable, expression, coeff):
	tokens = []
	for token in expression["tokens"]:
		if token["type"] == 'variable':
			tokens.append(multiply_variables(variable, token, expression["coefficient"]))
		elif token["type"] == 'constant':
			tokens.append(multiply_variable_constant(token, variable, expression["coefficient"]))
		elif token["type"] == 'expression':
			tokens.append(multiply_expression_variable(variable, token, expression["coefficient"]))
		elif token["type"] == 'binary':
			tokens.append(token)
	return tokens					

def multiply_select(token1, token2, coeff=1):
	if token1["type"] == "variable" and token2["type"] == "variable":
		return multiply_variables(token1, token2, coeff)
	elif token1["type"] == "variable" and token2["type"] == "constant":
		return multiply_variable_constant(token2, token1, coeff)
	elif token1["type"]	== "constant" and token2["type"] == "variable":
		return multiply_variable_constant(token1, token2, coeff)
	elif token1["type"]	== "constant" and token2["type"] == "constant":
		return multiply_constants(token1, token2, coeff)
 
def multiply_expressions(expression1, expression2):
	tokens = []
	tokens1 = expression1["tokens"]
	tokens2 = expression2["tokens"]
	coeff = expression1["coefficient"] * expression2["coefficient"]
	for i, token1 in enumerate(tokens1):
		#print token1["value"]
		op = 1
		if i != 0:
			if tokens1[i-1]["type"] == "binary":
				if tokens1[i-1]["value"] == '+':
					op *= 1
				elif tokens1[i-1]["value"] == '-':
					op *= -1	
		if token1["type"] == "variable" or token1["type"] == "constant":
			for j, token2 in enumerate(tokens2):
				#print token2["value"]
				op2 = op
				if token2["type"] == "variable" or token2["type"] == "constant":
					if j == 0 and i == 0:
						pass
					else:
						if j!= 0:
							if tokens2[j-1]["type"] == "binary":
								if tokens2[j-1]["value"] == "+":
									op2 *= 1
								elif tokens2[j-1]["value"] == "-":
									op2 *= -1					
						binary = {}
						binary["type"] = 'binary'
						if op2 == -1:
							binary["value"] = '-'
						elif op2 == 1:
							binary["value"] = '+'
						tokens.append(binary)				
					tokens.append(multiply_select(token1, token2, coeff))
					#print tokens
	print tokens				

def expression_multiplication(variables, tokens):
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
						tokens[i+1]["coefficient"] *=  evaluate_constant(tokens[i-1])
						removeScopes.append(tokens[i]["scope"])
						removeScopes.append(tokens[i-1]["scope"])
						return variables, tokens, removeScopes

					elif (tokens[i-1]["type"] == "variable" and tokens[i+1]["type"] == "constant"):
						tokens[i-1]["coefficient"] *= evaluate_constant(tokens[i+1])
						removeScopes.append(tokens[i]["scope"])
						removeScopes.append(tokens[i+1]["scope"])
						return variables, tokens, removeScopes

	return variables, tokens, removeScopes

def division_variables(variable1, variable2, coeff):
	variable = copy.deepcopy(variable1)	
	removeScopes = []
	for j, var in enumerate(variable["value"]):
		found = False
		for k, var2 in enumerate(variable2["value"]):
			if var == var2:
				if is_number(variable["power"][j])  and is_number(variable2["power"][k]):
					variable["power"][j] -= variable2["power"][k]
					found = True
					break
		if not found:
			variable["value"].append(variable2["value"][j])				
			variable["power"].append(-variable2["power"][j])	
	variable["coefficient"] /= variable2["coefficient"]
	variable["coefficient"] *= coeff
	#removeScopes.append(tokens[i]["scope"])
	#removeScopes.append(tokens[i+1]["scope"])
	return variable

def division_constants(constant1, constant2, coeff):
	no_1 = False
	no_2 = False
	removeScopes = []
	constant = {}
	if is_number(constant1["value"]):
		no_1 = True
	if is_number(constant2["value"]):
		no_2 = True
	if no_1 and no_2:
		constant["value"] = (evaluate_constant(constant1) / evaluate_constant(constant2)) * coeff
		constant["power"] = 1
		#removeScopes.append(tokens[i]["scope"])
		#removeScopes.append(tokens[i-1]["scope"])
	elif no_1 and not no_2:
		constant["value"] = [constant1["value"]]
		constant["power"] = [constant1["power"]]
		for i, val in enumerate(constant2["value"]):
			done = False
			for j, val2 in enumerate(constant["value"]):
				if val == val2:
					constant["power"][j] -= constant2["power"][i]
					done = True
					break
			if not done:
				constant["value"].append(val)
				constant["power"].append(-constant2["power"][i])

		constant["value"].append(coeff)
		constant["power"].append(1)
		#removeScopes.append(tokens[i]["scope"])
		#removeScopes.append(tokens[i-1]["scope"])
	elif not no_1 and no_2:	
		constant["value"] = constant1["value"]
		constant["power"] = constant1["power"]
		done = False
		for i, val in enumerate(constant["value"]):
			if val == constant2["value"]:
				constant["power"][i] -= constant2["power"]
				done = True
				break
		if not done:
			constant["value"].append(constant2["value"])
			constant["power"].append(-constant2["power"])
		constant["value"].append(coeff)
		constant["power"].append(1)
		#removeScopes.append(tokens[i]["scope"])
		#removeScopes.append(tokens[i+1]["scope"])
	elif not no_1 and not no_2:
		constant["value"] = constant1["value"]
		constant["power"] = constant1["power"]
		for i, val in enumerate(constant2["value"]):
			done = False
			for j, val2 in enumerate(constant["value"]):
				if val == val2:
					constant["power"][j] -= constant2["power"][i]
					done = True
					break
			if not done:
				constant["value"].append(val)
				constant["power"].append(-constant2["power"][i])		 
		constant["value"].append(coeff)
		constant["power"].append(1)	
		#removeScopes.append(tokens[i]["scope"])
		#removeScopes.append(tokens[i-1]["scope"])	
	
	return constant

def division_variable_constant(constant, variable, coeff):	
	variable1 = copy.deepcopy(variable)

	variable1["coefficient"] /=  evaluate_constant(constant)
	variable1["coefficient"] *= coeff
	#removeScopes.append(tokens[i]["scope"])
	#removeScopes.append(tokens[i-1]["scope"])
	return variable1

def division_constant_variable(constant, variable, coeff):
	variable1 = {}
	variable1["coefficient"] = (evaluate_constant(constant)/ variable["coefficient"]) * coeff
	variable1["value"] = []
	variable1["power"] = []
	for i, var in enumerate(variable):
		variable1["value"].append(var)
		variable1["power"].append(-variable["power"][i])
	return variable1

def division_expression_constant(constant, expression, coeff):
	tokens = copy.deepcopy(expression)
	tokens["coefficient"] /= (evaluate_constant(constant))
	tokens["coefficient"] *= coeff
	return tokens

def division_constant_expression(constant, expression, coeff):
	pass

def division_expression_variable(variable, expression, coeff):
	tokens = []
	for token in expression["tokens"]:
		if token["type"] == 'variable':
			tokens.append(division_variables(token, variable, expression["coefficient"]))
		elif token["type"] == 'constant':
			tokens.append(division_constant_variable(token, variable, expression["coefficient"]))
		elif token["type"] == 'expression':
			tokens.append(division_expression_variable(variable, token, expression["coefficient"]))
		elif token["type"] == 'binary':
			tokens.append(token)
	return tokens					

def division_variable_expression(variable, expression, coeff):
	pass	

def division_select(token1, token2, coeff=1):
	if token1["type"] == "variable" and token2["type"] == "variable":
		return division_variables(token1, token2, coeff)
	elif token1["type"] == "variable" and token2["type"] == "constant":
		return division_variable_constant(token2, token1, coeff)
	elif token1["type"]	== "constant" and token2["type"] == "variable":
		return division_variable_constant(token1, token2, coeff)
	elif token1["type"]	== "constant" and token2["type"] == "constant":
		return division_constants(token1, token2, coeff)
 
def division_expressions(expression1, expression2):
	pass

def expression_division(variables, tokens):
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
						tokens[i-1]["coefficient"] = val/tokens[i+1]["coefficient"]
						tokens[i-1]["power"] = []
						tokens[i-1]["type"] = 'variable'
						tokens[i-1]["scope"] = scope
						for pows in tokens[i+1]["power"]:
							tokens[i-1]["power"].append(-pows)

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
	if is_number(constant):
		return constant
	elif isinstance(constant, dict):	
		if is_number(constant["value"]):
			return math.pow(constant["value"], constant["power"])
		elif isinstance(constant["value"], list):
			val = 1
			if "coefficient" in constant:
				val*= constant["coefficient"]
			for i, c_val in enumerate(constant["value"]):
				val *= math.pow(c_val, constant["power"][i])
			return val		
							
def get_available_operations_equations(lVariables, lTokens, rVariables, rTokens):
	operations = []
	for i, token in enumerate(lTokens):
		if token["type"] == 'binary':
			if token["value"] in ['*', '/']:
				prev = False
				nxt = False
				if i != 0:
					if lTokens[i-1]["type"] in ["variable", "constant"]:
						prev = True
				if i+1 < len(lTokens):
					if lTokens[i+1]["type"] in ["variable", "constant"]:
						nxt = True	
				if nxt and prev:
					op = token["value"]
					if not op in operations:
						operations.append(op)

	for i, token in enumerate(rTokens):
		if token["type"] == 'binary':
			if token["value"] in ['*', '/']:
				prev = False
				nxt = False
				if i != 0:
					if rTokens[i-1]["type"] in ["variable", "constant"]:
						prev = True
				if i+1 < len(rTokens):
					if rTokens[i+1]["type"] in ["variable", "constant"]:
						nxt = True	
				if nxt and prev:
					op = token["value"]
					if not op in operations:
						operations.append(op)

	for i, variable in enumerate(lVariables):
		if variable["type"] == "constant":
			rCount = 0
			for variable2 in rVariables:
				if variable2["type"] == 'constant':
					if variable2["power"][0] == variable["power"][0]: 
						rCount += len(variable2["value"])
						break
			count = 0
			opCount = 0
			ops = []

			if len(variable["value"]) > 1:
				for j in xrange(len(variable["value"])):
					if variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+', '-']:
						count += 1
						opCount += 1
						if not (variable["before"][j] in ops):
							ops.append(variable["before"][j])
					elif variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+', '-', '']:
						count += 1			
			else:
				if variable["after"][0] in ['+','-',''] and variable["before"][0] in ['+', '-', '']:
					count += 1			
			
			if (len(variable["value"]) > 0 and rCount > 0):
				for k, variable2 in enumerate(rVariables):
					if variable2["type"] == 'constant':
						for l in xrange(len(variable2["value"])):
							if variable2["after"][l] in ['+', '-', ''] and variable2["before"][l] in ['+', '-', '']:
								count += 1
								opCount += 1
								tempOp = '+'
								if variable2["before"][l] == '+' or (variable2["before"][l] == '' and get_num(variable2["value"][l]) > 0):
									tempOp = '-'
								else:
									tempOp = '+'
								if not (tempOp in ops):
									ops.append(tempOp)

			if count > 1 and opCount > 0:
				for op in ops:
					if not op in operations:
						operations.append(op)

		elif variable["type"] == "variable":
			rCount = 0
			for variable2  in rVariables:
				if variable2["type"] == 'variable':
					if variable2["value"] == variable["value"]:
						if variable2["power"][0] == variable["power"][0]: 
							rCount += len(variable2["value"])
							break
			count = 0
			ops = []
			power = []
			scope = []
			opCount = 0			
			if len(variable["power"]) > 1:
				for j in xrange(len(variable["power"])):
					if variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+', '-']:
						count += 1
						opCount += 1						
						if not (variable["before"][j] in ops):
							ops.append(variable["before"][j])
							power.append(variable["power"][j])
					elif variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+', '-', '']:
						count += 1
			else:
				if variable["after"][0] in ['+','-',''] and variable["before"][0] in ['+', '-', '']:
					count += 1			

			if len(variable["power"]) > 0 and rCount > 0:
				for k, variable2 in enumerate(rVariables):
					if variable2["type"] == 'variable':
						if variable2["value"] == variable["value"] and variable2["power"][0] == variable["power"][0]:
							for l in xrange(len(variable2["power"])):
								if variable2["after"][l] in ['+','-',''] and variable2["before"][l] in ['+', '-', '']:
									count += 1
									opCount += 1
									tempOp = '+'
									if variable2["before"][l] == '+' or variable2["before"][l] == '':
										tempOp = '-'
									else:
										tempOp = '+'		
									if not (tempOp in ops):
										ops.append(tempOp)
										power.append(variable2["power"][l])

			if count > 1 and opCount > 0:					
				for i, op in enumerate(ops):
					if not (op in operations):
						operations.append(op)
									

		elif variable["type"] == "expression":
			ops = get_available_operations(variable["value"], variable["tokens"])
			for op in ops:
				if not op in operations:
					operations.append(op)

	for i, variable in enumerate(rVariables):
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
				opCount = 0
				for j in xrange(len(variable["power"])):
					if variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+', '-']:
						count += 1
						opCount += 1						
						if not (variable["before"][j] in ops):
							ops.append(variable["before"][j])
							power.append(variable["power"][j])
					elif variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+', '-', '']:
						count += 1

				if count > 1 and opCount > 0:					
					for i, op in enumerate(ops):
						if not (op in operations):
							operations.append(op)
									

		elif variable["type"] == "expression":
			ops = get_available_operations(variable["value"], variable["tokens"])
			for op in ops:
				if not op in operations:
					operations.append(op)

								
	return operations								


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
				opCount = 0
				ops = []
				for j in xrange(len(variable["value"])):
					if variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+', '-']:
						count += 1
						opCount += 1
						if not (variable["before"][j] in ops):
							ops.append(variable["before"][j])
					elif variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+', '-', '']:
						count += 1
		
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
				opCount = 0
				for j in xrange(len(variable["power"])):
					if variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+', '-']:
						count += 1
						opCount += 1						
						if not (variable["before"][j] in ops):
							ops.append(variable["before"][j])
							power.append(variable["power"][j])
					elif variable["after"][j] in ['+','-',''] and variable["before"][j] in ['+', '-', '']:
						count += 1

				if count > 1 and opCount > 0:					
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
					if var["power"][0] == term["power"]:
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
		return equationCompatibile.availableOperations, "equation"
	else:
		expressionCompatible = ExpressionCompatibility(lTokens)
		return expressionCompatible.availableOperations, "expression"

if __name__ == '__main__':
			#check_types()
			#test()
			
			multiply_expressions({'tokens': [{'coefficient': 1, 'scope': [0, 0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [0, 1], 'type': 'binary', 'value': '-'}, {'scope': [0, 2], 'type': 'constant', 'value': 1.0, 'power': 1}], 'scope': [0], 'coefficient': 1, 'type': 'expression'}, {'tokens': [{'coefficient': 1, 'scope': [1, 0], 'type': 'variable', 'power': [1], 'value': ['x']}, {'scope': [1, 1], 'type': 'binary', 'value': '+'}, {'scope': [1, 2], 'type': 'constant', 'value': 1.0, 'power': 1}], 'scope': [1], 'coefficient': 1, 'type': 'expression'})
