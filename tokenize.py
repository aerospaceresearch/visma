"""
Initial Author: Siddharth Kothiyal (sidkothiyal, https://github.com/sidkothiyal)
Other Authors: 
Owner: AerospaceResearch.net
About: This module's basic purpose is to be able to tokenize every possible input given by the user into a consistent key-value pair format for 
	each equation/expression. Redundant data has been provided with the tokens on purpose, to make the job of future developers easier. 
	Still far from perfect and requires a bit of clean up.
Note: Please try to maintain proper documentation
-1 -> power
-2 -> value
-3 -> sqrt expression
-4 -> sqrt power
Logic Description:
"""
#TODO: Fix brackets issue in brackets2 add power symbol check as well 

symbols = ['+', '-', '*', '/', '{', '}', '[',']', '^', '=']
greek = [u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0']
	
inputLaTeX = ['\\times', '\\div', '\\alpha', '\\beta', '\\gamma', '\\pi', '+', '-', '=', '^', '\\sqrt']
inputGreek = ['*', '/', u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0', '+', '-', '=', '^', 'sqrt']


def check_equation(terms, symTokens):
	brackets = 0
	sqrBrackets = 0
	for i, term in enumerate(terms):
		if term == '{':
			brackets += 1
		elif term == '}':
			brackets -= 1
			if brackets < 0:
				return False
		elif term == '[':
			sqrBrackets += 1
		elif term == ']':
			sqrBrackets -= 1
			if sqrBrackets < 0:
				return False
		elif term == '^':
			if symTokens[i+1] == 'binary':
				return False 				
		elif is_variable(term) or is_number(term):
			if i+1 < len(terms):
				if terms[i+1] == '{':
					return False
							
	if len(terms) != 0:
		i = len(terms) - 1
		if symTokens[i] == 'binary' or symTokens[i] == 'unary' or brackets != 0 or sqrBrackets != 0:
			return False				
	return True	

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

def is_number(term):
	if isinstance(term, int) or isinstance(term, float):
		return True
	else:
	    x = 0
	    dot = 0
	    while x < len(term):
	    	if (term[x] < '0' or term[x] > '9') and (dot!= 0 or term[x] != '.'):
	    		return False
	    	if term[x] == '.':
	    		dot += 1
	    	x += 1
	    return True

def get_num(term):
	return float(term)

def remove_spaces(eqn):
	cleanEqn = ''
	x = 0
	while x < len(eqn):
		cleanEqn += eqn[x]
		if eqn[x] == ' ':
			while (x+1 < len(eqn) and eqn[x+1] == ' '):
				if (eqn[x+1] == ' '):
					x += 1
		x += 1		
	return cleanEqn
	
def get_terms(eqn):
	x = 0
	terms = []
	while x < len(eqn):
		if (eqn[x] >= 'a' and eqn[x] <= 'z') or (eqn[x] >= 'A' and eqn[x] <= 'Z') or eqn[x] in greek:
				if eqn[x] == 's':
					i = x
					buf = eqn[x]
					while (i-x) < len("qrt") :
						i += 1
						if i < len(eqn):
							buf += eqn[i]
					if buf == "sqrt":
						terms.append(buf)
						x = i + 1
						continue 

					terms.append(eqn[x])
				else:
					terms.append(eqn[x])
				x += 1	
		elif eqn[x] == '\\':
			buf = '\\'
			x += 1
			while x < len(terms):
				if (eqn[x] >= 'a' and eqn[x] <= 'z') or (eqn[x] >= 'A' and eqn[x] <= 'Z'):
					buf += eqn[x]
				  	x +=1
			terms.append(buf)
		elif eqn[x] >= '0' and eqn[x] <= '9':
			buf = ''
			buf = eqn[x]
			x += 1
			dot = 0
			while x < len(eqn):
				if (eqn[x] >= '0' and eqn[x] <= '9'):
					buf += eqn[x]
					x += 1
				elif eqn[x] == '.':
					if dot == 0:
						buf += eqn[x]
						dot += 1
						x += 1
					else:
						break
				else:
					break			
			terms.append(buf)
		elif eqn[x] in symbols:				
			terms.append(eqn[x])
			x += 1
		else:
			x += 1
	return terms

def normalize(terms):
	for term in terms:
		for i, x in enumerate(inputLaTeX):
			if x == term:
				term = inputGreek[i]
	return terms

def get_variable(terms, symTokens, scope, coeff=1):
	variable = {}
	variable["type"] = "variable"
	value = []
	coefficient = coeff
	power = []
	x = 0
	level = 0
	while x < len(terms):
		if terms[0] == '{':
			print terms
			print terms[100]

		if is_variable(terms[x]) :
			value.append(terms[x])
			power.append(1)
			level += 1
			x += 1

		elif is_number(terms[x]):
			if x+1 < len(terms):
				if terms[x+1] != '^':
					coefficient *= get_num(terms[x])
				else:	
					value.append(get_num(terms[x]))
					power.append(1)
			else:
				value.append(get_num(terms[x]))
				power.append(1)		
			level += 1	
			x +=1 
		
		elif symTokens[x] == 'unary':
			c = 1
			if terms[x] == '-':
				c *= -1
			coefficient *= c
			x += 1
		elif terms[x] == '^':
			x += 1
			if terms[x] == '{':
				x += 1
				binary = 0
				nSqrt = 0
				varTerms = []
				varSymTokens = []
				brackets = 0
				while x < len(terms):
					if terms[x] != '}' or brackets != 0:
						if symTokens[x] == 'binary':
							if brackets == 0:
								binary += 1
						elif terms[x] == '{':
							brackets += 1
						elif terms[x] == '}':
							brackets -= 1	
						elif symTokens[x] == 'sqrt':
							if brackets == 0:
								nSqrt += 1	
						varTerms.append(terms[x])
						varSymTokens.append(symTokens[x])
						x += 1
					else: 
						break
				if x+1 < len(terms):		
					if terms[x+1] == '^':
						x += 2
						binary2 = 0
						nSqrt2 = 0
						brackets2 = 0
						varSymTokens2 = []
						varTerms2 = []
						power2 = []
						while x < len(terms):
							if symTokens[x] != 'binary' or brackets != 0:
								if symTokens[x] == 'binary':
									if brackets2 == 0:
										binary2 += 1
								elif terms[x] == '{':
									brackets2 += 1
								elif terms[x] == '}':
									brackets2 -= 1
								elif symTokens[x] == 'sqrt':
									if nSqrt2 == 0:
										nSqrt2 += 1
								varTerms2.append(terms[x])
								varSymTokens2.append(symTokens[x])
								x += 1
							else:
								break
							if len(varTerms2) == 1:
								if is_variable(terms[x-1]):
									variable = 	{}
									variable["type"] = "variable"
									variable["value"] = [terms[x-1]]
									variable["power"] = [1]
									variable["coefficient"] = 1
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									tempScope.append(-1)
									variable["scope"] = tempScope
									power2.append(variable)
								elif is_number(terms[x-1]):
									variable = {}
									variable["type"] = "constant"
									variable["value"] = get_num(terms[x-1])
									variable["power"] = 1
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									tempScope.append(-1)
									variable["scope"] = tempScope	
									power2.append(variable)
							else:		
								if binary2 == 0 and nSqrt2 == 0:
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									tempScope.append(-1)
									power2.append(get_variable(varTerms2, varSymTokens2, tempScope))
								else:
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									tempScope.append(-1)
									power2.append(get_token(varTerms2, varSymTokens2, tempScope))	
							if len(varTerms) == 1:
								if is_variable(varTerms[-1]):
									variable = {}
									variable["type"] = "variable"
									variable["value"] = [varTerms[-1]]
									variable["power"] = power2
									variable["coefficient"] = coeff
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									variable["scope"] = tempScope
									power[-1] = variable

								elif is_number(varTerms[-1]):
									variable = {}
									variable["type"] = "constant"
									variable["value"] = get_num(varTerms[-1])
									variable["power"] = power2
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									variable["scope"] = tempScope
									power[-1] = variable
							else:		
								if binary == 0 and nSqrt == 0:
									variable = {}
									variable["power"] = power2
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									variable["value"] = get_variable(varTerms, varSymTokens, tempScope)
									variable["coefficient"] = 1
									variable["type"] = "variable"
									power[-1] = variable
								else:
									variable = {}
									variable["power"] = power2
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									variable["value"] = get_token(varTerms, varSymTokens, tempScope)
									variable["coefficient"] = 1
									variable["type"] = "equation"
									power[-1] = variable	 

					else:
						if len(varTerms) == 1:
							if is_variable(terms[x-1]):
								power[-1] = terms[x-1]
							elif is_number(terms[x-1]):
								power[-1] *= get_num(terms[x-1])
						else:
							if binary == 0 and nSqrt == 0:
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)
								power[-1] = get_variable(varTerms, varSymTokens, tempScope)
							else:
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)
								power[-1] = get_token(varTerms, varSymTokens, tempScope)

				else:
					if len(varTerms) == 1:
						if is_variable(terms[x]):
							power[-1] = terms[x]
						elif is_number(terms[x]):
							power[-1] *= get_num(terms[x])
					else:
						if binary == 0 and nSqrt == 0:
							tempScope = []
							tempScope.extend(scope)
							tempScope.append(level)
							power[-1] = get_variable(varTerms, varSymTokens, tempScope)
						else:
							tempScope = []
							tempScope.extend(scope)
							tempScope.append(level)
							power[-1] = get_token(varTerms, varSymTokens, tempScope)

				x += 1
					
			elif is_variable(terms[x]) or is_number(terms[x]):
				if x+1 < len(terms):
					if terms[x+1] == '^' or is_number(terms[x]) or is_variable(terms[x]):
						varTerms = []
						varSymTokens = []
						brackets = 0
						nSqrt = 0
						binary = 0
						while x < len(terms):
							if symTokens[x] != "binary" or brackets != 0:
								if terms[x] == '{':
									brackets += 1
								elif terms[x] == '}':
									brackets -= 1
								elif symTokens[x] == 'binary':
									if brackets == 0:
										binary += 1	
								elif symTokens[x] == 'sqrt':
									if brackets == 0:	
										nSqrt += 1	
								varTerms.append(terms[x])
								varSymTokens.append(symTokens[x])
								x += 1
							else:
								break 
						if binary != 0 or nSqrt != 0:
							tempScope = []
							tempScope.extend(scope)
							tempScope.append(level)
							power[-1] = get_token(varTerms, varSymTokens, tempScope)
						else:			
							tempScope = []
							tempScope.extend(scope)
							tempScope.append(level)
							power[-1] = get_variable(varTerms, varSymTokens, tempScope)
						
					else:
						if is_number(terms[x]):
							power[-1] = get_num(terms[x])
						else:
							power[-1] = terms[x]	
						x += 1	
				else:
					if is_number(terms[x]):
						power[-1] = get_num(terms[x])
					else:	
						power[-1] = terms[x]
					x += 1

			elif symTokens[x] == 'unary':
				coeff = 1
				if terms[x] == '-':
					coeff = -1
				x += 1 
				if terms[x] == '{':
					x += 1
					binary = 0
					varTerms = []
					varSymTokens = []
					brackets = 0
					nSqrt = 0
					while x < len(terms): 
						if terms[x] != '}' or brackets != 0:
							if symTokens[x] == 'binary':
								if brackets == 0:
									binary += 1
							if terms[x] == '{':
								brackets += 1
							elif terms[x] == '}':
								brackets -= 1	
							elif symTokens[x] == 'sqrt':
								if brackets == 0:
									nSqrt += 1 	
							varTerms.append(terms[x])
							varSymTokens.append(symTokens[x])
							x += 1
						else: 
							break	
					if x+1 < len(terms):		
						if terms[x+1] == '^':
							x += 2
							binary2 = 0
							nSqrt2 = 0
							brackets2 = 0
							varSymTokens2 = []
							varTerms2 = []
							power2 = []
							while x < len(terms):
								if symTokens[x] != 'binary' or brackets != 0:
									if symTokens[x] == 'binary':
										if brackets2 == 0:
											binary2 += 1
									elif terms[x] == '{':
										brackets2 += 1
									elif terms[x] == '}':
										brackets2 -= 1
									elif symTokens[x] == 'sqrt':
										if nSqrt2 == 0:
											nSqrt2 += 1
									varTerms2.append(terms[x])
									varSymTokens2.append(symTokens[x])
									x += 1
								else:
									break
								if len(varTerms2) == 1:
									if is_variable(terms[x-1]):
										variable = 	{}
										variable["type"] = "variable"
										variable["value"] = terms[x-1]
										variable["power"] = [1]
										variable["coefficient"] = 1
										tempScope = []
										tempScope.extend(scope)
										tempScope.append(level)
										tempScope.append(-1)
										variable["scope"] = tempScope
										power2.append(variable)
									elif is_number(terms[x-1]):
										variable = {}
										variable["type"] = "constant"
										variable["value"] = get_num(terms[x-1])
										variable["power"] = 1
										tempScope = []
										tempScope.extend(scope)
										tempScope.append(level)
										tempScope.append(-1)
										variable["scope"] = tempScope	
										power2.append(variable)
								else:			
									if binary2 == 0 and nSqrt2 == 0:
										tempScope = []
										tempScope.extend(scope)
										tempScope.append(level)
										tempScope.append(-1)
										power2.append(get_variable(varTerms2, varSymTokens2, tempScope))
									else:
										tempScope = []
										tempScope.extend(scope)
										tempScope.append(level)
										tempScope.append(-1)
										power2.append(get_token(varTerms2, varSymTokens2, tempScope))	
								if len(varTerms) == 1:
									if is_variable(varTerms[-1]):
										variable["type"] = "variable"
										variable["value"] = [varTerms[-1]]
										variable["power"] = power2
										variable["coefficient"] = coeff
										power[-1] = variable
									elif is_number(varTerms[-1]):
										variable = {}
										variable["type"] = "constant"
										variable["value"] = coeff * get_num(varTerms[-1])
										variable["power"] = power2
										power[-1] = variable
								else:		
									if binary == 0 and nSqrt == 0:
										variable = {}
										variable["power"] = power2
										tempScope = []
										tempScope.extend(scope)
										tempScope.append(level)
										variable["value"] = get_variable(varTerms, varSymTokens, tempScope)
										variable["coefficient"] = coeff
										variable["type"] = "variable"
										power[-1] = variable
									else:
										variable = {}
										variable["power"] = power2
										tempScope = []
										tempScope.extend(scope)
										tempScope.append(level)
										variable["value"] = get_token(varTerms, varSymTokens, tempScope)
										variable["coefficient"] = coeff
										variable["type"] = "equation"
										power[-1] = variable	 
						else:
							if len(varTerms) == 1:
								if is_variable(terms[x-1]):
									variable["type"] = "variable"
									variable["value"] = [terms[x-1]]
									variable["power"] = power2
									variable["coefficient"] = coeff
									power[-1] = variable
								elif is_number(terms[x-1]):
									power[-1] *= (coeff * get_num(terms[x-1]))
							else:
								if binary == 0 and nSqrt == 0:
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									power[-1] = get_variable(varTerms, varSymTokens, tempScope,  coeff)
								else:
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									power[-1] = get_token(varTerms, varSymTokens, tempScope, coeff)

					else:			
						if len(varTerms) == 1:
							if is_variable(terms[x-1]):
								variable["type"] = "variable"
								variable["value"] = [terms[x-1]]
								variable["power"] = power2
								variable["coefficient"] = coeff
								power[-1] = variable
							elif is_number(terms[x-1]):
								power[-1] *= (coeff * get_num(terms[x-1]))
						else:
							if binary == 0 and nSqrt == 0:
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)
								power[-1] = get_variable(varTerms, varSymTokens, tempScope, coeff)
							else:
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)
								power[-1] = get_token(varTerms, varSymTokens, tempScope, coeff)
					x += 1
						
				elif is_variable(terms[x]) or is_number(terms[x]):
					
					if x+1 < len(terms):
						if terms[x+1] == '^' or is_number(terms[x]) or is_variable(terms[x]):
							varTerms = []
							varSymTokens = []
							brackets = 0
							binary = 0
							nSqrt = 0
							while x < len(terms):
								if symTokens[x] != "binary" or brackets != 0:
									if terms[x] == '{':
										brackets += 1
									elif terms[x] == '}':
										brackets -= 1
									elif symTokens[x] == 'binary':
										if brackets == 0:
											binary += 1		
									elif symTokens[x] == 'sqrt':
										if brackets == 0:
											nSqrt += 1
									varTerms.append(terms[x])
									varSymTokens.append(symTokens[x])
									x += 1
								else:
									break 
							if binary != 0 or nSqrt != 0:
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)
								power[-1] = get_token(varTerms, varSymTokens, tempScope, coeff)
							else:
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)			 						
								power[-1] = get_variable(varTerms, varSymTokens, tempScope, coeff)
							
						else:
							if is_number(terms[x]):
								power[-1] = get_num(terms[x])
							else:
								power[-1] = terms[x]	
							x += 1	
					else:
						if is_number(terms[x]):
							power[-1] = get_num(terms[x])
						else:	
							power[-1] = terms[x]
						x += 1

	variable["scope"] = scope
	variable["value"] = value
	variable["power"] = power
	variable["coefficient"] = coefficient
	return variable

