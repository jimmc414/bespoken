"""
Malbolge Self-Improving Optimizing Compiler

A complete toolchain for the Malbolge esoteric programming language,
including a meta-circular compiler that can improve itself.

Components:
- vm: Malbolge virtual machine
- generator: Code generation tools
- optimizer: Multi-pass optimization engine
- self_improve: Self-improving compiler system
- compiler_spec: High-level compiler specification

Example usage:

    # Run a Malbolge program
    from malbolge.vm import MalbolgeVM

    vm = MalbolgeVM()
    vm.load_program(program_code)
    vm.run()

    # Generate Malbolge code
    from malbolge.generator import MalbolgeGenerator

    gen = MalbolgeGenerator()
    gen.output_char().halt()
    code = gen.compile()

    # Optimize code
    from malbolge.optimizer import MalbolgeOptimizer

    opt = MalbolgeOptimizer()
    result = opt.optimize(code, passes=5)

    # Self-improving compiler
    from malbolge.self_improve import SelfImprovingCompiler

    compiler = SelfImprovingCompiler()
    compiler.bootstrap()
    best = compiler.evolve(generations=100)
"""

__version__ = "1.0.0"
__author__ = "Claude"

from .vm import MalbolgeVM, ExecutionState
from .generator import MalbolgeGenerator, MalbolgeAssembler
from .optimizer import MalbolgeOptimizer, OptimizationResult
from .self_improve import SelfImprovingCompiler, CompilerVariant
from .compiler_spec import MalbolgeCompilerSpec, generate_bootstrap_compiler

__all__ = [
    # VM
    'MalbolgeVM',
    'ExecutionState',

    # Generator
    'MalbolgeGenerator',
    'MalbolgeAssembler',

    # Optimizer
    'MalbolgeOptimizer',
    'OptimizationResult',

    # Self-improvement
    'SelfImprovingCompiler',
    'CompilerVariant',

    # Compiler spec
    'MalbolgeCompilerSpec',
    'generate_bootstrap_compiler',
]
