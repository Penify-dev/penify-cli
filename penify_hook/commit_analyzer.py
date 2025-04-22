import os
import re
import subprocess
import tempfile
from typing import Optional, List
from git import Repo
from tqdm import tqdm

from penify_hook.base_analyzer import BaseAnalyzer
from penify_hook.jira_client import JiraClient
from penify_hook.ui_utils import print_info, print_success, print_warning
from .api_client import APIClient

class CommitDocGenHook(BaseAnalyzer):
    def __init__(self, repo_path: str, api_client: APIClient, llm_client=None, jira_client=None):
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
        super().__init__(repo_path, api_client)

        self.llm_client = llm_client  # Add LLM client as an optional parameter
        self.jira_client: JiraClient = jira_client  # Add JIRA client as an optional parameter

    def get_summary(self, instruction: str, generate_description: bool) -> dict:
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
        diff = self.repo.git.diff('--cached')
        if not diff:
            raise ValueError("No changes to commit")
        
        # Get JIRA context if available
        jira_context = None
        if self.jira_client and self.jira_client.is_connected():
            try:
                # Check branch name for JIRA issues
                current_branch = self.repo.active_branch.name
                issue_keys = self.jira_client.extract_issue_keys_from_branch(current_branch)
                
                # If issues found in branch, get context
                if issue_keys:
                    jira_context = self.jira_client.get_commit_context_from_issues(issue_keys)
            except Exception as e:
                print(f"Could not get JIRA context: {e}")
        
        # Use LLM client if provided, otherwise use API client
        print_info("Fetching commit summary from LLM...")
        if self.llm_client:
            return self.api_client.generate_commit_summary_with_llm(
                diff, instruction, generate_description, self.repo_details, self.llm_client, jira_context
            )
        else:
            return self.api_client.generate_commit_summary(diff, instruction, self.repo_details, jira_context)
    
   
    def run(self, msg: Optional[str], edit_commit_message: bool, generate_description: bool):
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
        summary: dict = self.get_summary(msg, True)
        if not summary:
            raise Exception("Error generating commit summary")
        
        title = summary.get('title', "")
        description = summary.get('description', "")
        
        # If JIRA client is available, integrate JIRA information
        if self.jira_client and self.jira_client.is_connected():
            # Add JIRA information to commit message
            self.process_jira_integration(title, description, msg)
            
        # commit the changes to the repository with above details
        commit_msg = f"{title}\n\n{description}" if generate_description else title
        self.repo.git.commit('-m', commit_msg)
        print_success(f"Commit: {commit_msg}")
        
        if edit_commit_message:
            # Open the git commit edit terminal
            print_info("Opening git commit edit terminal...")
            self._amend_commit()
    
    def process_jira_integration(self, title: str, description: str, msg: str) -> tuple:
        # Look for JIRA issue keys in commit message, title, description and user message
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
        issue_keys = []
        if self.jira_client:
            # Extract from message content
            issue_keys = self.jira_client.extract_issue_keys(f"{title} {description} {msg}")
            
            # Also check the branch name (which often follows JIRA naming conventions)
            try:
                current_branch = self.repo.active_branch.name
                branch_issue_keys = self.jira_client.extract_issue_keys_from_branch(current_branch)
                
                # Add any new keys found in branch name
                for key in branch_issue_keys:
                    if key not in issue_keys:
                        issue_keys.append(key)
                        print_info(f"Added JIRA issue {key} from branch name: {current_branch}")
            except Exception as e:
                print_warning(f"Could not extract JIRA issues from branch name: {e}")
            
            if issue_keys:
                print_info(f"Found JIRA issues: {', '.join(issue_keys)}")
                
                # Format commit message with JIRA info
                
                # Add comments to JIRA issues
                for issue_key in issue_keys:
                    comment = (
                        f"Commit related to this issue:\n\n"
                        f"**{title}**\n\n"
                        f"{description}\n\n"
                    )
                    self.jira_client.add_comment(issue_key, comment)
            else:
                print_warning("No JIRA issues found in commit message or branch name")
                
        return title, description

    def _amend_commit(self):
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
        try:
            # Change to the repository directory
            os.chdir(self.repo_path)
            
            # Run git commit --amend
            subprocess.run(['git', 'commit', '--amend'], check=True)
            
            print("Commit message amended successfully.")
        except subprocess.CalledProcessError as e:
            print(f"Error amending commit message: {e}")
        finally:
            # Change back to the original directory
            os.chdir(os.path.dirname(os.path.abspath(__file__)))
