import json
import webbrowser
import http.server
import socketserver
import urllib.parse
import random
from threading import Thread
from pathlib import Path
from ..api_client import APIClient

def save_credentials(api_key):
    """Save or update the API keys in the .penify file in the user's home
    directory.

    This function checks if the .penify file exists in the user's home
    directory. If it does, it loads the existing credentials and updates the
    API key. If the file does not exist, it creates a new file with the
    provided API key. The function attempts to write the updated credentials
    back to the file and returns a boolean indicating whether the operation
    was successful.

    Args:
        api_key (str): The new API key to be saved or updated.

    Returns:
        bool: True if the credentials were successfully saved, False otherwise.
    """
    home_dir = Path.home()
    penify_file = home_dir / '.penify'
    

    # if the file already exists, add the new api key to the existing file
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
        return True
    except Exception as e:
        print(f"Error saving credentials: {str(e)}")
        return False

def login(api_url, dashboard_url):
    """Open the login page in a web browser and listen for the redirect URL to
    capture the token.

    This function generates a random redirect port, constructs the full
    login URL with the provided dashboard URL, opens the login page in the
    default web browser, and sets up a simple HTTP server to listen for the
    redirect. Upon receiving the redirect, it extracts the token from the
    query parameters, fetches API keys using the token, saves them if
    successful, and handles login failures by notifying the user.

    Args:
        api_url (str): The URL of the API service to fetch API keys.
        dashboard_url (str): The URL of the dashboard where the user will be redirected after logging
            in.
    """
    redirect_port = random.randint(30000, 50000)
    redirect_url = f"http://localhost:{redirect_port}/callback"
    
    full_login_url = f"{dashboard_url}?redirectUri={urllib.parse.quote(redirect_url)}"
    
    print(f"Opening login page in your default web browser: {full_login_url}")
    webbrowser.open(full_login_url)
    
    class TokenHandler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            """Handle a GET request to process login token and redirect or display
            error message.

            This method processes the incoming GET request, extracts the token from
            the query string, and performs actions based on whether the token is
            present. If the token is valid, it redirects the user to the Penify
            dashboard and fetches API keys if successful. If the token is invalid,
            it displays an error message.
            """

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
            return
    
    with socketserver.TCPServer(("", redirect_port), TokenHandler) as httpd:
        print(f"Listening on port {redirect_port} for the redirect...")
        httpd.serve_forever()
    
    print("Login process completed. You can now use other commands with your API token.")
