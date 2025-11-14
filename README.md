# bespoken

```

██████╗ ███████╗███████╗██████╗  ██████╗ ██╗  ██╗███████╗███╗   ██╗
██╔══██╗██╔════╝██╔════╝██╔══██╗██╔═══██╗██║ ██╔╝██╔════╝████╗  ██║
██████╔╝█████╗  ███████╗██████╔╝██║   ██║█████╔╝ █████╗  ██╔██╗ ██║
██╔══██╗██╔══╝  ╚════██║██╔═══╝ ██║   ██║██╔═██╗ ██╔══╝  ██║╚██╗██║
██████╔╝███████╗███████║██║     ╚██████╔╝██║  ██╗███████╗██║ ╚████║
╚═════╝ ╚══════╝╚══════╝╚═╝      ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═══╝


A terminal chat experience that you can configure yourself.
```

## Featured Project: Self-Improving Malbolge Compiler

Bespoken now includes a complete **self-improving optimizing compiler for Malbolge** - one of the most ambitious programming projects possible! This meta-circular compiler is written in Malbolge itself and can autonomously improve its own performance through evolutionary optimization.

🔥 **[Explore the Malbolge Compiler →](malbolge/)**

**Key Features:**
- Complete Malbolge VM implementation
- Programmatic code generator (essential for Malbolge)
- Multi-pass optimization engine with genetic algorithms
- Self-improving compiler that evolves over generations
- Comprehensive documentation, tests, and examples

**Quick Demo:**
```bash
cd malbolge
python demo.py  # See the complete system in action
```

See the [Malbolge Guide](malbolge/GUIDE.md) for complete documentation.

---

## Installation

Basic installation:

```bash
pip install bespoken
```

## AI Engine Options

Bespoken supports two ways to power your AI conversations:

### Option 1: Claude Code CLI (Recommended - No API Keys!)

Use Claude Code CLI as your AI engine for fast, local responses:

```bash
# Install Claude Code
npm install -g @anthropic/claude-code

# Use with bespoken  
python -m bespoken --model claude
```

**Benefits:**
- ✅ No API keys required
- ✅ 2-10x faster responses (100-300ms)
- ✅ Works offline
- ✅ No rate limits or costs

### Option 2: LLM Library (API-based models)

Use the [llm](https://llm.datasette.io/en/stable/) library for API-based models:

```bash
# Install model plugins
llm install llm-anthropic

# Set up API keys
export ANTHROPIC_API_KEY="your-key-here"

# Use with bespoken
python -m bespoken --model anthropic/claude-3-5-sonnet-20240620
```

## Usage

Here's an example using either engine:

![demo](https://github.com/user-attachments/assets/fd358f95-26dc-4f2d-adbd-2eb4ab1804af)

This interface was defined via below:

```python
from bespoken import chat
from bespoken.tools import FileTool, TodoTools, PlaywrightTool

# Using Claude Code CLI (recommended)
chat(
    model_name="claude",
    tools=[FileTool("edit.py")],
    system_prompt="You are a coding assistant that can make edits to a single file.",
    debug=True,
)

# Or using API-based models
chat(
    model_name="anthropic/claude-3-5-sonnet-20240620", 
    tools=[FileTool("edit.py")],
    system_prompt="You are a coding assistant that can make edits to a single file.",
    debug=True,
)
```

## Features 

### Autocomplete 

Tab completion for commands and file paths. Use `@file.py` to get file path suggestions, "/" + <kbd>TAB></kbd> to autocomplete commands or use arrow keys for command history.

![parrot](https://github.com/user-attachments/assets/284ce287-ecc6-4beb-8fb5-6df77d3704f7)

### Custom slash commands

Define your own `/commands` that either send text to the LLM or trigger interactive functions:

```python
def save_conversation():
    """Save conversation to file"""
    filename = ui.input("Filename: ")
    return f"Saved to {filename}"

# Works with both Claude Code and API models
chat(
    model_name="claude",  # or "anthropic/claude-3-5-sonnet-20240620"
    slash_commands={
        "/save": save_conversation,
        "/formal": "Please respond in a formal manner.",
    }
)
```

## Feature Compatibility

| Feature | Claude Code CLI | API Models (llm) | Notes |
|---------|----------------|------------------|-------|
| **File editing** | ✅ | ✅ | Full UI confirmations work |
| **Tool execution** | ✅ | ✅ | FileTool, CommandTool, etc. |
| **Slash commands** | ✅ | ✅ | Custom workflow commands |
| **Conversation memory** | ✅ | ✅ | Context preserved |
| **Tab completion** | ✅ | ✅ | `@file.py` autocompletion |
| **Rich UI** | ✅ | ✅ | Colors, confirmations, diffs |
| **Streaming** | ✅ (simulated) | ✅ | Word-by-word display |
| **Debug mode** | ✅ | ✅ | Shows actual commands |
| **Performance** | ✅ Fast (100-300ms) | ⚠️ Slower (500-2000ms) | Network latency |
| **Offline usage** | ✅ | ❌ | API requires internet |
| **API costs** | ✅ Free | ❌ Paid per token | Cost consideration |

## Quick Start Examples

### File Editing Assistant
```bash
# Create a file to edit
echo "def hello(): print('world')" > example.py

# Start bespoken with Claude Code
python -m bespoken --model claude

# Then try:
# > What's in example.py?
# > Add a docstring to the function
# > Make it print 'Hello, World!' instead
```

### Code Review Session
```python
from bespoken import chat
from bespoken.tools import FileTool

chat(
    model_name="claude",
    tools=[FileTool("src/")],
    system_prompt="You are a senior code reviewer. Focus on security and best practices."
)
```


You can swap out the AI engine between Claude Code CLI (for speed and offline use) or API-based models (for broader model selection and LLM feature set) as you see fit.

## Using Bespoken with Malbolge

The Malbolge compiler integrates seamlessly with bespoken. Create an AI assistant that can help you work with Malbolge code:

```python
from bespoken import chat
from bespoken.tools import MalbolgeTool

chat(
    model_name="claude",
    tools=[MalbolgeTool()],
    system_prompt="""You are a Malbolge programming expert. You can:
    - Generate Malbolge programs
    - Optimize existing code
    - Explain how Malbolge programs work
    - Run and debug Malbolge programs
    - Evolve the compiler to improve performance
    """
)
```

**Example session:**
```
> Generate a simple Malbolge program that outputs 'Hi'

I'll create a Malbolge program for you...
[Uses MalbolgeTool to generate and test code]

> Now optimize it to make it smaller

Running optimization passes...
[Shows before/after code size]

> Evolve the compiler for 20 generations

Starting evolution...
[Shows progress and fitness improvements]
```

See [examples/malbolge_assistant.py](examples/malbolge_assistant.py) for a complete working example.

## Project Structure

```
bespoken/
├── src/bespoken/          # Main framework
│   ├── tools/             # Built-in tools
│   │   ├── malbolge.py    # Malbolge integration tool
│   │   └── ...
│   └── ...
├── malbolge/              # Self-improving Malbolge compiler
│   ├── vm.py              # Virtual machine
│   ├── generator.py       # Code generator
│   ├── optimizer.py       # Optimization engine
│   ├── self_improve.py    # Self-improvement system
│   ├── tests/             # Test suite
│   ├── examples/          # Example programs
│   └── docs/              # Documentation
└── examples/
    └── malbolge_assistant.py  # Bespoken + Malbolge demo
```

## Contributing

Contributions are welcome! Whether you're improving the bespoken framework or enhancing the Malbolge compiler, we'd love your help.

## License

MIT License - See LICENSE file for details

