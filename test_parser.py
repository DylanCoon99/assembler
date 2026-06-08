import pytest
from lexer import Lexer
from parser import Parser, InstructionNode


class TestSingleInstructions:

	def test_nop(self):
		parser = Parser(Lexer("NOP"))
		head = parser.parse()
		assert head.opcode == "NOP"
		assert head.operand is None
		assert head.next is None

	def test_hlt(self):
		parser = Parser(Lexer("HLT"))
		head = parser.parse()
		assert head.opcode == "HLT"
		assert head.operand is None

	def test_lda_hex(self):
		parser = Parser(Lexer("LDA 0x0F"))
		head = parser.parse()
		assert head.opcode == "LDA"
		assert head.operand == 15

	def test_lda_decimal(self):
		parser = Parser(Lexer("LDA 10"))
		head = parser.parse()
		assert head.opcode == "LDA"
		assert head.operand == 10

	def test_lda_binary(self):
		parser = Parser(Lexer("LDA 0b1010"))
		head = parser.parse()
		assert head.opcode == "LDA"
		assert head.operand == 10

	def test_ldib(self):
		parser = Parser(Lexer("LDIB 0xFF"))
		head = parser.parse()
		assert head.opcode == "LDIB"
		assert head.operand == 255

	def test_movab(self):
		parser = Parser(Lexer("MOVAB"))
		head = parser.parse()
		assert head.opcode == "MOVAB"
		assert head.operand is None

	def test_movba(self):
		parser = Parser(Lexer("MOVBA"))
		head = parser.parse()
		assert head.opcode == "MOVBA"
		assert head.operand is None

	def test_out(self):
		parser = Parser(Lexer("OUT"))
		head = parser.parse()
		assert head.opcode == "OUT"
		assert head.operand is None


class TestLinkedListStructure:

	def test_two_instructions(self):
		parser = Parser(Lexer("LDA 0x01\nHLT"))
		head = parser.parse()
		assert head.opcode == "LDA"
		assert head.operand == 1
		assert head.next.opcode == "HLT"
		assert head.next.next is None

	def test_three_instructions(self):
		parser = Parser(Lexer("NOP\nNOP\nHLT"))
		head = parser.parse()
		assert head.opcode == "NOP"
		assert head.next.opcode == "NOP"
		assert head.next.next.opcode == "HLT"
		assert head.next.next.next is None

	def test_full_program(self):
		source = "LDA 0x01\nLDB 0x02\nADD 0x03\nJZ 0x0A\nSTA 0x03\nJMP 0x00\nNOP\nHLT"
		parser = Parser(Lexer(source))
		head = parser.parse()

		expected = [
			("LDA", 1),
			("LDB", 2),
			("ADD", 3),
			("JZ", 10),
			("STA", 3),
			("JMP", 0),
			("NOP", None),
			("HLT", None),
		]

		node = head
		for opcode, operand in expected:
			assert node is not None
			assert node.opcode == opcode
			assert node.operand == operand
			node = node.next

		assert node is None


class TestAllOpcodesParse:

	@pytest.mark.parametrize("opcode", ["NOP", "MOVAB", "MOVBA", "OUT", "HLT"])
	def test_no_operand_opcodes(self, opcode):
		parser = Parser(Lexer(opcode))
		head = parser.parse()
		assert head.opcode == opcode
		assert head.operand is None

	@pytest.mark.parametrize("opcode", ["LDA", "STA", "LDIA", "LDIB", "LDB", "STB", "ADD", "SUB", "JMP", "JZ", "JNZ"])
	def test_operand_opcodes(self, opcode):
		parser = Parser(Lexer(f"{opcode} 42"))
		head = parser.parse()
		assert head.opcode == opcode
		assert head.operand == 42


class TestNumberFormats:

	def test_hex_uppercase(self):
		parser = Parser(Lexer("LDA 0xAB"))
		head = parser.parse()
		assert head.operand == 171

	def test_hex_lowercase(self):
		parser = Parser(Lexer("LDA 0xab"))
		head = parser.parse()
		assert head.operand == 171

	def test_binary(self):
		parser = Parser(Lexer("LDA 0b11111111"))
		head = parser.parse()
		assert head.operand == 255

	def test_decimal_zero(self):
		parser = Parser(Lexer("JMP 0"))
		head = parser.parse()
		assert head.operand == 0


class TestErrors:

	def test_missing_operand(self):
		with pytest.raises(ValueError):
			parser = Parser(Lexer("LDA"))
			parser.parse()

	def test_invalid_instruction(self):
		with pytest.raises(Exception):
			parser = Parser(Lexer("FOO"))
			parser.parse()

	def test_number_without_opcode(self):
		with pytest.raises(Exception):
			parser = Parser(Lexer("42"))
			parser.parse()

	def test_empty_input(self):
		parser = Parser(Lexer(""))
		head = parser.parse()
		assert head is None
