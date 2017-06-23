
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
		self.baseVariables = get_base_variables()
	
	def get_base_variables(self):
				
		
def check_types(lTokens, rTokens = 0):
	if len(rTokens) != 0:
		equationCompatibile = EquationCompatibility(lTokens, rTokens)
	else:
		expressionCompatible = ExpressionCompatibility(tokens)		

if __name__ == '__main__':
			check_types([])		