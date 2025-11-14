"""
Simple Malbolge program that just halts

This demonstrates the most basic Malbolge program.
"""

from malbolge.generator import MalbolgeGenerator
from malbolge.vm import MalbolgeVM


def main():
    print("=== Simple Halt Program ===\n")

    # Generate program
    gen = MalbolgeGenerator()
    gen.halt()

    code = gen.compile()

    print(f"Generated code ({len(code)} bytes):")
    print(code)
    print()

    # Run program
    print("Running program...")
    vm = MalbolgeVM()
    vm.load_program(code)
    state = vm.run(max_steps=100)

    print(f"\nExecution completed:")
    print(f"  Instructions executed: {state.instructions_executed}")
    print(f"  Halted: {vm.halted}")


if __name__ == "__main__":
    main()
