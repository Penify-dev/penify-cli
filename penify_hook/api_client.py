import json
import os
import requests
from typing import Dict, Any, Optional

from penify_hook.ui_utils import print_info
from .llm_client import LLMClient

class APIClient:
    def __init__(self, api_key: str = None):
        """Initialize the API client with an API key.

        Args:
            api_key (str): API key for authentication.
        """
        self.api_key = api_key or os.environ.get('PENIFY_API_KEY')
        self.base_url = os.environ.get('PENIFY_API_URL', 'https://api.penify.ai')

    def send_file_for_docstring_generation(self, file_name, content, line_numbers, repo_details = None):
        """Send file content and modified lines to the API and return modified
        content.

        This function constructs a payload containing the file path, content,
        and modified line numbers, and sends it to a specified API endpoint for
        processing. It handles the response from the API, returning the modified
        content if the request is successful. If the request fails, it logs the
        error details and returns the original content.

        Args:
            file_name (str): The path to the file being sent.
            content (str): The content of the file to be processed.
            line_numbers (list): A list of line numbers that have been modified.
            repo_details (str?): Additional repository details if applicable.

        Returns:
            str: The modified content returned by the API, or the original content if the
                request fails.
        """
        payload = {
            'file_path': file_name,
            'content': content,
            'modified_lines': line_numbers
        }
        if repo_details:
            payload['git_repo'] = repo_details
        url = self.base_url+"/v1/hook/file/generate/doc"
        response = requests.post(url, json=payload,headers={"Authorization": f"Bearer {self.api_key}"}, timeout=60*10)
        if response.status_code == 200:
            response = response.json()
            return response.get('modified_content')
        else:
            error_message = response.json().get('detail')
            if not error_message:
                error_message = response.text

            raise Exception(f"API Error: {error_message}")

    def generate_commit_summary(self, diff: str, instruction: str, repo_details: Dict[str, str], ticket_context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Generate a commit summary using the provided diff and instruction.

        Args:
            diff (str): The diff of the staged changes.
            instruction (str): Custom instruction for generating the commit summary.
            repo_details (Dict[str, str]): Repository details.
            ticket_context (Optional[Dict[str, Any]]): Context from project management tools.

        Returns:
            Dict[str, str]: Dictionary containing 'title' and optionally 'description'.
        """
        url = f"{self.base_url}/v1/commit/summary"
        
        # Prepare the request body with enhanced context
        data = {
            "diff": diff,
            "instruction": instruction,
            "repoDetails": repo_details,
        }
        
        # Add ticket context if available
        if ticket_context:
            data["ticketContext"] = ticket_context
            print_info("Adding ticket context from project management tools")

        try:
            response = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to API: {e}")
            return {}

    def get_supported_file_types(self) -> list[str]:
        """Retrieve the supported file types from the API.

        This function sends a request to the API to obtain a list of supported
        file types. If the API responds successfully, it returns the list of
        supported file types. If the API call fails, it returns a default list
        of common file types.

        Returns:
            list[str]: A list of supported file types, either from the API or a default set.
        """

        url = self.base_url+"/v1/file/supported_languages"
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            return response
        else:
            return ["py", "js", "ts", "java", "kt", "cs", "c"]

    def generate_commit_summary_with_llm(self, diff: str, instruction: str, generate_description: bool,
                                       repo_details: Dict[str, str], llm_client: Any,
                                       ticket_context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Generate a commit summary using an LLM client.
        
        Args:
            diff (str): The diff of the staged changes.
            instruction (str): Custom instruction for generating the commit summary.
            generate_description (bool): Whether to generate a detailed description.
            repo_details (Dict[str, str]): Repository details.
            llm_client (Any): LLM client instance.
            ticket_context (Optional[Dict[str, Any]]): Context from project management tools.
            
        Returns:
            Dict[str, str]: Dictionary containing 'title' and optionally 'description'.
        """
        # Format the ticket context for the prompt
        ticket_context_str = ""
        if ticket_context:
            print_info("Adding ticket context from project management tools to LLM prompt")
            ticket_context_str = "Additional context from project management tools:\n"
            
            # Format JIRA ticket context
            if 'jira' in ticket_context:
                jira_ctx = ticket_context['jira']
                ticket_context_str += "\nJIRA Issues:\n"
                if 'issues' in jira_ctx:
                    for issue in jira_ctx['issues']:
                        ticket_context_str += f"- {issue.get('key', 'Unknown')}: {issue.get('summary', 'No summary')}\n"
                        if 'description' in issue and issue['description']:
                            ticket_context_str += f"  Description: {issue['description'][:150]}...\n"
            
            # Format Azure DevOps ticket context
            if 'azure_devops' in ticket_context:
                azdo_ctx = ticket_context['azure_devops']
                ticket_context_str += "\nAzure DevOps Work Items:\n"
                if 'work_item_ids' in azdo_ctx:
                    for item_id in azdo_ctx['work_item_ids']:
                        ticket_context_str += f"- Work Item #{item_id}\n"
            
            # Format GitHub ticket context
            if 'github' in ticket_context:
                github_ctx = ticket_context['github']
                ticket_context_str += "\nGitHub Issues:\n"
                if 'issue_numbers' in github_ctx:
                    for issue_num in github_ctx['issue_numbers']:
                        ticket_context_str += f"- Issue #{issue_num}\n"
            
            # Format Asana ticket context
            if 'asana' in ticket_context:
                asana_ctx = ticket_context['asana']
                ticket_context_str += "\nAsana Tasks:\n"
                if 'task_ids' in asana_ctx:
                    for task_id in asana_ctx['task_ids']:
                        ticket_context_str += f"- Task ID: {task_id}\n"
        
        # Create the prompt with system and user messages
        system_prompt = (
            "You are a helpful commit message generator. Given code changes, you will generate a concise, "
            "informative commit message title and optionally a detailed description. "
            "Follow common commit message conventions with a short subject line (<72 chars) and optional detailed body."
        )
        
        user_prompt = (
            f"Here are the code changes (diff):\n\n{diff}\n\n"
            f"Repository details:\n{json.dumps(repo_details, indent=2)}\n\n"
            f"{ticket_context_str}\n"
            f"Instructions: {instruction}\n\n"
            f"Please generate a {'commit message with title and detailed description' if generate_description else 'concise commit title only'}."
        )
        
        # Get response from LLM
        response = llm_client.get_completion(
            system_prompt=system_prompt,
            user_prompt=user_prompt
        )
        
        # Parse response to extract title and description
        if generate_description:
            # Try to parse title and description from the response
            lines = response.split('\n')
            if lines:
                title = lines[0].strip()
                # If there are more lines, join them as description
                description = '\n'.join(lines[1:]).strip() if len(lines) > 1 else ""
                return {'title': title, 'description': description}
            else:
                return {'title': response, 'description': ""}
        else:
            # Just return the first line as title
            return {'title': response.strip().split('\n')[0], 'description': ""}

    def analyze_folder(self, folder_path: str, readme_content: str = None) -> Dict[str, str]:
        """Analyze a folder and generate documentation.

        Args:
            folder_path (str): Path to the folder to analyze.
            readme_content (str, optional): Existing README content. Defaults to None.

        Returns:
            Dict[str, str]: Dictionary containing generated documentation.
        """
        url = f"{self.base_url}/v1/doc/folder"
        
        # Prepare the request body
        data = {
            "folderPath": folder_path,
        }
        
        if readme_content:
            data["readmeContent"] = readme_content
            
        try:
            response = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to API: {e}")
            return {}

    def analyze_file(self, file_path: str, file_content: str) -> Dict[str, str]:
        """Analyze a file and generate documentation.

        Args:
            file_path (str): Path to the file to analyze.
            file_content (str): Content of the file.

        Returns:
            Dict[str, str]: Dictionary containing generated documentation.
        """
        url = f"{self.base_url}/v1/doc/file"
        
        # Prepare the request body
        data = {
            "filePath": file_path,
            "fileContent": file_content,
        }
            
        try:
            response = requests.post(
                url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json=data
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Error sending request to API: {e}")
            return {}

    def get_api_key(self):

        url = self.base_url+"/v1/apiToken/get"
        response = requests.get(url, headers={"Authorization": f"Bearer {self.api_key}"}, timeout=60*10)
        if response.status_code == 200:
            response = response.json()
            return response.get('key')
        else:
            print(f"Response: {response.status_code}")
            print(f"Error: {response.text}")
            return None

