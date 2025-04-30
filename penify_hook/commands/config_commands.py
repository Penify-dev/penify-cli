import json
import os
import random
import webbrowser
import http.server
import socketserver
import pkg_resources
from pathlib import Path
from threading import Thread
import logging
import sys
from typing import Dict, Any, Optional, Union

# Try to import dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False


def load_env_files() -> None:
    """
    Load environment variables from .env files in various locations,
    with proper priority (later files override earlier ones):
    1. User home directory .env (lowest priority)
    2. Git repo root directory .env (if in a git repo)
    3. Current directory .env (highest priority)
    
    This function is called when the module is imported, ensuring env variables
    are available throughout the application lifecycle.
    """
    if not DOTENV_AVAILABLE:
        logging.warning("python-dotenv is not installed. .env file loading is disabled.")
        logging.warning("Run 'pip install python-dotenv' to enable .env file support.")
        return

    # Load from user home directory (lowest priority)
    try:
        home_env = Path.home() / '.env'
        if home_env.exists():
            load_dotenv(dotenv_path=home_env, override=False)
    except Exception as e:
        logging.warning(f"Failed to load .env from home directory: {str(e)}")
    
    # Load from Git repo root (medium priority)
    try:
        from penify_hook.utils import recursive_search_git_folder
        current_dir = os.getcwd()
        repo_root = recursive_search_git_folder(current_dir)
        if repo_root and repo_root != str(Path.home()):
            repo_env = Path(repo_root) / '.env'
            if repo_env.exists() and repo_env != home_env:
                load_dotenv(dotenv_path=repo_env, override=True)
    except Exception as e:
        logging.warning(f"Failed to load .env from Git repo: {str(e)}")
    
    # Load from current directory (highest priority)
    current_env = Path(os.getcwd()) / '.env'
    if current_env.exists() and (not repo_root or current_env != Path(repo_root) / '.env'):
        load_dotenv(dotenv_path=current_env, override=True)


# Load environment variables when module is imported
load_env_files()


def get_penify_config() -> Path:
    """
    Get the home directory for the .penify configuration file.
    This function searches for the .penify file in the current directory
    and its parent directories until it finds it or reaches the home directory.
    """
    current_dir = os.getcwd()
    from penify_hook.utils import recursive_search_git_folder
    home_dir = recursive_search_git_folder(current_dir)
    

    if not home_dir:
        home_dir = Path.home()
    else:
        home_dir = Path(home_dir)

    penify_dir = home_dir / '.penify'
    if penify_dir.exists():
        return penify_dir / 'config.json'
    else:
        # Create the .penify directory if it doesn't exist
        os.makedirs(penify_dir, exist_ok=True)
        ## update gitignore
        
        # Create the .penify directory
        os.makedirs(penify_dir, exist_ok=True)        
        # Create an empty config.json file
        with open(penify_dir / 'config.json', 'w') as f:
            json.dump({}, f)
    return penify_dir / 'config.json'


def get_env_var_or_default(env_var: str, default: Any = None) -> Any:
    """
    Get environment variable or return default value.
    
    Args:
        env_var: The environment variable name
        default: Default value if environment variable is not set
        
    Returns:
        Value of the environment variable or default
    """
    return os.environ.get(env_var, default)


