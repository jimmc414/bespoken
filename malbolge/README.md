# Malbolge Self-Improving Optimizing Compiler

A meta-circular, self-improving optimizing compiler for Malbolge, with the compiler core written in Malbolge itself.

## Overview

This project implements a complete toolchain for the Malbolge programming language:

1. **Malbolge VM** - A virtual machine interpreter that executes Malbolge programs
2. **Code Generator** - Tools to generate Malbolge code programmatically
3. **Optimizer** - Multi-pass optimization engine for Malbolge bytecode
4. **Self-Improving Compiler** - A meta-circular compiler that optimizes itself
5. **Bootstrap System** - Transpiles high-level compiler logic to Malbolge

## What is Malbolge?

Malbolge is an esoteric programming language designed by Ben Olmstead in 1998 to be as difficult as possible to program in. Features include:

- **Ternary (base-3) arithmetic** - All operations use modulo 3^10 (59049)
- **Self-modifying code** - Instructions encrypt themselves after execution
- **Encrypted instructions** - Commands are encoded using a complex cipher
- **Minimal instruction set** - Only 8 operations
- **Memory manipulation** - Direct access to a 59049-cell memory space

## Architecture

### 1. Malbolge Virtual Machine (`vm.py`)
Executes Malbolge programs with:
- Full instruction set implementation
- Memory and register management
- I/O handling
- Execution tracing and debugging

### 2. Code Generator (`generator.py`)
Programmatic Malbolge code generation:
- High-level instruction builder
- Memory layout management
- Automatic NOP generation
- Code positioning and alignment

### 3. Optimizer (`optimizer.py`)
Multi-pass optimization engine:
- Dead code elimination
- Constant folding
- Instruction combining
- Memory access optimization
- Self-modification pattern recognition

### 4. Self-Improvement Engine (`self_improve.py`)
Meta-circular compilation system:
- Compiles itself to Malbolge
- Measures compilation performance
- Applies optimizations iteratively
- Evolves optimization strategies
- Fitness-based selection

### 5. Bootstrap Compiler (`compiler.mal`)
The actual compiler written in Malbolge:
- Lexical analysis
- Parsing
- Code generation
- Optimization passes
- Generated from high-level specification

## Usage

```python
# Run a Malbolge program
from malbolge.vm import MalbolgeVM

vm = MalbolgeVM()
vm.load_program(program_code)
vm.run()

# Generate Malbolge code
from malbolge.generator import MalbolgeGenerator

gen = MalbolgeGenerator()
gen.set_register('a', 42)
gen.output_char()
code = gen.compile()

# Optimize Malbolge code
from malbolge.optimizer import MalbolgeOptimizer

opt = MalbolgeOptimizer()
optimized = opt.optimize(code, passes=10)

# Self-improve the compiler
from malbolge.self_improve import SelfImprovingCompiler

compiler = SelfImprovingCompiler()
compiler.bootstrap()
compiler.evolve(generations=100)
```

## File Structure

```
malbolge/
├── README.md                 # This file
├── vm.py                     # Malbolge virtual machine
├── generator.py              # Code generator
├── optimizer.py              # Optimization engine
├── self_improve.py           # Self-improvement system
├── compiler.mal              # Bootstrap compiler (in Malbolge)
├── compiler_spec.py          # High-level compiler specification
├── tests/                    # Test suite
│   ├── test_vm.py
│   ├── test_generator.py
│   ├── test_optimizer.py
│   └── test_self_improve.py
├── examples/                 # Example programs
│   ├── hello_world.mal
│   ├── cat.mal
│   └── compiler_demo.mal
└── docs/                     # Documentation
    ├── malbolge_spec.md
    ├── optimization_strategies.md
    └── self_improvement.md
```

## How Self-Improvement Works

1. **Bootstrap Phase**: The compiler spec is written in Python and transpiled to Malbolge
2. **Compilation Phase**: The Malbolge compiler compiles test programs
3. **Measurement Phase**: Compilation time, code size, and execution speed are measured
4. **Optimization Phase**: The optimizer modifies its own optimization strategies
5. **Selection Phase**: Better-performing compiler variants are kept
6. **Iteration**: The process repeats, creating increasingly efficient compilers

## Requirements

- Python 3.8+
- No external dependencies (pure Python implementation)

## License

MIT License
