#!/usr/bin/env python3
"""
Generator for P vs NP Diplomatic Solution Programs

This script generates the three philosophical Malbolge programs:
1. P_EQUALS_NP.mal - The Optimist's convergence
2. P_NOT_EQUALS_NP.mal - The Separatist's divergence
3. DIPLOMATIC_UNITY.mal - The Council's synthesis
"""

import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from malbolge import MalbolgeGenerator, MalbolgeOptimizer


def generate_p_equals_np():
    """Generate program representing P = NP perspective.

    This program demonstrates convergence - multiple paths merging into one.
    Through self-modification and optimization, it finds efficiency.

    Symbolism:
    - Initial complexity (many NOPs) represents the apparent difficulty
    - Rotations represent transformation and search
    - Self-modification shows how problems evolve
    - Optimization eliminates redundancy (P = NP means efficiency exists)
    """
    print("Generating P_EQUALS_NP.mal - The Optimist's Vision")
    print("-" * 60)

    gen = MalbolgeGenerator()

    # Start: The problem appears complex
    gen.label("complexity_illusion")
    for _ in range(8):
        gen.nop()  # Apparent complexity

    # Transform: Through rotation, we find patterns
    gen.label("discovery")
    gen.rotate_acc()  # Search for solution
    gen.rotate_acc()  # Transform problem space
    gen.rotate_acc()  # Converge toward answer

    # Simplify: The solution is simpler than it seemed
    gen.label("convergence")
    for _ in range(3):
        gen.nop()  # Fewer operations needed

    # Unite: Verification and solution merge
    gen.label("unity")
    gen.rotate_mem()  # Verification and generation are one

    # Success: We found the efficient path
    gen.label("triumph")
    gen.halt()

    code = gen.compile()

    print(f"Generated: {len(code)} bytes")
    print(f"Philosophy: Complexity is an illusion; efficiency awaits discovery")
    print(f"Labels: {gen.labels}")
    print()

    # Optimize to show P=NP nature (find the efficient version)
    print("Optimizing (finding the efficient algorithm)...")
    opt = MalbolgeOptimizer()
    result = opt.optimize(code, passes=5)

    print(f"Original: {result.original_size} bytes")
    print(f"Optimized: {result.optimized_size} bytes")
    print(f"Reduction: {result.stats['size_reduction_pct']:.1f}%")
    print(f"Message: The efficient solution exists! (P = NP)")
    print()

    return result.code


def generate_p_not_equals_np():
    """Generate program representing P ≠ NP perspective.

    This program demonstrates divergence - paths that cannot meet.
    It shows barriers and fundamental complexity that cannot be optimized away.

    Symbolism:
    - Complex interleaving shows irreducible difficulty
    - Position-dependency represents context-sensitive hardness
    - Minimal optimization shows fundamental barriers
    - Structure preserves essential complexity (P ≠ NP means hard is hard)
    """
    print("Generating P_NOT_EQUALS_NP.mal - The Separatist's Proof")
    print("-" * 60)

    gen = MalbolgeGenerator()

    # The Barrier: Fundamental complexity
    gen.label("barrier")
    for _ in range(5):
        gen.nop()  # Essential operations

    # The Search: Verification is easy
    gen.label("verification")
    gen.rotate_acc()  # Check the solution

    # The Wall: But finding is hard
    gen.label("generation_hardness")
    for _ in range(7):
        gen.nop()  # Exponential search space
    gen.rotate_mem()  # Complex transformation
    gen.rotate_mem()  # Cannot be simplified

    # The Gap: Paths diverge
    gen.label("divergence")
    for _ in range(6):
        gen.nop()  # Irreducible complexity
    gen.rotate_acc()

    # The Acceptance: Some problems are fundamentally hard
    gen.label("acceptance")
    for _ in range(4):
        gen.nop()

    gen.halt()

    code = gen.compile()

    print(f"Generated: {len(code)} bytes")
    print(f"Philosophy: Some complexity is fundamental and irreducible")
    print(f"Labels: {gen.labels}")
    print()

    # Try to optimize, but show minimal improvement
    print("Attempting optimization (hitting fundamental barriers)...")
    opt = MalbolgeOptimizer()
    result = opt.optimize(code, passes=5)

    print(f"Original: {result.original_size} bytes")
    print(f"Optimized: {result.optimized_size} bytes")
    print(f"Reduction: {result.stats['size_reduction_pct']:.1f}%")
    print(f"Message: Fundamental barriers remain! (P ≠ NP)")
    print()

    return result.code


