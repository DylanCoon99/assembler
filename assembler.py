from parser import Parser



OPCODE_MAP = {
	"NOP": 0,
	"LDA": 1,
	"STA": 2,
	"LDIA": 3,
	"LDIB": 4,
	"MOVAB": 5,
	"MOVBA": 6,
	"LDB": 7,
	"STB": 8,
	"ADD": 9,
	"SUB": 10,
	"JMP": 11,
	"JZ": 12,
	"JNZ": 13,
	"OUT": 14, 
	"HLT": 15,
}


class Assembler:


	def __init__(self, parser: Parser, output: str):
		self.parser = parser
		self.output = output


	@property
	def parser(self):
		return self._parser


	@parser.setter
	def parser(self, value):
		# Enfore validation logic
		if not isinstance(value, Parser):
			raise ValueError(f"Expected {value} to be Parser type")
		self._parser = value


	@staticmethod
	def encode(opcode: str) -> str:
		return f"{OPCODE_MAP[opcode]:08b}"


	def assemble(self):

		code = []

		instructions = self.parser.parse()
		current = instructions

		while current != None:
			opcode = OPCODE_MAP[current.opcode]
			operand = current.operand if current.operand else 0

			instr = int(f"{opcode:08b}{operand:08b}", 2).to_bytes(2, byteorder='big')
			code.append(instr)
			current = current.next


		with open(self.output, "wb") as f:
			for line in code:
				f.write(line)
			

		return


