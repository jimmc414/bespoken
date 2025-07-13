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


