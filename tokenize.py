symbols = ['+', '-', '*', '/', '{', '}', '[',']', '^', '=']
greek = [u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0']
	
inputLaTeX = ['\\times', '\\div', '\\alpha', '\\beta', '\\gamma', '\\pi', '+', '-', '=', '^', '\\sqrt']
inputGreek = ['*', '/', u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0', '+', '-', '=', '^', 'sqrt']

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
			while (x+1 < len(eqn) and eqn[x+1] == ' '):
				x += 1
		x += 1		
	return cleanEqn
	
def getTerms(eqn):
	x = 0
	terms = []
	while x < len(eqn):
		if (eqn[x] >= 'a' and eqn[x] <= 'z') or (eqn[x] >= 'A' and eqn[x] <= 'Z') or eqn[x] in greek:
				terms.append(eqn[x])
				x += 1	
		elif eqn[x] == '\\':
			buf = '\\'
			x += 1
			while (eqn[x] >= 'a' and eqn[x] <= 'z') or (eqn[x] >= 'A' and eqn[x] <= 'Z'):
				buf += eqn[x]
			  	x +=1
			terms.append(buf)
		elif eqn[x] > '0' and eqn[x] < '9':
			buf = eqn[x]
			x += 1
			while eqn[x] > '0' and eqn[x] < '9':
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
				varTerms = []
				varSymTokens = []
				while terms[x] == '}':
					if symTokens[x] == 'binary':
						binary += 1
					varTerms.append(terms[x])
					varSymTokens.append(symTokens[x])
					x += 1
				if len(varTerms) == 1:
					if isVariable(terms[x]):
						power[-1] = terms[x]
					elif isNumber(terms[x]):
						power[-1] *= getNum(terms[x])
				else:
					if binary == 0:
						power[-1] = getVariable(varTerms, symTokens)
					else:
						power[-1] = getToken(varTerms, symTokens)
				x += 1
					
			elif isVariable(terms[x]) or isNumber(terms[x]):
				if x+1 < len(terms):
					if terms[x+1] == '^':
						varTerms = []
						varSymTokens = []
						while (isVariable(terms[x]) or isNumber(terms[x])) and terms[x+1] == '^':
							varTerms.append(terms[x])
							varSymTokens.append(symTokens[x])
							varTerms.append(terms[x+1])
							varSymTokens.append(symTokens[x+1])
							if x + 3 < len(terms) and terms[x+3] == '^':
								x += 2
							else:
								varTerms.append(terms[x+2])
								varSymTokens.append(symTokens[x+2])
								break						
						power[-1] = getVariable(varTerms, symTokens)
						x += 3
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


	variable["value"] = value
	variable["power"] = power
	variable["coefficient"] = coefficient
	return variable

def getToken(terms, symTokens, coeff=1):
	eqn = {}
	eqn["type"] = "equation"
	eqn["coeff"] = coeff
	tokens = []
	x = 0
	while x < len(terms):
		if isVariable(terms[x]):
			varTerms = []
			varSymTokens = []
			brackets = 0
			while symTokens[x] != 'binary' and brackets == 0:
				if terms[x] == '{':
					brackets += 1
				elif terms[x] == '}':
					brackets -= 1	
				varTerms.append(terms[x])
				varSymTokens.append(symTokens[x])
				x += 1
			x -= 1	
			variable = getVariable(varTerms)
			tokens.append(variable)
	
		elif isNumber(terms[x]):
			if x + 1 < len(terms):
				if terms[x+1] == '^' or isVariable(terms[x+1]):
					varTerms = []
					brackets = 0
					while symTokens[x] != 'binary' and brackets = 0:
						if terms[x] == '}':
							brackets += 1
						elif terms[x] == '{':
							brackets -= 1	
						varTerms.append(terms[x])
						varSymTokens.append(symTokens[x])
						x += 1
					x -= 1	
					variable = getVariable(varTerms)
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
				
		elif terms[x] in ['-', '+', '/', '*', '=']:
			operator = {}
			operator["value"] = terms[x]
			if symTokens[x] == '':
				operator["type"] = "other"
			else:
				operator["type"] = symTokens[x]	
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
				if (isVariable(terms[i-1]) or terms[i-1] == '}') and (isVariable(terms[i+1]) or terms[i+1] == '{' or ((terms[i+1] == '-' or terms[i+1]) and (isVariable(terms[i+2] or terms[i+2])) )):  		
					symTokens[-1] = "binary"
			elif term == '+' or term == '-':
				if i == 0:
					symTokens[-1] = "unary"
				elif (isVariable(terms[i-1]) or terms[i-1] == '}') and (isVariable(terms[i+1]) or terms[i+1] == '{' or ((terms[i+1] == '-' or terms[i+1]) and (isVariable(terms[i+2] or terms[i+2])) )):  		
					symTokens[-1] = "binary"
				elif terms[i-1] in ['-', '+', '*', '/', '=', '^']:
					symTokens[-1] = "unary"
			elif term == '=':
				symTokens[-1] = "binary"
	return symTokens

	
def clean(eqn):
	cleanEqn = removeSpaces(eqn) 
	terms = getTerms(cleanEqn)
	normalizedTerms = normalize(terms)
	symTokens = tokenizeSymbols(normalizedTerms)
	tokens = getToken(normalizedTerms, symTokens)
	print tokens

def tokenizer(eqn="  -  x y^22^22^x^s    +     y^22    =    22   "):
	clean(eqn)

if __name__ == "__main__":
	tokenizer()
