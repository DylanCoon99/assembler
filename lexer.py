

'''
Key Concepts to Revisit

Token — the (type, value, source_location) triple your lexer emits
Lexeme — the raw matched string ("0x3F", "LDA")
Regular grammar — the class of languages a lexer can handle; anything you can describe with a regex lives here
Maximal munch — the rule that the lexer should always consume the longest possible match (important when JMP vs JMPZ are both opcodes, for example)
Lookahead — sometimes one character ahead is needed to decide whether to keep consuming or emit
Error recovery — what happens on an unexpected character? Halt, skip, emit an error token?

'''


OPCODES = {"NOP", "LDA", "STA", "LDIA", "LDIB", "MOVAB", "MOVBA", "LDB", "STB", "ADD", "SUB", "JMP", "JZ", "JNZ", "OUT", "HLT"}                                          



class Token:

	def __init__(self, type, value, location):
		self.type = type
		self.value = value
		self.location = location

	@property
	def type(self) -> str:
		return self._type

	@property
	def value(self) -> str:
		return self._value

	@type.setter
	def type(self, value: str):
		# Enforce validation logic
		allowed = {"OPCODE", "NUMBER"}
		if value not in allowed:
			raise ValueError(f"Invalid type. Must be one of {allowed}")
		self._type = value

	@value.setter
	def value(self, value: str):
		# Enforce validation logic
		if not isinstance(value, str):
			raise ValueError(f"Invalid value. Must be a string")
		self._value = value

	def __repr__(self):
		return f"Token: {self.type} {self.value} {self.location}"


class Lexer:

	def __init__(self, source):
		self.source = source
		self.current = 0
		self.line = 0
		self.column = 0


	def __iter__(self):

		'''
		each iteration of the loop should consume
		and yield exactly one token
		'''

		while self.current < len(self.source):

			token = ""
			location = (self.line, self.column)

			char = self.source[self.current]
			self.current += 1
			self.column += 1
			match char:			
				case "\n":
					# new line
					self.line += 1
					self.column = 0
					continue
				case " ":
					continue
				case _:
					if char.isalpha():
						# a letter
						token += char
						while True:
							char = self.peek()
							if not char:
								break
							elif char.isalpha():	
								self.current += 1
								self.column += 1
								token += char
							else:
								break
					elif char.isdigit():
						# a number
						token += char
						if char == '0':
							char = self.peek()

							if char == 'b':
								token += char
								self.current += 1
								self.column += 1
								# prefix 0b -> only 0s and 1s
								while True:
									char = self.peek()
									if not char:
										break
									elif char in {"0", "1"}:	
										self.current += 1
										self.column += 1

										token += char
									else:
										break
							elif char == 'x':
								token += char
								self.current += 1
								self.column += 1
								# prefix 0x -> only 0-9 and a-f 
								while True:
									char = self.peek()
									if not char:
										break
									elif char in {"a", "b", "c", "d", "e", "f", "A", "B", "C", "D", "E", "F"} or char.isdigit():	
										self.column += 1
										self.current += 1
										token += char
									else:
										break
						else:
							while True:
								char = self.peek()
								if not char:
									break
								elif char.isdigit():	
									self.column += 1
									self.current += 1
									token += char
								else:
									break
					else:
						raise Error(f"Unrecognized character on line: {self.line} column: {self.column}")


					if token in OPCODES:
						token_type = "OPCODE"
					elif token[0].isdigit():                                                                                                                                       
						token_type = "NUMBER"                                                                                                                                      
					else:                                                                                                                                                          
						raise RuntimeError(f"Unknown instruction '{token}' on line {location[0]} column {location[1]}")

					token = Token(token_type, token, location)

					yield token

	def peek(self):

		try:
			char = self.source[self.current]
		except Exception as e:
			char = None

		return char
				



		