def save_llm_config(model, api_base, api_key):
    """
    Save LLM configuration settings to .env file.
    
    This function saves LLM configuration in the following priority:
    1. Git repo root .env (if inside a git repo)
    2. User home directory .env
    """
    from pathlib import Path
    import os
    
    if not DOTENV_AVAILABLE:
        print("python-dotenv is not installed. Run 'pip install python-dotenv' to enable .env file support.")
        return False
    
    # Try to find Git repo root
    try:
        from penify_hook.utils import recursive_search_git_folder
        current_dir = os.getcwd()
        repo_root = recursive_search_git_folder(current_dir)
        env_file = Path(repo_root) / '.env' if repo_root else Path.home() / '.env'
    except Exception as e:
        print(f"Failed to determine Git repo root: {str(e)}")
        env_file = Path.home() / '.env'
    
    # Read existing .env content
    env_content = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_content[key.strip()] = value.strip()
    
    # Update LLM configuration
    env_content['PENIFY_LLM_MODEL'] = model
    env_content['PENIFY_LLM_API_BASE'] = api_base
    env_content['PENIFY_LLM_API_KEY'] = api_key
    
    # Write back to .env file
    try:
        with open(env_file, 'w') as f:
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")
        print(f"LLM configuration saved to {env_file}")
        
        # Reload environment variables to make changes immediately available
        if DOTENV_AVAILABLE:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=env_file, override=True)
            
        return True
    except Exception as e:
        print(f"Error saving LLM configuration: {str(e)}")
        return False


def save_jira_config(url, username, api_token):
    """
    Save JIRA configuration settings to .env file.
    
    This function saves JIRA configuration in the following priority:
    1. Git repo root .env (if inside a git repo)
    2. User home directory .env
    """
    from pathlib import Path
    import os
    
    if not DOTENV_AVAILABLE:
        print("python-dotenv is not installed. Run 'pip install python-dotenv' to enable .env file support.")
        return False
    
    # Try to find Git repo root
    try:
        from penify_hook.utils import recursive_search_git_folder
        current_dir = os.getcwd()
        repo_root = recursive_search_git_folder(current_dir)
        env_file = Path(repo_root) / '.env' if repo_root else Path.home() / '.env'
    except Exception as e:
        print(f"Failed to determine Git repo root: {str(e)}")
        env_file = Path.home() / '.env'
    
    # Read existing .env content
    env_content = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_content[key.strip()] = value.strip()
    
    # Update JIRA configuration
    env_content['PENIFY_JIRA_URL'] = url
    env_content['PENIFY_JIRA_USER'] = username
    env_content['PENIFY_JIRA_TOKEN'] = api_token
    
    # Write back to .env file
    try:
        with open(env_file, 'w') as f:
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")
        print(f"JIRA configuration saved to {env_file}")
        
        # Reload environment variables to make changes immediately available
        if DOTENV_AVAILABLE:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=env_file, override=True)
            
        return True
    except Exception as e:
        print(f"Error saving JIRA configuration: {str(e)}")
        return False


def save_azdo_config(url, project, pat_token):
    """
    Save Azure DevOps configuration settings to .env file.
    
    This function saves Azure DevOps configuration in the following priority:
    1. Git repo root .env (if inside a git repo)
    2. User home directory .env
    """
    from pathlib import Path
    import os
    
    if not DOTENV_AVAILABLE:
        print("python-dotenv is not installed. Run 'pip install python-dotenv' to enable .env file support.")
        return False
    
    # Try to find Git repo root
    try:
        from penify_hook.utils import recursive_search_git_folder
        current_dir = os.getcwd()
        repo_root = recursive_search_git_folder(current_dir)
        env_file = Path(repo_root) / '.env' if repo_root else Path.home() / '.env'
    except Exception as e:
        print(f"Failed to determine Git repo root: {str(e)}")
        env_file = Path.home() / '.env'
    
    # Read existing .env content
    env_content = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_content[key.strip()] = value.strip()
    
    # Update Azure DevOps configuration
    env_content['PENIFY_AZDO_URL'] = url
    env_content['PENIFY_AZDO_PROJECT'] = project
    env_content['PENIFY_AZDO_PAT_TOKEN'] = pat_token
    
    # Write back to .env file
    try:
        with open(env_file, 'w') as f:
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")
        print(f"Azure DevOps configuration saved to {env_file}")
        
        # Reload environment variables to make changes immediately available
        if DOTENV_AVAILABLE:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=env_file, override=True)
            
        return True
    except Exception as e:
        print(f"Error saving Azure DevOps configuration: {str(e)}")
        return False


