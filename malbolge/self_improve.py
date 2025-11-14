"""
Self-Improving Malbolge Compiler

A meta-circular compiler that compiles itself and improves through iteration.

The system works by:
1. Having a high-level specification of the compiler logic
2. Transpiling that specification to Malbolge
3. Running the Malbolge compiler to compile test programs
4. Measuring performance (compilation time, output quality)
5. Evolving the compiler through optimization
6. Selecting better-performing variants
7. Repeating the process

This creates a feedback loop where the compiler improves itself over time.
"""

import time
import json
import hashlib
from typing import List, Dict, Tuple, Optional, Any
from dataclasses import dataclass, field
from pathlib import Path

from .vm import MalbolgeVM, ExecutionState
from .generator import MalbolgeGenerator, MalbolgeAssembler
from .optimizer import MalbolgeOptimizer, OptimizationResult


@dataclass
class CompilerVariant:
    """Represents a variant of the compiler"""
    id: str
    generation: int
    code: str
    performance_metrics: Dict[str, float] = field(default_factory=dict)
    fitness: float = 0.0
    parent_id: Optional[str] = None


@dataclass
class CompilationBenchmark:
    """Benchmark for testing compiler performance"""
    name: str
    source_code: str
    expected_output: Optional[str] = None
    max_execution_steps: int = 100000


@dataclass
class EvolutionStats:
    """Statistics for evolution process"""
    generation: int
    best_fitness: float
    avg_fitness: float
    best_variant_id: str
    improvements: int
    timestamp: float


