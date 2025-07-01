import typer
from typing import Optional
import llm
import questionary
from questionary import Style
from dotenv import load_dotenv
from pathlib import Path
from rich import print
from rich.console import Console
from rich.spinner import Spinner
from rich.live import Live
import difflib
import threading


load_dotenv(".env")

class FileTools(llm.Toolbox):
    """File operations toolbox."""
    
    def __init__(self, working_directory: str = "."):
        self.working_directory = Path(working_directory).resolve()
        
    def _resolve_path(self, file_path: str) -> Path:
        if Path(file_path).is_absolute():
            return Path(file_path).resolve()
        return (self.working_directory / file_path).resolve()
    
    def list_files(self, directory: Optional[str] = None) -> str:
        """List files and directories."""
        print(f"[cyan]🔧 Listing files in {directory or 'current directory'}...[/cyan]")
        print()
        target_dir = self._resolve_path(directory) if directory else self.working_directory
        
        items = []
        for item in sorted(target_dir.iterdir()):
            if item.is_dir():
                items.append(f"{item.name}/ [DIR]")
            else:
                items.append(f"{item.name} ({item.stat().st_size} bytes)")
                
        return f"Files in {target_dir}:\n" + "\n".join(items) if items else "No files found"
    
    def read_file(self, file_path: str) -> str:
        """Read content from a file."""
        print(f"[cyan]🔧 Reading file: {file_path}[/cyan]")
        print()
        full_path = self._resolve_path(file_path)
        content = full_path.read_text(encoding='utf-8', errors='replace')
        
        if len(content) > 50_000:
            content = content[:50_000] + "\n... (truncated)"
            
        return content
    
    def write_file(self, file_path: str, content: str) -> str:
        """Write content to a file."""
        print(f"[cyan]🔧 Writing {len(content):,} characters to: {file_path}[/cyan]")
        print()
        full_path = self._resolve_path(file_path)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        full_path.write_text(content, encoding='utf-8')
        
        return f"Wrote {len(content):,} characters to '{file_path}'"
    
    def replace_in_file(self, file_path: str, old_string: str, new_string: str) -> str:
        """Replace string in file and show diff."""
        print(f"[cyan]🔧 Replacing text in: {file_path}[/cyan]")
        print()
        full_path = self._resolve_path(file_path)
        original_content = full_path.read_text(encoding='utf-8')
        new_content = original_content.replace(old_string, new_string)
        
        diff_lines = list(difflib.unified_diff(
            original_content.splitlines(keepends=True),
            new_content.splitlines(keepends=True),
            fromfile=f"{file_path} (before)",
            tofile=f"{file_path} (after)",
            n=3
        ))
        
        full_path.write_text(new_content, encoding='utf-8')
        diff_output = "".join(diff_lines)
        
        return f"Replaced in '{file_path}':\n{diff_output}" if diff_output else f"No changes made to '{file_path}'"


custom_style_fancy = Style([
    ('qmark', 'fg:#673ab7 bold'),       # token in front of the question
    ('question', 'bold'),               # question text
    ('answer', 'fg:#154a57'),      # submitted answer text behind the question
    ('pointer', 'fg:#673ab7 bold'),     # pointer used in select and checkbox prompts
    ('highlighted', 'fg:#673ab7 bold'), # pointed-at choice in select and checkbox prompts
    ('selected', 'fg:#154a57'),         # style for a selected item of a checkbox
    ('separator', 'fg:#154a57'),        # separator in lists
    ('instruction', ''),                # user instructions for select, rawselect, checkbox
    ('text', ''),                       # plain text
    ('disabled', 'fg:#858585 italic')   # disabled choices for select and checkbox prompts
])

console = Console()
model = llm.get_model("claude-4-sonnet")

conversation = model.conversation(tools=[FileTools()])
resp = conversation.prompt("You are a coding assistant that can make edits to a single file. In particular you will make edits to a marimo notebook.")
resp.text()

while True:
    out = questionary.text("", qmark=">", style=custom_style_fancy).ask()
    if out == "quit":
        break
    # Show spinner while getting initial response
    spinner = Spinner("dots", text="[dim]Thinking...[/dim]")
    response_started = False
    
    with Live(spinner, console=console, refresh_per_second=10) as live:
        for chunk in conversation.chain(out):
            if not response_started:
                # First chunk received, stop the spinner
                live.stop()
                response_started = True
            print(chunk, end="", flush=True)
    print()
