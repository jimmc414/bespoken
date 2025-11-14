"""
Malbolge Optimizer

Multi-pass optimization engine for Malbolge programs. Since Malbolge is
self-modifying and position-dependent, optimization is extremely complex.

Optimization Strategies:
1. Dead code elimination
2. NOP reduction
3. Rotation optimization (combine multiple rotations)
4. Memory access pattern optimization
5. Self-modification pattern recognition
6. Instruction reordering (when safe)
7. Code size minimization
8. Execution path optimization

The optimizer uses genetic algorithms and heuristics to evolve better code.
"""

import random
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
from copy import deepcopy

from .vm import MalbolgeVM


@dataclass
class OptimizationPass:
    """Represents an optimization pass"""
    name: str
    description: str
    enabled: bool = True
    priority: int = 0
    stats: Dict[str, int] = field(default_factory=dict)


@dataclass
class OptimizationResult:
    """Result of optimization"""
    original_size: int
    optimized_size: int
    passes_applied: List[str]
    execution_improvement: float  # Percentage
    code: str
    stats: Dict[str, any]


class MalbolgeOptimizer:
    """Optimize Malbolge programs"""

    MEMORY_SIZE = 59049

    # XLAT1 table for instruction normalization
    XLAT1 = (
        "+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI"
        ".v%{gJh4G\\-=O@5`_3i<?Z';FNQuY]szf$!/|S#~W>qxdRp0w"
    )

    def __init__(self, debug: bool = False):
        """Initialize optimizer

        Args:
            debug: Enable debug output
        """
        self.debug = debug
        self.passes: List[OptimizationPass] = []
        self._init_passes()

    def _init_passes(self) -> None:
        """Initialize optimization passes"""
        self.passes = [
            OptimizationPass(
                "dead_code_elimination",
                "Remove unreachable code",
                priority=10
            ),
            OptimizationPass(
                "nop_reduction",
                "Minimize consecutive NOPs",
                priority=9
            ),
            OptimizationPass(
                "rotation_combining",
                "Combine consecutive rotations",
                priority=8
            ),
            OptimizationPass(
                "memory_access_optimization",
                "Optimize memory access patterns",
                priority=7
            ),
            OptimizationPass(
                "instruction_reordering",
                "Reorder independent instructions",
                priority=6
            ),
            OptimizationPass(
                "constant_propagation",
                "Propagate constant values",
                priority=5
            ),
            OptimizationPass(
                "self_modification_optimization",
                "Optimize self-modifying patterns",
                priority=4
            ),
        ]

        # Sort by priority
        self.passes.sort(key=lambda p: p.priority, reverse=True)

    def _normalize_instruction(self, char: str, pos: int) -> str:
        """Normalize instruction character to operation

        Args:
            char: Character in program
            pos: Position in memory

        Returns:
            Normalized instruction
        """
        val = ord(char)
        if val < 33 or val > 126:
            return ' '

        xlat_pos = (pos + val - 33) % 94
        if xlat_pos >= len(self.XLAT1):
            return ' '

        return self.XLAT1[xlat_pos]

    def _analyze_program(self, code: str) -> Dict[str, any]:
        """Analyze program structure

        Args:
            code: Malbolge program

        Returns:
            Analysis results
        """
        instructions = []
        nop_count = 0
        rotation_count = 0
        io_count = 0

        for pos, char in enumerate(code):
            instr = self._normalize_instruction(char, pos)
            instructions.append(instr)

            if instr == 'o':
                nop_count += 1
            elif instr in ('/', '*'):
                rotation_count += 1
            elif instr in ('i', 'p'):
                io_count += 1

        return {
            'size': len(code),
            'instructions': instructions,
            'nop_count': nop_count,
            'rotation_count': rotation_count,
            'io_count': io_count,
            'nop_ratio': nop_count / max(len(code), 1)
        }

    def _pass_dead_code_elimination(self, code: str) -> Tuple[str, Dict]:
        """Remove unreachable code after halt

        Args:
            code: Malbolge program

        Returns:
            (optimized_code, stats)
        """
        stats = {'removed': 0}

        # Find first halt instruction
        halt_pos = None
        for pos, char in enumerate(code):
            instr = self._normalize_instruction(char, pos)
            if instr == 'v':
                halt_pos = pos
                break

        if halt_pos is not None and halt_pos < len(code) - 1:
            # Remove everything after halt
            optimized = code[:halt_pos + 1]
            stats['removed'] = len(code) - len(optimized)
            return optimized, stats

        return code, stats

    def _pass_nop_reduction(self, code: str) -> Tuple[str, Dict]:
        """Reduce consecutive NOPs

        Args:
            code: Malbolge program

        Returns:
            (optimized_code, stats)
        """
        stats = {'removed': 0}

        # Find sequences of 3+ NOPs and keep only 2
        # (some NOPs may be needed for timing/position)
        result = []
        consecutive_nops = 0

        for pos, char in enumerate(code):
            instr = self._normalize_instruction(char, pos)

            if instr == 'o':
                consecutive_nops += 1
                if consecutive_nops <= 2:  # Keep first 2 NOPs
                    result.append(char)
                else:
                    stats['removed'] += 1
            else:
                consecutive_nops = 0
                result.append(char)

        return ''.join(result), stats

    def _pass_rotation_combining(self, code: str) -> Tuple[str, Dict]:
        """Combine consecutive rotation operations

        Args:
            code: Malbolge program

        Returns:
            (optimized_code, stats)
        """
        stats = {'combined': 0}

        # Multiple rotations can sometimes be simplified
        # This is complex due to position-dependency
        # For now, this is a placeholder

        # TODO: Implement rotation combining logic
        # This requires understanding the rotation patterns

        return code, stats

    def _pass_memory_access_optimization(self, code: str) -> Tuple[str, Dict]:
        """Optimize memory access patterns

        Args:
            code: Malbolge program

        Returns:
            (optimized_code, stats)
        """
        stats = {'optimized': 0}

        # Analyze memory access patterns and optimize
        # This is extremely complex in Malbolge
        # Placeholder for future implementation

        return code, stats

    def _pass_instruction_reordering(self, code: str) -> Tuple[str, Dict]:
        """Reorder independent instructions for better performance

        Args:
            code: Malbolge program

        Returns:
            (optimized_code, stats)
        """
        stats = {'reordered': 0}

        # In Malbolge, most instructions are position-dependent
        # Safe reordering is very limited
        # Placeholder for future implementation

        return code, stats

    def _pass_constant_propagation(self, code: str) -> Tuple[str, Dict]:
        """Propagate constant values

        Args:
            code: Malbolge program

        Returns:
            (optimized_code, stats)
        """
        stats = {'propagated': 0}

        # Track constant values and propagate them
        # Placeholder for future implementation

        return code, stats

    def _pass_self_modification_optimization(self, code: str) -> Tuple[str, Dict]:
        """Optimize self-modification patterns

        Args:
            code: Malbolge program

        Returns:
            (optimized_code, stats)
        """
        stats = {'optimized': 0}

        # Recognize and optimize common self-modification patterns
        # This is one of the most complex optimizations
        # Placeholder for future implementation

        return code, stats

    def optimize(self, code: str, passes: int = 1,
                 enabled_passes: Optional[List[str]] = None) -> OptimizationResult:
        """Optimize Malbolge program

        Args:
            code: Malbolge program to optimize
            passes: Number of optimization iterations
            enabled_passes: List of pass names to enable (None = all)

        Returns:
            Optimization result
        """
        original_size = len(code)
        current_code = code
        applied_passes = []

        # Measure original execution performance
        original_perf = self._measure_performance(code)

        for iteration in range(passes):
            if self.debug:
                print(f"\n=== Optimization Pass {iteration + 1}/{passes} ===")

            for opt_pass in self.passes:
                if not opt_pass.enabled:
                    continue

                if enabled_passes and opt_pass.name not in enabled_passes:
                    continue

                # Apply optimization pass
                method = getattr(self, f"_pass_{opt_pass.name}", None)
                if method:
                    prev_size = len(current_code)
                    current_code, stats = method(current_code)
                    new_size = len(current_code)

                    if new_size != prev_size:
                        applied_passes.append(opt_pass.name)
                        opt_pass.stats = stats

                        if self.debug:
                            print(f"{opt_pass.name}: {prev_size} -> {new_size} bytes")

        # Measure optimized execution performance
        optimized_perf = self._measure_performance(current_code)

        # Calculate improvement
        if original_perf > 0:
            improvement = ((original_perf - optimized_perf) / original_perf) * 100
        else:
            improvement = 0.0

        return OptimizationResult(
            original_size=original_size,
            optimized_size=len(current_code),
            passes_applied=applied_passes,
            execution_improvement=improvement,
            code=current_code,
            stats={
                'original_perf': original_perf,
                'optimized_perf': optimized_perf,
                'size_reduction': original_size - len(current_code),
                'size_reduction_pct': (
                    (original_size - len(current_code)) / max(original_size, 1)
                ) * 100
            }
        )

    def _measure_performance(self, code: str, max_steps: int = 10000) -> float:
        """Measure execution performance of code

        Args:
            code: Malbolge program
            max_steps: Maximum steps to measure

        Returns:
            Performance metric (lower is better)
        """
        try:
            vm = MalbolgeVM()
            vm.load_program(code)
            state = vm.run(max_steps=max_steps)

            # Performance metric: instructions executed
            # Could also include memory accesses, etc.
            return float(state.instructions_executed)

        except Exception:
            # If code doesn't run, return high penalty
            return float('inf')

    def genetic_optimize(self, code: str, generations: int = 100,
                        population_size: int = 20,
                        mutation_rate: float = 0.1) -> OptimizationResult:
        """Optimize using genetic algorithm

        Args:
            code: Malbolge program
            generations: Number of generations
            population_size: Population size
            mutation_rate: Mutation probability

        Returns:
            Best optimization result
        """
        # Initialize population
        population = [code] * population_size

        best_result = None
        best_fitness = float('inf')

        for gen in range(generations):
            # Evaluate fitness
            fitness_scores = []
            for individual in population:
                fitness = self._measure_performance(individual)
                fitness_scores.append(fitness)

                if fitness < best_fitness:
                    best_fitness = fitness
                    best_result = individual

            if self.debug and gen % 10 == 0:
                print(f"Generation {gen}: Best fitness = {best_fitness}")

            # Selection (tournament selection)
            selected = self._tournament_selection(
                population, fitness_scores, population_size
            )

            # Crossover and mutation
            next_generation = []
            for i in range(0, len(selected), 2):
                if i + 1 < len(selected):
                    child1, child2 = self._crossover(selected[i], selected[i + 1])
                    next_generation.append(self._mutate(child1, mutation_rate))
                    next_generation.append(self._mutate(child2, mutation_rate))
                else:
                    next_generation.append(selected[i])

            population = next_generation

        # Return best result
        return self.optimize(best_result, passes=1)

    def _tournament_selection(self, population: List[str],
                             fitness_scores: List[float],
                             count: int) -> List[str]:
        """Tournament selection for genetic algorithm

        Args:
            population: Current population
            fitness_scores: Fitness scores
            count: Number to select

        Returns:
            Selected individuals
        """
        selected = []
        for _ in range(count):
            # Tournament of size 3
            contestants = random.sample(list(zip(population, fitness_scores)), 3)
            winner = min(contestants, key=lambda x: x[1])
            selected.append(winner[0])

        return selected

    def _crossover(self, parent1: str, parent2: str) -> Tuple[str, str]:
        """Crossover two programs

        Args:
            parent1, parent2: Parent programs

        Returns:
            Two child programs
        """
        # Single-point crossover
        if len(parent1) == 0 or len(parent2) == 0:
            return parent1, parent2

        point = random.randint(1, min(len(parent1), len(parent2)) - 1)

        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]

        return child1, child2

    def _mutate(self, code: str, rate: float) -> str:
        """Mutate a program

        Args:
            code: Program to mutate
            rate: Mutation rate

        Returns:
            Mutated program
        """
        if random.random() > rate or len(code) == 0:
            return code

        # Random mutation
        mutation_type = random.choice(['insert', 'delete', 'modify'])

        code_list = list(code)

        if mutation_type == 'insert' and len(code_list) < 1000:
            pos = random.randint(0, len(code_list))
            char = chr(random.randint(33, 126))
            code_list.insert(pos, char)

        elif mutation_type == 'delete' and len(code_list) > 1:
            pos = random.randint(0, len(code_list) - 1)
            del code_list[pos]

        elif mutation_type == 'modify' and len(code_list) > 0:
            pos = random.randint(0, len(code_list) - 1)
            char = chr(random.randint(33, 126))
            code_list[pos] = char

        return ''.join(code_list)