def save_asana_config(token, workspace, project=None):
    """
    Save Asana configuration settings to .env file.
    
    This function saves Asana configuration in the following priority:
    1. Git repo root .env (if inside a git repo)
    2. User home directory .env
    """
    from pathlib import Path
    import os
    
    if not DOTENV_AVAILABLE:
        print("python-dotenv is not installed. Run 'pip install python-dotenv' to enable .env file support.")
        return False
    
    # Try to find Git repo root
    try:
        from penify_hook.utils import recursive_search_git_folder
        current_dir = os.getcwd()
        repo_root = recursive_search_git_folder(current_dir)
        env_file = Path(repo_root) / '.env' if repo_root else Path.home() / '.env'
    except Exception as e:
        print(f"Failed to determine Git repo root: {str(e)}")
        env_file = Path.home() / '.env'
    
    # Read existing .env content
    env_content = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_content[key.strip()] = value.strip()
    
    # Update Asana configuration
    env_content['PENIFY_ASANA_TOKEN'] = token
    env_content['PENIFY_ASANA_WORKSPACE'] = workspace
    if project:
        env_content['PENIFY_ASANA_PROJECT'] = project
    
    # Write back to .env file
    try:
        with open(env_file, 'w') as f:
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")
        print(f"Asana configuration saved to {env_file}")
        
        # Reload environment variables to make changes immediately available
        if DOTENV_AVAILABLE:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=env_file, override=True)
            
        return True
    except Exception as e:
        print(f"Error saving Asana configuration: {str(e)}")
        return False


def save_github_config(token, owner=None, repo=None):
    """
    Save GitHub configuration settings to .env file.
    
    This function saves GitHub configuration in the following priority:
    1. Git repo root .env (if inside a git repo)
    2. User home directory .env
    """
    from pathlib import Path
    import os
    
    if not DOTENV_AVAILABLE:
        print("python-dotenv is not installed. Run 'pip install python-dotenv' to enable .env file support.")
        return False
    
    # Try to find Git repo root
    try:
        from penify_hook.utils import recursive_search_git_folder
        current_dir = os.getcwd()
        repo_root = recursive_search_git_folder(current_dir)
        env_file = Path(repo_root) / '.env' if repo_root else Path.home() / '.env'
    except Exception as e:
        print(f"Failed to determine Git repo root: {str(e)}")
        env_file = Path.home() / '.env'
    
    # Read existing .env content
    env_content = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_content[key.strip()] = value.strip()
    
    # Update GitHub configuration
    env_content['PENIFY_GITHUB_TOKEN'] = token
    if owner:
        env_content['PENIFY_GITHUB_OWNER'] = owner
    if repo:
        env_content['PENIFY_GITHUB_REPO'] = repo
    
    # Write back to .env file
    try:
        with open(env_file, 'w') as f:
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")
        print(f"GitHub configuration saved to {env_file}")
        
        # Reload environment variables to make changes immediately available
        if DOTENV_AVAILABLE:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=env_file, override=True)
            
        return True
    except Exception as e:
        print(f"Error saving GitHub configuration: {str(e)}")
        return False


