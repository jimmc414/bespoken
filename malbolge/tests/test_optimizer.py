"""
Tests for Malbolge Optimizer
"""

import pytest

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from malbolge.optimizer import MalbolgeOptimizer
from malbolge.generator import MalbolgeGenerator


class TestMalbolgeOptimizer:
    """Test cases for Malbolge optimizer"""

    def test_optimizer_initialization(self):
        """Test optimizer initializes correctly"""
        opt = MalbolgeOptimizer()

        assert len(opt.passes) > 0
        assert all(p.enabled for p in opt.passes)

    def test_dead_code_elimination(self):
        """Test dead code elimination pass"""
        gen = MalbolgeGenerator()
        gen.nop()
        gen.halt()
        gen.nop().nop().nop()  # Dead code after halt

        code = gen.compile()
        original_size = len(code)

        opt = MalbolgeOptimizer()
        result = opt.optimize(code, passes=1)

        # Should remove dead code
        assert result.optimized_size < original_size

    def test_nop_reduction(self):
        """Test NOP reduction pass"""
        gen = MalbolgeGenerator()

        # Many consecutive NOPs
        for _ in range(10):
            gen.nop()
        gen.halt()

        code = gen.compile()
        original_size = len(code)

        opt = MalbolgeOptimizer()
        result = opt.optimize(code, passes=1, enabled_passes=['nop_reduction'])

        # Should reduce NOPs
        assert result.optimized_size <= original_size

    def test_multiple_passes(self):
        """Test multiple optimization passes"""
        gen = MalbolgeGenerator()

        for _ in range(5):
            gen.nop()
        gen.rotate_acc()
        gen.halt()
        gen.nop().nop()

        code = gen.compile()

        opt = MalbolgeOptimizer()
        result = opt.optimize(code, passes=3)

        assert 'dead_code_elimination' in result.passes_applied or \
               'nop_reduction' in result.passes_applied

    def test_optimization_preserves_functionality(self):
        """Test that optimization preserves program functionality"""
        gen = MalbolgeGenerator()
        gen.nop()
        gen.halt()

        code = gen.compile()

        opt = MalbolgeOptimizer()
        result = opt.optimize(code, passes=2)

        # Both should halt
        from malbolge.vm import MalbolgeVM

        vm1 = MalbolgeVM()
        vm1.load_program(code)
        vm1.run(max_steps=100)

        vm2 = MalbolgeVM()
        vm2.load_program(result.code)
        vm2.run(max_steps=100)

        assert vm1.halted and vm2.halted

    def test_performance_measurement(self):
        """Test performance measurement"""
        gen = MalbolgeGenerator()
        gen.nop()
        gen.halt()
        code = gen.compile()

        opt = MalbolgeOptimizer()
        perf = opt._measure_performance(code, max_steps=100)

        assert perf > 0
        assert perf != float('inf')


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
