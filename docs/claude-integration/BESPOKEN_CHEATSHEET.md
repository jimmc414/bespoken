# Bespoken Test Plan & Command Cheatsheet 🚀

## 🎯 **Step-by-Step Test Plan**

Follow this sequence to test all features systematically:

### **Phase 1: Basic Functionality** (5 minutes)

#### Step 1: Start Basic Chat
```bash
python -m bespoken --model claude
```
**Expected:** Banner appears, shows "Using Claude Code CLI", prompt `>` ready

#### Step 2: Test Basic Inference
```
What is 2+2?
```
**Expected:** Fast response (under 1 second), answer "4"
**✅ Check:** Response speed noticeably faster than API calls

#### Step 3: Test Built-in Commands
```
/help
```
**Expected:** Shows list of available commands
**✅ Check:** Commands listed: /quit, /help, /tools, /debug

#### Step 4: Test Debug Mode
```
/debug
```
**Expected:** "Debug mode enabled" message
**✅ Check:** Now shows actual `claude -p` commands being executed

#### Step 5: Ask Question in Debug Mode
```
What is Python?
```
**Expected:** See the actual command: `claude -p "What is Python?" --system-prompt ...`
**✅ Check:** Command visible, response received

#### Step 6: Exit
```
/quit
```

### **Phase 2: Conversation Memory** (3 minutes)

#### Step 1: Start Fresh Session
```bash
python -m bespoken --model claude
```

#### Step 2: Give Context
```
My name is Jim and my favorite programming language is Python
```
**Expected:** Acknowledgment of information

#### Step 3: Test Memory
```
What's my name and what language do I like?
```
**Expected:** "Your name is Jim and you like Python"
**✅ Check:** Context remembered across exchanges

#### Step 4: Build on Context
```
Why do you think I chose that language?
```
**Expected:** Response references previous context about Python
**✅ Check:** Coherent conversation flow

### **Phase 3: System Prompts** (2 minutes)

#### Step 1: Start with System Prompt
```bash
python -m bespoken --model claude --system "You are a pirate. Always say 'Arrr!' and speak like a pirate."
```

#### Step 2: Test System Behavior
```
How are you today?
```
**Expected:** Response includes "Arrr!" and pirate speech
**✅ Check:** System prompt is working

#### Step 3: Ask Technical Question
```
How do I write a Python function?
```
**Expected:** Technical answer but still in pirate style
**✅ Check:** System prompt maintained

### **Phase 4: Tool Integration** (10 minutes)

#### Step 1: Create Test Environment
```bash
# Create test files first
echo "def hello(): print('Hello World')" > test.py
echo "# This is a sample file" > sample.txt
```

#### Step 2: Create Tool Test Script
```python
# Save as test_tools.py
from bespoken import chat
from bespoken.tools import FileTool

chat(
    model_name="claude",
    tools=[FileTool("test.py")],
    system_prompt="You can read and edit the file test.py"
)
```

#### Step 3: Run Tool Test
```bash
python test_tools.py
```

#### Step 4: Test File Reading
```
What's in the file?
```
**Expected:** Shows actual content: "def hello(): print('Hello World')"
**✅ Check:** File was actually read and analyzed

#### Step 5: Test File Editing
```
Add a docstring to the function
```
**Expected:** Suggests or implements docstring addition
**✅ Check:** Tool execution working

#### Step 6: Test Directory Exploration
```python
# Save as explore_test.py
from bespoken import chat
from bespoken.tools import FileTool

chat(
    model_name="claude",
    tools=[FileTool(".")],
    system_prompt="You are a project explorer."
)
```

#### Step 7: Run Directory Test
```bash
python explore_test.py
```

#### Step 8: Test Directory Analysis
```
What Python files are in this directory?
```
**Expected:** Lists actual .py files found
**✅ Check:** Directory traversal working

### **Phase 5: Custom Slash Commands** (5 minutes)