def get_token(terms, symTokens, scope=[], coeff=1):
	eqn = {}
	eqn["type"] = "expression"
	eqn["coeff"] = coeff
	tokens = []
	x = 0
	level = 0
	while x < len(terms):
		if is_variable(terms[x]) and symTokens[x] != 'sqrt':
			varTerms = []
			varSymTokens = []
			brackets = 0
			nSqrt = 0
			binary = 0
			while x < len(terms):
				if symTokens[x] != 'binary' or brackets != 0:
					if terms[x] == '{':
						brackets += 1
					elif terms[x] == '}':
						brackets -= 1
					elif symTokens[x] == 'sqrt':
						if brackets == 0:
							nSqrt += 1				
					varTerms.append(terms[x])
					varSymTokens.append(symTokens[x])	
					x += 1
				else:
					break		
			x -= 1	
			if nSqrt != 0 :
				tempScope = []
				tempScope.extend(scope)
				tempScope.append(level)
				variable = get_token(varTerms, varSymTokens, tempScope)
			else:	
				tempScope = []
				tempScope.extend(scope)
				tempScope.append(level)
				variable = get_variable(varTerms, varSymTokens, tempScope)
			level += 1
			tokens.append(variable)

	
		elif is_number(terms[x]):
			if x + 1 < len(terms):
				if terms[x+1] == '^' or is_variable(terms[x+1]):
					varTerms = []
					brackets = 0
					nSqrt = 0
					varSymTokens = []
					while x < len (terms):
						if symTokens[x] != 'binary' or brackets != 0:
							if terms[x] == '}':
								brackets += 1
							elif terms[x] == '{':
								brackets -= 1	
							elif symTokens == 'sqrt':
								nSqrt += 1	
							varTerms.append(terms[x])
							varSymTokens.append(symTokens[x])
						else:
							break	
						x += 1
					x -= 1	
					if nSqrt != 0:
						tempScope = []
						tempScope.extend(scope)
						tempScope.append(level)
						variable = get_token(varTerms, varSymTokens, tempScope)
					else:	
						tempScope = []
						tempScope.extend(scope)
						tempScope.append(level)
						variable = get_variable(varTerms, varSymTokens, tempScope)
					level += 1
					tokens.append(variable)
				else:
					variable = {}
					tempScope = []
					tempScope.extend(scope)
					tempScope.append(level)
					variable["type"] = "constant"
					variable["scope"] = tempScope
					variable["power"] = 1
					variable["value"] = get_num(terms[x])
					level += 1
					tokens.append(variable)
			else:
				variable = {}
				tempScope = []
				tempScope.extend(scope)
				tempScope.append(level)
				variable["type"] = "constant"
				variable["scope"] = tempScope
				variable["power"] = 1
				variable["value"] = get_num(terms[x])
				level += 1
				tokens.append(variable)
				
		elif terms[x] in ['='] or symTokens[x] == 'binary':
			operator = {}
			operator["value"] = terms[x]
			tempScope = []
			tempScope.extend(scope)
			tempScope.append(level)
			if symTokens[x] == '':
				operator["type"] = "other"
			else:
				operator["type"] = symTokens[x]
			operator["scope"] = tempScope	
			level += 1	
			tokens.append(operator)
		elif terms[x] == '{':
			x += 1
			binary = 0
			varTerms = []
			varSymTokens = []
			brackets = 0
			nSqrt = 0
			while x < len(terms): 
				if terms[x] != '}' or brackets != 0:
					if symTokens[x] == 'binary':
						if brackets == 0:
							binary += 1
					if terms[x] == '{':
						brackets += 1
					elif terms[x] == '}':
						brackets -= 1	
					elif symTokens[x] == 'sqrt':
						if brackets == 0:
							nSqrt += 1 	
					varTerms.append(terms[x])
					varSymTokens.append(symTokens[x])
					x += 1
				else: 
					break	
			if x+1 < len(terms):		
				if terms[x+1] == '^':
					x += 2
					binary2 = 0
					nSqrt2 = 0
					brackets2 = 0
					varSymTokens2 = []
					varTerms2 = []
					power2 = []
					while x < len(terms):
						if symTokens[x] != 'binary' or brackets2 != 0:
							if symTokens[x] == 'binary':
								if brackets2 == 0:
									binary2 += 1
							elif terms[x] == '{':
								brackets2 += 1
							elif terms[x] == '}':
								brackets2 -= 1
							elif symTokens[x] == 'sqrt':
								if nSqrt2 == 0:
									nSqrt2 += 1
							varTerms2.append(terms[x])
							varSymTokens2.append(symTokens[x])
							x += 1
						else:
							break
						if len(varTerms2) == 1:
							if is_variable(terms[x-1]):
								variable = 	{}
								variable["type"] = "variable"
								variable["value"] = terms[x-1]
								variable["power"] = [1]
								variable["coefficient"] = 1
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)
								tempScope.append(-1)
								variable["scope"] = tempScope
								power2.append(variable)
							elif is_number(terms[x-1]):
								variable = {}
								variable["type"] = "constant"
								variable["value"] = get_num(terms[x-1])
								variable["power"] = 1
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)
								tempScope.append(-1)
								variable["scope"] = tempScope	
								power2.append(variable)
						else:			
							if binary2 == 0 and nSqrt2 == 0:
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)
								tempScope.append(-1)
								power2.append(get_variable(varTerms2, varSymTokens2, tempScope))
							else:
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)
								tempScope.append(-1)
								power2.append(get_token(varTerms2, varSymTokens2, tempScope))	
						if len(varTerms) == 1:
							if is_variable(varTerms[-1]):
								variable["type"] = "variable"
								variable["value"] = [varTerms[-1]]
								variable["power"] = power2
								variable["coefficient"] = coeff
								tokens.append(variable)
							elif is_number(varTerms[-1]):
								variable = {}
								variable["type"] = "constant"
								variable["value"] = coeff * get_num(varTerms[-1])
								variable["power"] = power2
								tokens.append(variable)
						else:		
							if binary == 0 and nSqrt == 0:
								variable = {}
								variable["power"] = power2
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)
								variable["value"] = get_variable(varTerms, varSymTokens, tempScope)
								variable["coefficient"] = coeff
								variable["type"] = "variable"
								tokens.append(variable)
							else:
								variable = {}
								variable["power"] = power2
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)
								variable["value"] = get_token(varTerms, varSymTokens, tempScope)
								variable["coefficient"] = coeff
								variable["type"] = "equation"
								tokens.append(variable)	 
				else:
					if len(varTerms) == 1:
						if is_variable(terms[x-1]):
							variable["type"] = "variable"
							variable["value"] = [terms[x-1]]
							variable["power"] = power2
							variable["coefficient"] = coeff
							tokens.append(variable)
						elif is_number(terms[x-1]):
							tokens.append(coeff * get_num(terms[x-1]))
					else:
						if binary == 0 and nSqrt == 0:
							tempScope = []
							tempScope.extend(scope)
							tempScope.append(level)
							tokens.append(get_variable(varTerms, varSymTokens, tempScope,  coeff))
						else:
							tempScope = []
							tempScope.extend(scope)
							tempScope.append(level)
							tokens.append(get_token(varTerms, varSymTokens, tempScope, coeff))

			else:			
				if len(varTerms) == 1:
					if is_variable(terms[x-1]):
						variable["type"] = "variable"
						variable["value"] = [terms[x-1]]
						variable["power"] = power2
						variable["coefficient"] = coeff
						tokens.append(variable)
					elif is_number(terms[x-1]):
						tokens.append(coeff * get_num(terms[x-1]))
				else:
					if binary == 0 and nSqrt == 0:
						tempScope = []
						tempScope.extend(scope)
						tempScope.append(level)
						tokens.append(get_variable(varTerms, varSymTokens, tempScope, coeff))
					else:
						tempScope = []
						tempScope.extend(scope)
						tempScope.append(level)
						tokens.append(get_token(varTerms, varSymTokens, tempScope, coeff))
			x += 1
		elif symTokens[x] == 'unary':
			coeff = 1
			if terms[x] == '-':
				coeff *= -1
			x += 1
			if terms[x] == '{':
				x += 1
				binary = 0
				varTerms = []
				varSymTokens = []
				brackets = 0
				nSqrt = 0
				while x < len(terms): 
					if terms[x] != '}' or brackets != 0:
						if symTokens[x] == 'binary':
							if brackets == 0:
								binary += 1
						if terms[x] == '{':
							brackets += 1
						elif terms[x] == '}':
							brackets -= 1	
						elif symTokens[x] == 'sqrt':
							if brackets == 0:
								nSqrt += 1 	
						varTerms.append(terms[x])
						varSymTokens.append(symTokens[x])
						x += 1
					else: 
						break	
				if x+1 < len(terms):		
					if terms[x+1] == '^':
						x += 2
						binary2 = 0
						nSqrt2 = 0
						brackets2 = 0
						varSymTokens2 = []
						varTerms2 = []
						power2 = []
						while x < len(terms):
							if symTokens[x] != 'binary' or brackets != 0:
								if symTokens[x] == 'binary':
									if brackets2 == 0:
										binary2 += 1
								elif terms[x] == '{':
									brackets2 += 1
								elif terms[x] == '}':
									brackets2 -= 1
								elif symTokens[x] == 'sqrt':
									if nSqrt2 == 0:
										nSqrt2 += 1
								varTerms2.append(terms[x])
								varSymTokens2.append(symTokens[x])
								x += 1
							else:
								break
							if len(varTerms2) == 1:
								if is_variable(terms[x-1]):
									variable = 	{}
									variable["type"] = "variable"
									variable["value"] = terms[x-1]
									variable["power"] = [1]
									variable["coefficient"] = 1
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									tempScope.append(-1)
									variable["scope"] = tempScope
									power2.append(variable)
								elif is_number(terms[x-1]):
									variable = {}
									variable["type"] = "constant"
									variable["value"] = get_num(terms[x-1])
									variable["power"] = 1
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									tempScope.append(-1)
									variable["scope"] = tempScope	
									power2.append(variable)
							else:			
								if binary2 == 0 and nSqrt2 == 0:
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									tempScope.append(-1)
									power2.append(get_variable(varTerms2, varSymTokens2, tempScope))
								else:
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									tempScope.append(-1)
									power2.append(get_token(varTerms2, varSymTokens2, tempScope))	
							if len(varTerms) == 1:
								if is_variable(varTerms[-1]):
									variable["type"] = "variable"
									variable["value"] = [varTerms[-1]]
									variable["power"] = power2
									variable["coefficient"] = coeff
									tokens.append(variable)
								elif is_number(varTerms[-1]):
									variable = {}
									variable["type"] = "constant"
									variable["value"] = coeff * get_num(varTerms[-1])
									variable["power"] = power2
									tokens.append(variable)
							else:		
								if binary == 0 and nSqrt == 0:
									variable = {}
									variable["power"] = power2
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									variable["value"] = get_variable(varTerms, varSymTokens, tempScope)
									variable["coefficient"] = coeff
									variable["type"] = "variable"
									tokens.append(variable)
								else:
									variable = {}
									variable["power"] = power2
									tempScope = []
									tempScope.extend(scope)
									tempScope.append(level)
									variable["value"] = get_token(varTerms, varSymTokens, tempScope)
									variable["coefficient"] = coeff
									variable["type"] = "equation"
									tokens.append(variable) 
					else:
						if len(varTerms) == 1:
							if is_variable(terms[x-1]):
								variable["type"] = "variable"
								variable["value"] = [terms[x-1]]
								variable["power"] = power2
								variable["coefficient"] = coeff
								tokens.append(variable)
							elif is_number(terms[x-1]):
								tokens.append(coeff * get_num(terms[x-1]))
						else:
							if binary == 0 and nSqrt == 0:
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)
								tokens.append(get_variable(varTerms, varSymTokens, tempScope,  coeff))
							else:
								tempScope = []
								tempScope.extend(scope)
								tempScope.append(level)
								tokens.append(get_token(varTerms, varSymTokens, tempScope, coeff))

				else:			
					if len(varTerms) == 1:
						if is_variable(terms[x-1]):
							variable["type"] = "variable"
							variable["value"] = [terms[x-1]]
							variable["power"] = power2
							variable["coefficient"] = coeff
							tokens.append(variable)
						elif is_number(terms[x-1]):
							tokens.append((coeff * get_num(terms[x-1])))
					else:
						if binary == 0 and nSqrt == 0:
							tempScope = []
							tempScope.extend(scope)
							tempScope.append(level)
							tokens.append(get_variable(varTerms, varSymTokens, tempScope, coeff))
						else:
							tempScope = []
							tempScope.extend(scope)
							tempScope.append(level)
							tokens.append(get_token(varTerms, varSymTokens, tempScope, coeff))
				x += 1
			elif is_variable(terms[x]):
				varTerms = []
				varSymTokens = []
				brackets = 0
				binary = 0
				nSqrt = 0
				while x < len(terms):
					if symTokens[x] != 'binary' or brackets != 0:
						if terms[x] == '{':
							brackets += 1
						elif terms[x] == '}':
							brackets -= 1	
						elif symTokens[x] == 'sqrt':
							nSqrt += 1
						elif symTokens[x] == 'binary':
							if brackets == 0:
								binary += 1	
 						varTerms.append(terms[x])
						varSymTokens.append(symTokens[x])	
						x += 1
					else:
						break			
				x -= 1		
				if nSqrt != 0 or binary != 0:
					tempScope = []
					tempScope.extend(scope)
					tempScope.append(level)
					variable = get_token(varTerms, varSymTokens, tempScope, coeff)
				else:	
					tempScope = []
					tempScope.extend(scope)
					tempScope.append(level)
					variable = get_variable(varTerms, varSymTokens, tempScope, coeff)
				level += 1	
				tokens.append(variable)

			elif is_number(terms[x]):
				if x + 1 < len(terms):
					if terms[x+1] == '^' or is_variable(terms[x+1]):
						varTerms = []
						varSymTokens = []
						brackets = 0
						binary = 0
						nSqrt = 0
						while x < len (terms):
							if symTokens[x] != 'binary' or brackets != 0:
								if terms[x] == '}':
									brackets += 1
								elif terms[x] == '{':
									brackets -= 1	
								elif symTokens[x] == 'sqrt':
									nSqrt += 1
								elif symTokens[x] == 'binary':
									if brackets == 0:
										binary += 1	
								varTerms.append(terms[x])
								varSymTokens.append(symTokens[x])
							else:
								break	
							x += 1
						x -= 1	
						if nSqrt != 0 or binary != 0:
							tempScope = []
							tempScope.extend(scope)
							tempScope.append(level)
							variable = get_token(varTerms, varSymTokens, tempScope, coeff)
						else:	
							tempScope = []
							tempScope.extend(scope)
							tempScope.append(level)
							variable = get_variable(varTerms, varSymTokens, tempScope, coeff)
						level += 1	
						tokens.append(variable)
					else:
						variable = {}
						variable["type"] = "constant"
						variable["value"] = coeff * get_num(terms[x])
						variable["power"] = 1
						tempScope = []
						tempScope.extend(scope)
						tempScope.append(level)
						variable["scope"] = tempScope
						level += 1
						tokens.append(variable)
				else:
					variable = {}
					variable["type"] = "constant"
					variable["value"] = coeff * get_num(terms[x])
					variable["power"] = 1
					tempScope = []
					tempScope.extend(scope)
					tempScope.append(level)
					variable["scope"] = tempScope
					level += 1
					tokens.append(variable)
		elif symTokens[x] == 'sqrt':
			x += 2
			binary = 0
			brackets = 0
			sqrBrackets = 0
			nSqrt = 0
			varTerms = []
			varSymTokens = []
			while x < len(terms):
				if terms[x] != ']' or sqrBrackets != 0 or brackets != 0:
					if terms[x] == '{':
						brackets += 1
					elif terms[x] == '}':
						brackets -= 1
					elif symTokens[x] == 'binary':
						binary += 1
					elif terms[x] == '[':
						sqrBrackets += 1
					elif terms[x] == ']':
						sqrBrackets -= 1
					elif symTokens[x] == 'sqrt':
						nSqrt += 1				
					varTerms.append(terms[x])
					varSymTokens.append(symTokens[x])
					x += 1
				else:
					break		
			operator = {}
			operator["type"] = "sqrt"
			if len(varTerms) == 1:
				if is_number(terms[x-1]):
					variable = {}
					variable["type"] = "constant"
					variable["value"] = get_num(terms[x-1])
					variable["power"] = 1
					tempScope = []
					tempScope.extend(scope)
					tempScope.append(level)
					tempScope.append(0)
					variable["scope"] = tempScope
					operator["power"] =	variable	
				elif is_variable(terms[x-1]):
					variable = {}
					variable["type"] = "variable"
					variable["value"] = [terms[x-1]]
					variable["power"] = [1]
					variable["coefficient"] = 1
					tempScope = []
					tempScope.extend(scope)
					tempScope.append(level)
					tempScope.append(0)
					variable["scope"] = tempScope
					operator["power"] = variable
			else:
				if binary != 0 or nSqrt != 0:
					tempScope = []
					tempScope.extend(scope)
					tempScope.append(level)
					tempScope.append(0)
					operator["power"] = get_token(varTerms, varSymTokens, tempScope)
				else:
					tempScope = []
					tempScope.extend(scope)
					tempScope.append(level)
					tempScope.append(0)
					operator["power"] = get_variable(varTerms, varSymTokens, tempScope)
			x += 2
			binary = 0
			brackets = 0
			nSqrt = 0
			varTerms = []
			varSymTokens = []
			while x < len(terms):
				if terms[x] != '}' or brackets != 0:
					if terms[x] == '{':
						brackets += 1
					elif terms[x] == '}':
						brackets -= 1
					elif symTokens[x] == 'binary':
						if brackets == 0:
							binary += 1
					elif symTokens[x] == 'sqrt':
						nSqrt += 1				
					varTerms.append(terms[x])
					varSymTokens.append(symTokens[x])
					x += 1
				else:
					break
			if len(varTerms) == 1:
				if is_number(terms[x-1]):
					variable = {}
					variable["type"] = "constant"
					variable["value"] = get_num(terms[x-1])
					variable["power"] = 1
					tempScope = []
					tempScope.extend(scope)
					tempScope.append(level)
					tempScope.append(1)
					variable["scope"] = tempScope
					operator["eqn"] =	variable	
				elif is_variable(terms[x-1]):
					variable = {}
					variable["type"] = "variable"
					variable["value"] = [terms[x-1]]
					variable["power"] = [1]
					variable["coefficient"] = 1
					tempScope = []
					tempScope.extend(scope)
					tempScope.append(level)
					tempScope.append(1)
					variable["scope"] = tempScope
					operator["eqn"] = variable
			else:
				if binary == 0 and nSqrt == 0:
					tempScope = []
					tempScope.extend(scope)
					tempScope.append(level)
					tempScope.append(1)
					operator["eqn"] = get_variable(varTerms, varSymTokens, tempScope)
				else:
					tempScope = []
					tempScope.extend(scope)
					tempScope.append(level)
					tempScope.append(1)
					operator["eqn"] = get_token(varTerms, varSymTokens, tempScope)
			level += 1
			tokens.append(operator)		
						
				
		x += 1	
	eqn["scope"] = scope
	eqn["tokens"] = tokens	
	return eqn		  

