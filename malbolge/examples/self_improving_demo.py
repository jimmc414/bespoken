"""
Demonstration of the self-improving Malbolge compiler

This shows how the compiler evolves and improves itself over generations.
"""

from malbolge.self_improve import SelfImprovingCompiler
from pathlib import Path


def main():
    print("=== Self-Improving Malbolge Compiler Demo ===\n")

    # Create compiler
    compiler = SelfImprovingCompiler(
        debug=True,
        save_dir=Path("./compiler_output")
    )

    # Bootstrap initial compiler
    print("Bootstrapping initial compiler...\n")
    initial = compiler.bootstrap()

    print(f"\nInitial compiler:")
    print(f"  ID: {initial.id}")
    print(f"  Fitness: {initial.fitness:.6f}")
    print(f"  Code size: {len(initial.code)} bytes")
    print(f"  Metrics: {initial.performance_metrics}")
    print()

    # Evolve compiler
    print("\nEvolving compiler over multiple generations...")
    print("This will take a few moments...\n")

    best = compiler.evolve(
        generations=20,
        population_size=5,
        mutation_rate=0.15,
        elite_count=1
    )

    print(f"\n=== Evolution Complete ===\n")
    print(f"Best compiler:")
    print(f"  ID: {best.id}")
    print(f"  Generation: {best.generation}")
    print(f"  Fitness: {best.fitness:.6f}")
    print(f"  Code size: {len(best.code)} bytes")
    print(f"  Metrics: {best.performance_metrics}")
    print()

    # Calculate improvement
    improvement = (best.fitness - initial.fitness) / max(initial.fitness, 0.0001) * 100
    print(f"Overall improvement: {improvement:+.1f}%")
    print()

    # Show evolution statistics
    compiler.print_stats()

    print(f"\nCompiler variants saved to: {compiler.save_dir}")


if __name__ == "__main__":
    main()
