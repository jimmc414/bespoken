"""
Malbolge Code Generator

Programmatic generation of Malbolge code. This is essential for building
a compiler, as writing Malbolge by hand is practically impossible.

The generator provides:
- High-level instruction building
- Memory layout management
- Automatic NOP generation
- Position-aware code generation
- Code alignment and padding
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field


@dataclass
class CodeBlock:
    """Represents a block of generated code"""
    instructions: List[str] = field(default_factory=list)
    position: int = 0
    label: Optional[str] = None


class MalbolgeGenerator:
    """Generate Malbolge code programmatically"""

    MEMORY_SIZE = 59049  # 3^10

    # Translation table (XLAT1) for instruction normalization
    XLAT1 = (
        "+b(29e*j1VMEKLyC})8&m#~W>qxdRp0wkrUo[D7,XTcA\"lI"
        ".v%{gJh4G\\-=O@5`_3i<?Z';FNQuY]szf$!/|S#~W>qxdRp0w"
    )

    # Reverse mapping: instruction -> possible characters
    INSTRUCTION_CHARS = {
        'j': [],  # set_data
        'i': [],  # input
        '/': [],  # rotate_acc
        '*': [],  # rotate_mem
        'p': [],  # output
        'o': [],  # nop
        '<': [],  # move_data
        'v': []   # halt
    }

    def __init__(self):
        """Initialize the code generator"""
        self.blocks: List[CodeBlock] = []
        self.current_block = CodeBlock()
        self.labels: Dict[str, int] = {}
        self.position = 0

        # Build reverse mapping for each position
        self._build_instruction_map()

    def _build_instruction_map(self) -> None:
        """Build mapping of instructions to characters for each position"""
        # For each ASCII printable character
        for ascii_val in range(33, 127):
            char = chr(ascii_val)

            # For each position, see what instruction it normalizes to
            for pos in range(self.MEMORY_SIZE):
                xlat_pos = (pos + ascii_val - 33) % 94

                if xlat_pos < len(self.XLAT1):
                    instruction = self.XLAT1[xlat_pos]

                    if instruction in self.INSTRUCTION_CHARS:
                        # Store (char, position) tuples
                        if not hasattr(self, '_pos_char_map'):
                            self._pos_char_map: Dict[Tuple[str, int], List[str]] = {}

                        key = (instruction, pos)
                        if key not in self._pos_char_map:
                            self._pos_char_map[key] = []
                        self._pos_char_map[key].append(char)

    def _find_char_for_instruction(self, instruction: str, position: int) -> str:
        """Find a character that produces the given instruction at position

        Args:
            instruction: Desired instruction (j, i, /, *, p, o, <, v)
            position: Memory position

        Returns:
            ASCII character that produces the instruction

        Raises:
            ValueError: If no character produces the instruction at this position
        """
        key = (instruction, position % self.MEMORY_SIZE)

        if key in self._pos_char_map and self._pos_char_map[key]:
            return self._pos_char_map[key][0]

        # Fallback: brute force search
        for ascii_val in range(33, 127):
            xlat_pos = (position + ascii_val - 33) % 94
            if xlat_pos < len(self.XLAT1) and self.XLAT1[xlat_pos] == instruction:
                return chr(ascii_val)

        raise ValueError(
            f"Cannot generate instruction '{instruction}' at position {position}"
        )

    def emit(self, instruction: str) -> 'MalbolgeGenerator':
        """Emit an instruction

        Args:
            instruction: Instruction to emit (j, i, /, *, p, o, <, v)

        Returns:
            Self for chaining
        """
        char = self._find_char_for_instruction(instruction, self.position)
        self.current_block.instructions.append(char)
        self.position += 1
        return self

    def set_data(self) -> 'MalbolgeGenerator':
        """Emit set_data instruction (j)"""
        return self.emit('j')

    def input_char(self) -> 'MalbolgeGenerator':
        """Emit input instruction (i)"""
        return self.emit('i')

    def rotate_acc(self) -> 'MalbolgeGenerator':
        """Emit rotate accumulator instruction (/)"""
        return self.emit('/')

    def rotate_mem(self) -> 'MalbolgeGenerator':
        """Emit rotate memory instruction (*)"""
        return self.emit('*')

    def output_char(self) -> 'MalbolgeGenerator':
        """Emit output instruction (p)"""
        return self.emit('p')

    def nop(self) -> 'MalbolgeGenerator':
        """Emit no-op instruction (o)"""
        return self.emit('o')

    def move_data(self) -> 'MalbolgeGenerator':
        """Emit move data pointer instruction (<)"""
        return self.emit('<')

    def halt(self) -> 'MalbolgeGenerator':
        """Emit halt instruction (v)"""
        return self.emit('v')

    def label(self, name: str) -> 'MalbolgeGenerator':
        """Create a label at current position

        Args:
            name: Label name

        Returns:
            Self for chaining
        """
        self.labels[name] = self.position
        return self

    def align(self, boundary: int) -> 'MalbolgeGenerator':
        """Align code to boundary with NOPs

        Args:
            boundary: Alignment boundary

        Returns:
            Self for chaining
        """
        while self.position % boundary != 0:
            self.nop()
        return self

    def pad_to(self, position: int) -> 'MalbolgeGenerator':
        """Pad with NOPs to reach position

        Args:
            position: Target position

        Returns:
            Self for chaining
        """
        while self.position < position:
            self.nop()
        return self

    def repeat(self, instruction: str, count: int) -> 'MalbolgeGenerator':
        """Repeat an instruction multiple times

        Args:
            instruction: Instruction to repeat
            count: Number of times to repeat

        Returns:
            Self for chaining
        """
        for _ in range(count):
            self.emit(instruction)
        return self

    def new_block(self, label: Optional[str] = None) -> 'MalbolgeGenerator':
        """Start a new code block

        Args:
            label: Optional label for the block

        Returns:
            Self for chaining
        """
        if self.current_block.instructions:
            self.current_block.position = self.position - len(
                self.current_block.instructions
            )
            self.blocks.append(self.current_block)

        self.current_block = CodeBlock(label=label, position=self.position)

        if label:
            self.labels[label] = self.position

        return self

    def get_label_position(self, label: str) -> Optional[int]:
        """Get position of a label

        Args:
            label: Label name

        Returns:
            Position or None if not found
        """
        return self.labels.get(label)

    def compile(self) -> str:
        """Compile all blocks into final Malbolge code

        Returns:
            Generated Malbolge program
        """
        # Add current block if it has instructions
        if self.current_block.instructions:
            self.current_block.position = self.position - len(
                self.current_block.instructions
            )
            self.blocks.append(self.current_block)
            self.current_block = CodeBlock()

        # Concatenate all blocks
        code = []
        for block in self.blocks:
            code.extend(block.instructions)

        return ''.join(code)

    def reset(self) -> 'MalbolgeGenerator':
        """Reset generator to initial state

        Returns:
            Self for chaining
        """
        self.blocks = []
        self.current_block = CodeBlock()
        self.labels = {}
        self.position = 0
        return self

    def info(self) -> Dict[str, any]:
        """Get generator information

        Returns:
            Dictionary with generator stats
        """
        return {
            'position': self.position,
            'blocks': len(self.blocks),
            'labels': dict(self.labels),
            'current_block_size': len(self.current_block.instructions)
        }


class MalbolgeAssembler:
    """Higher-level assembler for Malbolge

    Provides pseudo-instructions and macros for common operations.
    """

    def __init__(self):
        self.gen = MalbolgeGenerator()

    def hello_world(self) -> str:
        """Generate Hello World program

        Returns:
            Malbolge Hello World program
        """
        # This is a simplified approach - real Hello World in Malbolge
        # requires complex initialization
        self.gen.reset()

        # Character output sequence for "Hello, World!"
        chars = "Hello, World!\n"

        for char in chars:
            # In practice, setting up the accumulator for specific
            # characters in Malbolge is extremely complex
            # This is a placeholder for the concept
            self.gen.nop()  # Setup for character would go here

        self.gen.halt()
        return self.gen.compile()

    def echo_program(self) -> str:
        """Generate program that echoes input to output (cat)

        Returns:
            Malbolge echo program
        """
        self.gen.reset()

        self.gen.label("loop")
        self.gen.input_char()    # Read character
        self.gen.output_char()   # Output character
        # In real Malbolge, we'd need to loop back to 'loop'
        # This requires careful position management
        self.gen.nop()           # Placeholder for loop logic

        self.gen.halt()
        return self.gen.compile()

    def set_accumulator(self, value: int) -> 'MalbolgeAssembler':
        """Macro: Set accumulator to specific value

        This is extremely complex in Malbolge and would require
        many rotation operations.

        Args:
            value: Desired accumulator value

        Returns:
            Self for chaining
        """
        # Calculate number of rotations needed
        # This is a simplified placeholder
        rotations_needed = value % 59049

        for _ in range(min(rotations_needed, 100)):  # Limit iterations
            self.gen.rotate_acc()

        return self

    def compile(self) -> str:
        """Compile assembled code

        Returns:
            Generated Malbolge program
        """
        return self.gen.compile()


def main():
    """Demo the code generator"""
    print("=== Malbolge Code Generator Demo ===\n")

    # Create generator
    gen = MalbolgeGenerator()

    # Generate simple program
    gen.label("start")
    gen.nop()
    gen.rotate_acc()
    gen.output_char()
    gen.halt()

    code = gen.compile()

    print(f"Generated code ({len(code)} bytes):")
    print(code)
    print(f"\nLabels: {gen.labels}")
    print(f"Info: {gen.info()}")

    # Try assembler
    print("\n=== Assembler Demo ===\n")
    asm = MalbolgeAssembler()
    echo_code = asm.echo_program()
    print(f"Echo program ({len(echo_code)} bytes):")
    print(echo_code)


if __name__ == "__main__":
    main()
