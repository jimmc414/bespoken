"""
Demonstration of Malbolge code optimization

This shows how the optimizer can reduce code size and improve performance.
"""

from malbolge.generator import MalbolgeGenerator
from malbolge.optimizer import MalbolgeOptimizer
from malbolge.vm import MalbolgeVM


def main():
    print("=== Malbolge Optimization Demo ===\n")

    # Generate inefficient program
    print("Generating inefficient program...")
    gen = MalbolgeGenerator()

    # Lots of unnecessary NOPs
    for _ in range(20):
        gen.nop()

    gen.rotate_acc()
    gen.rotate_acc()

    for _ in range(10):
        gen.nop()

    gen.halt()

    # Dead code after halt
    for _ in range(15):
        gen.nop()

    original_code = gen.compile()

    print(f"Original program: {len(original_code)} bytes")
    print(f"Code preview: {original_code[:50]}...")
    print()

    # Run original
    print("Running original program...")
    vm1 = MalbolgeVM()
    vm1.load_program(original_code)
    state1 = vm1.run(max_steps=10000)
    print(f"  Instructions executed: {state1.instructions_executed}")
    print()

    # Optimize
    print("Optimizing program...")
    optimizer = MalbolgeOptimizer(debug=True)
    result = optimizer.optimize(original_code, passes=5)

    print(f"\nOptimization results:")
    print(f"  Original size: {result.original_size} bytes")
    print(f"  Optimized size: {result.optimized_size} bytes")
    print(f"  Size reduction: {result.stats['size_reduction']} bytes "
          f"({result.stats['size_reduction_pct']:.1f}%)")
    print(f"  Passes applied: {', '.join(result.passes_applied)}")
    print(f"  Execution improvement: {result.execution_improvement:.1f}%")
    print()

    # Run optimized
    print("Running optimized program...")
    vm2 = MalbolgeVM()
    vm2.load_program(result.code)
    state2 = vm2.run(max_steps=10000)
    print(f"  Instructions executed: {state2.instructions_executed}")
    print()

    print(f"Optimized code preview: {result.code[:50]}...")


if __name__ == "__main__":
    main()
