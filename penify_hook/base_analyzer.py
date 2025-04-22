import os
from git import Repo
from .api_client import APIClient
from penify_hook.utils import get_repo_details, recursive_search_git_folder


class BaseAnalyzer:
    
    def __init__(self, folder_path: str, api_client: APIClient):
        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        Args:
            dictionary (dict): The processed files map.
        
        Returns:
            bool: True if successful, False otherwise.
            The return type is optional and may be specified at the beginning of
            the ``Returns`` section followed by a colon.
            The ``Returns`` section may span multiple lines and paragraphs.
            Following lines should be indented to match the first line.
            The ``Returns`` section supports any reStructuredText formatting,
            including literal blocks::
                
                {
                'param1': param1,
                'param2': param2
                }
        """
        self.folder_path = folder_path
        self.repo_path = recursive_search_git_folder(folder_path)
        self.repo = None
        self.repo_details = None
        if self.folder_path:
            self.repo = Repo(self.repo_path)
            self.repo_details = get_repo_details(self.repo)

        self.relative_file_path = os.path.relpath(folder_path)
        self.api_client = api_client
        self.supported_file_types = set(api_client.get_supported_file_types())