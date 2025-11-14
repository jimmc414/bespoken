#!/usr/bin/env python3
"""
Automated Malbolge Workflow Example

This example demonstrates a programmatic workflow using bespoken with
the Malbolge compiler to:
1. Generate a program
2. Run and test it
3. Optimize it
4. Evolve the compiler

This shows how to integrate the Malbolge tools into automated workflows.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from malbolge import (
    MalbolgeVM,
    MalbolgeGenerator,
    MalbolgeOptimizer,
    SelfImprovingCompiler
)


def workflow_demo():
    """Demonstrate a complete Malbolge workflow."""

    print("=" * 70)
    print("  AUTOMATED MALBOLGE WORKFLOW")
    print("=" * 70)

    # Step 1: Generate a program
    print("\n1. GENERATING PROGRAM")
    print("-" * 70)

    gen = MalbolgeGenerator()
    gen.label("start")

    # Create inefficient program for demonstration
    for _ in range(10):
        gen.nop()

    gen.rotate_acc()
    gen.rotate_acc()

    for _ in range(5):
        gen.nop()

    gen.halt()

    # Dead code (will be optimized away)
    for _ in range(8):
        gen.nop()

    original = gen.compile()
    print(f"Generated program: {len(original)} bytes")
    print(f"Preview: {original[:60]}...")

    # Step 2: Run the program
    print("\n2. RUNNING PROGRAM")
    print("-" * 70)

    vm = MalbolgeVM()
    vm.load_program(original)
    state = vm.run(max_steps=10000)

    print(f"Execution completed:")
    print(f"  Instructions executed: {state.instructions_executed}")
    print(f"  Memory accesses: {state.memory_accesses}")
    print(f"  Halted: {vm.halted}")

    # Step 3: Optimize the program
    print("\n3. OPTIMIZING PROGRAM")
    print("-" * 70)

    optimizer = MalbolgeOptimizer(debug=False)
    result = optimizer.optimize(original, passes=5)

    print(f"Optimization results:")
    print(f"  Original size: {result.original_size} bytes")
    print(f"  Optimized size: {result.optimized_size} bytes")
    print(f"  Reduction: {result.stats['size_reduction']} bytes "
          f"({result.stats['size_reduction_pct']:.1f}%)")

    if result.passes_applied:
        print(f"  Passes applied: {', '.join(result.passes_applied)}")

    # Verify optimized program still works
    print("\nVerifying optimized program...")
    vm2 = MalbolgeVM()
    vm2.load_program(result.code)
    state2 = vm2.run(max_steps=10000)
    print(f"  Optimized program executed: {state2.instructions_executed} instructions")
    print(f"  Halted: {vm2.halted}")

    # Step 4: Compiler Evolution (optional, takes time)
    print("\n4. COMPILER EVOLUTION (OPTIONAL)")
    print("-" * 70)
    print("This step evolves the compiler to improve its performance.")
    print("It can take a few minutes...")

    response = input("\nRun compiler evolution? (y/N): ").strip().lower()

    if response == 'y':
        compiler = SelfImprovingCompiler(
            debug=False,
            save_dir=Path("./workflow_compiler")
        )

        print("\nBootstrapping compiler...")
        initial = compiler.bootstrap()
        print(f"Initial fitness: {initial.fitness:.6f}")

        print(f"\nEvolving for 15 generations...")
        best = compiler.evolve(
            generations=15,
            population_size=5,
            mutation_rate=0.15,
            elite_count=1
        )

        print(f"\nEvolution complete:")
        print(f"  Final fitness: {best.fitness:.6f}")
        improvement = ((best.fitness / initial.fitness) - 1) * 100
        print(f"  Improvement: {improvement:+.1f}%")
        print(f"  Compiler saved to: {compiler.save_dir}")
    else:
        print("Skipping compiler evolution.")

    # Summary
    print("\n" + "=" * 70)
    print("  WORKFLOW COMPLETE")
    print("=" * 70)
    print(f"\n✓ Generated {len(original)} byte program")
    print(f"✓ Optimized to {len(result.code)} bytes")
    print(f"✓ Size reduction: {result.stats['size_reduction_pct']:.1f}%")
    print("\nThe Malbolge toolchain is ready for your projects!")


def interactive_demo():
    """Run an interactive demo with the assistant."""

    print("\n" + "=" * 70)
    print("  INTERACTIVE MALBOLGE ASSISTANT")
    print("=" * 70)
    print("\nStarting interactive assistant...")
    print("(This requires bespoken to be installed)\n")

    try:
        from bespoken import chat
        from bespoken.tools import MalbolgeTool

        chat(
            model_name="claude",
            tools=[MalbolgeTool()],
            system_prompt="""You are a Malbolge programming expert.
            Help users generate, run, optimize, and understand Malbolge programs."""
        )

    except ImportError as e:
        print(f"Error: {e}")
        print("\nTo use the interactive assistant, install bespoken:")
        print("  pip install bespoken")


def main():
    """Main entry point."""

    print("\nMALBOLGE WORKFLOW EXAMPLES\n")
    print("Choose an option:")
    print("  1. Automated workflow (generate, run, optimize)")
    print("  2. Interactive assistant (chat-based)")
    print("  3. Both")

    choice = input("\nEnter choice (1-3): ").strip()

    if choice == "1":
        workflow_demo()
    elif choice == "2":
        interactive_demo()
    elif choice == "3":
        workflow_demo()
        print("\n\nNow starting interactive assistant...\n")
        interactive_demo()
    else:
        print("Invalid choice. Running automated workflow...")
        workflow_demo()


if __name__ == "__main__":
    main()