def save_kanban_config(tool, board_id, columns=None):
    """
    Save Kanban board configuration settings to .env file.
    
    This function saves Kanban board configuration in the following priority:
    1. Git repo root .env (if inside a git repo)
    2. User home directory .env
    """
    from pathlib import Path
    import os
    
    if not DOTENV_AVAILABLE:
        print("python-dotenv is not installed. Run 'pip install python-dotenv' to enable .env file support.")
        return False
    
    # Try to find Git repo root
    try:
        from penify_hook.utils import recursive_search_git_folder
        current_dir = os.getcwd()
        repo_root = recursive_search_git_folder(current_dir)
        env_file = Path(repo_root) / '.env' if repo_root else Path.home() / '.env'
    except Exception as e:
        print(f"Failed to determine Git repo root: {str(e)}")
        env_file = Path.home() / '.env'
    
    # Read existing .env content
    env_content = {}
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_content[key.strip()] = value.strip()
    
    # Update Kanban configuration
    env_content['PENIFY_KANBAN_TOOL'] = tool
    env_content['PENIFY_KANBAN_BOARD_ID'] = board_id
    if columns:
        env_content['PENIFY_KANBAN_COLUMNS'] = columns
    
    # Write back to .env file
    try:
        with open(env_file, 'w') as f:
            for key, value in env_content.items():
                f.write(f"{key}={value}\n")
        print(f"Kanban configuration saved to {env_file}")
        
        # Reload environment variables to make changes immediately available
        if DOTENV_AVAILABLE:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=env_file, override=True)
            
        return True
    except Exception as e:
        print(f"Error saving Kanban configuration: {str(e)}")
        return False


def get_llm_config() -> Dict[str, str]:
    """
    Get LLM configuration from environment variables.
    
    Environment variables:
    - PENIFY_LLM_MODEL: Model name
    - PENIFY_LLM_API_BASE: API base URL
    - PENIFY_LLM_API_KEY: API key
    
    Returns:
        dict: Configuration dictionary with model, api_base, and api_key
    """
    # Ensure environment variables are loaded
    if DOTENV_AVAILABLE:
        load_env_files()
    
    # Get values from environment variables
    config = {
        'model': get_env_var_or_default('PENIFY_LLM_MODEL', ''),
        'api_base': get_env_var_or_default('PENIFY_LLM_API_BASE', ''),
        'api_key': get_env_var_or_default('PENIFY_LLM_API_KEY', '')
    }
    
    # Remove empty values
    config = {k: v for k, v in config.items() if v}
    
    return config


def get_jira_config() -> Dict[str, str]:
    """
    Get JIRA configuration from environment variables.
    
    Environment variables:
    - PENIFY_JIRA_URL: JIRA URL
    - PENIFY_JIRA_USER: JIRA username
    - PENIFY_JIRA_TOKEN: JIRA API token
    
    Returns:
        dict: Configuration dictionary with url, username, and api_token
    """
    # Ensure environment variables are loaded
    if DOTENV_AVAILABLE:
        load_env_files()
    
    # Get values from environment variables
    config = {
        'url': get_env_var_or_default('PENIFY_JIRA_URL', ''),
        'username': get_env_var_or_default('PENIFY_JIRA_USER', ''),
        'api_token': get_env_var_or_default('PENIFY_JIRA_TOKEN', '')
    }
    
    # Remove empty values
    config = {k: v for k, v in config.items() if v}
    
    return config


def get_azdo_config() -> Dict[str, str]:
    """
    Get Azure DevOps configuration from environment variables.
    
    Environment variables:
    - PENIFY_AZDO_URL: Azure DevOps URL
    - PENIFY_AZDO_PROJECT: Azure DevOps project name
    - PENIFY_AZDO_PAT_TOKEN: Azure DevOps Personal Access Token
    
    Returns:
        dict: Configuration dictionary with url, project, and pat_token
    """
    # Ensure environment variables are loaded
    if DOTENV_AVAILABLE:
        load_env_files()
    
    # Get values from environment variables
    config = {
        'url': get_env_var_or_default('PENIFY_AZDO_URL', ''),
        'project': get_env_var_or_default('PENIFY_AZDO_PROJECT', ''),
        'pat_token': get_env_var_or_default('PENIFY_AZDO_PAT_TOKEN', '')
    }
    
    # Remove empty values
    config = {k: v for k, v in config.items() if v}
    
    return config


