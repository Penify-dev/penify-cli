import json
import webbrowser
import http.server
import socketserver
import urllib.parse
import random
import os
from threading import Thread
from pathlib import Path

def save_credentials(api_key):
    # Try to save in .env file in git repo first
    """Save the API key in a priority-based manner.
    
    This function attempts to save the API key in two locations, based on priority:
    1. In a `.env` file located in the root of the Git repository if one is found.
    2. In a global `.penify` file located in the user's home directory as a
    fallback.  The function first tries to locate the Git repository using
    `recursive_search_git_folder`. If a Git repository is found, it reads the
    existing `.env` file (if present), updates or adds the API key under the key
    `PENIFY_API_TOKEN`, and writes the updated content back. If any error occurs
    during this process, it falls back to saving the credentials in the global
    `.penify` file. The function handles exceptions and prints appropriate error
    messages.
    
    Args:
        api_key (str): The API key to save.
    
    Returns:
        bool: True if the API key is saved successfully, False otherwise.
    """
    try:
        from ..utils import recursive_search_git_folder
        current_dir = os.getcwd()
        repo_root = recursive_search_git_folder(current_dir)
        
        if repo_root:
            # We're in a git repo, save to .env file
            env_file = Path(repo_root) / '.env'
            try:
                # Read existing .env content
                env_content = {}
                if env_file.exists():
                    with open(env_file, 'r') as f:
                        for line in f:
                            line = line.strip()
                            if line and not line.startswith('#') and '=' in line:
                                key, value = line.split('=', 1)
                                env_content[key.strip()] = value.strip()
                
                # Update API token
                env_content['PENIFY_API_TOKEN'] = api_key
                
                # Write back to .env file
                with open(env_file, 'w') as f:
                    for key, value in env_content.items():
                        f.write(f"{key}={value}\n")
                
                print(f"API token saved to {env_file}")
                return True
            except Exception as e:
                print(f"Error saving to .env file: {str(e)}")
                # Fall back to saving in .penify global config
    except Exception as e:
        print(f"Error finding git repository: {str(e)}")
    
    # Fall back to global .penify file in home directory
    home_dir = Path.home()
    penify_file = home_dir / '.penify'
    
    # If the file already exists, add the new api key to the existing file
    if penify_file.exists():
        with open(penify_file, 'r') as f:
            credentials = json.load(f)
            credentials['api_keys'] = api_key
    else:
        credentials = {
            'api_keys': api_key
        }

    try:
        with open(penify_file, 'w') as f:
            json.dump(credentials, f)
        print(f"API token saved to global config {penify_file}")
        return True
    except Exception as e:
        print(f"Error saving credentials: {str(e)}")
        return False

def login(api_url, dashboard_url):
    """Open the login page in a web browser and capture the token via redirect."""
    redirect_port = random.randint(30000, 50000)
    redirect_url = f"http://localhost:{redirect_port}/callback"
    
    full_login_url = f"{dashboard_url}?redirectUri={urllib.parse.quote(redirect_url)}"
    
    print(f"Opening login page in your default web browser: {full_login_url}")
    webbrowser.open(full_login_url)
    
    class TokenHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):

            """Handle a GET request to process login token and redirect or display error
            message."""
            query = urllib.parse.urlparse(self.path).query
            query_components = urllib.parse.parse_qs(query)
            token = query_components.get("token", [None])[0]
            
            if token:
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                response = """
                <html>
                <head>
                    <script>
                        setTimeout(function() {
                            window.location.href = 'https://dashboard.penify.dev';
                        }, 5000);
                    </script>
                </head>
                <body>
                    <h1>Login Successful!</h1>
                    <p>You will be redirected to the Penify dashboard in 5 seconds. You can also close this window and return to the CLI.</p>
                </body>
                </html>
                """
                self.wfile.write(response.encode())
                
                print(f"\nLogin successful! Fetching API keys...")
                from ..api_client import APIClient
                api_key = APIClient(api_url, None, token).get_api_key()
                if api_key:
                    save_credentials(api_key)
                    print("API keys fetched and saved successfully.")
                    print("You'll be redirected to the Penify dashboard. You can continue using the CLI.")
                else:
                    print("Failed to fetch API keys.")
            else:
                self.send_response(400)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                response = """
                <html>
                <body>
                <h1>Login Failed</h1>
                <p>Please try again.</p>
                </body>
                </html>
                """
                self.wfile.write(response.encode())
                print("\nLogin failed. Please try again.")
            
            # Schedule the server shutdown
            thread = Thread(target=self.server.shutdown)
            thread.daemon = True
            thread.start()

        def log_message(self, format, *args):
            # Suppress log messages
            """Suppress log messages."""
            return
    
    with socketserver.TCPServer(("", redirect_port), TokenHandler) as httpd:
        print(f"Listening on port {redirect_port} for the redirect...")
        httpd.serve_forever()
    
    print("Login process completed. You can now use other commands with your API token.")
