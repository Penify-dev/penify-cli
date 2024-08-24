import sys
import os
import argparse
from pathlib import Path

from .commit_analyzer import CommitDocGenHook

from .folder_analyzer import FolderAnalyzerGenHook
from .file_analyzer import FileAnalyzerGenHook
from .api_client import APIClient
from .git_analyzer import GitDocGenHook

HOOK_FILENAME = "post-commit"
HOOK_TEMPLATE = """#!/bin/sh
# This is a post-commit hook generated by penify-cli.

penify-cli -t {token} -gf {git_folder_path}
"""
api_url = 'https://production-gateway.snorkell.ai/api'

def install_git_hook(location, token):
    hooks_dir = Path(location) / ".git/hooks"
    hook_path = hooks_dir / HOOK_FILENAME
    
    if not hooks_dir.exists():
        print(f"Error: The hooks directory {hooks_dir} does not exist.")
        sys.exit(1)
    
    hook_content = HOOK_TEMPLATE.format(token=token, git_folder_path=location)
    hook_path.write_text(hook_content)
    hook_path.chmod(0o755)  # Make the hook script executable

    print(f"Post-commit hook installed in {hook_path}")

def uninstall_git_hook(location):
    hook_path = Path(location) / ".git/hooks" / HOOK_FILENAME
    
    if hook_path.exists():
        hook_path.unlink()
        print(f"Post-commit hook uninstalled from {hook_path}")
    else:
        print(f"No post-commit hook found in {hook_path}")

def generate_doc(token, file_path=None, complete_folder_path=None, git_folder_path=None):
    
    api_client = APIClient(api_url, token)

    if file_path:
        try:
            analyzer = FileAnalyzerGenHook(file_path, api_client)
            analyzer.run()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    elif complete_folder_path:
        try:
            analyzer = FolderAnalyzerGenHook(complete_folder_path, api_client)
            analyzer.run()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    else:
        try:
            analyzer = GitDocGenHook(git_folder_path, api_client)
            analyzer.run()
        except Exception as e:
            print(f"Error: {e}")
            sys.exit(1)
    
def commit_code(gf_path: str, token: str, message: str, open_terminal: bool):
    # Implement the logic to perform a commit with a message
    api_client = APIClient(api_url, token)
    try:
        analyzer = CommitDocGenHook(gf_path, api_client)
        analyzer.run(message, open_terminal)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
    # You can add actual Git commit logic here using subprocess or GitPython, etc.

def main():
    parser = argparse.ArgumentParser(description="Penify CLI tool for managing Git hooks and generating documentation.")
    
    subparsers = parser.add_subparsers(title="subcommands", dest="subcommand")

    # Subcommand: install-hook
    install_parser = subparsers.add_parser("install-hook", help="Install the Git post-commit hook.")
    install_parser.add_argument("-l", "--location", required=True, help="Location in which to install the Git hook.")
    install_parser.add_argument("-t", "--token", help="API token for authentication. If not provided, the environment variable 'PENIFY_API_TOKEN' will be used.", default=os.getenv('PENIFY_API_TOKEN'))

    # Subcommand: uninstall-hook
    uninstall_parser = subparsers.add_parser("uninstall-hook", help="Uninstall the Git post-commit hook.")
    uninstall_parser.add_argument("-l", "--location", required=True, help="Location from which to uninstall the Git hook.")

    # Subcommand: doc-gen
    doc_gen_parser = subparsers.add_parser("doc-gen", help="Generate documentation for specified files or folders.")
    doc_gen_parser.add_argument("-t", "--token", help="API token for authentication. If not provided, the environment variable 'PENIFY_API_TOKEN' will be used.", default=os.getenv('PENIFY_API_TOKEN'))
    doc_gen_parser.add_argument("-fl", "--file_path", help="Path of the file to generate documentation.")
    doc_gen_parser.add_argument("-cf", "--complete_folder_path", help="Generate documentation for the entire folder.")
    doc_gen_parser.add_argument("-gf", "--git_folder_path", help="Path to the folder, with git, to scan for modified files. Defaults to the current folder.", default=os.getcwd())

    # Subcommand: commit
    commit_parser = subparsers.add_parser("commit", help="Commit with a message.")
    commit_parser.add_argument("-gf", "--git_folder_path", help="Path to the folder, with git, to scan for modified files. Defaults to the current folder.", default=os.getcwd())
    commit_parser.add_argument("-t", "--token", help="API token for authentication. If not provided, the environment variable 'PENIFY_API_TOKEN' will be used.", default=os.getenv('PENIFY_API_TOKEN'))
    commit_parser.add_argument("-m", "--message", required=False, help="Commit message.", default="N/A")
    commit_parser.add_argument("-e", "--terminal", required=False, help="Open edit terminal", default="False")

    args = parser.parse_args()

    if args.subcommand == "install-hook":
        install_git_hook(args.location, args.token)
    elif args.subcommand == "uninstall-hook":
        uninstall_git_hook(args.location)
    elif args.subcommand == "doc-gen":
        generate_doc(args.token, args.file_path, args.complete_folder_path, args.git_folder_path)
    elif args.subcommand == "commit":
        open_terminal = args.terminal.lower() == "true"
        commit_code(args.git_folder_path, args.token, args.message, open_terminal)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