def get_asana_config() -> Dict[str, str]:
    """
    Get Asana configuration from environment variables.
    
    Environment variables:
    - PENIFY_ASANA_TOKEN: Asana Personal Access Token
    - PENIFY_ASANA_WORKSPACE: Asana workspace name or ID
    - PENIFY_ASANA_PROJECT: Asana project name or ID (optional)
    
    Returns:
        dict: Configuration dictionary with token, workspace, and project
    """
    # Ensure environment variables are loaded
    if DOTENV_AVAILABLE:
        load_env_files()
    
    # Get values from environment variables
    config = {
        'token': get_env_var_or_default('PENIFY_ASANA_TOKEN', ''),
        'workspace': get_env_var_or_default('PENIFY_ASANA_WORKSPACE', ''),
        'project': get_env_var_or_default('PENIFY_ASANA_PROJECT', '')
    }
    
    # Remove empty values
    config = {k: v for k, v in config.items() if v}
    
    return config


def get_github_config() -> Dict[str, str]:
    """
    Get GitHub configuration from environment variables.
    
    Environment variables:
    - PENIFY_GITHUB_TOKEN: GitHub Personal Access Token
    - PENIFY_GITHUB_OWNER: GitHub repository owner (optional)
    - PENIFY_GITHUB_REPO: GitHub repository name (optional)
    
    Returns:
        dict: Configuration dictionary with token, owner, and repo
    """
    # Ensure environment variables are loaded
    if DOTENV_AVAILABLE:
        load_env_files()
    
    # Get values from environment variables
    config = {
        'token': get_env_var_or_default('PENIFY_GITHUB_TOKEN', ''),
        'owner': get_env_var_or_default('PENIFY_GITHUB_OWNER', ''),
        'repo': get_env_var_or_default('PENIFY_GITHUB_REPO', '')
    }
    
    # Remove empty values
    config = {k: v for k, v in config.items() if v}
    
    return config


def get_kanban_config() -> Dict[str, str]:
    """
    Get Kanban board configuration from environment variables.
    
    Environment variables:
    - PENIFY_KANBAN_TOOL: Kanban tool name (jira, azdo, trello, github, asana)
    - PENIFY_KANBAN_BOARD_ID: ID or name of the Kanban board
    - PENIFY_KANBAN_COLUMNS: Comma-separated list of column names (optional)
    
    Returns:
        dict: Configuration dictionary with tool, board_id, and columns
    """
    # Ensure environment variables are loaded
    if DOTENV_AVAILABLE:
        load_env_files()
    
    # Get values from environment variables
    config = {
        'tool': get_env_var_or_default('PENIFY_KANBAN_TOOL', ''),
        'board_id': get_env_var_or_default('PENIFY_KANBAN_BOARD_ID', ''),
        'columns': get_env_var_or_default('PENIFY_KANBAN_COLUMNS', '')
    }
    
    # Remove empty values
    config = {k: v for k, v in config.items() if v}
    
    return config


def config_llm_web():
    """
    Open a web browser interface for configuring LLM settings.
    """
    redirect_port = random.randint(30000, 50000)
    server_url = f"http://localhost:{redirect_port}"
    
    print(f"Starting configuration server on {server_url}")
    
    class ConfigHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                # Read the template HTML file
                template_path = pkg_resources.resource_filename(
                    "penify_hook", "templates/llm_config.html"
                )
                
                with open(template_path, 'r') as f:
                    content = f.read()
                
                self.wfile.write(content.encode())
            elif self.path == "/get_config":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                # Get current LLM configuration
                current_config = get_llm_config()
                
                if current_config:
                    response = {
                        "success": True,
                        "config": current_config
                    }
                else:
                    response = {
                        "success": False,
                        "message": "No configuration found"
                    }
                
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Not Found")

        def do_POST(self):
            if self.path == "/save":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())
                
                model = data.get('model')
                api_base = data.get('api_base')
                api_key = data.get('api_key')
                
                try:
                    save_llm_config(model, api_base, api_key)
                    
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {
                        "success": True, 
                        "message": f"LLM configuration saved successfully. Using model: {model}"
                    }
                    self.wfile.write(json.dumps(response).encode())
                    
                    # Schedule the server shutdown
                    thread = Thread(target=self.server.shutdown)
                    thread.daemon = True
                    thread.start()
                    
                except Exception as e:
                    self.send_response(500)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {"success": False, "message": f"Error saving configuration: {str(e)}"}
                    self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "Not Found"}).encode())
        
        def log_message(self, format, *args):
            # Suppress log messages
            return

    with socketserver.TCPServer(("", redirect_port), ConfigHandler) as httpd:
        print(f"Opening configuration page in your browser...")
        webbrowser.open(server_url)
        print(f"Waiting for configuration to be submitted...")
        httpd.serve_forever()
    
    print("Configuration completed.")


