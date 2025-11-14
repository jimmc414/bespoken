"""
Malbolge Virtual Machine

A complete implementation of the Malbolge esoteric programming language VM.

Malbolge Specification:
- Memory: 59049 (3^10) ternary cells
- Registers: a (accumulator), c (code pointer), d (data pointer)
- All arithmetic is modulo 59049
- Instructions encrypt themselves after execution
- Only 8 valid operations

Instruction Set:
- j: Set data pointer
- i: Input character
- /: Rotate accumulator right (ternary)
- *: Rotate memory right (ternary, then op)
- p: Output accumulator as character
- o: No operation
- <: Move data pointer
- v: Stop execution
"""

import sys
from typing import Optional, List, Tuple, IO
from dataclasses import dataclass


@dataclass
class ExecutionState:
    """Tracks execution state for debugging and optimization"""
    instructions_executed: int = 0
    memory_accesses: int = 0
    rotations: int = 0
    io_operations: int = 0


class MalbolgeVM:
    """Malbolge Virtual Machine Implementation"""

    # Constants
    MEMORY_SIZE = 59049  # 3^10

    # Translation tables
    XLAT1 = (
        "+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI"
        ".v%{gJh4G\\-=O@5`_3i<?Z';FNQuY]szf$!/|S#~W>qxdRp0w"
    )

    XLAT2 = (
        "5z]&gqtyfr$(we4{WP)H-Zn,[%\\3dL+Q;>U!pJS72FhOA1C"
        "B6v^=I_0/8|jsb9m<.TVac`uY*MK'X~xDl}REokN:#?G\"i@"
    )

    # Operation mapping (normalized instructions)
    OPS = {
        'j': 'set_data',
        'i': 'input',
        '/': 'rotate_acc',
        '*': 'rotate_mem',
        'p': 'output',
        'o': 'nop',
        '<': 'move_data',
        'v': 'halt'
    }

    def __init__(self, input_stream: Optional[IO] = None,
                 output_stream: Optional[IO] = None,
                 debug: bool = False):
        """Initialize the Malbolge VM

        Args:
            input_stream: Input stream (default: stdin)
            output_stream: Output stream (default: stdout)
            debug: Enable debug tracing
        """
        self.memory = [0] * self.MEMORY_SIZE
        self.a = 0  # Accumulator
        self.c = 0  # Code pointer
        self.d = 0  # Data pointer

        self.input_stream = input_stream or sys.stdin
        self.output_stream = output_stream or sys.stdout
        self.debug = debug

        self.halted = False
        self.state = ExecutionState()

        # Execution trace for debugging
        self.trace: List[Tuple[int, str, int, int, int]] = []

    def load_program(self, program: str) -> None:
        """Load a Malbolge program into memory

        Args:
            program: Malbolge source code

        Raises:
            ValueError: If program contains invalid characters
        """
        # Valid Malbolge characters (printable ASCII 33-126)
        valid_chars = set(chr(i) for i in range(33, 127))

        program = program.strip()

        for i, char in enumerate(program):
            if i >= self.MEMORY_SIZE:
                break

            if char not in valid_chars:
                raise ValueError(f"Invalid character at position {i}: {repr(char)}")

            # Convert to memory value
            self.memory[i] = ord(char)

            # Validate instruction at this position
            normalized = self._normalize_instruction(i)
            if normalized not in self.OPS:
                raise ValueError(
                    f"Invalid instruction at position {i}: {char} "
                    f"(normalizes to {normalized})"
                )

        # Fill rest of memory with crazy operations (NOP equivalent)
        for i in range(len(program), self.MEMORY_SIZE):
            self.memory[i] = self._crazy_op(i)

    def _normalize_instruction(self, pos: int) -> str:
        """Normalize instruction at given position

        Args:
            pos: Memory position

        Returns:
            Normalized instruction character
        """
        val = self.memory[pos]
        if val < 33 or val > 126:
            return ' '  # Invalid

        char = chr(val)
        xlat_pos = (pos + val - 33) % 94

        if xlat_pos >= len(self.XLAT1):
            return ' '

        return self.XLAT1[xlat_pos]

    def _crazy_op(self, pos: int) -> int:
        """Generate crazy operation (NOP) for position

        Args:
            pos: Memory position

        Returns:
            ASCII value that produces NOP at this position
        """
        # Find a value that normalizes to 'o' (NOP)
        for val in range(33, 127):
            xlat_pos = (pos + val - 33) % 94
            if xlat_pos < len(self.XLAT1) and self.XLAT1[xlat_pos] == 'o':
                return val
        return ord('o')  # Fallback

    def _encrypt_instruction(self, pos: int) -> None:
        """Encrypt instruction at position (self-modification)

        Args:
            pos: Memory position to encrypt
        """
        val = self.memory[pos]
        if val < 33 or val > 126:
            return

        xlat_pos = val - 33
        if xlat_pos >= len(self.XLAT2):
            return

        self.memory[pos] = ord(self.XLAT2[xlat_pos])

    def _ternary_rotate_right(self, val: int) -> int:
        """Rotate value right in ternary (base-3)

        This is the crazy rotation that Malbolge uses.

        Args:
            val: Value to rotate

        Returns:
            Rotated value
        """
        # Convert to ternary, rotate, convert back
        ternary = []
        temp = val
        for _ in range(10):  # 3^10 = 59049
            ternary.append(temp % 3)
            temp //= 3

        # Rotate right
        ternary = [ternary[-1]] + ternary[:-1]

        # Convert back to decimal
        result = 0
        for i in range(10):
            result += ternary[i] * (3 ** i)

        return result % self.MEMORY_SIZE

    def _tritwise_op(self, a: int, b: int) -> int:
        """Perform tritwise operation (like XOR but for ternary)

        Truth table:
        0,0 -> 1  0,1 -> 0  0,2 -> 0
        1,0 -> 1  1,1 -> 0  1,2 -> 2
        2,0 -> 2  2,1 -> 2  2,2 -> 1

        Args:
            a, b: Values to combine

        Returns:
            Result of tritwise op
        """
        table = [
            [1, 0, 0],
            [1, 0, 2],
            [2, 2, 1]
        ]

        result = 0
        for i in range(10):
            digit_a = (a // (3 ** i)) % 3
            digit_b = (b // (3 ** i)) % 3
            result += table[digit_a][digit_b] * (3 ** i)

        return result % self.MEMORY_SIZE

    def step(self) -> bool:
        """Execute one instruction

        Returns:
            True if should continue, False if halted
        """
        if self.halted:
            return False

        # Get current instruction
        normalized = self._normalize_instruction(self.c)
        op = self.OPS.get(normalized)

        if self.debug:
            self.trace.append((
                self.c,
                normalized,
                self.a,
                self.d,
                self.memory[self.d] if self.d < self.MEMORY_SIZE else 0
            ))

        self.state.instructions_executed += 1

        if not op:
            # Invalid instruction, treat as NOP
            op = 'nop'

        # Execute operation
        if op == 'set_data':
            self.d = self.memory[self.d]
            self.state.memory_accesses += 1

        elif op == 'input':
            char = self.input_stream.read(1)
            if char:
                self.a = ord(char)
            else:
                self.a = self.MEMORY_SIZE - 1  # EOF
            self.state.io_operations += 1

        elif op == 'rotate_acc':
            self.a = self._ternary_rotate_right(self.a)
            self.state.rotations += 1

        elif op == 'rotate_mem':
            mem_val = self.memory[self.d]
            self.memory[self.d] = self._ternary_rotate_right(mem_val)
            self.a = self._tritwise_op(self.a, self.memory[self.d])
            self.state.memory_accesses += 2
            self.state.rotations += 1

        elif op == 'output':
            if 0 <= self.a <= 255:
                self.output_stream.write(chr(self.a))
                self.output_stream.flush()
            self.state.io_operations += 1

        elif op == 'move_data':
            self.d = (self.d + 1) % self.MEMORY_SIZE

        elif op == 'halt':
            self.halted = True
            return False

        # Encrypt current instruction
        self._encrypt_instruction(self.c)

        # Move to next instruction
        self.c = (self.c + 1) % self.MEMORY_SIZE
        self.d = (self.d + 1) % self.MEMORY_SIZE

        return True

    def run(self, max_steps: Optional[int] = None) -> ExecutionState:
        """Run the program until halt or max steps

        Args:
            max_steps: Maximum steps to execute (None = unlimited)

        Returns:
            Execution state statistics
        """
        steps = 0
        while not self.halted:
            if max_steps and steps >= max_steps:
                break

            if not self.step():
                break

            steps += 1

        return self.state

    def print_trace(self, limit: int = 100) -> None:
        """Print execution trace

        Args:
            limit: Maximum number of trace entries to print
        """
        print("\n=== Execution Trace ===")
        print(f"{'Pos':>6} {'Op':>3} {'A':>6} {'D':>6} {'[D]':>6}")
        print("-" * 36)

        for i, (pos, op, a, d, mem_d) in enumerate(self.trace[:limit]):
            print(f"{pos:6d} {op:>3} {a:6d} {d:6d} {mem_d:6d}")

        if len(self.trace) > limit:
            print(f"... ({len(self.trace) - limit} more entries)")

    def print_state(self) -> None:
        """Print current VM state"""
        print("\n=== VM State ===")
        print(f"Accumulator (a): {self.a}")
        print(f"Code pointer (c): {self.c}")
        print(f"Data pointer (d): {self.d}")
        print(f"Halted: {self.halted}")
        print(f"\nInstructions executed: {self.state.instructions_executed}")
        print(f"Memory accesses: {self.state.memory_accesses}")
        print(f"Rotations: {self.state.rotations}")
        print(f"I/O operations: {self.state.io_operations}")


def main():
    """Command-line interface for Malbolge VM"""
    import argparse

    parser = argparse.ArgumentParser(description="Malbolge Virtual Machine")
    parser.add_argument("program", help="Malbolge program file")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--trace", action="store_true", help="Print execution trace")
    parser.add_argument("--max-steps", type=int, help="Maximum steps to execute")

    args = parser.parse_args()

    with open(args.program, 'r') as f:
        program = f.read()

    vm = MalbolgeVM(debug=args.debug or args.trace)

    try:
        vm.load_program(program)
        print(f"Loaded program ({len(program)} bytes)")

        vm.run(max_steps=args.max_steps)

        if args.trace:
            vm.print_trace()

        vm.print_state()

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