class SelfImprovingCompiler:
    """Self-improving meta-circular Malbolge compiler"""

    def __init__(self, debug: bool = False, save_dir: Optional[Path] = None):
        """Initialize self-improving compiler

        Args:
            debug: Enable debug output
            save_dir: Directory to save compiler variants
        """
        self.debug = debug
        self.save_dir = save_dir or Path("./compiler_generations")
        self.save_dir.mkdir(parents=True, exist_ok=True)

        self.generator = MalbolgeGenerator()
        self.optimizer = MalbolgeOptimizer(debug=debug)

        # Compiler variants
        self.variants: Dict[str, CompilerVariant] = {}
        self.current_generation = 0

        # Evolution statistics
        self.stats: List[EvolutionStats] = []

        # Benchmarks for testing compiler performance
        self.benchmarks = self._init_benchmarks()

    def _init_benchmarks(self) -> List[CompilationBenchmark]:
        """Initialize compilation benchmarks

        Returns:
            List of benchmarks
        """
        return [
            CompilationBenchmark(
                name="nop_sequence",
                source_code="o" * 10,  # 10 NOPs
            ),
            CompilationBenchmark(
                name="simple_rotation",
                source_code="/////",  # 5 rotations
            ),
            CompilationBenchmark(
                name="halt_program",
                source_code="v",  # Just halt
            ),
        ]

    def _generate_variant_id(self, code: str) -> str:
        """Generate unique ID for compiler variant

        Args:
            code: Compiler code

        Returns:
            Unique ID
        """
        hash_obj = hashlib.sha256(code.encode())
        return f"v{self.current_generation}_{hash_obj.hexdigest()[:12]}"

    def bootstrap(self) -> CompilerVariant:
        """Bootstrap initial compiler from high-level specification

        Returns:
            Initial compiler variant
        """
        if self.debug:
            print("=== Bootstrapping Compiler ===")

        # Generate initial compiler
        # This is a simplified compiler that can process basic Malbolge
        initial_code = self._generate_initial_compiler()

        variant = CompilerVariant(
            id=self._generate_variant_id(initial_code),
            generation=0,
            code=initial_code,
            fitness=0.0
        )

        # Evaluate initial compiler
        variant.performance_metrics = self._evaluate_compiler(variant.code)
        variant.fitness = self._calculate_fitness(variant.performance_metrics)

        self.variants[variant.id] = variant
        self.current_generation = 0

        if self.debug:
            print(f"Created initial variant: {variant.id}")
            print(f"Initial fitness: {variant.fitness:.4f}")

        self._save_variant(variant)

        return variant

    def _generate_initial_compiler(self) -> str:
        """Generate initial compiler implementation

        Returns:
            Malbolge compiler code
        """
        # This generates a basic Malbolge "compiler" that processes input
        # In reality, a full compiler would be much more complex

        self.generator.reset()

        # Compiler structure:
        # 1. Read input (source code)
        # 2. Parse/tokenize
        # 3. Generate output code
        # 4. Output result

        # For simplicity, this is a pass-through that just copies input
        self.generator.label("start")

        # Input loop
        self.generator.label("read_loop")
        self.generator.input_char()      # Read character
        self.generator.output_char()     # Output character
        # In real implementation: parsing and code generation

        # Simplified loop continuation
        for _ in range(5):
            self.generator.nop()

        # End
        self.generator.halt()

        return self.generator.compile()

    def _evaluate_compiler(self, compiler_code: str) -> Dict[str, float]:
        """Evaluate compiler performance

        Args:
            compiler_code: Compiler implementation

        Returns:
            Performance metrics
        """
        metrics = {
            'compilation_time': 0.0,
            'output_quality': 0.0,
            'code_size': len(compiler_code),
            'benchmark_success': 0.0
        }

        total_time = 0.0
        successful_compilations = 0

        # Run compiler on each benchmark
        for benchmark in self.benchmarks:
            start_time = time.time()

            try:
                # "Compile" the benchmark using our compiler
                output = self._run_compiler(
                    compiler_code,
                    benchmark.source_code,
                    benchmark.max_execution_steps
                )

                compilation_time = time.time() - start_time
                total_time += compilation_time

                # Check if compilation succeeded
                if output is not None:
                    successful_compilations += 1

                    # Evaluate output quality
                    if benchmark.expected_output:
                        quality = self._evaluate_output_quality(
                            output,
                            benchmark.expected_output
                        )
                        metrics['output_quality'] += quality

            except Exception as e:
                if self.debug:
                    print(f"Compilation failed for {benchmark.name}: {e}")
                total_time += 10.0  # Penalty for failure

        # Average metrics
        num_benchmarks = len(self.benchmarks)
        if num_benchmarks > 0:
            metrics['compilation_time'] = total_time / num_benchmarks
            metrics['output_quality'] /= num_benchmarks
            metrics['benchmark_success'] = successful_compilations / num_benchmarks

        return metrics

    def _run_compiler(self, compiler_code: str, source_code: str,
                     max_steps: int) -> Optional[str]:
        """Run compiler on source code

        Args:
            compiler_code: Compiler implementation
            source_code: Source to compile
            max_steps: Maximum execution steps

        Returns:
            Compiled output or None if failed
        """
        try:
            # Create VM with source code as input
            from io import StringIO

            input_stream = StringIO(source_code)
            output_stream = StringIO()

            vm = MalbolgeVM(
                input_stream=input_stream,
                output_stream=output_stream
            )

            vm.load_program(compiler_code)
            vm.run(max_steps=max_steps)

            return output_stream.getvalue()

        except Exception:
            return None

    def _evaluate_output_quality(self, output: str, expected: str) -> float:
        """Evaluate quality of compiler output

        Args:
            output: Actual output
            expected: Expected output

        Returns:
            Quality score (0.0 to 1.0)
        """
        if output == expected:
            return 1.0

        # Partial credit for similarity
        matches = sum(1 for a, b in zip(output, expected) if a == b)
        max_len = max(len(output), len(expected))

        if max_len == 0:
            return 0.0

        return matches / max_len

    def _calculate_fitness(self, metrics: Dict[str, float]) -> float:
        """Calculate fitness score from metrics

        Args:
            metrics: Performance metrics

        Returns:
            Fitness score (higher is better)
        """
        # Weighted fitness calculation
        # Lower compilation time is better
        # Higher output quality is better
        # Smaller code size is better
        # Higher benchmark success is better

        time_score = 1.0 / (1.0 + metrics.get('compilation_time', 1.0))
        quality_score = metrics.get('output_quality', 0.0)
        size_score = 1.0 / (1.0 + metrics.get('code_size', 1000) / 1000.0)
        success_score = metrics.get('benchmark_success', 0.0)

        fitness = (
            0.3 * time_score +
            0.3 * quality_score +
            0.2 * size_score +
            0.2 * success_score
        )

        return fitness

    def evolve(self, generations: int = 100,
               population_size: int = 10,
               mutation_rate: float = 0.1,
               elite_count: int = 2) -> CompilerVariant:
        """Evolve the compiler through multiple generations

        Args:
            generations: Number of generations to evolve
            population_size: Population size per generation
            mutation_rate: Mutation probability
            elite_count: Number of elite variants to preserve

        Returns:
            Best compiler variant
        """
        if self.debug:
            print(f"\n=== Starting Evolution ===")
            print(f"Generations: {generations}")
            print(f"Population size: {population_size}")
            print(f"Mutation rate: {mutation_rate}")

        # Get initial population
        if not self.variants:
            self.bootstrap()

        current_population = list(self.variants.values())

        best_variant = max(current_population, key=lambda v: v.fitness)

        for gen in range(generations):
            self.current_generation = gen + 1

            if self.debug:
                print(f"\n=== Generation {self.current_generation} ===")

            # Sort by fitness
            current_population.sort(key=lambda v: v.fitness, reverse=True)

            # Keep elites
            next_population = current_population[:elite_count]

            # Generate new variants
            while len(next_population) < population_size:
                # Selection (tournament)
                parent1, parent2 = self._select_parents(current_population)

                # Create offspring through optimization
                child = self._create_offspring(parent1, parent2, mutation_rate)

                next_population.append(child)

            current_population = next_population

            # Track statistics
            fitnesses = [v.fitness for v in current_population]
            best_gen_variant = max(current_population, key=lambda v: v.fitness)

            stats = EvolutionStats(
                generation=self.current_generation,
                best_fitness=best_gen_variant.fitness,
                avg_fitness=sum(fitnesses) / len(fitnesses),
                best_variant_id=best_gen_variant.id,
                improvements=sum(1 for v in current_population if v.generation == self.current_generation),
                timestamp=time.time()
            )

            self.stats.append(stats)

            # Update best variant
            if best_gen_variant.fitness > best_variant.fitness:
                best_variant = best_gen_variant

                if self.debug:
                    print(f"New best variant: {best_variant.id}")
                    print(f"Fitness: {best_variant.fitness:.4f}")

            if self.debug and gen % 10 == 0:
                print(f"Best fitness: {stats.best_fitness:.4f}")
                print(f"Avg fitness: {stats.avg_fitness:.4f}")

        # Save evolution stats
        self._save_stats()

        return best_variant

    def _select_parents(self, population: List[CompilerVariant]) -> Tuple[CompilerVariant, CompilerVariant]:
        """Select two parents for breeding

        Args:
            population: Current population

        Returns:
            Two parent variants
        """
        import random

        # Tournament selection
        tournament_size = 3

        tournament1 = random.sample(population, min(tournament_size, len(population)))
        parent1 = max(tournament1, key=lambda v: v.fitness)

        tournament2 = random.sample(population, min(tournament_size, len(population)))
        parent2 = max(tournament2, key=lambda v: v.fitness)

        return parent1, parent2

    def _create_offspring(self, parent1: CompilerVariant,
                         parent2: CompilerVariant,
                         mutation_rate: float) -> CompilerVariant:
        """Create offspring from two parents

        Args:
            parent1, parent2: Parent variants
            mutation_rate: Mutation probability

        Returns:
            Child variant
        """
        # Optimize one of the parents
        import random

        parent = parent1 if random.random() < 0.5 else parent2

        # Apply optimization
        result = self.optimizer.optimize(parent.code, passes=2)

        # Optionally mutate
        if random.random() < mutation_rate:
            result.code = self.optimizer._mutate(result.code, rate=0.1)

        # Create new variant
        variant = CompilerVariant(
            id=self._generate_variant_id(result.code),
            generation=self.current_generation,
            code=result.code,
            parent_id=parent.id
        )

        # Evaluate
        variant.performance_metrics = self._evaluate_compiler(variant.code)
        variant.fitness = self._calculate_fitness(variant.performance_metrics)

        # Store variant
        self.variants[variant.id] = variant
        self._save_variant(variant)

        return variant

    def _save_variant(self, variant: CompilerVariant) -> None:
        """Save compiler variant to disk

        Args:
            variant: Variant to save
        """
        gen_dir = self.save_dir / f"gen_{variant.generation:04d}"
        gen_dir.mkdir(parents=True, exist_ok=True)

        # Save code
        code_file = gen_dir / f"{variant.id}.mal"
        code_file.write_text(variant.code)

        # Save metadata
        meta_file = gen_dir / f"{variant.id}.json"
        metadata = {
            'id': variant.id,
            'generation': variant.generation,
            'fitness': variant.fitness,
            'performance_metrics': variant.performance_metrics,
            'parent_id': variant.parent_id,
            'code_size': len(variant.code)
        }
        meta_file.write_text(json.dumps(metadata, indent=2))

    def _save_stats(self) -> None:
        """Save evolution statistics"""
        stats_file = self.save_dir / "evolution_stats.json"

        stats_data = [
            {
                'generation': s.generation,
                'best_fitness': s.best_fitness,
                'avg_fitness': s.avg_fitness,
                'best_variant_id': s.best_variant_id,
                'improvements': s.improvements,
                'timestamp': s.timestamp
            }
            for s in self.stats
        ]

        stats_file.write_text(json.dumps(stats_data, indent=2))

    def get_best_variant(self) -> Optional[CompilerVariant]:
        """Get best compiler variant

        Returns:
            Best variant or None if no variants exist
        """
        if not self.variants:
            return None

        return max(self.variants.values(), key=lambda v: v.fitness)

    def print_stats(self) -> None:
        """Print evolution statistics"""
        if not self.stats:
            print("No evolution statistics available")
            return

        print("\n=== Evolution Statistics ===")
        print(f"{'Gen':>5} {'Best Fitness':>15} {'Avg Fitness':>15} {'Improvements':>15}")
        print("-" * 60)

        for stat in self.stats[-20:]:  # Last 20 generations
            print(f"{stat.generation:5d} {stat.best_fitness:15.6f} "
                  f"{stat.avg_fitness:15.6f} {stat.improvements:15d}")

        best = self.get_best_variant()
        if best:
            print(f"\nBest variant: {best.id}")
            print(f"Fitness: {best.fitness:.6f}")
            print(f"Generation: {best.generation}")
            print(f"Code size: {len(best.code)} bytes")


def main():
    """Demo the self-improving compiler"""
    print("=== Self-Improving Malbolge Compiler ===\n")

    compiler = SelfImprovingCompiler(debug=True)

    # Bootstrap
    initial = compiler.bootstrap()
    print(f"\nInitial compiler fitness: {initial.fitness:.6f}")

    # Evolve
    print("\nEvolving compiler...")
    best = compiler.evolve(generations=20, population_size=5)

    print(f"\n=== Final Results ===")
    print(f"Best variant: {best.id}")
    print(f"Final fitness: {best.fitness:.6f}")
    print(f"Improvement: {(best.fitness - initial.fitness) / initial.fitness * 100:.1f}%")

    compiler.print_stats()


if __name__ == "__main__":
    main()
