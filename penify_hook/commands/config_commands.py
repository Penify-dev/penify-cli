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
from penify_hook.utils import recursive_search_git_folder


def get_penify_config() -> Path:
    """Get the home directory for the .penify configuration file.

    This function searches for the `.penify` file in the current directory
    and its parent directories until it finds it or reaches the home
    directory. If not found, it creates the `.penify` directory and an empty
    `config.json` file.

    Returns:
        Path: The path to the `config.json` file within the `.penify` directory.
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
    

def save_llm_config(model, api_base, api_key):
    """Save LLM configuration settings in the .penify file.

    It reads the existing configuration from the .penify file if it exists,
    updates or adds the LLM configuration with the provided model, API base,
    and API key, and then writes the updated configuration back to the file.

    Args:
        model (str): The name of the language model.
        api_base (str): The base URL for the API.
        api_key (str): The API key for authentication.

    Returns:
        bool: True if the LLM configuration was successfully saved, False otherwise.
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
    """Save JIRA configuration settings in the .penify file.

    This function reads existing JIRA configuration from the .penify file,
    updates or adds new JIRA configuration details, and writes it back to
    the file.

    Args:
        url (str): The URL of the JIRA instance.
        username (str): The username for accessing the JIRA instance.
        api_token (str): The API token used for authentication.

    Returns:
        bool: True if the configuration was successfully saved, False otherwise.
    """
    from penify_hook.utils import recursive_search_git_folder

    home_dir = Path.home()
    penify_file = home_dir / '.penify'
    
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

def get_llm_config():
    """Retrieve LLM configuration from the .penify file.

    This function reads the .penify configuration file and extracts the LLM
    settings. If the file does not exist or contains invalid JSON, it
    returns an empty dictionary.

    Returns:
        dict: A dictionary containing the LLM configuration, or an empty dictionary if
            the file is missing or invalid.
    """
    config_file = get_penify_config()
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('llm', {})
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error reading .penify config file: {str(e)}")
    
    return {}

def get_jira_config():
    """Get JIRA configuration from the .penify file.

    This function reads the JIRA configuration from a JSON file specified in
    the .penify file. If the .penify file exists and contains valid JSON
    with a 'jira' key, it returns the corresponding configuration.
    Otherwise, it returns an empty dictionary.

    Returns:
        dict: The JIRA configuration or an empty dictionary if not found or invalid.
    """
    config_file = get_penify_config()
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('jira', {})
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error reading .penify config file: {str(e)}")
    
    return {}

def config_llm_web():
    """Open a web browser interface for configuring LLM settings.

    This function starts a temporary HTTP server that serves an HTML
    template for configuring Large Language Model (LLM) settings. It handles
    GET and POST requests to retrieve the current configuration, save new
    configurations, and suppress log messages.  The server runs on a random
    port between 30000 and 50000, and it is accessible via a URL like
    http://localhost:<redirect_port>. The function opens this URL in the
    default web browser for configuration. Once configured, the server shuts
    down.
    """
    redirect_port = random.randint(30000, 50000)
    server_url = f"http://localhost:{redirect_port}"
    
    print(f"Starting configuration server on {server_url}")
    
    class ConfigHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            """Handle HTTP GET requests.

            This function processes incoming GET requests and sends appropriate
            responses based on the requested path. It serves an HTML template for
            the root path ("/") and returns a JSON response with the current LLM
            configuration for the "/get_config" path. For any other paths, it
            returns a "Not Found" error.
            """

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
            """Handle POST requests on the /save endpoint.

            This method processes incoming POST requests to save language model
            configuration data. It extracts the necessary parameters from the
            request body, saves the configuration using the provided details, and
            then schedules the server to shut down after a successful save.

            Args:
                self (HTTPRequestHandler): The instance of the HTTPRequestHandler class handling the request.
            """

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
    """Open a web browser interface for configuring JIRA settings.

    This function sets up a simple HTTP server using Python's built-in
    `http.server` module to handle GET and POST requests. The server serves
    an HTML page for configuration and handles saving the JIRA configuration
    details through API tokens and URLs. Upon successful configuration, it
    shuts down the server gracefully.
    """
    redirect_port = random.randint(30000, 50000)
    server_url = f"http://localhost:{redirect_port}"
    
    print(f"Starting configuration server on {server_url}")
    
    class ConfigHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            """Handle GET requests for different paths.

            This function processes GET requests based on the path requested. It
            serves an HTML template for the root path, returns a JSON configuration
            for a specific endpoint, and handles any other paths by returning a 404
            error.
            """

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
            """Handle HTTP POST requests to save JIRA configuration.

            This method processes incoming POST requests to save JIRA configuration
            details. It reads JSON data from the request body, extracts necessary
            parameters (URL, username, API token, and verify), saves the
            configuration using the `save_jira_config` function, and responds with
            success or error messages. If an exception occurs during the process, it
            sends a 500 Internal Server Error response.
            """

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

def get_token():
    """Get the token based on priority from environment variables or
    configuration files.

    Returns:
        str: The API token if found, otherwise None.
    """
    import os
    env_token = os.getenv('PENIFY_API_TOKEN')
    if env_token:
        return env_token
    
    config_file = Path.home() / '.penify'
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
                return config.get('api_keys')
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error reading .penify config file: {str(e)}")
    
    return None