def config_jira_web():
    """
    Open a web browser interface for configuring JIRA settings.
    """
    redirect_port = random.randint(30000, 50000)
    server_url = f"http://localhost:{redirect_port}"
    
    print(f"Starting configuration server on {server_url}")
    
    class ConfigHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                # Read the template HTML file
                template_path = pkg_resources.resource_filename(
                    "penify_hook", "templates/jira_config.html"
                )
                
                with open(template_path, 'r') as f:
                    content = f.read()
                
                self.wfile.write(content.encode())
            elif self.path == "/get_config":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                # Get current JIRA configuration
                current_config = get_jira_config()
                
                if current_config:
                    response = {
                        "success": True,
                        "config": current_config
                    }
                else:
                    response = {
                        "success": False,
                        "message": "No JIRA configuration found"
                    }
                
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Not Found")

        def do_POST(self):
            if self.path == "/save":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())
                
                url = data.get('url')
                username = data.get('username')
                api_token = data.get('api_token')
                verify = data.get('verify', False)
                
                try:
                    # Save the configuration
                    save_jira_config(url, username, api_token)
                    
                    # Verify connection option is handled in main.py
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {
                        "success": True, 
                        "message": f"JIRA configuration saved successfully."
                    }
                    self.wfile.write(json.dumps(response).encode())
                    
                    # Schedule the server shutdown
                    thread = Thread(target=self.server.shutdown)
                    thread.daemon = True
                    thread.start()
                    
                except Exception as e:
                    self.send_response(500)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {"success": False, "message": f"Error saving configuration: {str(e)}"}
                    self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "Not Found"}).encode())
        
        def log_message(self, format, *args):
            # Suppress log messages
            return

    with socketserver.TCPServer(("", redirect_port), ConfigHandler) as httpd:
        print(f"Opening configuration page in your browser...")
        webbrowser.open(server_url)
        print(f"Waiting for configuration to be submitted...")
        httpd.serve_forever()
    
    print("Configuration completed.")


def config_azdo_web():
    """
    Open a web browser interface for configuring Azure DevOps settings.
    """
    redirect_port = random.randint(30000, 50000)
    server_url = f"http://localhost:{redirect_port}"
    
    print(f"Starting configuration server on {server_url}")
    
    class ConfigHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                # Read the template HTML file
                template_path = pkg_resources.resource_filename(
                    "penify_hook", "templates/azdo_config.html"
                )
                
                with open(template_path, 'r') as f:
                    content = f.read()
                
                self.wfile.write(content.encode())
            elif self.path == "/get_config":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                # Get current Azure DevOps configuration
                current_config = get_azdo_config()
                
                if current_config:
                    response = {
                        "success": True,
                        "config": current_config
                    }
                else:
                    response = {
                        "success": False,
                        "message": "No Azure DevOps configuration found"
                    }
                
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Not Found")

        def do_POST(self):
            if self.path == "/save":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())
                
                url = data.get('url')
                project = data.get('project')
                pat_token = data.get('pat_token')
                verify = data.get('verify', False)
                
                try:
                    # Save the configuration
                    save_azdo_config(url, project, pat_token)
                    
                    # Verify connection option is handled in main.py
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {
                        "success": True, 
                        "message": f"Azure DevOps configuration saved successfully."
                    }
                    self.wfile.write(json.dumps(response).encode())
                    
                    # Schedule the server shutdown
                    thread = Thread(target=self.server.shutdown)
                    thread.daemon = True
                    thread.start()
                    
                except Exception as e:
                    self.send_response(500)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {"success": False, "message": f"Error saving configuration: {str(e)}"}
                    self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "Not Found"}).encode())
        
        def log_message(self, format, *args):
            # Suppress log messages
            return

    with socketserver.TCPServer(("", redirect_port), ConfigHandler) as httpd:
        print(f"Opening configuration page in your browser...")
        webbrowser.open(server_url)
        print(f"Waiting for configuration to be submitted...")
        httpd.serve_forever()
    
    print("Configuration completed.")


