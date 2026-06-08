import pytest
from lexer import Lexer, Token


class TestSingleTokens:

	def test_nop(self):
		tokens = list(Lexer("NOP"))
		assert len(tokens) == 1
		assert tokens[0].type == "OPCODE"
		assert tokens[0].value == "NOP"

	def test_hlt(self):
		tokens = list(Lexer("HLT"))
		assert len(tokens) == 1
		assert tokens[0].type == "OPCODE"
		assert tokens[0].value == "HLT"

	def test_decimal_number(self):
		tokens = list(Lexer("15"))
		assert len(tokens) == 1
		assert tokens[0].type == "NUMBER"
		assert tokens[0].value == "15"

	def test_hex_number(self):
		tokens = list(Lexer("0xFF"))
		assert len(tokens) == 1
		assert tokens[0].type == "NUMBER"
		assert tokens[0].value == "0xFF"

	def test_binary_number(self):
		tokens = list(Lexer("0b1010"))
		assert len(tokens) == 1
		assert tokens[0].type == "NUMBER"
		assert tokens[0].value == "0b1010"

	def test_zero(self):
		tokens = list(Lexer("0"))
		assert len(tokens) == 1
		assert tokens[0].type == "NUMBER"
		assert tokens[0].value == "0"


class TestInstructions:

	def test_lda_hex(self):
		tokens = list(Lexer("LDA 0x0F"))
		assert len(tokens) == 2
		assert tokens[0].type == "OPCODE"
		assert tokens[0].value == "LDA"
		assert tokens[1].type == "NUMBER"
		assert tokens[1].value == "0x0F"

	def test_ldib_decimal(self):
		tokens = list(Lexer("LDIB 5"))
		assert len(tokens) == 2
		assert tokens[0].type == "OPCODE"
		assert tokens[0].value == "LDIB"
		assert tokens[1].type == "NUMBER"
		assert tokens[1].value == "5"

	def test_jz_binary(self):
		tokens = list(Lexer("JZ 0b1100"))
		assert len(tokens) == 2
		assert tokens[0].type == "OPCODE"
		assert tokens[0].value == "JZ"
		assert tokens[1].type == "NUMBER"
		assert tokens[1].value == "0b1100"

	def test_movab_no_operand(self):
		tokens = list(Lexer("MOVAB"))
		assert len(tokens) == 1
		assert tokens[0].type == "OPCODE"
		assert tokens[0].value == "MOVAB"


class TestLocations:

	def test_first_token_location(self):
		tokens = list(Lexer("LDA 0x0F"))
		assert tokens[0].location == (0, 0)

	def test_second_token_location(self):
		tokens = list(Lexer("LDA 0x0F"))
		assert tokens[1].location == (0, 4)

	def test_second_line(self):
		tokens = list(Lexer("LDA 0x0F\nHLT"))
		assert tokens[2].location == (1, 0)

	def test_multiple_lines(self):
		tokens = list(Lexer("NOP\nNOP\nHLT"))
		assert tokens[0].location == (0, 0)
		assert tokens[1].location == (1, 0)
		assert tokens[2].location == (2, 0)


class TestMultipleSpaces:

	def test_extra_spaces(self):
		tokens = list(Lexer("LDA   0x0F"))
		assert len(tokens) == 2
		assert tokens[0].value == "LDA"
		assert tokens[1].value == "0x0F"


class TestFullProgram:

	def test_program(self):
		source = "LDA 0x01\nLDB 0x02\nADD 0x03\nJZ 0x0A\nSTA 0x03\nJMP 0x00\nNOP\nHLT"
		tokens = list(Lexer(source))
		assert len(tokens) == 14

		expected_values = [
			"LDA", "0x01",
			"LDB", "0x02",
			"ADD", "0x03",
			"JZ", "0x0A",
			"STA", "0x03",
			"JMP", "0x00",
			"NOP",
			"HLT",
		]
		for token, expected in zip(tokens, expected_values):
			assert token.value == expected


class TestAllOpcodes:

	@pytest.mark.parametrize("opcode", [
		"NOP", "LDA", "STA", "LDIA", "LDIB", "MOVAB", "MOVBA",
		"LDB", "STB", "ADD", "SUB", "JMP", "JZ", "JNZ", "OUT", "HLT"
	])
	def test_opcode_recognized(self, opcode):
		tokens = list(Lexer(opcode))
		assert tokens[0].type == "OPCODE"
		assert tokens[0].value == opcode


class TestErrors:

	def test_invalid_instruction(self):
		with pytest.raises(Exception):
			list(Lexer("FOO"))

	def test_invalid_character(self):
		with pytest.raises(Exception):
			list(Lexer("@"))

	def test_empty_input(self):
		tokens = list(Lexer(""))
		assert tokens == []
