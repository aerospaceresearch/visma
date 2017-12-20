class BaseTypes(object):
	"""docstring for BaseTypes"""
	def __init__(self, arg):
		super(BaseTypes, self).__init__()
		self.scope = []
		self.value = []


class Constant(BaseTypes):
	"""docstring for Constant"""
	def __init__(self, arg):
		super(Constant, self).__init__()
		self.coefficient = 1
		self.power = []
	
	def set_values(value=None, power=None, coefficient=None, scope=None):
		if value != None:
			self.value = value
		if power != None:
			self.power = power
		if coefficient != None:
			self.coefficient = coefficient
		if scope != None:
			self.scope = scope

	def __str__(self):
		pass

	def __repr__(self):
		print "Constant"
		if self.coefficient == -1:
			print('-', end='')
		if isinstance(self.value, list):
			

class Variable(BaseTypes):
	"""docstring for Variable"""
	def __init__(self, arg):
		super(Variable, self).__init__()
		self.coefficient = 1
		self.power = []
	
	def set_values(value=None, power=None, coefficient=None, scope=None):
		if value != None:
			self.value = value
		if power != None:
			self.power = power
		if coefficient != None:
			self.coefficient = coefficient
		if scope != None:
			self.scope = scope
			

class Operations(BaseTypes):
	"""docstring for Operations"""
	def __init__(self, arg):
		super(Operations, self).__init__()
		self.type = None

	def set_values(value=None, type=None, scope=None):
		if value != None:
			self.value = value
		if type != None:
			self.type = type
		if scope != None:
			self.scope = scope
	