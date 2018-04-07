# This module contains classes for all functions
# TODO: Add exponential, logarithmic, trigonometric and hyperbolic functions
# TODO: Fix method arguments


class Function(object):

    def __init__(self, args):
        self.id = ""
        self.scope = []
    	self.coefficient = []
		self.power = []
		self.operand = []
    	self.operator = []

	def set(operand=None, operator=None, power=None, coefficient=None, scope=None):
		if operand != None:
			self.operand = operand
		if operator != None:
			self.operand = operator
		if power != None:
			self.power = power
		if coefficient != None:
			self.coefficient = coefficient
		if scope != None:
			self.scope = scope

    def inverse(self, RHS):
        RHS.coefficient = (RHS.coefficient /
                           self.coefficient)**(1 / self.power)
		RHS.power /= self.power
		self.operand = RHS
		self.coefficient = 1
		self.power = 1

    def differentiate(self):
        self.power = 1
        self.coefficient = 1

    def level(self):
        return (int((len(self.id))/2))


##########################
# Variable and Constants #
##########################

class Variable(Function):

	def __init__(self, arg):
		super().__init__()
		self.value = []

    def set(args):
		super().set()

    def inverse(self,RHS):
		self.operand = RHS.operand
		self.coefficient = (RHS.coefficient/self.coefficient)**(1/self.power)
		self.power = RHS.power/self.power
		self.__class__ = RHS.__class__

	def differentiate(self):
        super().differentiate()
		self.value = 1
		self.__class__ = Constant

	def integrate(self):
		if self.power == -1:
            self.power = 1
			self.__class__ = Logarithm
		else:
			self.coefficient /= power+1
			self.power += 1

	def calculate(self, input):
		return self.coefficient*((input**(self.power)))


class Constant(Function):

	def __init__(self, arg):
		super().__init__()
		self.value = []

    def set(args):
		super().set()

	def inverse(self,RHS):

	def differentiate(self):
        super().differentiate()
		self.value = 0

	def integrate(self,d):
		self.power = 1:
        self.coefficient = (self.value)**(self.power)
		self.__class__ = Variable
        self.value = intwrt.value

	def calculate(self, input):
		return self.coefficient*((self.value**(self.power)))


##########################
# Trignometric Functions #
##########################

class Sine(Function):

	def __init__(self, arg):
		super().__init__()
		self.value = 'sin'

    def set(args):
		super().set()

	def inverse(self,RHS):
		super().inverse()
		self.__class__ = ArcSine

	def differentiate(self):
        super().differentiate()
		self.__class__ = Cosine

	def integrate(self):
		self.coefficient = -1
		self.__class__ = Cosine

	def calculate(self, input):
		return coefficient*((math.sin(input))**power)


class Cosine(Function):

	def __init__(self, arg):
		super().__init__()
		self.value = 'cos'

    def set(args):
		super().set()

	def inverse(self,RHS):
		super().inverse()
		self.__class__ = ArcCosine

	def differentiate(self):
        super().differentiate()
        self.coefficient = -1
		self.__class__ = Sine

	def integrate(self):
		self.__class__ = Sine

	def calculate(self, input):
		return coefficient*((math.cos(input))**power)


class Tangent(Function):

	def __init__(self, arg):
		super().__init__()
		self.value = 'tan'

    def set(args):
		super().set()

	def inverse(self,RHS):
		super().inverse()
		self.__class__ = ArcTangent

	def differentiate(self):
        super().differentiate()
		self.power = 2
		self.__class__ = Secant

	def integrate(self):
		###

	def calculate(self, input):
		return coefficient*((math.tan(input))**power)


class Cotangent(Function):

	def __init__(self, arg):
		super().__init__()
		self.value = 'cot'

    def set(args):
		super().set()

	def inverse(self,RHS):
		super().inverse()
		self.__class__ = ArcCot

	def differentiate(self):
        super().differentiate()
        self.coefficient = -1
		self.power = 2
		self.__class__ = Cosecant

	def integrate(self):
        ###

	def calculate(self, input):
		return coefficient*((math.cot(input))**power)

### incomplete ###
class Secant(Function):

	def __init__(self, arg):
		super().__init__()
		self.value = 'cot'

    def set(args):
		super().set()

	def inverse(self,RHS):
		super().inverse()
		self.__class__ = ArcSec

	def differentiate(self):
        super().differentiate()


	def integrate(self):
        ###

	def calculate(self, input):
		return coefficient*((math.cot(input))**power)

##################################
# Inverse Trignometric Functions #
##################################

########################
# Hyberbolic Functions #
########################

################################
# Inverse Hyperbolic Functions #
################################

#########################
# Exponential Functions #
#########################

class Logarithm(Function):

	def __init__(self, arg):
		super().__init__()
		self.value = []

    def set(args):
		super().set()

	def inverse(self,RHS):
        super().inverse()

	def differentiate(self):
        super().differentiate()
        self.power = -1
        self.__class__ = operand.__class__

	def integrate(self,d):
        ###
        # call by_parts method from calculus.py

	def calculate(self, input):
		return self.coefficient*((math.log(input,self.base)))


class Exponential(Function):

	def __init__(self, arg):
		super().__init__()
		self.value = []

    def set(args):
		super().set()

	def inverse(self,RHS):
        super().inverse()

	def differentiate(self):
        super().differentiate()

	def integrate(self,d):
        ###

	def calculate(self, input):
		return self.coefficient*((math.exp(input)))


###################
# Mixed Functions #
###################
# For example: sec(x)*tan(x) or sin(x)*log(x) or e^(x)*cot(x)
# Will be taken care by function 'ID'ing/tokening module
