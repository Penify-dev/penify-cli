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
from penify_hook.utils import recursive_search_git_folder

# Try to import dotenv, but don't fail if it's not available
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False


def load_env_files() -> None:
    """
    Load environment variables from .env files in various locations:
    1. Current directory
    2. Git repo root directory
    3. User home directory
    
    This function is called when the module is imported, ensuring env variables
    are available throughout the application lifecycle.
    """
    if not DOTENV_AVAILABLE:
        logging.warning("python-dotenv is not installed. .env file loading is disabled.")
        logging.warning("Run 'pip install python-dotenv' to enable .env file support.")
        return

    # Load from current directory
    load_dotenv(override=True)
    
    # Load from Git repo root
    try:
        current_dir = os.getcwd()
        repo_root = recursive_search_git_folder(current_dir)
        if repo_root:
            repo_env = Path(repo_root) / '.env'
            if repo_env.exists():
                load_dotenv(dotenv_path=repo_env, override=True)
    except Exception as e:
        logging.warning(f"Failed to load .env from Git repo: {str(e)}")
    
    # Load from user home directory
    try:
        home_env = Path.home() / '.env'
        if home_env.exists():
            load_dotenv(dotenv_path=home_env, override=True)
    except Exception as e:
        logging.warning(f"Failed to load .env from home directory: {str(e)}")


# Load environment variables when module is imported
load_env_files()


def get_penify_config() -> Path:
    """
    Get the home directory for the .penify configuration file.
    This function searches for the .penify file in the current directory
    and its parent directories until it finds it or reaches the home directory.
    """
    current_dir = os.getcwd()
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
    Save LLM configuration settings in the .penify file.
    """

    penify_file = get_penify_config()
    
    config = {}
    if penify_file.exists():
        try:
            with open(penify_file, 'r') as f:
                config = json.load(f)
        except (json.JSONDecodeError, IOError, OSError) as e:
            print(f"Error reading configuration file: {str(e)}")
            # Continue with empty config
    
    # Update or add LLM configuration
    config['llm'] = {
        'model': model,
        'api_base': api_base,
        'api_key': api_key
    }
    
    try:
        with open(penify_file, 'w') as f:
            json.dump(config, f)
        print(f"LLM configuration saved to {penify_file}")
        return True
    except Exception as e:
        print(f"Error saving LLM configuration: {str(e)}")
        return False


def save_jira_config(url, username, api_token):
    """
    Save JIRA configuration settings in the .penify file.
    """
    from penify_hook.utils import recursive_search_git_folder

    penify_file = get_penify_config()
    
    config = {}
    if penify_file.exists():
        try:
            with open(penify_file, 'r') as f:
                config = json.load(f)
        except json.JSONDecodeError:
            pass
    
    # Update or add JIRA configuration
    config['jira'] = {
        'url': url,
        'username': username,
        'api_token': api_token
    }
    
    try:
        with open(penify_file, 'w') as f:
            json.dump(config, f)
        print(f"JIRA configuration saved to {penify_file}")
        return True
    except Exception as e:
        print(f"Error saving JIRA configuration: {str(e)}")
        return False


def get_llm_config() -> Dict[str, str]:
    """
    Get LLM configuration with environment variables having highest priority.
    
    Environment variables:
    - PENIFY_LLM_MODEL: Model name
    - PENIFY_LLM_API_BASE: API base URL
    - PENIFY_LLM_API_KEY: API key
    
    Returns:
        dict: Configuration dictionary with model, api_base, and api_key
    """
    # Initialize with environment variables
    config = {
        'model': get_env_var_or_default('PENIFY_LLM_MODEL'),
        'api_base': get_env_var_or_default('PENIFY_LLM_API_BASE'),
        'api_key': get_env_var_or_default('PENIFY_LLM_API_KEY')
    }
    
    # Remove None values
    config = {k: v for k, v in config.items() if v is not None}
    
    # If we have all config from environment variables, return early
    if all(k in config for k in ['model', 'api_base', 'api_key']):
        return config
    
    # Otherwise load from config file and merge
    config_file = get_penify_config()
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                file_llm_config = file_config.get('llm', {})
                
                # Only override values not set by environment variables
                for k, v in file_llm_config.items():
                    if k not in config:
                        config[k] = v
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error reading .penify config file: {str(e)}")
    
    return config


def get_jira_config() -> Dict[str, str]:
    """
    Get JIRA configuration with environment variables having highest priority.
    
    Environment variables:
    - PENIFY_JIRA_URL: JIRA URL
    - PENIFY_JIRA_USER: JIRA username
    - PENIFY_JIRA_TOKEN: JIRA API token
    
    Returns:
        dict: Configuration dictionary with url, username, and api_token
    """
    # Initialize with environment variables
    config = {
        'url': get_env_var_or_default('PENIFY_JIRA_URL'),
        'username': get_env_var_or_default('PENIFY_JIRA_USER'),
        'api_token': get_env_var_or_default('PENIFY_JIRA_TOKEN')
    }
    
    # Remove None values
    config = {k: v for k, v in config.items() if v is not None}
    
    # If we have all config from environment variables, return early
    if all(k in config for k in ['url', 'username', 'api_token']):
        return config
    
    # Otherwise load from config file and merge
    config_file = get_penify_config()
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                file_config = json.load(f)
                file_jira_config = file_config.get('jira', {})
                
                # Only override values not set by environment variables
                for k, v in file_jira_config.items():
                    if k not in config:
                        config[k] = v
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error reading .penify config file: {str(e)}")
    
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


def get_token() -> Optional[str]:
    """
    Get the API token based on priority:
    1. Environment variable PENIFY_API_TOKEN
    2. Config file 'api_keys' value
    
    Returns:
        str or None: API token if found, None otherwise
    """
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
