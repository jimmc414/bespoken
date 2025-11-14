# Working with Malbolge

Bespoken includes a complete **self-improving optimizing compiler for Malbolge**, one of the most challenging programming languages ever created. This guide shows you how to use bespoken with the Malbolge compiler.

## What is Malbolge?

Malbolge is an esoteric programming language designed by Ben Olmstead in 1998 to be as difficult as possible to program in. Key features:

- **Position-dependent instructions**: The meaning of a character depends on where it is in memory
- **Self-modifying code**: Instructions encrypt themselves after execution
- **Ternary arithmetic**: All operations use base-3 math
- **8 instructions only**: j, i, /, *, p, o, <, v
- **No direct control flow**: Must use self-modification for loops

The first "Hello World" program wasn't written until 2000 and required a beam search algorithm!

## The Malbolge Toolchain

The Malbolge compiler includes:

1. **Virtual Machine** - Executes Malbolge programs
2. **Code Generator** - Creates Malbolge code programmatically
3. **Optimizer** - Multi-pass optimization with genetic algorithms
4. **Self-Improving Compiler** - Meta-circular compiler that evolves itself

## Quick Start

### 1. Direct Usage

You can use the Malbolge modules directly:

```python
from malbolge import MalbolgeVM, MalbolgeGenerator, MalbolgeOptimizer

# Generate a program
gen = MalbolgeGenerator()
gen.nop().rotate_acc().halt()
program = gen.compile()

# Run it
vm = MalbolgeVM()
vm.load_program(program)
vm.run()

# Optimize it
opt = MalbolgeOptimizer()
result = opt.optimize(program, passes=5)
```

### 2. Using with Bespoken

Create an AI assistant that helps with Malbolge:

```python
from bespoken import chat
from bespoken.tools import MalbolgeTool

chat(
    model_name="claude",
    tools=[MalbolgeTool()],
    system_prompt="You are a Malbolge programming expert."
)
```

## MalbolgeTool API

The `MalbolgeTool` provides these methods for the LLM:

### `generate_program(instructions: str)`

Generate a Malbolge program from high-level instructions.

**Instructions**: Comma-separated list:
- `nop` - No operation
- `halt` - Stop execution
- `rotate_acc` - Rotate accumulator
- `rotate_mem` - Rotate memory
- `output_char` - Output character
- `input_char` - Input character
- `move_data` - Move data pointer
- `set_data` - Set data pointer

**Example**:
```
> Generate a program: nop, nop, rotate_acc, output_char, halt
```

### `run_program(program=None, max_steps=10000)`

Execute a Malbolge program and show output.

**Example**:
```
> Run the program and show me what it does
```

### `optimize_program(program=None, passes=3)`

Optimize a program to reduce size and improve performance.

**Example**:
```
> Optimize my program with 5 passes
```

### `evolve_compiler(generations=10, population_size=5)`

Evolve the self-improving compiler using genetic algorithms.

**Example**:
```
> Evolve the compiler for 20 generations
```

### `get_compiler_stats()`

View compiler evolution statistics.

**Example**:
```
> Show me compiler statistics
```

### `explain_malbolge()`

Get detailed information about Malbolge.

**Example**:
```
> What is Malbolge?
```

## Example Session

Here's a typical interaction with the Malbolge assistant:

```
> What is Malbolge?

[Assistant explains Malbolge and its features]

> Generate a simple program with 3 NOPs and a halt

I'll generate that for you...
[Generates: "...")
Generated Malbolge program (4 bytes): ...

> Run it

[Executes program]
Program executed successfully
Instructions executed: 4
Halted: True
No output produced

> Now make an inefficient version with 20 NOPs

[Generates larger program]
Generated Malbolge program (21 bytes): ...

> Optimize it

[Runs optimization]
Optimization complete
Original size: 21 bytes
Optimized size: 5 bytes
Size reduction: 16 bytes (76.2%)
Passes applied: dead_code_elimination, nop_reduction

> Evolve the compiler for 10 generations

[Runs evolution - this takes time]
Evolution complete
Generations: 10
Final fitness: 0.234567
Improvement: +15.3%
Compiler saved to: ./bespoken_malbolge_compiler
```

## Complete Examples

### Basic Assistant

