#!/usr/bin/env python3
"""
Malbolge Self-Improving Compiler - Complete Demo

This script demonstrates all components of the Malbolge toolchain:
1. Virtual Machine
2. Code Generator
3. Optimizer
4. Self-Improving Compiler

Run this to see the entire system in action.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from malbolge import (
    MalbolgeVM,
    MalbolgeGenerator,
    MalbolgeOptimizer,
    SelfImprovingCompiler,
    generate_bootstrap_compiler
)


def print_section(title):
    """Print a section header"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")


def demo_vm():
    """Demonstrate the Malbolge VM"""
    print_section("1. Malbolge Virtual Machine")

    print("Creating a simple program that halts...")

    gen = MalbolgeGenerator()
    gen.nop()
    gen.nop()
    gen.halt()

    program = gen.compile()
    print(f"Program code: {program}")
    print(f"Program size: {len(program)} bytes\n")

    print("Executing program...")
    vm = MalbolgeVM()
    vm.load_program(program)
    state = vm.run(max_steps=1000)

    print(f"✓ Execution completed")
    print(f"  Instructions executed: {state.instructions_executed}")
    print(f"  Memory accesses: {state.memory_accesses}")
    print(f"  VM halted: {vm.halted}")


def demo_generator():
    """Demonstrate the code generator"""
    print_section("2. Malbolge Code Generator")

    print("Generating a program programmatically...")

    gen = MalbolgeGenerator()

    # Create a simple program
    gen.label("start")
    gen.nop()
    gen.rotate_acc()
    gen.nop()
    gen.label("end")
    gen.halt()

    code = gen.compile()

    print(f"Generated {len(code)} bytes of Malbolge code")
    print(f"Code: {code}")
    print(f"\nLabels:")
    for label, pos in gen.labels.items():
        print(f"  {label}: position {pos}")


def demo_optimizer():
    """Demonstrate the optimizer"""
    print_section("3. Malbolge Optimizer")

    print("Creating an inefficient program...")

    gen = MalbolgeGenerator()

    # Intentionally inefficient code
    for _ in range(15):
        gen.nop()

    gen.rotate_acc()

    for _ in range(10):
        gen.nop()

    gen.halt()

    # Dead code
    for _ in range(20):
        gen.nop()

    original = gen.compile()

    print(f"Original program: {len(original)} bytes")
    print(f"Preview: {original[:50]}...\n")

    print("Running optimizer...")
    optimizer = MalbolgeOptimizer(debug=False)
    result = optimizer.optimize(original, passes=5)

    print(f"\n✓ Optimization complete")
    print(f"  Original size: {result.original_size} bytes")
    print(f"  Optimized size: {result.optimized_size} bytes")
    print(f"  Reduction: {result.stats['size_reduction']} bytes "
          f"({result.stats['size_reduction_pct']:.1f}%)")
    print(f"  Passes applied: {len(result.passes_applied)}")

    if result.passes_applied:
        print(f"  Optimizations: {', '.join(result.passes_applied)}")


def demo_self_improving():
    """Demonstrate self-improving compiler"""
    print_section("4. Self-Improving Compiler")

    print("Initializing self-improving compiler...")

    save_dir = Path("./demo_compiler_output")
    compiler = SelfImprovingCompiler(debug=False, save_dir=save_dir)

    print("✓ Compiler initialized\n")

    print("Bootstrapping initial compiler from specification...")
    initial = compiler.bootstrap()

    print(f"✓ Bootstrap complete")
    print(f"  Variant ID: {initial.id}")
    print(f"  Code size: {len(initial.code)} bytes")
    print(f"  Initial fitness: {initial.fitness:.6f}\n")

    print("Evolving compiler over 10 generations...")
    print("(This may take a minute...)\n")

    best = compiler.evolve(
        generations=10,
        population_size=5,
        mutation_rate=0.15,
        elite_count=1
    )

    print(f"\n✓ Evolution complete")
    print(f"  Final variant ID: {best.id}")
    print(f"  Final generation: {best.generation}")
    print(f"  Final fitness: {best.fitness:.6f}")
    print(f"  Code size: {len(best.code)} bytes")

    if best.fitness > initial.fitness:
        improvement = (best.fitness - initial.fitness) / initial.fitness * 100
        print(f"  Improvement: +{improvement:.1f}%")
        print(f"\n✓ Compiler successfully improved itself!")
    else:
        print(f"\n⚠ No improvement in this run (try more generations)")

    print(f"\nCompiler variants saved to: {save_dir}")


def demo_bootstrap_compiler():
    """Show the bootstrap compiler"""
    print_section("5. Bootstrap Compiler (Written in Malbolge)")

    print("The compiler is written in Malbolge itself!")
    print("Generating compiler code...\n")

    compiler_code = generate_bootstrap_compiler()

    print(f"Compiler size: {len(compiler_code)} bytes")
    print(f"First 100 characters:")
    print(compiler_code[:100])

    if len(compiler_code) > 100:
        print("...")

    print(f"\n✓ This Malbolge program IS the compiler!")


def main():
    """Run all demos"""
    print("\n" + "=" * 70)
    print("  MALBOLGE SELF-IMPROVING OPTIMIZING COMPILER")
    print("  Complete System Demonstration")
    print("=" * 70)

    try:
        demo_vm()
        demo_generator()
        demo_optimizer()
        demo_self_improving()
        demo_bootstrap_compiler()

        print("\n" + "=" * 70)
        print("  DEMONSTRATION COMPLETE")
        print("=" * 70)

        print("\nAll components working successfully!")
        print("\nNext steps:")
        print("  • Run examples in malbolge/examples/")
        print("  • Run tests: python -m pytest malbolge/tests/")
        print("  • Read docs in malbolge/docs/")
        print("  • Experiment with longer evolution runs")

    except Exception as e:
        print(f"\n✗ Error during demonstration: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
