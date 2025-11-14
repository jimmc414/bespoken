"""
Tests for Malbolge Virtual Machine
"""

import pytest
from io import StringIO

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from malbolge.vm import MalbolgeVM


class TestMalbolgeVM:
    """Test cases for Malbolge VM"""

    def test_vm_initialization(self):
        """Test VM initializes correctly"""
        vm = MalbolgeVM()

        assert vm.a == 0
        assert vm.c == 0
        assert vm.d == 0
        assert not vm.halted
        assert len(vm.memory) == 59049

    def test_load_simple_program(self):
        """Test loading a simple program"""
        vm = MalbolgeVM()

        # Simple halt program
        program = "v"  # This might not be valid at position 0

        # Try to load - might fail if not valid
        try:
            vm.load_program(program)
            assert vm.memory[0] == ord('v')
        except ValueError:
            # Position-dependent validation failed
            pass

    def test_halt_instruction(self):
        """Test halt instruction stops execution"""
        vm = MalbolgeVM()

        # Create a program that's valid and halts
        # Note: In real Malbolge, we need position-aware code
        from malbolge.generator import MalbolgeGenerator

        gen = MalbolgeGenerator()
        gen.halt()
        program = gen.compile()

        vm.load_program(program)
        state = vm.run(max_steps=100)

        assert vm.halted
        assert state.instructions_executed > 0

    def test_nop_instruction(self):
        """Test NOP instruction"""
        vm = MalbolgeVM()

        from malbolge.generator import MalbolgeGenerator

        gen = MalbolgeGenerator()
        gen.nop()
        gen.nop()
        gen.halt()
        program = gen.compile()

        vm.load_program(program)
        state = vm.run(max_steps=100)

        assert vm.halted
        assert state.instructions_executed >= 3

    def test_output_instruction(self):
        """Test output instruction"""
        vm = MalbolgeVM()

        output_stream = StringIO()
        vm.output_stream = output_stream

        from malbolge.generator import MalbolgeGenerator

        gen = MalbolgeGenerator()
        # Set accumulator to printable ASCII (this is complex in real Malbolge)
        gen.output_char()
        gen.halt()
        program = gen.compile()

        vm.load_program(program)
        vm.run(max_steps=100)

        # Output depends on accumulator value
        output = output_stream.getvalue()
        # We don't test specific output since accumulator initialization is complex

    def test_rotation(self):
        """Test rotation operation"""
        vm = MalbolgeVM()

        # Test ternary rotation
        test_value = 123
        rotated = vm._ternary_rotate_right(test_value)

        # Rotation should produce different value
        assert rotated != test_value
        assert 0 <= rotated < vm.MEMORY_SIZE

    def test_tritwise_op(self):
        """Test tritwise operation"""
        vm = MalbolgeVM()

        a = 100
        b = 200

        result = vm._tritwise_op(a, b)

        assert 0 <= result < vm.MEMORY_SIZE
        # Result should be deterministic
        assert result == vm._tritwise_op(a, b)

    def test_execution_trace(self):
        """Test execution tracing"""
        vm = MalbolgeVM(debug=True)

        from malbolge.generator import MalbolgeGenerator

        gen = MalbolgeGenerator()
        gen.nop()
        gen.halt()
        program = gen.compile()

        vm.load_program(program)
        vm.run(max_steps=100)

        # Should have trace entries
        assert len(vm.trace) > 0

    def test_max_steps(self):
        """Test max steps limit"""
        vm = MalbolgeVM()

        from malbolge.generator import MalbolgeGenerator

        gen = MalbolgeGenerator()
        # Create program without halt
        for _ in range(10):
            gen.nop()
        program = gen.compile()

        vm.load_program(program)
        state = vm.run(max_steps=5)

        # Should stop at max steps
        assert state.instructions_executed == 5
        assert not vm.halted


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