def main():
    """Demo the optimizer"""
    print("=== Malbolge Optimizer Demo ===\n")

    # Create simple test program
    from .generator import MalbolgeGenerator

    gen = MalbolgeGenerator()
    gen.nop().nop().nop().nop().nop()  # Many NOPs
    gen.rotate_acc()
    gen.output_char()
    gen.nop().nop().nop()
    gen.halt()
    gen.nop().nop().nop()  # Dead code after halt

    code = gen.compile()

    print(f"Original program ({len(code)} bytes):")
    print(code[:100], "..." if len(code) > 100 else "")

    # Optimize
    optimizer = MalbolgeOptimizer(debug=True)
    result = optimizer.optimize(code, passes=3)

    print(f"\n=== Optimization Results ===")
    print(f"Original size: {result.original_size} bytes")
    print(f"Optimized size: {result.optimized_size} bytes")
    print(f"Size reduction: {result.stats['size_reduction']} bytes "
          f"({result.stats['size_reduction_pct']:.1f}%)")
    print(f"Passes applied: {', '.join(result.passes_applied)}")
    print(f"Execution improvement: {result.execution_improvement:.1f}%")

    print(f"\nOptimized program ({len(result.code)} bytes):")
    print(result.code[:100], "..." if len(result.code) > 100 else "")


if __name__ == "__main__":
    main()