#### Step 1: Create Custom Commands Script
```python
# Save as custom_test.py
from bespoken import chat

def pirate_mode():
    return "You are now a pirate! Always say 'Arrr!'"

def current_time():
    import datetime
    return f"Current time: {datetime.datetime.now()}"

chat(
    model_name="claude",
    slash_commands={
        "/pirate": pirate_mode,
        "/time": current_time,
        "/joke": "Tell me a programming joke"
    }
)
```

#### Step 2: Run Custom Commands Test
```bash
python custom_test.py
```

#### Step 3: Test Custom Commands
```
/pirate
```
**Expected:** "You are now a pirate!" message, behavior change

```
How are you?
```
**Expected:** Pirate-style response

```
/time
```
**Expected:** Shows current timestamp

```
/joke
```
**Expected:** Programming joke

**✅ Check:** All custom commands working

### **Phase 6: Performance Comparison** (3 minutes)

#### Step 1: Time Bespoken
```bash
time python -c "
from bespoken.claude_simple import get_model
model = get_model('claude')
conv = model.conversation()
print(conv.chain('What is 2+2?').text())
"
```
**Expected:** Under 0.5 seconds total

#### Step 2: Time Raw Claude
```bash
time claude -p "What is 2+2?"
```
**Expected:** Similar or slightly faster

**✅ Check:** Bespoken overhead is minimal

### **Phase 7: Error Handling** (2 minutes)

#### Step 1: Test Invalid Command
```bash
python -m bespoken --model claude
```
```
/invalidcommand
```
**Expected:** Graceful error or "unknown command" message

#### Step 2: Test Long Input
```
Write a very long detailed explanation about quantum computing, machine learning, artificial intelligence, and how they all interconnect in modern technology stacks, including examples and code samples
```
**Expected:** Handles long input gracefully, doesn't crash

**✅ Check:** No crashes, graceful error handling

## 🔍 **Areas to Explore Further**

### **Advanced File Operations**
- Test with multiple files
- Try editing large files  
- Test with different file types (JSON, markdown, etc.)

### **Complex Conversations**
- Multi-turn technical discussions
- Code review sessions
- Learning/tutorial scenarios

### **Custom Workflows**
- Create domain-specific slash commands
- Build project-specific helpers
- Integrate with external tools

### **Performance Edge Cases**
- Very long responses
- Rapid-fire questions
- Complex file operations

## 📝 **Test Results Checklist**

- [ ] **Basic chat works** - Fast responses, no errors
- [ ] **System prompts work** - Behavior changes as expected  
- [ ] **Conversation memory works** - Context preserved
- [ ] **File tools work** - Actually reads/edits files
- [ ] **Custom slash commands work** - Commands execute properly
- [ ] **Debug mode works** - Shows actual `claude -p` commands
- [ ] **Performance is good** - Under 1 second for simple queries
- [ ] **Error handling is graceful** - No crashes on bad input
- [ ] **Tab completion works** - File path completion
- [ ] **Overall UX is smooth** - Pleasant to use for extended sessions

## 🎯 **Success Criteria**