def config_asana_web():
    """
    Open a web browser interface for configuring Asana settings.
    """
    redirect_port = random.randint(30000, 50000)
    server_url = f"http://localhost:{redirect_port}"
    
    print(f"Starting configuration server on {server_url}")
    
    class ConfigHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                # Read the template HTML file
                template_path = pkg_resources.resource_filename(
                    "penify_hook", "templates/asana_config.html"
                )
                
                with open(template_path, 'r') as f:
                    content = f.read()
                
                self.wfile.write(content.encode())
            elif self.path == "/get_config":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                # Get current Asana configuration
                current_config = get_asana_config()
                
                if current_config:
                    response = {
                        "success": True,
                        "config": current_config
                    }
                else:
                    response = {
                        "success": False,
                        "message": "No Asana configuration found"
                    }
                
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Not Found")

        def do_POST(self):
            if self.path == "/save":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())
                
                token = data.get('token')
                workspace = data.get('workspace')
                project = data.get('project')
                verify = data.get('verify', False)
                
                try:
                    # Save the configuration
                    save_asana_config(token, workspace, project)
                    
                    # Verify connection option is handled in main.py
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {
                        "success": True, 
                        "message": f"Asana configuration saved successfully."
                    }
                    self.wfile.write(json.dumps(response).encode())
                    
                    # Schedule the server shutdown
                    thread = Thread(target=self.server.shutdown)
                    thread.daemon = True
                    thread.start()
                    
                except Exception as e:
                    self.send_response(500)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {"success": False, "message": f"Error saving configuration: {str(e)}"}
                    self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "Not Found"}).encode())
        
        def log_message(self, format, *args):
            # Suppress log messages
            return

    with socketserver.TCPServer(("", redirect_port), ConfigHandler) as httpd:
        print(f"Opening configuration page in your browser...")
        webbrowser.open(server_url)
        print(f"Waiting for configuration to be submitted...")
        httpd.serve_forever()
    
    print("Configuration completed.")


def config_github_web():
    """
    Open a web browser interface for configuring GitHub settings.
    """
    redirect_port = random.randint(30000, 50000)
    server_url = f"http://localhost:{redirect_port}"
    
    print(f"Starting configuration server on {server_url}")
    
    class ConfigHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                # Read the template HTML file
                template_path = pkg_resources.resource_filename(
                    "penify_hook", "templates/github_config.html"
                )
                
                with open(template_path, 'r') as f:
                    content = f.read()
                
                self.wfile.write(content.encode())
            elif self.path == "/get_config":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                # Get current GitHub configuration
                current_config = get_github_config()
                
                if current_config:
                    response = {
                        "success": True,
                        "config": current_config
                    }
                else:
                    response = {
                        "success": False,
                        "message": "No GitHub configuration found"
                    }
                
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Not Found")

        def do_POST(self):
            if self.path == "/save":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())
                
                token = data.get('token')
                owner = data.get('owner')
                repo = data.get('repo')
                verify = data.get('verify', False)
                
                try:
                    # Save the configuration
                    save_github_config(token, owner, repo)
                    
                    # Verify connection option is handled in main.py
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {
                        "success": True, 
                        "message": f"GitHub configuration saved successfully."
                    }
                    self.wfile.write(json.dumps(response).encode())
                    
                    # Schedule the server shutdown
                    thread = Thread(target=self.server.shutdown)
                    thread.daemon = True
                    thread.start()
                    
                except Exception as e:
                    self.send_response(500)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {"success": False, "message": f"Error saving configuration: {str(e)}"}
                    self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "Not Found"}).encode())
        
        def log_message(self, format, *args):
            # Suppress log messages
            return

    with socketserver.TCPServer(("", redirect_port), ConfigHandler) as httpd:
        print(f"Opening configuration page in your browser...")
        webbrowser.open(server_url)
        print(f"Waiting for configuration to be submitted...")
        httpd.serve_forever()
    
    print("Configuration completed.")


