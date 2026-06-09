import pytest
import os
from lexer import Lexer
from parser import Parser
from assembler import Assembler, ROM_SIZE


@pytest.fixture
def assemble(tmp_path):
	def _assemble(source):
		output = str(tmp_path / "out")
		lexer = Lexer(source)
		parser = Parser(lexer)
		assembler = Assembler(parser, output)
		assembler.assemble()
		upper = (tmp_path / "out_upper.bin").read_bytes()
		lower = (tmp_path / "out_lower.bin").read_bytes()
		return upper, lower
	return _assemble


class TestFileOutput:

	def test_files_are_rom_size(self, assemble):
		upper, lower = assemble("NOP")
		assert len(upper) == ROM_SIZE
		assert len(lower) == ROM_SIZE

	def test_padding_is_zeros(self, assemble):
		upper, lower = assemble("HLT")
		assert upper[1:] == b'\x00' * (ROM_SIZE - 1)
		assert lower[1:] == b'\x00' * (ROM_SIZE - 1)


class TestSingleInstructions:

	def test_nop(self, assemble):
		upper, lower = assemble("NOP")
		assert upper[0] == 0x00
		assert lower[0] == 0x00

	def test_hlt(self, assemble):
		upper, lower = assemble("HLT")
		assert upper[0] == 0x0F
		assert lower[0] == 0x00

	def test_lda(self, assemble):
		upper, lower = assemble("LDA 0x0F")
		assert upper[0] == 0x01
		assert lower[0] == 0x0F

	def test_sta(self, assemble):
		upper, lower = assemble("STA 0x05")
		assert upper[0] == 0x02
		assert lower[0] == 0x05

	def test_ldia(self, assemble):
		upper, lower = assemble("LDIA 10")
		assert upper[0] == 0x03
		assert lower[0] == 10

	def test_ldib(self, assemble):
		upper, lower = assemble("LDIB 0xFF")
		assert upper[0] == 0x04
		assert lower[0] == 0xFF

	def test_movab(self, assemble):
		upper, lower = assemble("MOVAB")
		assert upper[0] == 0x05
		assert lower[0] == 0x00

	def test_movba(self, assemble):
		upper, lower = assemble("MOVBA")
		assert upper[0] == 0x06
		assert lower[0] == 0x00

	def test_ldb(self, assemble):
		upper, lower = assemble("LDB 0x0A")
		assert upper[0] == 0x07
		assert lower[0] == 0x0A

	def test_stb(self, assemble):
		upper, lower = assemble("STB 0x03")
		assert upper[0] == 0x08
		assert lower[0] == 0x03

	def test_add(self, assemble):
		upper, lower = assemble("ADD 0x03")
		assert upper[0] == 0x09
		assert lower[0] == 0x03

	def test_sub(self, assemble):
		upper, lower = assemble("SUB 0x0F")
		assert upper[0] == 0x0A
		assert lower[0] == 0x0F

	def test_jmp(self, assemble):
		upper, lower = assemble("JMP 0x00")
		assert upper[0] == 0x0B
		assert lower[0] == 0x00

	def test_jz(self, assemble):
		upper, lower = assemble("JZ 0x0E")
		assert upper[0] == 0x0C
		assert lower[0] == 0x0E

	def test_jnz(self, assemble):
		upper, lower = assemble("JNZ 0x05")
		assert upper[0] == 0x0D
		assert lower[0] == 0x05

	def test_out(self, assemble):
		upper, lower = assemble("OUT")
		assert upper[0] == 0x0E
		assert lower[0] == 0x00


class TestMultipleInstructions:

	def test_instruction_ordering(self, assemble):
		upper, lower = assemble("LDA 0x01\nSTB 0x02\nHLT")
		assert upper[0] == 0x01  # LDA
		assert upper[1] == 0x08  # STB
		assert upper[2] == 0x0F  # HLT
		assert lower[0] == 0x01
		assert lower[1] == 0x02
		assert lower[2] == 0x00

	def test_full_program(self, assemble):
		source = "LDA 0x01\nLDB 0x02\nADD 0x03\nJZ 0x0A\nSTA 0x03\nJMP 0x00\nNOP\nHLT"
		upper, lower = assemble(source)

		expected_upper = [0x01, 0x07, 0x09, 0x0C, 0x02, 0x0B, 0x00, 0x0F]
		expected_lower = [0x01, 0x02, 0x03, 0x0A, 0x03, 0x00, 0x00, 0x00]

		for i, (eu, el) in enumerate(zip(expected_upper, expected_lower)):
			assert upper[i] == eu, f"upper byte {i} mismatch"
			assert lower[i] == el, f"lower byte {i} mismatch"

		# rest is zeros
		assert upper[8:] == b'\x00' * (ROM_SIZE - 8)
		assert lower[8:] == b'\x00' * (ROM_SIZE - 8)


class TestOperandZero:

	def test_jmp_zero(self, assemble):
		upper, lower = assemble("JMP 0")
		assert upper[0] == 0x0B
		assert lower[0] == 0x00

	def test_ldia_zero(self, assemble):
		upper, lower = assemble("LDIA 0")
		assert upper[0] == 0x03
		assert lower[0] == 0x00


class TestEmptyInput:

	def test_empty(self, assemble):
		upper, lower = assemble("")
		assert upper == b'\x00' * ROM_SIZE
		assert lower == b'\x00' * ROM_SIZE
