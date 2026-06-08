from lexer import Token, Lexer



class TreeNode:

	def __init__(self, token: Token, right, left):
		self.token = Token
		self.right = right
		self.left = left

	@property
	def token(self) -> str:
		return self._token


	@token.setter
	def token(self, value):
		if not isinstance(value, Token):
			raise ValueError("Token must be of Token type!")
		self._token = value

	@property
	def right(self) -> str:
		return self._right


	@right.setter
	def right(self, value):
		if not isinstance(value, TreeNode) and value != None:
			raise ValueError("Right must be of type TreeNode or None")
		self._right = value


	@property
	def left(self) -> str:
		return self._left


	@left.setter
	def left(self, value):
		if not isinstance(value, TreeNode) and value != None:
			raise ValueError("Left must be of type TreeNode or None")
		self._left = value



class ASTree:

	def __init__(self, root):
		self.root = root


	@property
	def root(self):
		return self._root


	@root.setter
	def root(self, value):
		if not isinstance(value, TreeNode):
			raise ValueError("Root must be of type TreeNode")
		self._root = value


class Parser:


	def __init__(self, lexer):
		self.lexer = lexer
		self.ast = None


	@property
	def lexer(self):
		return self._lexer


	@lexer.setter
	def lexer(self, value)	:
		if not isinstance(value, Lexer):
			raise ValueError("Lexer must be of type Lexer")
		self._lexer = value


	def parse(self):

		'''
		Grammar Rules

		program     = instruction*                                                                                                                                   
		instruction = opcode operand?                                                                                                                                  
		opcode      = OPCODE token                  
		operand     = NUMBER token   

		'''

		# generate the AST here

		return self.ast

	