```python title="examples/malbolge_assistant.py"
from bespoken import chat
from bespoken.tools import MalbolgeTool

chat(
    model_name="claude",
    tools=[MalbolgeTool()],
    system_prompt="""You are a Malbolge expert. Help users:
    - Generate Malbolge programs
    - Optimize existing code
    - Understand how Malbolge works
    - Run and debug programs
    """
)
```

Run with:
```bash
python examples/malbolge_assistant.py
```

### Automated Workflow

```python title="examples/malbolge_workflow.py"
from malbolge import MalbolgeGenerator, MalbolgeOptimizer

# Generate
gen = MalbolgeGenerator()
gen.nop().nop().halt()
program = gen.compile()

# Optimize
opt = MalbolgeOptimizer()
result = opt.optimize(program, passes=3)

print(f"Reduced from {result.original_size} to {result.optimized_size} bytes")
```

Run with:
```bash
python examples/malbolge_workflow.py
```

## Advanced: Self-Improving Compiler

The compiler can evolve and improve itself:

```python
from malbolge import SelfImprovingCompiler
from pathlib import Path

compiler = SelfImprovingCompiler(
    save_dir=Path("./my_compiler")
)

# Bootstrap initial compiler
initial = compiler.bootstrap()
print(f"Initial fitness: {initial.fitness}")

# Evolve for 100 generations
best = compiler.evolve(
    generations=100,
    population_size=10,
    mutation_rate=0.1
)

print(f"Final fitness: {best.fitness}")
print(f"Improvement: {(best.fitness/initial.fitness - 1)*100:.1f}%")

# View statistics
compiler.print_stats()
```

The compiler uses genetic algorithms to:
1. Compile test programs
2. Measure performance (speed, size, quality)
3. Generate variants through mutation and crossover
4. Select best performers
5. Iterate to improve

## Documentation

Complete documentation is available in the `malbolge/` directory:

- **[Malbolge Guide](../../malbolge/GUIDE.md)** - Complete usage guide
- **[Language Specification](../../malbolge/docs/malbolge_spec.md)** - Malbolge language details
- **[Optimization Strategies](../../malbolge/docs/optimization_strategies.md)** - How optimization works
- **[Self-Improvement Architecture](../../malbolge/docs/self_improvement.md)** - Compiler evolution

## Running Tests

The Malbolge compiler includes comprehensive tests:

```bash
cd malbolge
python -m pytest tests/ -v
```

## Demo

See the complete system in action:

```bash
cd malbolge
python demo.py
```

This demonstrates:
- Virtual machine execution
- Code generation
- Optimization
- Self-improvement
- The bootstrap compiler (written in Malbolge!)

## Tips

### For Best Results

1. **Use the code generator** - Don't try to write Malbolge by hand
2. **Optimize liberally** - The optimizer is safe and effective
3. **Start simple** - Begin with basic programs before complex ones
4. **Evolve patiently** - Compiler evolution takes time but shows real improvements
5. **Debug with traces** - Use `debug=True` on the VM to see execution

### Common Patterns

**Generate and test**:
```python
gen.generate_program("nop, nop, halt")
run_program()
```

**Iterative optimization**:
```python
for passes in [1, 3, 5, 10]:
    result = optimize_program(passes=passes)
    print(f"{passes} passes: {result.optimized_size} bytes")
```

**Evolution experiments**:
```python
# Quick evolution
evolve_compiler(generations=10, population_size=5)

# Deep evolution
evolve_compiler(generations=100, population_size=20)
```

## Why This Matters

The Malbolge self-improving compiler demonstrates:

- **Meta-circular compilation**: A compiler that compiles itself
- **Autonomous optimization**: The compiler improves without human intervention
- **Genetic algorithms**: Evolution applied to code optimization
- **Tool integration**: Complex functionality made accessible through chat

It's a showcase of what's possible when you combine:
- Esoteric programming languages
- Modern AI assistants
- Evolutionary algorithms
- User-friendly interfaces

## Next Steps

- Try the examples in `examples/malbolge_*.py`
- Read the [Complete Guide](../../malbolge/GUIDE.md)
- Explore the [source code](../../malbolge/)
- Experiment with evolution parameters
- Build your own Malbolge programs!

---

**Happy Malbolge programming!** 🔥

*"If it compiles, you're probably doing something wrong."*
