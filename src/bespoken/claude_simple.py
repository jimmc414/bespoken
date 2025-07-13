"""
Minimal wrapper to make 'claude -p' work as a drop-in replacement for llm.
Simple, fast, and actually works.
"""

import subprocess
import json
import re
import time
from typing import Optional, List, Dict, Any, Iterator
from dataclasses import dataclass


@dataclass 
class Message:
    """Simple message for conversation history."""
    role: str
    content: str


class ClaudeModel:
    """Minimal wrapper around claude CLI that looks like an llm model."""
    
    def __init__(self, model_name: str = "claude"):
        self.model_name = model_name
        # Check claude is available
        try:
            subprocess.run(["claude", "--version"], capture_output=True, check=True, timeout=2)
        except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
            raise RuntimeError(
                "Claude Code CLI not found. Install with:\n"
                "npm install -g @anthropic/claude-code"
            )
    
    def conversation(self, system: Optional[str] = None, tools: Optional[List] = None):
        """Create a conversation (llm compatible interface)."""
        return ClaudeConversation(system, tools)


class ClaudeConversation:
    """Handles a conversation with Claude."""
    
    def __init__(self, system: Optional[str] = None, tools: Optional[List] = None):
        self.system = system
        self.tools = tools or []
        self.messages: List[Message] = []
    
    def _run_claude(self, prompt: str) -> str:
        """Run claude -p and get response."""
        cmd = ["claude", "-p", prompt]
        
        if self.system:
            cmd.extend(["--system-prompt", self.system])
        
        # Add conversation context if we have history
        if self.messages:
            # Include recent context
            context_messages = self.messages[-6:]  # Last 3 exchanges
            context = "\n\n".join([
                f"{msg.role.upper()}: {msg.content}" 
                for msg in context_messages
            ])
            full_prompt = f"{context}\n\nUSER: {prompt}"
            cmd[2] = full_prompt
        
        # Debug output if enabled
        try:
            from . import config
            if getattr(config, 'DEBUG_MODE', False):
                # Show the actual command being executed
                cmd_str = ' '.join(f'"{arg}"' if ' ' in arg else arg for arg in cmd)
                print(f">>> Executing: {cmd_str}")
        except ImportError:
            pass
        
        # Run claude
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=60,
                check=True
            )
            return result.stdout.strip()
            
        except subprocess.CalledProcessError as e:
            # Return error as response rather than crashing
            return f"Error: {e.stderr.strip() if e.stderr else 'Command failed'}"
        except subprocess.TimeoutExpired:
            return "Error: Request timed out after 60 seconds"
        except Exception as e:
            return f"Error: {str(e)}"
    
    def chain(self, prompt: str, **kwargs) -> 'ClaudeResponse':
        """Send prompt and get response (non-streaming)."""
        # Record user message
        self.messages.append(Message("user", prompt))
        
        # Get response
        response_text = self._run_claude(prompt)
        
        # Record assistant response
        self.messages.append(Message("assistant", response_text))
        
        # Create response object that can handle tools
        return ClaudeResponse(response_text, self.tools)
    
    def stream(self, prompt: str, **kwargs) -> Iterator['StreamChunk']:
        """Stream response. Claude CLI doesn't support streaming, so simulate it."""
        # Record user message
        self.messages.append(Message("user", prompt))
        
        # Get the full response first
        response_text = self._run_claude(prompt)
        
        # Record assistant response
        self.messages.append(Message("assistant", response_text))
        
        # Simulate streaming by yielding chunks with small delays
        words = response_text.split()
        
        for i, word in enumerate(words):
            # Yield word with space (except for last word)
            word_with_space = word + (" " if i < len(words) - 1 else "")
            yield StreamChunk(word_with_space)
            time.sleep(0.02)  # Small delay for streaming effect


class ClaudeResponse:
    """Response object that handles tool execution."""
    
    def __init__(self, text: str, tools: Optional[List] = None):
        self._text = text
        self.tools = tools or []
        self.usage = {"input_tokens": 0, "output_tokens": len(text.split())}
        
        # Execute tools if found
        if self.tools:
            self._execute_tools()
    
    def text(self) -> str:
        """Get response text."""
        return self._text
    
    def _execute_tools(self):
        """Parse response for tool calls and execute them."""
        # Look for function call patterns
        # Patterns: function_name("arg") or function_name('arg') or function_name(arg1, arg2)
        pattern = r'\b(\w+)\s*\(\s*([^)]*)\s*\)'
        
        for match in re.finditer(pattern, self._text):
            func_name = match.group(1)
            args_str = match.group(2)
            
            # Check if this function exists in our tools
            for tool in self.tools:
                if hasattr(tool, func_name):
                    try:
                        # Parse arguments
                        args = self._parse_args(args_str)
                        
                        # Get the method
                        method = getattr(tool, func_name)
                        
                        # Execute based on argument count
                        if not args:
                            result = method()
                        elif len(args) == 1:
                            result = method(args[0])
                        elif len(args) == 2:
                            result = method(args[0], args[1])
                        elif len(args) == 3:
                            result = method(args[0], args[1], args[2])
                        else:
                            result = method(*args)
                        
                        # Tool executed successfully
                        # In a more complete implementation, we might want to
                        # feed results back to Claude
                        
                    except Exception as e:
                        # Tool execution failed, but don't crash
                        print(f"Tool execution error: {e}")
    
    def _parse_args(self, args_str: str) -> List[str]:
        """Simple argument parser."""
        if not args_str.strip():
            return []
        
        # Handle quoted strings
        args = []
        current = ""
        in_quotes = False
        quote_char = None
        
        for char in args_str:
            if char in ['"', "'"] and not in_quotes:
                in_quotes = True
                quote_char = char
            elif char == quote_char and in_quotes:
                in_quotes = False
                quote_char = None
            elif char == ',' and not in_quotes:
                args.append(current.strip())
                current = ""
            else:
                current += char
        
        if current.strip():
            args.append(current.strip())
        
        # Remove quotes from arguments
        return [arg.strip('"\'') for arg in args]


@dataclass
class StreamChunk:
    """Chunk for streaming responses."""
    text: str
    type: str = "text"


# Make it work as a drop-in replacement
def get_model(model_name: str) -> ClaudeModel:
    """Get a model by name (llm compatible)."""
    if "claude" in model_name.lower():
        return ClaudeModel(model_name)
    else:
        # Try to fall back to real llm
        try:
            import llm
            return llm.get_model(model_name)
        except ImportError:
            raise ValueError(f"Model '{model_name}' requires llm library")