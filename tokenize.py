
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
	
def clean(eqn):
	cleanEqn = removeSpaces(eqn)
	x = 0
	terms = []
	symbols = ['+', '-', '*', '/', '{', '}', '[',']', '^', '=']
	greek = [u'\u03B1', u'\u03B2', u'\u03B3', u'\u03C0']
	while x < len(cleanEqn):
		if (cleanEqn[x] >= 'a' and cleanEqn[x] <= 'z') or (cleanEqn[x] >= 'A' and cleanEqn[x] <= 'Z'):
				terms.append(cleanEqn[x])
				x += 1	
		elif cleanEqn[x] == '\\':
			buf = '\\'
			x += 1
			while (cleanEqn[x] >= a and cleanEqn[x] <= z) or (cleanEqn[x] >= A and cleanEqn[x] <= Z):
				buf += cleanEqn[x]
			  	x +=1
			terms.append(buf)
		elif cleanEqn[x] > '0' and cleanEqn[x] < '9':
			buf = cleanEqn[x]
			x += 1
			while cleanEqn[x] > '0' and cleanEqn[x] < '9':
				buf += cleanEqn[x]
				x += 1
			terms.append(buf)
		elif cleanEqn[x] in symbols:				
			terms.append(cleanEqn[x])
			x += 1
		else:
			x += 1	
		print x	
	print terms


def tokenizer(eqn="    x     +     y   =    2   "):
	clean(eqn)

if __name__ == "__main__":
	tokenizer()