def generate_diplomatic_unity():
    """Generate program representing the diplomatic solution.

    This program synthesizes both perspectives, showing how they coexist.
    It demonstrates practical wisdom and meta-understanding.

    Symbolism:
    - Balanced structure honors both perspectives
    - Multiple paths show different valid approaches
    - Self-modification represents learning and evolution
    - Unified halt shows consensus despite different paths
    """
    print("Generating DIPLOMATIC_UNITY.mal - The Council's Synthesis")
    print("-" * 60)

    gen = MalbolgeGenerator()

    # Acknowledge both perspectives
    gen.label("recognition")
    for _ in range(3):
        gen.nop()  # The Optimist's hope
    gen.rotate_acc()  # The Separatist's realism
    for _ in range(3):
        gen.nop()  # Balance

    # The wisdom: Both illuminate truth
    gen.label("illumination")
    gen.rotate_mem()  # Transform through understanding

    # Practical focus: What we can solve
    gen.label("pragmatism")
    for _ in range(2):
        gen.nop()  # Practical work
    gen.rotate_acc()  # Incremental progress

    # Theoretical depth: What we can understand
    gen.label("theory")
    for _ in range(2):
        gen.nop()  # Theoretical insight
    gen.rotate_mem()  # Deep comprehension

    # Meta-level: The debate advances us
    gen.label("meta_understanding")
    gen.rotate_acc()  # Evolution of thought

    # Unity: All paths lead to progress
    gen.label("consensus")
    for _ in range(2):
        gen.nop()  # Peaceful coexistence

    # Resolution: Forward together
    gen.label("resolution")
    gen.halt()

    code = gen.compile()

    print(f"Generated: {len(code)} bytes")
    print(f"Philosophy: Synthesis transcends debate; wisdom embraces both")
    print(f"Labels: {gen.labels}")
    print()

    # Moderate optimization showing balanced approach
    print("Optimizing with diplomatic balance...")
    opt = MalbolgeOptimizer()
    result = opt.optimize(code, passes=3)  # Balanced optimization

    print(f"Original: {result.original_size} bytes")
    print(f"Optimized: {result.optimized_size} bytes")
    print(f"Reduction: {result.stats['size_reduction_pct']:.1f}%")
    print(f"Message: Progress through synthesis! (Diplomatic wisdom)")
    print()

    return result.code


def save_programs():
    """Generate and save all three programs."""

    print("=" * 60)
    print("P vs NP DIPLOMATIC SOLUTION GENERATOR")
    print("=" * 60)
    print()

    # Generate programs
    p_eq_np = generate_p_equals_np()
    p_neq_np = generate_p_not_equals_np()
    diplomatic = generate_diplomatic_unity()

    # Save to files
    output_dir = Path(__file__).parent

    print("=" * 60)
    print("SAVING PROGRAMS")
    print("=" * 60)

    files = [
        ("P_EQUALS_NP.mal", p_eq_np, "The Optimist's convergence"),
        ("P_NOT_EQUALS_NP.mal", p_neq_np, "The Separatist's divergence"),
        ("DIPLOMATIC_UNITY.mal", diplomatic, "The Council's synthesis")
    ]

    for filename, code, description in files:
        filepath = output_dir / filename
        filepath.write_text(code)
        print(f"✓ Saved {filename} - {description}")
        print(f"  Path: {filepath}")
        print(f"  Size: {len(code)} bytes")
        print()

    print("=" * 60)
    print("THE COUNCIL'S VERDICT")
    print("=" * 60)
    print()
    print("Three programs, three perspectives, one truth:")
    print()
    print("1. P = NP:  Optimism shows us possibility")
    print("2. P ≠ NP:  Realism shows us limits")
    print("3. Unity:   Wisdom shows us the way forward")
    print()
    print("Vote: 7-0 in favor of diplomatic synthesis")
    print()
    print("The Council has spoken:")
    print('"Focus not on the answer, but on what we learn by asking."')
    print()
    print("Programs ready for execution and contemplation.")
    print("=" * 60)


def analyze_programs():
    """Analyze the philosophical and technical properties of each program."""

    print("\n" + "=" * 60)
    print("PROGRAM ANALYSIS")
    print("=" * 60)

    from malbolge import MalbolgeVM

    output_dir = Path(__file__).parent

    for filename in ["P_EQUALS_NP.mal", "P_NOT_EQUALS_NP.mal", "DIPLOMATIC_UNITY.mal"]:
        print(f"\n{filename}")
        print("-" * 60)

        filepath = output_dir / filename
        if not filepath.exists():
            print("File not found - run save_programs() first")
            continue

        code = filepath.read_text()

        # Execute
        vm = MalbolgeVM()
        vm.load_program(code)
        state = vm.run(max_steps=10000)

        print(f"Size: {len(code)} bytes")
        print(f"Instructions executed: {state.instructions_executed}")
        print(f"Memory accesses: {state.memory_accesses}")
        print(f"Rotations: {state.rotations}")
        print(f"Complexity ratio: {state.instructions_executed / len(code):.2f}x")

        # Philosophical interpretation
        if "EQUALS" in filename:
            print(f"Philosophy: High optimization potential = P = NP optimism")
        elif "NOT" in filename:
            print(f"Philosophy: Minimal optimization = P ≠ NP barriers")
        else:
            print(f"Philosophy: Balanced complexity = Diplomatic synthesis")


if __name__ == "__main__":
    save_programs()
    analyze_programs()
