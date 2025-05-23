import sys
from pathlib import Path

HOOK_FILENAME = "post-commit"
HOOK_TEMPLATE = """#!/bin/sh
# This is a post-commit hook generated by penify.
# Automatically generates documentation for changed files after each commit.

penify docgen -gf {git_folder_path} -t {token}
"""

def install_git_hook(location, token):
    """Install a post-commit Git hook that generates documentation for changed files."""
    hooks_dir = Path(location) / ".git/hooks"
    hook_path = hooks_dir / HOOK_FILENAME
    
    if not hooks_dir.exists():
        print(f"Error: The hooks directory {hooks_dir} does not exist.")
        sys.exit(1)
    
    hook_content = HOOK_TEMPLATE.format(token=token, git_folder_path=location)
    hook_path.write_text(hook_content)
    hook_path.chmod(0o755)  # Make the hook script executable

    print(f"Post-commit hook installed in {hook_path}")
    print(f"Documentation will now be automatically generated after each commit.")

def uninstall_git_hook(location):
    """Uninstalls the post-commit hook from the specified location."""
    hook_path = Path(location) / ".git/hooks" / HOOK_FILENAME
    
    if hook_path.exists():
        hook_path.unlink()
        print(f"Post-commit hook uninstalled from {hook_path}")
    else:
        print(f"No post-commit hook found in {hook_path}")
