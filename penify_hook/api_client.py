import json
import os
import requests
from .llm_client import LLMClient

class APIClient:
    def __init__(self, api_url, api_token: str = None, bearer_token: str = None):
        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        @type dictionary: dict
        @param dictionary: The processed files map.
        @rtype: bool
        @return: True if successful, False otherwise.
        @return: The return type is optional and may be specified at the beginning of
        @return: the ``Returns`` section followed by a colon.
        @return: The ``Returns`` section may span multiple lines and paragraphs.
        @return: Following lines should be indented to match the first line.
        @return: The ``Returns`` section supports any reStructuredText formatting,
        @return: including literal blocks::
            
            {
            'param1': param1,
            'param2': param2
            }
        """
        self.api_url = api_url
        self.AUTH_TOKEN = api_token
        self.BEARER_TOKEN = bearer_token

    def send_file_for_docstring_generation(self, file_name, content, line_numbers, repo_details = None):
        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        @type dictionary: dict
        @param dictionary: The processed files map.
        @rtype: bool
        @return: True if successful, False otherwise.
        @return: The return type is optional and may be specified at the beginning of
        @return: the ``Returns`` section followed by a colon.
        @return: The ``Returns`` section may span multiple lines and paragraphs.
        @return: Following lines should be indented to match the first line.
        @return: The ``Returns`` section supports any reStructuredText formatting,
        @return: including literal blocks::
            
            {
            'param1': param1,
            'param2': param2
            }
        """
        payload = {
            'file_path': file_name,
            'content': content,
            'modified_lines': line_numbers
        }
        if repo_details:
            payload['git_repo'] = repo_details
        url = self.api_url+"/v1/hook/file/generate/doc"
        response = requests.post(url, json=payload,headers={"api-key": f"{self.AUTH_TOKEN}"}, timeout=60*10)
        if response.status_code == 200:
            response = response.json()
            return response.get('modified_content')
        else:
            error_message = response.json().get('detail')
            if not error_message:
                error_message = response.text

            raise Exception(f"API Error: {error_message}")
        
    def generate_commit_summary(self, git_diff, instruction: str = "", repo_details = None, jira_context: dict = None):
        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        @type dictionary: dict
        @param dictionary: The processed files map.
        @rtype: bool
        @return: True if successful, False otherwise.
        @return: The return type is optional and may be specified at the beginning of
        @return: the ``Returns`` section followed by a colon.
        @return: The ``Returns`` section may span multiple lines and paragraphs.
        @return: Following lines should be indented to match the first line.
        @return: The ``Returns`` section supports any reStructuredText formatting,
        @return: including literal blocks::
            
            {
            'param1': param1,
            'param2': param2
            }
        """
        payload = {
            'git_diff': git_diff,
            'additional_instruction': instruction
        }
        if repo_details:
            payload['git_repo'] = repo_details
            
        # Add JIRA context if available
        if jira_context:
            payload['jira_context'] = jira_context

        url = self.api_url+"/v1/hook/commit/summary"
        try:
            response = requests.post(url, json=payload, headers
            ={"api-key": f"{self.AUTH_TOKEN}"}, timeout=60*10)
            if response.status_code == 200:
                response = response.json()
                return response
            else:
                # print(f"Response: {response.status_code}")
                # print(f"Error: {response.text}")
                raise Exception(f"API Error: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
            return None

    def get_supported_file_types(self) -> list[str]:

        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        @type dictionary: dict
        @param dictionary: The processed files map.
        @rtype: bool
        @return: True if successful, False otherwise.
        @return: The return type is optional and may be specified at the beginning of
        @return: the ``Returns`` section followed by a colon.
        @return: The ``Returns`` section may span multiple lines and paragraphs.
        @return: Following lines should be indented to match the first line.
        @return: The ``Returns`` section supports any reStructuredText formatting,
        @return: including literal blocks::
            
            {
            'param1': param1,
            'param2': param2
            }
        """
        url = self.api_url+"/v1/file/supported_languages"
        response = requests.get(url)
        if response.status_code == 200:
            response = response.json()
            return response
        else:
            return ["py", "js", "ts", "java", "kt", "cs", "c"]

    def generate_commit_summary_with_llm(self, diff, message, generate_description: bool, repo_details, llm_client : LLMClient, jira_context=None):
        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        @type dictionary: dict
        @param dictionary: The processed files map.
        @rtype: bool
        @return: True if successful, False otherwise.
        @return: The return type is optional and may be specified at the beginning of
        @return: the ``Returns`` section followed by a colon.
        @return: The ``Returns`` section may span multiple lines and paragraphs.
        @return: Following lines should be indented to match the first line.
        @return: The ``Returns`` section supports any reStructuredText formatting,
        @return: including literal blocks::
            
            {
            'param1': param1,
            'param2': param2
            }
        """
        try:
            return llm_client.generate_commit_summary(diff, message, generate_description, repo_details, jira_context)
        except Exception as e:
            print(f"Error using local LLM: {e}")
            # Fall back to API for commit summary
            return self.generate_commit_summary(diff, message, repo_details, jira_context)

    def get_api_key(self):


        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        @type dictionary: dict
        @param dictionary: The processed files map.
        @rtype: bool
        @return: True if successful, False otherwise.
        @return: The return type is optional and may be specified at the beginning of
        @return: the ``Returns`` section followed by a colon.
        @return: The ``Returns`` section may span multiple lines and paragraphs.
        @return: Following lines should be indented to match the first line.
        @return: The ``Returns`` section supports any reStructuredText formatting,
        @return: including literal blocks::
            
            {
            'param1': param1,
            'param2': param2
            }
        """
        url = self.api_url+"/v1/apiToken/get"
        response = requests.get(url, headers={"Authorization": f"Bearer {self.BEARER_TOKEN}"}, timeout=60*10)
        if response.status_code == 200:
            response = response.json()
            return response.get('key')
        else:
            print(f"Response: {response.status_code}")
            print(f"Error: {response.text}")
            return None

