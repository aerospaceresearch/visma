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

	def remove_ones(self):
		#remove random ones
		pass

	def __str__(self):
		pass

	def __repr__(self):
		print "Constant"
		if isinstance(self.coefficient, Constant):
			self.coefficient.__repr__()
			print "check coeff in " + self.coefficient + self.value + self.power
		elif self.coefficient == -1:
			print('-', end='')
		elif self.coefficient != 0:
			print(self.coefficient, end='')
		else:
			pass
			#delete the constant

		if isinstance(self.value, list):
			for i, val in enumerate(self.value):
				if isinstance(val, Constant):
					val.__repr__()
					print "check " + i + " in " + self.value + self.power
				elif val != 1 or val != 0:
					print(val, end='')
					if isinstance(self.power[i], Constant):
						self.power[i].__repr__()
					elif self.power[i] == 0:
						self.power[i] = 1
						self.value[i] = 1	
					elif self.power[i] != 1:
						print('^' +self.power, end=' ')
					else:
						print(' ')
				elif val == 0:
					pass
					#delete const




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

	def __str__(self):
		pass

	def __repr__(self):
		print "Variable"
		if self.coefficient == -1:
			print('-', end='')
		elif self.coefficient != 0:
			print(self.coefficient, end='')
		else:
			pass
			#delete the variable

		if isinstance(self.value, list):
			for i, val in enumerate(self.value):
				if val != 1:
					print(val, end='')
					if self.power[i] != 1:
						print('^' +self.power, end=' ')
					else:
						print(' ')
			

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
	