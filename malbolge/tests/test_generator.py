"""
Tests for Malbolge Code Generator
"""

import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from malbolge.generator import MalbolgeGenerator, MalbolgeAssembler


class TestMalbolgeGenerator:
    """Test cases for Malbolge code generator"""

    def test_generator_initialization(self):
        """Test generator initializes correctly"""
        gen = MalbolgeGenerator()

        assert gen.position == 0
        assert len(gen.blocks) == 0
        assert len(gen.labels) == 0

    def test_emit_single_instruction(self):
        """Test emitting a single instruction"""
        gen = MalbolgeGenerator()

        gen.emit('o')  # NOP
        code = gen.compile()

        assert len(code) > 0
        assert gen.position == 1

    def test_emit_multiple_instructions(self):
        """Test emitting multiple instructions"""
        gen = MalbolgeGenerator()

        gen.nop().nop().nop()
        code = gen.compile()

        assert len(code) == 3
        assert gen.position == 3

    def test_halt_instruction(self):
        """Test halt instruction generation"""
        gen = MalbolgeGenerator()

        gen.halt()
        code = gen.compile()

        assert len(code) == 1

    def test_label_creation(self):
        """Test label creation"""
        gen = MalbolgeGenerator()

        gen.label("start")
        gen.nop()
        gen.label("end")
        gen.halt()

        assert "start" in gen.labels
        assert "end" in gen.labels
        assert gen.labels["start"] == 0
        assert gen.labels["end"] == 1

    def test_alignment(self):
        """Test code alignment"""
        gen = MalbolgeGenerator()

        gen.nop()  # Position 1
        gen.align(4)  # Align to 4

        assert gen.position % 4 == 0

    def test_padding(self):
        """Test padding to position"""
        gen = MalbolgeGenerator()

        gen.pad_to(10)

        assert gen.position == 10

    def test_repeat_instruction(self):
        """Test repeating instruction"""
        gen = MalbolgeGenerator()

        gen.repeat('o', 5)

        assert gen.position == 5

    def test_reset(self):
        """Test generator reset"""
        gen = MalbolgeGenerator()

        gen.nop().nop()
        gen.label("test")

        gen.reset()

        assert gen.position == 0
        assert len(gen.labels) == 0

    def test_position_aware_generation(self):
        """Test position-aware code generation"""
        gen = MalbolgeGenerator()

        # Each position may require different character for same instruction
        gen.nop()
        pos1 = gen.position

        gen.nop()
        pos2 = gen.position

        assert pos2 == pos1 + 1

    def test_chaining(self):
        """Test method chaining"""
        gen = MalbolgeGenerator()

        code = gen.nop().rotate_acc().output_char().halt().compile()

        assert len(code) == 4


class TestMalbolgeAssembler:
    """Test cases for Malbolge assembler"""

    def test_assembler_initialization(self):
        """Test assembler initializes correctly"""
        asm = MalbolgeAssembler()

        assert asm.gen is not None

    def test_echo_program(self):
        """Test echo program generation"""
        asm = MalbolgeAssembler()

        code = asm.echo_program()

        assert len(code) > 0

    def test_set_accumulator(self):
        """Test set accumulator macro"""
        asm = MalbolgeAssembler()

        asm.set_accumulator(42)
        code = asm.compile()

        # Should generate rotation instructions
        assert len(code) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
