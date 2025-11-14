#!/usr/bin/env python3
"""
Malbolge Programming Assistant

An interactive AI assistant that helps you work with the Malbolge programming
language using the bespoken framework.

This example demonstrates the integration between bespoken and the Malbolge
compiler, allowing you to:
- Generate Malbolge programs
- Run and debug Malbolge code
- Optimize programs
- Evolve the compiler

Usage:
    python examples/malbolge_assistant.py

Example interactions:
    > Generate a simple Malbolge program with 3 NOPs and a halt
    > Run the program and show me the output
    > Optimize it to reduce size
    > Evolve the compiler for 10 generations
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from bespoken import chat
from bespoken.tools import MalbolgeTool

def main():
    """Run the Malbolge programming assistant."""

    system_prompt = """You are an expert in the Malbolge esoteric programming language.

You have access to tools that let you:
- generate_program: Create Malbolge programs from high-level instructions
- run_program: Execute Malbolge programs and see output
- optimize_program: Optimize programs to reduce size and improve performance
- evolve_compiler: Evolve the self-improving compiler through genetic algorithms
- get_compiler_stats: View compiler evolution statistics
- explain_malbolge: Get detailed information about Malbolge

When generating programs, use instruction names like:
- nop (no operation)
- halt (stop execution)
- rotate_acc (rotate accumulator)
- output_char (output character)
- input_char (input character)
- move_data (move data pointer)
- set_data (set data pointer)
- rotate_mem (rotate memory)

Separate multiple instructions with commas.

Be helpful and educational. Explain what Malbolge is, how it works, and
what makes it challenging. Help users understand the programs you generate.

Remember that Malbolge is extremely difficult to program in by hand, so
the code generator is essential. The self-modifying nature and position-
dependent instructions make it one of the hardest programming languages
ever created.
"""

    print("\n" + "=" * 70)
    print("  MALBOLGE PROGRAMMING ASSISTANT")
    print("  Powered by bespoken + Malbolge Compiler")
    print("=" * 70)
    print("\nWelcome! I can help you work with Malbolge, one of the hardest")
    print("programming languages ever created.")
    print("\nTry asking:")
    print("  - What is Malbolge?")
    print("  - Generate a simple program")
    print("  - Optimize my code")
    print("  - Evolve the compiler")
    print("\nType '/quit' to exit.\n")

    # Start chat with Malbolge tools
    chat(
        model_name="claude",  # Use Claude Code CLI for fast responses
        tools=[MalbolgeTool()],
        system_prompt=system_prompt,
        debug=False,  # Set to True to see tool calls
    )


if __name__ == "__main__":
    main()
