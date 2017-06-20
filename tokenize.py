symbols = ['+', '-', '*', '/', '{', '}', '[',']', '^', '=']
greek = [u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0']
	
inputLaTeX = ['\\times', '\\div', '\\alpha', '\\beta', '\\gamma', '\\pi', '+', '-', '=', '^', '\\sqrt']
inputGreek = ['*', '/', u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0', '+', '-', '=', '^', 'sqrt']


def checkEquation(terms, symTokens):
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
		elif isVariable(term) or isNumber(term):
			if i+1 < len(terms):
				if terms[i+1] == '{':
					return False
							
	i = len(terms) - 1
	if symTokens[i] == 'binary' or symTokens[i] == 'unary' or brackets != 0 or sqrBrackets != 0:
		return False				
	return True	

def isVariable(term):
	if term in greek: 
		return True
	elif (term[0] >= 'a' and term[0] <= 'z') or (term[0] >= 'A' and term[0] <= 'Z'):
		x = 0
		while x < len(term):
			if term[x] < 'A' or (term[x] > 'Z' and term[x] < 'a') or term[x] > 'z':
				return False
			x += 1
		return True

def isNumber(term):
	x = 0
	while x < len(term):
		if term[x] < '0' or term[x] > '9':
			return False
		x += 1	
	return True

def getNum(term):
	x = 0
	val = 0
	while x < len(term):
		val *= 10
		val += int(term[x])
		x += 1
	return val	

def removeSpaces(eqn):
	cleanEqn = ''
	x = 0
	while x < len(eqn):
		cleanEqn += eqn[x]
		if eqn[x] == ' ':
			while (x+1 < len(eqn)):
				if (eqn[x+1] == ' '):
					x += 1
		x += 1		
	return cleanEqn
	
def getTerms(eqn):
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
		elif eqn[x] > '0' and eqn[x] < '9':
			buf = eqn[x]
			x += 1
			while x < len(terms):
				if eqn[x] > '0' and eqn[x] < '9':
					buf += eqn[x]
					x += 1
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

def getVariable(terms, symTokens, coeff=1):
	variable = {}
	variable["type"] = "variable"
	value = []
	coefficient = coeff
	power = []
	x = 0
	while x < len(terms):

		if isVariable(terms[x]) :
			value.append(terms[x])
			power.append(1)
			x += 1


		elif isNumber(terms[x]):
			if x+1 < len(terms):
				if terms[x+1] != '^':
					coefficient *= getNum(terms[x])
				else:	
					value.append(getNum(terms[x]))
					power.append(1)
			else:
				value.append(getNum(terms[x]))
				power.append(1)		
			x +=1 
				
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
									if brackets2 == 0:
										nSqrt2 += 1
								varTerms2.append(terms[x])
								varSymTokens2.append(symTokens[x])
								x += 1
							else:
								break
							if binary2 == 0 and nSqrt2 == 0:
								power2.append(getVariable(varTerms2, varSymTokens2))
							else:
								power2.append(getToken(varTerms2, varSymTokens2))	
							if len(varTerms) == 1:
								if isVariable(terms[x-1]):
									variable["type"] = "variable"
									variable["value"] = [terms[x-1]]
									variable["power"] = power2
									variable["coefficient"] = coeff
									power[-1] = variable
								elif isNumber(terms[x-1]):
									variable = {}
									variable["type"] = "constant"
									variable["value"] = getNum(terms[x-1])
									variable["power"] = power2
									power[-1] = variable
							else:		
								if binary == 0 and nSqrt == 0:
									variable = {}
									variable["power"] = power2
									variable["value"] = getVariable(varTerms, varSymTokens)
									variable["coefficient"] = 1
									variable["type"] = "variable"
									power[-1] = variable
								else:
									variable = {}
									variable["power"] = power2
									variable["value"] = getToken(varTerms, varSymTokens)
									variable["coefficient"] = 1
									variable["type"] = "equation"
									power[-1] = variable	 
					else:
						if len(varTerms) == 1:
							if isVariable(terms[x-1]):
								power[-1] = terms[x-1]
							elif isNumber(terms[x-1]):
								power[-1] *= getNum(terms[x-1])
						else:
							if binary == 0 and nSqrt == 0:
								power[-1] = getVariable(varTerms, varSymTokens)
							else:
								power[-1] = getToken(varTerms, varSymTokens)

				else:
					if len(varTerms) == 1:
						if isVariable(terms[x]):
							power[-1] = terms[x]
						elif isNumber(terms[x]):
							power[-1] *= getNum(terms[x])
					else:
						if binary == 0 and nSqrt == 0:
							power[-1] = getVariable(varTerms, varSymTokens)
						else:
							power[-1] = getToken(varTerms, varSymTokens)

				x += 1
					
			elif isVariable(terms[x]) or isNumber(terms[x]):
				if x+1 < len(terms):
					if terms[x+1] == '^' or isNumber(terms[x]) or isVariable(terms[x]):
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
							power[-1] = getToken(varTerms, varSymTokens)
						else:			
							power[-1] = getVariable(varTerms, varSymTokens)
						
					else:
						if isNumber(terms[x]):
							power[-1] = getNum(terms[x])
						else:
							power[-1] = terms[x]	
						x += 1	
				else:
					if isNumber(terms[x]):
						power[-1] = getNum(terms[x])
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
										if brackets2 == 0:
											nSqrt2 += 1
									varTerms2.append(terms[x])
									varSymTokens2.append(symTokens[x])
									x += 1
								else:
									break
								if binary2 == 0 and nSqrt2 == 0:
									power2.append(getVariable(varTerms2, varSymTokens2))
								else:
									power2.append(getToken(varTerms2, varSymTokens2))	
								if len(varTerms) == 1:
									if isVariable(terms[x-1]):
										variable["type"] = "variable"
										variable["value"] = [terms[x-1]]
										variable["power"] = power2
										variable["coefficient"] = coeff
										power[-1] = variable
									elif isNumber(terms[x-1]):
										variable = {}
										variable["type"] = "constant"
										variable["value"] = coeff * getNum(terms[x-1])
										variable["power"] = power2
										power[-1] = variable
								else:		
									if binary == 0 and nSqrt == 0:
										variable = {}
										variable["power"] = power2
										variable["value"] = getVariable(varTerms, varSymTokens)
										variable["coefficient"] = coeff
										variable["type"] = "variable"
										power[-1] = variable
									else:
										variable = {}
										variable["power"] = power2
										variable["value"] = getToken(varTerms, varSymTokens)
										variable["coefficient"] = coeff
										variable["type"] = "equation"
										power[-1] = variable	 
						else:
							if len(varTerms) == 1:
								if isVariable(terms[x-1]):
									variable["type"] = "variable"
									variable["value"] = [terms[x-1]]
									variable["power"] = power2
									variable["coefficient"] = coeff
									power[-1] = variable
								elif isNumber(terms[x-1]):
									power[-1] *= (coeff * getNum(terms[x-1]))
							else:
								if binary == 0 and nSqrt == 0:
									power[-1] = getVariable(varTerms, varSymTokens, coeff)
								else:
									power[-1] = getToken(varTerms, varSymTokens, coeff)

					else:			
						if len(varTerms) == 1:
							if isVariable(terms[x-1]):
								variable["type"] = "variable"
								variable["value"] = [terms[x-1]]
								variable["power"] = power2
								variable["coefficient"] = coeff
								power[-1] = variable
							elif isNumber(terms[x-1]):
								power[-1] *= (coeff * getNum(terms[x-1]))
						else:
							if binary == 0 and nSqrt == 0:
								power[-1] = getVariable(varTerms, varSymTokens, coeff)
							else:
								power[-1] = getToken(varTerms, varSymTokens , coeff)
					x += 1
						
				elif isVariable(terms[x]) or isNumber(terms[x]):
					
					if x+1 < len(terms):
						if terms[x+1] == '^' or isNumber(terms[x]) or isVariable(terms[x]):
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
								power[-1] = getToken(varTerms, varSymTokens, coeff)
							else:			 						
								power[-1] = getVariable(varTerms, varSymTokens, coeff)
							
						else:
							if isNumber(terms[x]):
								power[-1] = getNum(terms[x])
							else:
								power[-1] = terms[x]	
							x += 1	
					else:
						if isNumber(terms[x]):
							power[-1] = getNum(terms[x])
						else:	
							power[-1] = terms[x]
						x += 1
	
	variable["value"] = value
	variable["power"] = power
	variable["coefficient"] = coefficient
	return variable

def getToken(terms, symTokens, coeff=1):
	eqn = {}
	eqn["type"] = "expression"
	eqn["coeff"] = coeff
	tokens = []
	x = 0
	while x < len(terms):
		if isVariable(terms[x]) and symTokens[x] != 'sqrt':
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
				variable = getToken(varTerms, varSymTokens)
			else:	
				variable = getVariable(varTerms, varSymTokens)

			tokens.append(variable)
	
		elif isNumber(terms[x]):
			if x + 1 < len(terms):
				if terms[x+1] == '^' or isVariable(terms[x+1]):
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
						variable = getToken(varTerms, varSymTokens)
					else:	
						variable = getVariable(varTerms, varSymTokens)
					tokens.append(variable)
				else:
					variable = {}
					variable["type"] = "constant"
					variable["value"] = getNum(terms[x])
					tokens.append(variable)
			else:
				variable = {}
				variable["type"] = "constant"
				variable["value"] = getNum(terms[x])
				tokens.append(variable)
				
		elif terms[x] in ['='] or symTokens[x] == 'binary':
			operator = {}
			operator["value"] = terms[x]
			if symTokens[x] == '':
				operator["type"] = "other"
			else:
				operator["type"] = symTokens[x]	
			tokens.append(operator)
		elif terms[x] == '{':
			x += 1
			brackets = 0
			binary = 0
			nSqrt = 0
			varTerms = []
			varSymTokens = []
			while x < len (terms):
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
					varSymTokens.append(symTokens[x])
					varTerms.append(terms[x])
					x += 1
				else:
					break
			if len(varTerms) == 1:
				if isVariable(terms[x-1]):
					variable["type"] = "variable"
					variable["value"] = [terms[x-1]]
					variable["power"] = [1]
					variable["coefficient"] = coeff
					tokens.append(variable)
				elif isNumber(terms[x-1]):
					variable = {}
					variable["type"] = "constant"
					variable["value"] = getNum(terms[x-1])
					tokens.append(variable)
			else:
				if nSqrt == 0 and binary == 0:
					tokens.append(getVariable(varTerms, varSymTokens, coeff))
				else:
					tokens.append(getToken(varTerms, varSymTokens , coeff))
			x += 1 		

		elif symTokens[x] == 'unary':
			coeff = 1
			if terms[x] == '-':
				coeff *= -1
			x += 1
			if terms[x] == '{':
				x += 1
				brackets = 0
				binary = 0
				nSqrt = 0
				varTerms = []
				varSymTokens = []
				while x < len (terms):
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
						varSymTokens.append(symTokens[x])
						varTerms.append(terms[x])
						x += 1
					else:
						break
				if len(varTerms) == 1:
					if isVariable(terms[x-1]):
						variable["type"] = "variable"
						variable["value"] = [terms[x-1]]
						variable["power"] = [1]
						variable["coefficient"] = coeff
						tokens.append(variable)
					elif isNumber(terms[x-1]):
						variable = {}
						variable["type"] = "constant"
						variable["value"] = getNum(terms[x-1])
						tokens.append(variable)
				else:
					if binary == 0 and nSqrt == 0:
						tokens.append(getVariable(varTerms, varSymTokens, coeff))
					else:
						tokens.append(getToken(varTerms, varSymTokens , coeff))
				x += 1 		

			elif isVariable(terms[x]):
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
					variable = getToken(varTerms, varSymTokens, coeff)
				else:	
					variable = getVariable(varTerms, varSymTokens, coeff)
				tokens.append(variable)

			elif isNumber(terms[x]):
				if x + 1 < len(terms):
					if terms[x+1] == '^' or isVariable(terms[x+1]):
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
							variable = getToken(varTerms, varSymTokens, coeff)
						else:	
							variable = getVariable(varTerms, varSymTokens, coeff)
						tokens.append(variable)
					else:
						variable = {}
						variable["type"] = "constant"
						variable["value"] = getNum(terms[x])
						tokens.append(variable)
				else:
					variable = {}
					variable["type"] = "constant"
					variable["value"] = getNum(terms[x])
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
				if isNumber(terms[x-1]):
					variable = {}
					variable["type"] = "constant"
					variable["value"] = getNum(terms[x-1])
					operator["power"] =	variable	
				elif isVariable(terms[x-1]):
					variable = {}
					variable["type"] = "variable"
					variable["value"] = [terms[x-1]]
					variable["power"] = [1]
					variable["coefficient"] = 1
					operator["power"] = variable
			else:
				if binary != 0 or nSqrt != 0:
					operator["power"] = getToken(varTerms, varSymTokens)
				else:
					operator["power"] = getVariable(varTerms, varSymTokens)
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
				if isNumber(terms[x-1]):
					variable = {}
					variable["type"] = "constant"
					variable["value"] = getNum(terms[x-1])
					operator["eqn"] =	variable	
				elif isVariable(terms[x-1]):
					variable = {}
					variable["type"] = "variable"
					variable["value"] = [terms[x-1]]
					variable["power"] = [1]
					variable["coefficient"] = 1
					operator["eqn"] = variable
			else:
				if binary == 0 and nSqrt == 0:
					operator["eqn"] = getVariable(varTerms, varSymTokens)
				else:
					operator["eqn"] = getToken(varTerms, varSymTokens)
			tokens.append(operator)		
						
				
		x += 1	
	
	eqn["tokens"] = tokens	
	return eqn		  

def tokenizeSymbols(terms):
	symTokens=[]
	for i, term in enumerate(terms):
		symTokens.append('')
		if term in symbols:
			if term == '*' or term == '/':
				if (isVariable(terms[i-1]) or isNumber(terms[i-1]) or terms[i-1] == '}') and (isVariable(terms[i+1]) or isNumber(terms[i+1]) or terms[i+1] == '{' or ((terms[i+1] == '-' or terms[i+1] == '+') and (isVariable(terms[i+2]) or isNumber(terms[i+2])) )):  		
					symTokens[-1] = "binary"
			elif term == '+' or term == '-':
				if i == 0:
					symTokens[-1] = "unary"
				elif terms[i-1] in ['-', '+', '*', '/', '=', '^']:
					symTokens[-1] = "unary"	
				elif (isVariable(terms[i-1]) or isNumber(terms[i-1]) or terms[i-1] == '}') and (isVariable(terms[i+1]) or isNumber(terms[i+1]) or terms[i+1] == '{' or ((terms[i+1] == '-' or terms[i+1] == '+') and (isVariable(terms[i+2]) or isNumber(terms[i+2])) )):
					symTokens[-1] = "binary"
			elif term == '=':
				symTokens[-1] = "binary"
		elif term == "sqrt":
			symTokens[-1] = "sqrt"	
	return symTokens

	
def clean(eqn):
	print eqn
	cleanEqn = removeSpaces(eqn) 
	terms = getTerms(cleanEqn)
	normalizedTerms = normalize(terms)
	symTokens = tokenizeSymbols(normalizedTerms)
	if checkEquation(normalizedTerms, symTokens):
		tokens = getToken(normalizedTerms, symTokens)
		print tokens["tokens"]

def tokenizer(eqn="x+y=2^-{x+y} "):
	clean(eqn)

if __name__ == "__main__":
	tokenizer()
#-xy^22^22^-z^{s+y}^22=sqrt[x+1]{x}