def tokenize_symbols(terms):
	symTokens=[]
	for i, term in enumerate(terms):
		symTokens.append('')
		if term in symbols:
			if term == '*' or term == '/':
				if (is_variable(terms[i-1]) or is_number(terms[i-1]) or terms[i-1] == '}') and (is_variable(terms[i+1]) or is_number(terms[i+1]) or terms[i+1] == '{' or ((terms[i+1] == '-' or terms[i+1] == '+') and (is_variable(terms[i+2]) or is_number(terms[i+2])) )):  		
					symTokens[-1] = "binary"
			elif term == '+' or term == '-':
				if i == 0:
					symTokens[-1] = "unary"
				elif terms[i-1] in ['-', '+', '*', '/', '=', '^', '{']:
					symTokens[-1] = "unary"	
				elif (is_variable(terms[i-1]) or is_number(terms[i-1]) or terms[i-1] == '}') and (is_variable(terms[i+1]) or is_number(terms[i+1]) or terms[i+1] == '{' or ((terms[i+1] == '-' or terms[i+1] == '+') and (is_variable(terms[i+2]) or is_number(terms[i+2])) )):
					symTokens[-1] = "binary"
				else:
					print terms[i-1], terms[i], is_number(terms[i+1])	
			elif term == '=':
				symTokens[-1] = "binary"
		elif term == "sqrt":
			symTokens[-1] = "sqrt"	
	return symTokens

	
