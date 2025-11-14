#!/usr/bin/env python3
"""
Malbolge Quick Start

The simplest possible example of using the Malbolge compiler
with bespoken.

This demonstrates:
- Importing the Malbolge modules
- Generating a simple program
- Running it
- Basic optimization
"""

import sys
from pathlib import Path

# Add paths
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))
sys.path.insert(0, str(Path(__file__).parent.parent))

from malbolge import MalbolgeVM, MalbolgeGenerator, MalbolgeOptimizer


def main():
    print("MALBOLGE QUICK START\n")

    # 1. Generate a program
    print("1. Generating program...")
    gen = MalbolgeGenerator()
    gen.nop().nop().nop()  # 3 NOPs
    gen.halt()             # Halt
    program = gen.compile()
    print(f"   Generated: {program}")
    print(f"   Size: {len(program)} bytes\n")

    # 2. Run it
    print("2. Running program...")
    vm = MalbolgeVM()
    vm.load_program(program)
    state = vm.run()
    print(f"   Executed {state.instructions_executed} instructions")
    print(f"   Halted: {vm.halted}\n")

    # 3. Optimize it
    print("3. Optimizing...")
    opt = MalbolgeOptimizer()
    result = opt.optimize(program, passes=1)
    print(f"   Original: {result.original_size} bytes")
    print(f"   Optimized: {result.optimized_size} bytes")
    print(f"   Saved: {result.stats['size_reduction']} bytes\n")

    print("✓ Complete! The Malbolge toolchain is working.")
    print("\nNext steps:")
    print("  • Try: python examples/malbolge_assistant.py")
    print("  • Try: python examples/malbolge_workflow.py")
    print("  • Read: malbolge/GUIDE.md")


if __name__ == "__main__":
    main()
