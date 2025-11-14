# Malbolge Self-Improving Compiler - Complete Guide

## Table of Contents

1. [Introduction](#introduction)
2. [Quick Start](#quick-start)
3. [Installation](#installation)
4. [Components](#components)
5. [Usage Examples](#usage-examples)
6. [Understanding Malbolge](#understanding-malbolge)
7. [How Self-Improvement Works](#how-self-improvement-works)
8. [Advanced Usage](#advanced-usage)
9. [Troubleshooting](#troubleshooting)
10. [Contributing](#contributing)

## Introduction

This project implements a complete toolchain for the Malbolge esoteric programming language, culminating in a **self-improving optimizing compiler written in Malbolge itself**.

### What Makes This Special?

- **Meta-circular**: The compiler is written in Malbolge and compiles Malbolge
- **Self-improving**: The compiler optimizes itself through evolution
- **Complete toolchain**: VM, code generator, optimizer, all included
- **Actually works**: Despite Malbolge's extreme difficulty

### Key Features

- ✅ Full Malbolge virtual machine implementation
- ✅ Programmatic code generation
- ✅ Multi-pass optimization engine
- ✅ Genetic algorithm-based evolution
- ✅ Bootstrap compiler in pure Malbolge
- ✅ Comprehensive test suite
- ✅ Example programs and documentation

## Quick Start

### Run the Complete Demo

```bash
cd malbolge
python demo.py
```

This runs a complete demonstration of all components.

### Try the Examples

```bash
# Simple halt program
python examples/simple_halt.py

# Optimization demonstration
python examples/optimization_demo.py

# Self-improving compiler (takes a few minutes)
python examples/self_improving_demo.py
```

### Run Tests

```bash
python -m pytest tests/ -v
```

## Installation

### Requirements

- Python 3.8 or higher
- No external dependencies (pure Python)

### Setup

```bash
# Clone the repository (if needed)
cd /path/to/bespoken

# The malbolge package is ready to use
cd malbolge

# Optional: Run tests to verify
python -m pytest tests/
```

## Components

### 1. Virtual Machine (`vm.py`)

The Malbolge VM executes Malbolge programs.

```python
from malbolge import MalbolgeVM

vm = MalbolgeVM()
vm.load_program(malbolge_code)
state = vm.run(max_steps=10000)

print(f"Executed {state.instructions_executed} instructions")
```

**Features**:
- Full instruction set (j, i, /, *, p, o, <, v)
- Ternary arithmetic
- Self-modifying code execution
- Position-dependent instruction normalization
- Execution tracing and debugging

### 2. Code Generator (`generator.py`)

Generate Malbolge code programmatically.

```python
from malbolge import MalbolgeGenerator

gen = MalbolgeGenerator()
gen.label("start")
gen.nop()
gen.rotate_acc()
gen.output_char()
gen.halt()

code = gen.compile()
```

**Features**:
- High-level instruction API
- Label management
- Code alignment and padding
- Position-aware generation
- Method chaining

### 3. Optimizer (`optimizer.py`)

Optimize Malbolge programs.

```python
from malbolge import MalbolgeOptimizer

opt = MalbolgeOptimizer()
result = opt.optimize(code, passes=5)

print(f"Size reduced by {result.stats['size_reduction_pct']:.1f}%")
```

**Optimization Passes**:
- Dead code elimination
- NOP reduction
- Rotation combining
- Memory access optimization
- Instruction reordering
- Constant propagation
- Self-modification optimization

### 4. Self-Improving Compiler (`self_improve.py`)

Meta-circular compiler that improves itself.

```python
from malbolge import SelfImprovingCompiler

compiler = SelfImprovingCompiler()
compiler.bootstrap()
best = compiler.evolve(generations=100)

print(f"Fitness improved to {best.fitness:.6f}")
```

**Features**:
- Genetic algorithm evolution
- Fitness-based selection
- Multi-generational improvement
- Automatic variant management
- Performance tracking

## Usage Examples

### Example 1: Execute a Malbolge Program

```python
from malbolge import MalbolgeVM, MalbolgeGenerator

# Generate simple program
gen = MalbolgeGenerator()
gen.nop()
gen.halt()
program = gen.compile()

# Execute it
vm = MalbolgeVM()
vm.load_program(program)
vm.run()

print(f"Program halted: {vm.halted}")
```

### Example 2: Optimize Code

```python
from malbolge import MalbolgeGenerator, MalbolgeOptimizer

# Create inefficient program
gen = MalbolgeGenerator()
for _ in range(20):
    gen.nop()
gen.halt()
for _ in range(10):
    gen.nop()  # Dead code

original = gen.compile()

# Optimize
opt = MalbolgeOptimizer()
result = opt.optimize(original, passes=3)

print(f"Reduced from {len(original)} to {len(result.code)} bytes")
```

### Example 3: Evolve the Compiler

```python
from malbolge import SelfImprovingCompiler
from pathlib import Path

# Create compiler
compiler = SelfImprovingCompiler(
    debug=True,
    save_dir=Path("./my_compiler")
)

# Bootstrap initial version
initial = compiler.bootstrap()
print(f"Initial fitness: {initial.fitness:.6f}")

# Evolve for 50 generations
best = compiler.evolve(
    generations=50,
    population_size=10,
    mutation_rate=0.1,
    elite_count=2
)

print(f"Final fitness: {best.fitness:.6f}")
print(f"Improvement: {(best.fitness/initial.fitness - 1)*100:.1f}%")

# View statistics
compiler.print_stats()
```

## Understanding Malbolge

### Why Is Malbolge Hard?

1. **Position-Dependent Instructions**
   - A character's meaning depends on where it is in the program
   - Same character at different positions = different instructions

2. **Self-Modifying Code**
   - Instructions change after execution
   - Programs evolve as they run

3. **Ternary Arithmetic**
   - Everything uses base-3 math
   - Unusual rotation and operations

4. **No Direct Control Flow**
   - No jumps or loops (must use self-modification)
   - Very limited instructions

### Key Concepts

**Instruction Normalization**:
```
normalized = XLAT1[(position + ASCII_value - 33) mod 94]
```

**Self-Modification**:
```
After execution: memory[position] = XLAT2[original_char - 33]
```

**Ternary Rotation**:
```
Convert to base-3 → Rotate right → Convert back
```

See `docs/malbolge_spec.md` for complete specification.

## How Self-Improvement Works

### The Evolution Loop

```
1. Bootstrap compiler from high-level spec
   ↓
2. Compile test programs (measure performance)
   ↓
3. Calculate fitness (speed, size, quality)
   ↓
4. Generate variants (crossover + mutation)
   ↓
5. Select best performers
   ↓
6. Repeat → Compiler improves itself
```

### Fitness Function

The compiler is evaluated on:
- **Compilation speed** (30%): How fast it compiles programs
- **Output quality** (30%): How good the compiled code is
- **Code size** (20%): How small the compiler is
- **Success rate** (20%): How many benchmarks it passes

### Why It Works

- Genetic algorithms explore solution space
- Fitness function guides evolution
- Elite preservation maintains progress
- Mutations provide innovation
- Over generations, better compilers emerge

See `docs/self_improvement.md` for detailed architecture.

## Advanced Usage

### Custom Benchmarks

Add your own benchmarks to test specific scenarios:

```python
from malbolge import SelfImprovingCompiler, CompilationBenchmark

compiler = SelfImprovingCompiler()

# Add custom benchmark
custom_benchmark = CompilationBenchmark(
    name="my_test",
    source_code="oo/pv",  # Your Malbolge code
    expected_output="...",
    max_execution_steps=50000
)

compiler.benchmarks.append(custom_benchmark)
compiler.bootstrap()
compiler.evolve(generations=20)
```

### Custom Optimization Passes

Create your own optimization pass:

```python
from malbolge import MalbolgeOptimizer

class MyOptimizer(MalbolgeOptimizer):
    def _pass_my_optimization(self, code):
        """My custom optimization"""
        stats = {'optimized': 0}

        # Your optimization logic here
        optimized_code = code  # modify code

        return optimized_code, stats

opt = MyOptimizer()
opt.passes.append(OptimizationPass(
    "my_optimization",
    "My custom optimization",
    enabled=True,
    priority=5
))

result = opt.optimize(code, passes=3)
```

### Genetic Algorithm Tuning

Experiment with evolution parameters:

```python
# Fast exploration (high mutation, large population)
best = compiler.evolve(
    generations=50,
    population_size=20,
    mutation_rate=0.3,
    elite_count=3
)

# Stable refinement (low mutation, small population)
best = compiler.evolve(
    generations=200,
    population_size=5,
    mutation_rate=0.05,
    elite_count=1
)
```

### Parallel Evolution

Run multiple evolutionary runs in parallel:

```python
from multiprocessing import Pool

def evolve_compiler(seed):
    import random
    random.seed(seed)

    compiler = SelfImprovingCompiler(
        save_dir=Path(f"./run_{seed}")
    )
    compiler.bootstrap()
    return compiler.evolve(generations=50)

# Run 4 parallel evolution runs
with Pool(4) as pool:
    results = pool.map(evolve_compiler, range(4))

# Get best from all runs
best = max(results, key=lambda v: v.fitness)
```

## Troubleshooting

### Program Won't Load

**Problem**: `ValueError: Invalid instruction at position X`

**Solution**: The character at that position doesn't normalize to a valid instruction. Use the generator instead of writing raw characters.

### Optimization Makes Code Worse

**Problem**: Optimized code performs worse

**Solution**:
- Reduce number of optimization passes
- Disable risky passes (instruction_reordering, self_modification_optimization)
- Use only safe passes (dead_code_elimination, nop_reduction)

### Evolution Not Improving

**Problem**: Fitness doesn't increase over generations

**Solution**:
- Increase population size (more diversity)
- Increase mutation rate (more exploration)
- Check that benchmarks are appropriate
- Run for more generations (may need 100+)
- Try multiple runs with different seeds

### Out of Memory

**Problem**: Process runs out of memory during evolution

**Solution**:
- Reduce population size
- Reduce number of benchmarks
- Set lower max_execution_steps
- Process generations in batches

### Code Doesn't Run

**Problem**: Generated code fails to execute

**Solution**:
- Verify with `vm.load_program()` first
- Check for position-dependent errors
- Use `debug=True` to trace execution
- Start with simpler programs

## Contributing

### Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_vm.py -v

# Run with coverage
python -m pytest tests/ --cov=malbolge
```

### Adding Tests

Add tests to `tests/test_*.py` files:

```python
def test_my_feature():
    """Test my new feature"""
    # Test code here
    assert expected == actual
```

### Code Style

- Follow PEP 8
- Use type hints where appropriate
- Add docstrings to functions
- Keep functions focused and small

### Documentation

Update documentation in `docs/` when adding features:
- `malbolge_spec.md`: Language specification
- `optimization_strategies.md`: Optimization techniques
- `self_improvement.md`: Evolution architecture

## Additional Resources

### Files to Explore

- `vm.py`: Virtual machine implementation
- `generator.py`: Code generation
- `optimizer.py`: Optimization engine
- `self_improve.py`: Self-improvement system
- `compiler_spec.py`: High-level compiler spec
- `compiler.mal`: The Malbolge compiler itself!

### Documentation

- `docs/malbolge_spec.md`: Complete language specification
- `docs/optimization_strategies.md`: Optimization techniques
- `docs/self_improvement.md`: Evolution architecture
- `README.md`: Project overview

### Examples

- `examples/simple_halt.py`: Basic program execution
- `examples/optimization_demo.py`: Optimization demonstration
- `examples/self_improving_demo.py`: Evolution demonstration

### Tests

- `tests/test_vm.py`: VM tests
- `tests/test_generator.py`: Generator tests
- `tests/test_optimizer.py`: Optimizer tests
- `tests/test_self_improve.py`: Evolution tests

## License

MIT License - See LICENSE file for details

## Acknowledgments

- Ben Olmstead: Creator of Malbolge
- The esoteric programming community
- All contributors to this project

---

**Happy Malbolge programming!** 🔥

*Remember: If it compiles, you're probably doing something wrong.* 😄