def clean(eqn):
	cleanEqn = remove_spaces(eqn) 
	terms = get_terms(cleanEqn)
	normalizedTerms = normalize(terms)
	symTokens = tokenize_symbols(normalizedTerms)
	if check_equation(normalizedTerms, symTokens):
		tokens = get_token(normalizedTerms, symTokens)
		return tokens["tokens"]

def constant_variable(variable):
	constant = True
	for var in variable["value"]:
		if isinstance(var, dict):
			if var["type"] == "expression":
				result, token = constant_conversion(var["tokens"])
				if not result:
					constant = False
			elif var["type"] == "variable":
				if not constant_variable(var):
					constant = False
		elif not is_number(var):
			constant = False

						
	for p in variable["power"]:
		if isinstance(p, dict):
			if p["type"] == "expression":
				result, token = constant_conversion(p["tokens"])
				if not result:
					constant = False
			elif p["type"] == "variable":
				if not constant_variable(p):
					constant = False		
		elif not is_number(p):
			constant = False

	return constant

def constant_conversion(tokens):
	constantExpression = True
	for token in tokens:
		if token["type"] == "variable":
			constant = True
			if not constant_variable(token):
				constant = False
				constantExpression = False
			if constant:
				token["type"] = "constant"

		elif token["type"] == "binary":
			constantExpression = False
		
		elif token["type"] == "expression":
			result, token = constant_conversion(token["tokens"])
			if not result:
				constantExpression = False
	return constantExpression, tokens

def tokenizer(eqn=" x^5  - x^4 "):
	result, tokens = constant_conversion(clean(eqn))
	return tokens
def get_lhs_rhs(tokens):
	lhs = []
	rhs = []
	eqn = False
	if not isinstance(tokens, list):
		return False, False
	for token in tokens:
		if token["type"] == 'binary' :
			if token["value"] == '=':
				eqn = True
			elif not eqn:
				lhs.append(token)
			else:
				rhs.append(token)		
		elif not eqn:
			lhs.append(token)
		else:
			rhs.append(token)	
	return lhs, rhs			

if __name__ == "__main__":
	print tokenizer()
#-xy^22^22^-z^{s+y}^22=sqrt[x+1]{x}
#x+y=2^-{x+y}
#x + 6.00 / 3 + 2 - 2x
#x^{1} - x^{-1}
