from parser import Parser

ROM_SIZE = 32768


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


	def __init__(self, parser: Parser, output_name: str):
		self.parser = parser
		self.output = output_name


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

		lower_bytes = []
		upper_bytes = []

		instructions = self.parser.parse()
		current = instructions

		while current != None:
			opcode = OPCODE_MAP[current.opcode]
			operand = current.operand if current.operand is not None else 0

			lower_instr = operand.to_bytes(1, byteorder='big')
			upper_instr = opcode.to_bytes(1, byteorder='big')
			lower_bytes.append(lower_instr)
			upper_bytes.append(upper_instr)
			current = current.next


		with open(f"{self.output}_lower.bin", "wb") as f_lower, open(f"{self.output}_upper.bin", "wb") as f_upper:
			for line in lower_bytes:
				f_lower.write(line)
			for line in upper_bytes:
				f_upper.write(line)
			f_lower.write(b'\x00' * (ROM_SIZE - len(lower_bytes)))
			f_upper.write(b'\x00' * (ROM_SIZE - len(upper_bytes)))
			

		return 


