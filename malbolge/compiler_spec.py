"""
Malbolge Compiler Specification

High-level specification of the Malbolge compiler logic.
This specification is transpiled to Malbolge to create the bootstrap compiler.

The compiler consists of:
1. Lexer - Tokenize input
2. Parser - Build abstract syntax tree
3. Code Generator - Generate Malbolge bytecode
4. Optimizer - Optimize generated code
5. Emitter - Output final program
"""

from typing import List, Dict, Optional
from dataclasses import dataclass
from enum import Enum

from .generator import MalbolgeGenerator


class TokenType(Enum):
    """Token types for Malbolge source"""
    INSTRUCTION = "instruction"
    WHITESPACE = "whitespace"
    EOF = "eof"
    INVALID = "invalid"


@dataclass
class Token:
    """Represents a token"""
    type: TokenType
    value: str
    position: int


class MalbolgeCompilerSpec:
    """High-level specification of Malbolge compiler

    This specification describes the compiler logic in a way that can
    be transpiled to Malbolge itself.
    """

    # Valid Malbolge instructions
    INSTRUCTIONS = {'j', 'i', '/', '*', 'p', 'o', '<', 'v'}

    def __init__(self):
        """Initialize compiler specification"""
        self.generator = MalbolgeGenerator()

    def tokenize(self, source: str) -> List[Token]:
        """Tokenize Malbolge source code

        Args:
            source: Source code

        Returns:
            List of tokens
        """
        tokens = []

        for pos, char in enumerate(source):
            if char in self.INSTRUCTIONS:
                tokens.append(Token(
                    type=TokenType.INSTRUCTION,
                    value=char,
                    position=pos
                ))
            elif char.isspace():
                tokens.append(Token(
                    type=TokenType.WHITESPACE,
                    value=char,
                    position=pos
                ))
            else:
                # In real Malbolge, we need to consider position-dependent
                # instruction normalization
                tokens.append(Token(
                    type=TokenType.INVALID,
                    value=char,
                    position=pos
                ))

        tokens.append(Token(
            type=TokenType.EOF,
            value='',
            position=len(source)
        ))

        return tokens

    def parse(self, tokens: List[Token]) -> List[Token]:
        """Parse tokens into AST

        For Malbolge, parsing is simple - we just validate instructions.

        Args:
            tokens: List of tokens

        Returns:
            Validated instruction tokens
        """
        instructions = []

        for token in tokens:
            if token.type == TokenType.INSTRUCTION:
                instructions.append(token)
            elif token.type == TokenType.INVALID:
                raise ValueError(f"Invalid character at position {token.position}: {token.value}")

        return instructions

    def generate_code(self, instructions: List[Token]) -> str:
        """Generate Malbolge code from AST

        Args:
            instructions: Instruction tokens

        Returns:
            Generated Malbolge code
        """
        self.generator.reset()

        for token in instructions:
            self.generator.emit(token.value)

        return self.generator.compile()

    def optimize(self, code: str) -> str:
        """Optimize generated code

        Args:
            code: Generated code

        Returns:
            Optimized code
        """
        from .optimizer import MalbolgeOptimizer

        optimizer = MalbolgeOptimizer()
        result = optimizer.optimize(code, passes=1)
        return result.code

    def compile(self, source: str) -> str:
        """Compile Malbolge source to optimized Malbolge

        Args:
            source: Source code

        Returns:
            Compiled and optimized code
        """
        # Tokenize
        tokens = self.tokenize(source)

        # Parse
        instructions = self.parse(tokens)

        # Generate code
        code = self.generate_code(instructions)

        # Optimize
        optimized = self.optimize(code)

        return optimized

    def transpile_to_malbolge(self) -> str:
        """Transpile this compiler specification to Malbolge

        This creates a Malbolge program that implements the compiler.

        Returns:
            Malbolge compiler code
        """
        gen = MalbolgeGenerator()
        gen.reset()

        # Generate compiler in Malbolge
        # This is a simplified version - a full compiler would be much larger

        # Compiler main structure:
        # 1. Read input character by character
        # 2. Validate each character
        # 3. Output valid characters
        # 4. Halt when done

        gen.label("start")

        # Main compilation loop
        gen.label("compile_loop")

        # Read input
        gen.input_char()

        # Check if character is valid instruction
        # (In real implementation: complex validation logic)

        # Output character
        gen.output_char()

        # Continue loop
        # (In real implementation: loop control logic)
        gen.nop()
        gen.nop()

        # Eventually halt
        gen.halt()

        return gen.compile()


def generate_bootstrap_compiler() -> str:
    """Generate the bootstrap compiler in Malbolge

    Returns:
        Bootstrap compiler code
    """
    spec = MalbolgeCompilerSpec()
    return spec.transpile_to_malbolge()


def main():
    """Demo the compiler specification"""
    print("=== Malbolge Compiler Specification ===\n")

    spec = MalbolgeCompilerSpec()

    # Test compilation
    test_source = "ooo/p<v"  # Simple program
    print(f"Source: {test_source}")

    try:
        compiled = spec.compile(test_source)
        print(f"Compiled ({len(compiled)} bytes): {compiled}")
    except Exception as e:
        print(f"Compilation error: {e}")

    # Generate bootstrap compiler
    print("\n=== Bootstrap Compiler ===")
    bootstrap = generate_bootstrap_compiler()
    print(f"Bootstrap compiler ({len(bootstrap)} bytes):")
    print(bootstrap[:200], "..." if len(bootstrap) > 200 else "")


if __name__ == "__main__":
    main()
