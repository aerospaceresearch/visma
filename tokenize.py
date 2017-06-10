symbols = ['+', '-', '*', '/', '{', '}', '[',']', '^', '=']
greek = [u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0']
	
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

def getVariable(terms):
	variable = {}
	variable["type"] = "variable"
	value = []
	coefficient = 1
	power = []
	value.append(terms[x])
	power.append(1)
	while terms[x] != '+' and terms[x] != '-' and terms[x] != '*' and terms[x] != '*' and terms[x] != '=':
		if (terms[x][0] >= 'a' and terms[x][0] <= 'z') or (terms[x][0] >= 'A' and terms[x][0] <= 'Z') or terms[x][0] in greek:
			value.append(terms[x])
			power.append(1) 	
	variable["value"] = value
	variable["coefficient"] = coefficient
	

def getToken(terms):
	tokens = []
	x = 0
	while x < len(terms):
		if (terms[x][0] >= 'a' and terms[x][0] <= 'z') or (terms[x][0] >= 'A' and terms[x][0] <= 'Z') or terms[x][0] in greek:
			varTerms = []
			while terms[x] != '+' and terms[x] != '-' and terms[x] != '*' and terms[x] != '*' and terms[x] != '=':
				varTerms.append(terms[x])
				x += 1
			variable = getVariable(varTerms)
			tokens.append(variable)
		x += 1	
	print tokens		  

				
def clean(eqn):
	cleanEqn = removeSpaces(eqn)
	terms = getTerms(cleanEqn)
	
def tokenizer(eqn="    x     +     y^22    =    22   "):
	clean(eqn)

if __name__ == "__main__":
	tokenizer()