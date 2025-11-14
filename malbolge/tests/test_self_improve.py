"""
Tests for Self-Improving Compiler
"""

import pytest
from pathlib import Path
import tempfile

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from malbolge.self_improve import SelfImprovingCompiler


class TestSelfImprovingCompiler:
    """Test cases for self-improving compiler"""

    def test_compiler_initialization(self):
        """Test compiler initializes correctly"""
        with tempfile.TemporaryDirectory() as tmpdir:
            compiler = SelfImprovingCompiler(save_dir=Path(tmpdir))

            assert len(compiler.benchmarks) > 0
            assert compiler.current_generation == 0

    def test_bootstrap(self):
        """Test compiler bootstrap"""
        with tempfile.TemporaryDirectory() as tmpdir:
            compiler = SelfImprovingCompiler(save_dir=Path(tmpdir))

            variant = compiler.bootstrap()

            assert variant is not None
            assert variant.generation == 0
            assert len(variant.code) > 0
            assert variant.fitness >= 0

    def test_fitness_calculation(self):
        """Test fitness calculation"""
        with tempfile.TemporaryDirectory() as tmpdir:
            compiler = SelfImprovingCompiler(save_dir=Path(tmpdir))

            metrics = {
                'compilation_time': 1.0,
                'output_quality': 0.8,
                'code_size': 100,
                'benchmark_success': 1.0
            }

            fitness = compiler._calculate_fitness(metrics)

            assert 0.0 <= fitness <= 1.0

    def test_variant_saving(self):
        """Test variant is saved to disk"""
        with tempfile.TemporaryDirectory() as tmpdir:
            compiler = SelfImprovingCompiler(save_dir=Path(tmpdir))

            variant = compiler.bootstrap()

            # Check files exist
            gen_dir = Path(tmpdir) / "gen_0000"
            assert gen_dir.exists()

            code_file = gen_dir / f"{variant.id}.mal"
            meta_file = gen_dir / f"{variant.id}.json"

            assert code_file.exists()
            assert meta_file.exists()

    def test_evolution_single_generation(self):
        """Test single generation evolution"""
        with tempfile.TemporaryDirectory() as tmpdir:
            compiler = SelfImprovingCompiler(save_dir=Path(tmpdir))

            compiler.bootstrap()
            best = compiler.evolve(generations=1, population_size=3)

            assert best is not None
            assert len(compiler.stats) == 1

    def test_get_best_variant(self):
        """Test getting best variant"""
        with tempfile.TemporaryDirectory() as tmpdir:
            compiler = SelfImprovingCompiler(save_dir=Path(tmpdir))

            compiler.bootstrap()
            best = compiler.get_best_variant()

            assert best is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