def config_kanban_web():
    """
    Open a web browser interface for configuring Kanban board settings.
    """
    redirect_port = random.randint(30000, 50000)
    server_url = f"http://localhost:{redirect_port}"
    
    print(f"Starting configuration server on {server_url}")
    
    class ConfigHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                
                # Read the template HTML file
                template_path = pkg_resources.resource_filename(
                    "penify_hook", "templates/kanban_config.html"
                )
                
                with open(template_path, 'r') as f:
                    content = f.read()
                
                self.wfile.write(content.encode())
            elif self.path == "/get_config":
                self.send_response(200)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                
                # Get current Kanban configuration
                current_config = get_kanban_config()
                
                if current_config:
                    response = {
                        "success": True,
                        "config": current_config
                    }
                else:
                    response = {
                        "success": False,
                        "message": "No Kanban configuration found"
                    }
                
                self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/plain")
                self.end_headers()
                self.wfile.write(b"Not Found")

        def do_POST(self):
            if self.path == "/save":
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                data = json.loads(post_data.decode())
                
                tool = data.get('tool')
                board_id = data.get('board_id')
                columns = data.get('columns')
                
                try:
                    # Save the configuration
                    save_kanban_config(tool, board_id, columns)
                    
                    self.send_response(200)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {
                        "success": True, 
                        "message": f"Kanban configuration saved successfully."
                    }
                    self.wfile.write(json.dumps(response).encode())
                    
                    # Schedule the server shutdown
                    thread = Thread(target=self.server.shutdown)
                    thread.daemon = True
                    thread.start()
                    
                except Exception as e:
                    self.send_response(500)
                    self.send_header("Content-type", "application/json")
                    self.end_headers()
                    response = {"success": False, "message": f"Error saving configuration: {str(e)}"}
                    self.wfile.write(json.dumps(response).encode())
            else:
                self.send_response(404)
                self.send_header("Content-type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"success": False, "message": "Not Found"}).encode())
        
        def log_message(self, format, *args):
            # Suppress log messages
            return

    with socketserver.TCPServer(("", redirect_port), ConfigHandler) as httpd:
        print(f"Opening configuration page in your browser...")
        webbrowser.open(server_url)
        print(f"Waiting for configuration to be submitted...")
        httpd.serve_forever()
    
    print("Configuration completed.")


def get_token() -> Optional[str]:
    """
    Get the API token based on priority:
    1. Environment variable PENIFY_API_TOKEN from any .env file
    2. Config file 'api_keys' value
    
    Returns:
        str or None: API token if found, None otherwise
    """
    # Ensure environment variables are loaded from all .env files
    if DOTENV_AVAILABLE:
        load_env_files()
    
    # Check environment variable first
    env_token = get_env_var_or_default('PENIFY_API_TOKEN')
    if env_token:
        return env_token
    
    # Check config file
    config_file = get_penify_config()
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('api_keys')
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error reading .penify config file: {str(e)}")
    
    return None
