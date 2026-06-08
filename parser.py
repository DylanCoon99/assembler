from lexer import Token, Lexer

OPCODES = {"NOP", "LDA", "STA", "LDIA", "LDIB", "MOVAB", "MOVBA", "LDB", "STB", "ADD", "SUB", "JMP", "JZ", "JNZ", "OUT", "HLT"}      
NEEDS_OPERAND = {"LDA", "STA", "LDIA", "LDIB", "LDB", "STB", "ADD", "SUB", "JMP", "JZ", "JNZ"}

class InstructionNode:

	def __init__(self, opcode: str, operand=None):
		self.opcode = opcode
		self.operand = operand
		self.next = None


	@property
	def opcode(self) -> str:
		return self._opcode


	@opcode.setter
	def opcode(self, value):
		if value not in OPCODES:
			raise ValueError("Opcode is invalid")
		self._opcode = value


	@property
	def next(self) -> str:
		return self._next


	@next.setter
	def next(self, value):
		if not isinstance(value, InstructionNode) and value != None:
			raise ValueError("Next must be of type InstructionNode or None")
		self._next = value




class Parser:

	def __init__(self, lexer):
		self.lexer = lexer
		self.instruction_list = None
		self.tail = None


	@property
	def lexer(self):
		return self._lexer


	@lexer.setter
	def lexer(self, value):
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
		tokens = iter(self.lexer)

		# generate the instruction list here

		for token in self.lexer:
			# need to build the instructions based off of the rules
			if token.type == "OPCODE":
				instruction = token.value

				if instruction in NEEDS_OPERAND:
					# the instruction expects an operand in the next token
					# need to check the next token
					try:                                                                                                                                                           
						next_token = next(self.lexer)                                                                                                                              
					except StopIteration:                                                                                                                                        
						raise ValueError(f"Expected operand for instruction: {instruction}") 
					
					if next_token.type != "NUMBER":
						raise RuntimeError(f"Expected operand for this instruction: {instruction}")


					number = next_token.value

					if number.startswith("0b") or number.startswith("0B"):
						# binary number
						number = int(number, 2)
					elif number.startswith("0x") or number.startswith("0X"):
						# hex number
						number = int(number, 16)
					else:
						# decimal number
						number = int(number, 10)
					
					node = InstructionNode(instruction, number)
				else:
					# the instruction does not need an operand
					node = InstructionNode(instruction)
				# append the node to the list
				if self.instruction_list is None:
					self.instruction_list = node
					self.tail = node
				else:
					# append to the end of the list
					self.tail.next = node
					self.tail = node
			
			else:
				raise RuntimeError(f"Unrecognized type for token: {token}")
		



		return self.instruction_list

	
