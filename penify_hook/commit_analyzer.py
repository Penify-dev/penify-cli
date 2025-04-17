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
        """Initialize a new instance of the class.
        
        Args:
            repo_path (str): The path to the repository.
            api_client (APIClient): An instance of the API client.
            llm_client (LLMClient?): An instance of the LLM client. Defaults to None.
            jira_client (JiraClient?): An instance of the JIRA client. Defaults to None.
        """
        super().__init__(repo_path, api_client)

        self.llm_client = llm_client  # Add LLM client as an optional parameter
        self.jira_client: JiraClient = jira_client  # Add JIRA client as an optional parameter

    def get_summary(self, instruction: str, generate_description: bool) -> dict:
        """Generate a summary for the commit based on the staged changes.
        
        This function retrieves the differences of the staged changes in the repository and generates a commit summary using the
        provided instruction. If there are no changes staged for commit, an exception is raised. If a JIRA client is connected,
        it will attempt to extract issue keys from the current branch and use them to fetch context. The summary can be
        generated either with a Language Model (LLM) client or through the API client.
        
        Args:
            instruction (str): A string containing instructions for generating the commit summary.
            generate_description (bool): Whether to include detailed descriptions in the summary.
        
        Returns:
            dict: The generated commit summary based on the staged changes, provided instruction, and any relevant JIRA context. The
                dictionary contains keys such as 'summary', 'description', etc., depending on whether a description was requested.
        
        Raises:
            ValueError: If there are no changes staged for commit.
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
        """Run the post-commit hook.
        
        This method processes the modified files from the last commit, stages them, and creates an auto-commit with an optional
        message. It also handles JIRA integration if available. If there is an error generating the commit summary, an exception
        is raised.
        
        Args:
            msg (Optional[str]): An optional message to include in the commit.
            edit_commit_message (bool): A flag indicating whether to open the git commit edit terminal after
                committing.
            generate_description (bool): A flag indicating whether to include a description in the commit
                message.
        
        Raises:
            Exception: If there is an error generating the commit summary.
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
        """Process JIRA integration for the commit message.
        
        This function looks for JIRA issue keys within the provided commit title, description, and user message. It then
        extracts any additional issue keys from the current branch name. If JIRA issues are found, it formats the commit message
        with this information and adds a comment to each relevant JIRA issue.
        
        Args:
            title (str): Generated commit title.
            description (str): Generated commit description.
            msg (str): Original user message that might contain JIRA references.
        
        Returns:
            tuple: A tuple containing the updated commit title and description with included JIRA information.
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
        """Amend the last commit's message using the default git editor.
        
        This function changes the current working directory to the repository path, runs the `git commit --amend` command to
        modify the last commit, and opens the default git editor for the user to edit the commit message. After the operation,
        it returns to the original directory.
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
