"""
Malbolge programming tool for bespoken.

Provides tools for working with the Malbolge esoteric programming language,
including code generation, optimization, execution, and compiler evolution.
"""

import sys
import os
from pathlib import Path
from typing import Any, Dict, Optional
from io import StringIO

import llm
from rich import print

from .. import config

# Add malbolge to path
malbolge_path = Path(__file__).parent.parent.parent.parent / "malbolge"
if malbolge_path.exists():
    sys.path.insert(0, str(malbolge_path.parent))


class MalbolgeTool(llm.Toolbox):
    """Toolbox for Malbolge programming and compiler operations."""

    def __init__(self):
        """Initialize the Malbolge toolbox."""
        self.compiler = None
        self.last_program = None
        self.last_output = None

        # Import Malbolge modules
        try:
            from malbolge import (
                MalbolgeVM,
                MalbolgeGenerator,
                MalbolgeOptimizer,
                SelfImprovingCompiler
            )
            self.MalbolgeVM = MalbolgeVM
            self.MalbolgeGenerator = MalbolgeGenerator
            self.MalbolgeOptimizer = MalbolgeOptimizer
            self.SelfImprovingCompiler = SelfImprovingCompiler
            self._malbolge_available = True
        except ImportError as e:
            self._malbolge_available = False
            self._import_error = str(e)

    def _check_available(self) -> bool:
        """Check if Malbolge modules are available."""
        if not self._malbolge_available:
            return False
        return True

    def _debug_return(self, value: str) -> str:
        """Helper to show what the LLM receives from tools"""
        config.tool_debug(f"\n>>> Tool returning to LLM: {repr(value)}\n")
        return value

    def generate_program(self, instructions: str) -> str:
        """Generate a Malbolge program from high-level instructions.

        Args:
            instructions: Comma-separated list of instructions (nop, halt, rotate_acc, output_char, etc.)

        Returns:
            Generated Malbolge program code
        """
        config.tool_debug(f">>> LLM calling tool: generate_program(instructions={repr(instructions)})")
        config.tool_status(f"Generating Malbolge program...")

        if not self._check_available():
            return self._debug_return("Error: Malbolge modules not available")

        try:
            gen = self.MalbolgeGenerator()

            # Parse and emit instructions
            for instr in instructions.split(','):
                instr = instr.strip().lower()

                if instr == 'nop':
                    gen.nop()
                elif instr == 'halt':
                    gen.halt()
                elif instr == 'rotate_acc':
                    gen.rotate_acc()
                elif instr == 'rotate_mem':
                    gen.rotate_mem()
                elif instr == 'output_char' or instr == 'output':
                    gen.output_char()
                elif instr == 'input_char' or instr == 'input':
                    gen.input_char()
                elif instr == 'move_data':
                    gen.move_data()
                elif instr == 'set_data':
                    gen.set_data()
                else:
                    return self._debug_return(f"Error: Unknown instruction '{instr}'")

            self.last_program = gen.compile()

            return self._debug_return(
                f"Generated Malbolge program ({len(self.last_program)} bytes):\n{self.last_program}"
            )

        except Exception as e:
            return self._debug_return(f"Error generating program: {e}")

    def run_program(self, program: Optional[str] = None, max_steps: int = 10000) -> str:
        """Run a Malbolge program and return the output.

        Args:
            program: Malbolge program code (uses last generated if not provided)
            max_steps: Maximum execution steps

        Returns:
            Program output and execution statistics
        """
        config.tool_debug(f">>> LLM calling tool: run_program(program={repr(program)[:50] if program else 'None'}, max_steps={max_steps})")
        config.tool_status("Running Malbolge program...")

        if not self._check_available():
            return self._debug_return("Error: Malbolge modules not available")

        if program is None:
            program = self.last_program

        if program is None:
            return self._debug_return("Error: No program to run. Generate or provide a program first.")

        try:
            # Create output stream to capture output
            output_stream = StringIO()

            vm = self.MalbolgeVM(output_stream=output_stream)
            vm.load_program(program)
            state = vm.run(max_steps=max_steps)

            output = output_stream.getvalue()
            self.last_output = output

            result = []
            result.append(f"Program executed successfully")
            result.append(f"Instructions executed: {state.instructions_executed}")
            result.append(f"Memory accesses: {state.memory_accesses}")
            result.append(f"I/O operations: {state.io_operations}")
            result.append(f"Halted: {vm.halted}")

            if output:
                result.append(f"\nProgram output:\n{output}")
            else:
                result.append("\nNo output produced")

            return self._debug_return("\n".join(result))

        except Exception as e:
            return self._debug_return(f"Error running program: {e}")

    def optimize_program(self, program: Optional[str] = None, passes: int = 3) -> str:
        """Optimize a Malbolge program.

        Args:
            program: Malbolge program code (uses last generated if not provided)
            passes: Number of optimization passes

        Returns:
            Optimization results and optimized code
        """
        config.tool_debug(f">>> LLM calling tool: optimize_program(program={repr(program)[:50] if program else 'None'}, passes={passes})")
        config.tool_status(f"Optimizing Malbolge program with {passes} passes...")

        if not self._check_available():
            return self._debug_return("Error: Malbolge modules not available")

        if program is None:
            program = self.last_program

        if program is None:
            return self._debug_return("Error: No program to optimize. Generate or provide a program first.")

        try:
            optimizer = self.MalbolgeOptimizer()
            result = optimizer.optimize(program, passes=passes)

            self.last_program = result.code

            output = []
            output.append(f"Optimization complete")
            output.append(f"Original size: {result.original_size} bytes")
            output.append(f"Optimized size: {result.optimized_size} bytes")
            output.append(f"Size reduction: {result.stats['size_reduction']} bytes ({result.stats['size_reduction_pct']:.1f}%)")

            if result.passes_applied:
                output.append(f"Passes applied: {', '.join(result.passes_applied)}")

            output.append(f"\nOptimized program:\n{result.code}")

            return self._debug_return("\n".join(output))

        except Exception as e:
            return self._debug_return(f"Error optimizing program: {e}")

    def evolve_compiler(self, generations: int = 10, population_size: int = 5) -> str:
        """Evolve the self-improving Malbolge compiler.

        Args:
            generations: Number of generations to evolve
            population_size: Population size per generation

        Returns:
            Evolution results and statistics
        """
        config.tool_debug(f">>> LLM calling tool: evolve_compiler(generations={generations}, population_size={population_size})")
        config.tool_status(f"Evolving Malbolge compiler for {generations} generations...")

        if not self._check_available():
            return self._debug_return("Error: Malbolge modules not available")

        try:
            if self.compiler is None:
                save_dir = Path("./bespoken_malbolge_compiler")
                self.compiler = self.SelfImprovingCompiler(
                    debug=False,
                    save_dir=save_dir
                )
                config.tool_status("Bootstrapping compiler...")
                initial = self.compiler.bootstrap()
                initial_fitness = initial.fitness
            else:
                initial_fitness = self.compiler.get_best_variant().fitness

            # Evolve
            best = self.compiler.evolve(
                generations=generations,
                population_size=population_size,
                mutation_rate=0.15,
                elite_count=1
            )

            output = []
            output.append(f"Evolution complete")
            output.append(f"Generations: {generations}")
            output.append(f"Best variant: {best.id}")
            output.append(f"Final fitness: {best.fitness:.6f}")
            output.append(f"Improvement: {((best.fitness / initial_fitness) - 1) * 100:.1f}%")
            output.append(f"Code size: {len(best.code)} bytes")
            output.append(f"\nCompiler saved to: {self.compiler.save_dir}")

            return self._debug_return("\n".join(output))

        except Exception as e:
            return self._debug_return(f"Error evolving compiler: {e}")

    def get_compiler_stats(self) -> str:
        """Get statistics about the evolved compiler.

        Returns:
            Compiler evolution statistics
        """
        config.tool_debug(">>> LLM calling tool: get_compiler_stats()")
        config.tool_status("Getting compiler statistics...")

        if not self._check_available():
            return self._debug_return("Error: Malbolge modules not available")

        if self.compiler is None:
            return self._debug_return("No compiler available. Run evolve_compiler first.")

        try:
            best = self.compiler.get_best_variant()

            if not self.compiler.stats:
                return self._debug_return("No evolution statistics available yet.")

            output = []
            output.append("Compiler Evolution Statistics")
            output.append("=" * 50)
            output.append(f"Best variant: {best.id}")
            output.append(f"Generation: {best.generation}")
            output.append(f"Fitness: {best.fitness:.6f}")
            output.append(f"Code size: {len(best.code)} bytes")
            output.append(f"\nRecent generations:")

            for stat in self.compiler.stats[-10:]:
                output.append(
                    f"  Gen {stat.generation}: "
                    f"fitness={stat.best_fitness:.4f}, "
                    f"avg={stat.avg_fitness:.4f}"
                )

            return self._debug_return("\n".join(output))

        except Exception as e:
            return self._debug_return(f"Error getting stats: {e}")

    def explain_malbolge(self) -> str:
        """Explain what Malbolge is and how it works.

        Returns:
            Explanation of Malbolge
        """
        config.tool_debug(">>> LLM calling tool: explain_malbolge()")
        config.tool_status("Explaining Malbolge...")

        explanation = """
Malbolge: The Hardest Programming Language

Malbolge is an esoteric programming language designed by Ben Olmstead in 1998
to be as difficult as possible to program in. Key features:

1. POSITION-DEPENDENT INSTRUCTIONS
   - A character's meaning depends on where it is in memory
   - Same character at different positions = different instructions

2. SELF-MODIFYING CODE
   - Instructions encrypt themselves after execution
   - Programs evolve as they run

3. TERNARY ARITHMETIC
   - Everything uses base-3 math (modulo 3^10 = 59049)
   - Unusual rotation and operations

4. 8 INSTRUCTIONS ONLY
   - j: Set data pointer
   - i: Input character
   - /: Rotate accumulator
   - *: Rotate memory
   - p: Output character
   - o: No operation
   - <: Move data pointer
   - v: Halt

5. NO DIRECT CONTROL FLOW
   - No jumps or loops (must use self-modification)

The first "Hello World" program wasn't written until 2000 (2 years after the
language was created) and had to be generated by a beam search algorithm!

This toolbox provides a complete implementation including a self-improving
compiler that can autonomously optimize itself through evolution.
"""

        return self._debug_return(explanation.strip())