**✅ Integration Working** if:
- All basic tests pass
- Tools actually execute (don't just pretend)
- Performance is noticeably fast
- No major crashes or errors
- Memory/context works across conversation

**🚀 Ready for Production** if:
- All test phases complete successfully
- Performance meets expectations
- Error handling is robust
- UX feels polished and responsive

**Start with Phase 1 and work through each phase systematically!** 🎉

## 🛠️ Tool Integration Examples

### File Tool Setup
```python
# Save as test_files.py
from bespoken import chat
from bespoken.tools import FileTool

# Create test file first
with open("example.py", "w") as f:
    f.write("def hello():\n    print('Hello World')")

chat(
    model_name="claude",
    tools=[FileTool("example.py")],
    system_prompt="You can read and edit the file example.py"
)
```

Then try these prompts:
```
What's in the file?
Add a docstring to the function
Make it print "Hello Claude" instead
Add error handling to the function
```

### Directory Tool
```python
# Save as explore_project.py
from bespoken import chat
from bespoken.tools import FileTool

chat(
    model_name="claude",
    tools=[FileTool(".")],
    system_prompt="You are a project explorer. Help analyze this codebase."
)
```

Try:
```
What files are in this directory?
Show me the main Python files
What does this project do?
Find any TODO comments in the code
```

### Command Tool
```python
# Save as terminal_helper.py
from bespoken import chat
from bespoken.tools import CommandTool

chat(
    model_name="claude",
    tools=[CommandTool()],
    system_prompt="You are a terminal assistant. You can run commands to help."
)
```

Try:
```
What's my current directory?
List all Python files here
Show me system information
What processes are running?
```

## 🎭 Custom Slash Commands

```python
# Save as custom_commands.py
from bespoken import chat, ui

def pirate_mode():
    """Switch to pirate speaking mode"""
    return "You are now a pirate! Always say 'Arrr!' and speak like a pirate."

def formal_mode():
    """Switch to formal academic mode"""
    return "Please respond in a formal, academic tone with proper citations."

def save_chat():
    """Save conversation"""
    filename = ui.input("Save conversation as: ")
    return f"Conversation saved to {filename} (simulated)"

def show_time():
    """Show current time"""
    import datetime
    return f"Current time: {datetime.datetime.now()}"

chat(
    model_name="claude",
    slash_commands={
        "/pirate": pirate_mode,
        "/formal": formal_mode,
        "/save": save_chat,
        "/time": show_time,
        "/joke": "Tell me a programming joke",
        "/explain": "Explain the last response in simpler terms"
    }
)
```

Test the commands:
```
/pirate
How are you today?
/formal  
Explain machine learning
/time
/joke
/save
```

## 🧪 Specific Feature Tests

### Test System Prompts
```bash
python -m bespoken --model claude --system "You are Shakespeare. Speak in old English."
```
Try: `How do you feel about modern technology?`

### Test Conversation Memory
```bash
python -m bespoken --model claude
```
```
My favorite color is purple
I like pizza with mushrooms
Tell me a story that incorporates my preferences
```

### Test Debug Mode
```bash
python -m bespoken --model claude --debug
```
```
What is recursion?
```
(You'll see the actual `claude -p` command being executed)

### Test Tab Completion
```bash
python -m bespoken --model claude
```
Then type: `Read the file @` and press TAB to see file completion

## 🎯 Comparison Tests

### Speed Test
```bash
# Time a simple query
time python -c "
from bespoken.claude_simple import get_model
model = get_model('claude')
conv = model.conversation()
print(conv.chain('What is 2+2?').text())
"
```

### vs Raw Claude
```bash
# Compare with raw claude
time claude -p "What is 2+2?"
```

## 🚀 Advanced Scenarios

### Code Review Session
```python
# Save as code_review.py
from bespoken import chat
from bespoken.tools import FileTool

chat(
    model_name="claude",
    tools=[FileTool("src/")],
    system_prompt="You are a senior code reviewer. Look for bugs, improvements, and best practices."
)
```

Try:
```
Review all Python files in this directory
What are the main functions and classes?
Are there any potential security issues?
Suggest improvements for code quality
```

### Learning Assistant
```python
# Save as tutor.py
from bespoken import chat

def quiz_mode():
    return "Switch to quiz mode. Ask me questions to test my understanding."

def explain_mode():
    return "Switch to explanation mode. Explain concepts step by step."

chat(
    model_name="claude",
    system_prompt="You are a programming tutor.",
    slash_commands={
        "/quiz": quiz_mode,
        "/explain": explain_mode,
        "/example": "Show me a practical example",
        "/practice": "Give me a coding exercise"
    }
)
```

## 📝 Quick Test Checklist

- [ ] Basic chat works
- [ ] System prompts work
- [ ] Conversation memory works
- [ ] File tools work
- [ ] Custom slash commands work
- [ ] Debug mode shows commands
- [ ] Tab completion works
- [ ] Streaming works (simulated)
- [ ] Speed is noticeably faster than API calls

**Start with the basic commands, then work your way up to the tool integration examples!** 🎉