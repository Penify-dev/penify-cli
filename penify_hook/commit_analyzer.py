import os
import re
import subprocess
import tempfile
from typing import Optional, List, Dict, Any
from git import Repo
from tqdm import tqdm

from penify_hook.base_analyzer import BaseAnalyzer
from penify_hook.jira_client import JiraClient
from penify_hook.ui_utils import print_info, print_success, print_warning
from penify_hook.commands.config_commands import get_jira_config, get_azdo_config, get_github_config, get_asana_config
from .api_client import APIClient

class CommitDocGenHook(BaseAnalyzer):
    def __init__(self, repo_path: str, api_client: APIClient, llm_client=None, jira_client=None):
        super().__init__(repo_path, api_client)

        self.llm_client = llm_client  # Add LLM client as an optional parameter
        self.jira_client: JiraClient = jira_client  # Add JIRA client as an optional parameter

    def get_summary(self, instruction: str, generate_description: bool) -> dict:
        """Generate a summary for the commit based on the staged changes.

        This function retrieves the differences of the staged changes in the
        repository and generates a commit summary using the provided
        instruction. If there are no changes staged for commit, an exception is
        raised. If an LLM client is provided, it will use that for generating
        the summary, otherwise it will use the API client.

        Args:
            instruction (str): A string containing instructions for generating the commit summary.
            generate_description (bool): Whether to generate a detailed description

        Returns:
            str: The generated commit summary based on the staged changes and provided
                instruction.

        Raises:
            Exception: If there are no changes staged for commit.
        """
        diff = self.repo.git.diff('--cached')
        if not diff:
            raise ValueError("No changes to commit")
        
        # Get ticket context from all available project management tools
        ticket_context = self._get_ticket_context()
        
        # Use LLM client if provided, otherwise use API client
        print_info("Fetching commit summary from LLM...")
        if self.llm_client:
            return self.api_client.generate_commit_summary_with_llm(
                diff, instruction, generate_description, self.repo_details, self.llm_client, ticket_context
            )
        else:
            return self.api_client.generate_commit_summary(diff, instruction, self.repo_details, ticket_context)
    
    def _get_ticket_context(self) -> Dict[str, Any]:
        """Get ticket context from all available project management tools.
        
        Checks all configured project management tools for relevant ticket information
        based on branch name, previous commits, etc.
        
        Returns:
            Dict[str, Any]: Combined context from all available project management tools
        """
        context = {}
        
        # Get current branch name for ticket extraction
        try:
            current_branch = self.repo.active_branch.name
        except Exception as e:
            print_warning(f"Could not get current branch: {e}")
            current_branch = ""
            
        # 1. Get JIRA context if available
        jira_context = self._get_jira_context(current_branch)
        if jira_context:
            context['jira'] = jira_context
            
        # 2. Get Azure DevOps context if available
        azdo_context = self._get_azdo_context(current_branch)
        if azdo_context:
            context['azure_devops'] = azdo_context
            
        # 3. Get GitHub context if available
        github_context = self._get_github_context(current_branch)
        if github_context:
            context['github'] = github_context
            
        # 4. Get Asana context if available
        asana_context = self._get_asana_context(current_branch)
        if asana_context:
            context['asana'] = asana_context
            
        # If any context was found, log it
        if context:
            tools = list(context.keys())
            print_info(f"Found relevant ticket context in: {', '.join(tools)}")
        else:
            print_info("No ticket context found in any configured project management tools")
            
        return context
    
    def _get_jira_context(self, branch_name: str) -> Dict[str, Any]:
        """Get JIRA context based on branch name and configuration.
        
        Args:
            branch_name (str): Current git branch name
            
        Returns:
            Dict[str, Any]: JIRA context information if available
        """
        jira_context = {}
        
        # Check if JIRA is configured either through jira_client or config
        if self.jira_client and self.jira_client.is_connected():
            try:
                # Check branch name for JIRA issues
                issue_keys = self.jira_client.extract_issue_keys_from_branch(branch_name)
                
                # If issues found in branch, get context
                if issue_keys:
                    jira_context = self.jira_client.get_commit_context_from_issues(issue_keys)
                    print_info(f"Found JIRA issues: {', '.join(issue_keys)}")
            except Exception as e:
                print_warning(f"Could not get JIRA context: {e}")
        else:
            # Check if JIRA is configured in the environment
            jira_config = get_jira_config()
            if jira_config and 'url' in jira_config and 'username' in jira_config and 'api_token' in jira_config:
                try:
                    # Create a temporary JIRA client for this operation
                    temp_jira_client = JiraClient(
                        jira_url=jira_config['url'],
                        jira_user=jira_config['username'],
                        jira_api_token=jira_config['api_token']
                    )
                    
                    if temp_jira_client.is_connected():
                        # Extract JIRA issues from branch name
                        issue_keys = temp_jira_client.extract_issue_keys_from_branch(branch_name)
                        if issue_keys:
                            jira_context = temp_jira_client.get_commit_context_from_issues(issue_keys)
                            print_info(f"Found JIRA issues using config: {', '.join(issue_keys)}")
                except Exception as e:
                    print_warning(f"Error using JIRA configuration: {e}")
                    
        return jira_context
    
    def _get_azdo_context(self, branch_name: str) -> Dict[str, Any]:
        """Get Azure DevOps context based on branch name and configuration.
        
        Args:
            branch_name (str): Current git branch name
            
        Returns:
            Dict[str, Any]: Azure DevOps context information if available
        """
        azdo_context = {}
        
        # Check if Azure DevOps is configured
        azdo_config = get_azdo_config()
        if azdo_config and 'url' in azdo_config and 'project' in azdo_config and 'pat_token' in azdo_config:
            try:
                # Extract work item IDs from branch name (common format: feature/12345-description)
                work_item_pattern = r'(?:^|\/)(\d+)(?:-|_|\s|$)'
                work_item_matches = re.findall(work_item_pattern, branch_name)
                
                if work_item_matches:
                    # Here we would call Azure DevOps API to get work item details
                    # For now, just include the IDs
                    azdo_context['work_item_ids'] = work_item_matches
                    print_info(f"Found Azure DevOps work items: {', '.join(work_item_matches)}")
                    
                    # In a real implementation, we would use the Azure DevOps Python SDK:
                    # from azure.devops.connection import Connection
                    # from msrest.authentication import BasicAuthentication
                    # credentials = BasicAuthentication('', azdo_config['pat_token'])
                    # connection = Connection(base_url=azdo_config['url'], creds=credentials)
                    # work_item_client = connection.clients.get_work_item_tracking_client()
                    # work_item_details = work_item_client.get_work_item(int(work_item_matches[0]))
                    # azdo_context['work_items'] = [work_item_details]
            except Exception as e:
                print_warning(f"Error getting Azure DevOps context: {e}")
                
        return azdo_context
    
    def _get_github_context(self, branch_name: str) -> Dict[str, Any]:
        """Get GitHub context based on branch name and configuration.
        
        Args:
            branch_name (str): Current git branch name
            
        Returns:
            Dict[str, Any]: GitHub context information if available
        """
        github_context = {}
        
        # Check if GitHub is configured
        github_config = get_github_config()
        if github_config and 'token' in github_config:
            try:
                # Extract GitHub issue numbers from branch name (common format: feature/12-description)
                issue_pattern = r'(?:^|\/)(?:issue-|issue\/|#)?(\d+)(?:-|_|\s|$)'
                issue_matches = re.findall(issue_pattern, branch_name)
                
                if issue_matches:
                    # Here we would call GitHub API to get issue details
                    # For now, just include the issue numbers
                    github_context['issue_numbers'] = issue_matches
                    print_info(f"Found GitHub issues: {', '.join(issue_matches)}")
                    
                    # In a real implementation, we would use the GitHub API:
                    # import requests
                    # headers = {'Authorization': f'token {github_config["token"]}'}
                    # owner = github_config.get('owner', '')
                    # repo = github_config.get('repo', '')
                    # if owner and repo:
                    #     response = requests.get(f'https://api.github.com/repos/{owner}/{repo}/issues/{issue_matches[0]}', headers=headers)
                    #     if response.status_code == 200:
                    #         github_context['issues'] = [response.json()]
            except Exception as e:
                print_warning(f"Error getting GitHub context: {e}")
                
        return github_context
    
    def _get_asana_context(self, branch_name: str) -> Dict[str, Any]:
        """Get Asana context based on branch name and configuration.
        
        Args:
            branch_name (str): Current git branch name
            
        Returns:
            Dict[str, Any]: Asana context information if available
        """
        asana_context = {}
        
        # Check if Asana is configured
        asana_config = get_asana_config()
        if asana_config and 'token' in asana_config and 'workspace' in asana_config:
            try:
                # Extract Asana task IDs from branch name (common Asana format uses UUIDs)
                # Example: feature/1234567890123456-description
                task_pattern = r'(?:^|\/)([0-9a-f]{16})(?:-|_|\s|$)'
                task_matches = re.findall(task_pattern, branch_name)
                
                if task_matches:
                    # Here we would call Asana API to get task details
                    # For now, just include the task IDs
                    asana_context['task_ids'] = task_matches
                    print_info(f"Found Asana tasks: {', '.join(task_matches)}")
                    
                    # In a real implementation, we would use the Asana Python SDK:
                    # import asana
                    # client = asana.Client.access_token(asana_config['token'])
                    # task = client.tasks.find_by_id(task_matches[0])
                    # asana_context['tasks'] = [task]
            except Exception as e:
                print_warning(f"Error getting Asana context: {e}")
                
        return asana_context
   
    def run(self, msg: Optional[str], edit_commit_message: bool, generate_description: bool):
        """Run the post-commit hook.

        This method retrieves the list of modified files from the last commit
        and processes each file. It stages any files that have been modified
        during processing and creates an auto-commit if changes were made. A
        progress bar is displayed to indicate the processing status of each
        file. If there is an error generating the commit summary, an exception
        is raised.

        Args:
            msg (Optional[str]): An optional message to include in the commit.
            edit_commit_message (bool): A flag indicating whether to open the
                git commit edit terminal after committing.
            generate_description (bool): Whether to generate a detailed description

        Raises:
            Exception: If there is an error generating the commit summary.
        """
        summary: dict = self.get_summary(msg, generate_description)
        if not summary:
            raise Exception("Error generating commit summary")
        
        title = summary.get('title', "")
        description = summary.get('description', "")
        
        # Integrate information from all available project management tools
        title, description = self._integrate_ticket_information(title, description, msg)
        
        # commit the changes to the repository with above details
        commit_msg = f"{title}\n\n{description}" if generate_description else title
        self.repo.git.commit('-m', commit_msg)
        print_success(f"Commit: {commit_msg}")
        
        if edit_commit_message:
            # Open the git commit edit terminal
            print_info("Opening git commit edit terminal...")
            self._amend_commit()
    
    def _integrate_ticket_information(self, title: str, description: str, msg: str) -> tuple:
        """
        Integrate ticket information from all available project management tools into the commit message.
        
        Args:
            title: Generated commit title
            description: Generated commit description 
            msg: Original user message
            
        Returns:
            tuple: (updated_title, updated_description) with ticket information
        """
        # Collect ticket references from all available tools
        ticket_references = []
        
        # 1. Process JIRA integration if available
        if self.jira_client and self.jira_client.is_connected():
            jira_tickets = self._process_jira_integration(title, description, msg)
            ticket_references.extend([f"JIRA: {ticket}" for ticket in jira_tickets])
        
        # 2. Process Azure DevOps integration if available
        azdo_tickets = self._process_azdo_integration(title, description, msg)
        ticket_references.extend([f"AB#{ticket}" for ticket in azdo_tickets])  # AB# is Azure Boards prefix
        
        # 3. Process GitHub integration if available
        github_tickets = self._process_github_integration(title, description, msg)
        ticket_references.extend([f"#{ticket}" for ticket in github_tickets])  # # is GitHub issue prefix
        
        # 4. Process Asana integration if available
        asana_tickets = self._process_asana_integration(title, description, msg)
        if asana_tickets:
            ticket_references.extend([f"Asana: {ticket}" for ticket in asana_tickets])
        
        # Format the ticket references in the commit message if any found
        if ticket_references:
            # Update title if no ticket reference is already in the title
            has_reference_in_title = any(ref.split(':')[0].strip() in title for ref in ticket_references)
            if not has_reference_in_title and ticket_references:
                # Add first reference to the title
                title = f"{ticket_references[0]} {title}"
            
            # Add all references to the description
            references_text = "Related tickets: " + ", ".join(ticket_references)
            if description:
                description = f"{description}\n\n{references_text}"
            else:
                description = references_text
        
        return title, description
    
    def _process_jira_integration(self, title: str, description: str, msg: str) -> List[str]:
        """
        Process JIRA integration for the commit message.
        
        Args:
            title: Generated commit title
            description: Generated commit description 
            msg: Original user message that might contain JIRA references
            
        Returns:
            List[str]: List of JIRA issue keys
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
                
        return issue_keys

    def _process_azdo_integration(self, title: str, description: str, msg: str) -> List[str]:
        """
        Process Azure DevOps integration for the commit message.
        
        Args:
            title: Generated commit title
            description: Generated commit description 
            msg: Original user message
            
        Returns:
            List[str]: List of Azure DevOps work item IDs
        """
        # Check Azure DevOps configuration
        work_item_ids = []
        azdo_config = get_azdo_config()
        
        if azdo_config and 'url' in azdo_config and 'project' in azdo_config:
            # Look for work item IDs in commit message and branch name
            # Azure DevOps uses format: #123, AB#123, or workitems/123
            work_item_pattern = r'(?:AB#|#|workitems\/|work items\/|items\/)(\d+)'
            
            # Extract from commit content
            content_to_search = f"{title} {description} {msg}"
            work_item_ids.extend(re.findall(work_item_pattern, content_to_search))
            
            # Also check the branch name
            try:
                current_branch = self.repo.active_branch.name
                branch_work_items = re.findall(r'(?:^|\/)(\d+)(?:-|_|\s|$)', current_branch)
                
                # Add any new IDs found in branch name
                for item_id in branch_work_items:
                    if item_id not in work_item_ids:
                        work_item_ids.append(item_id)
                        print_info(f"Added Azure DevOps work item #{item_id} from branch name: {current_branch}")
            except Exception as e:
                print_warning(f"Could not extract Azure DevOps work items from branch name: {e}")
            
            if work_item_ids:
                print_info(f"Found Azure DevOps work items: {', '.join(work_item_ids)}")
                # In a full implementation, we would update work items here
                
        return work_item_ids
    
    def _process_github_integration(self, title: str, description: str, msg: str) -> List[str]:
        """
        Process GitHub integration for the commit message.
        
        Args:
            title: Generated commit title
            description: Generated commit description 
            msg: Original user message
            
        Returns:
            List[str]: List of GitHub issue numbers
        """
        # Check GitHub configuration
        issue_numbers = []
        github_config = get_github_config()
        
        if github_config and 'token' in github_config:
            # Look for issue numbers in commit message and branch name
            # GitHub uses format: #123, GH-123, or issues/123
            issue_pattern = r'(?:#|GH-|issues\/|issue\/|pull\/|pulls\/)(\d+)'
            
            # Extract from commit content
            content_to_search = f"{title} {description} {msg}"
            issue_numbers.extend(re.findall(issue_pattern, content_to_search))
            
            # Also check the branch name
            try:
                current_branch = self.repo.active_branch.name
                branch_issues = re.findall(r'(?:issue-|issue\/|#)(\d+)', current_branch)
                
                # Add any new numbers found in branch name
                for issue_num in branch_issues:
                    if issue_num not in issue_numbers:
                        issue_numbers.append(issue_num)
                        print_info(f"Added GitHub issue #{issue_num} from branch name: {current_branch}")
            except Exception as e:
                print_warning(f"Could not extract GitHub issues from branch name: {e}")
            
            if issue_numbers:
                print_info(f"Found GitHub issues: {', '.join(issue_numbers)}")
                # In a full implementation, we would add comments to GitHub issues here
                
        return issue_numbers
    
    def _process_asana_integration(self, title: str, description: str, msg: str) -> List[str]:
        """
        Process Asana integration for the commit message.
        
        Args:
            title: Generated commit title
            description: Generated commit description 
            msg: Original user message
            
        Returns:
            List[str]: List of Asana task IDs
        """
        # Check Asana configuration
        task_ids = []
        asana_config = get_asana_config()
        
        if asana_config and 'token' in asana_config:
            # Look for task IDs in commit message and branch name
            # Asana task IDs are typically 16-character hexadecimal strings
            task_pattern = r'(?:asana\/|task\/|tasks\/)([0-9a-f]{16})'
            
            # Extract from commit content
            content_to_search = f"{title} {description} {msg}"
            task_ids.extend(re.findall(task_pattern, content_to_search))
            
            # Also check the branch name
            try:
                current_branch = self.repo.active_branch.name
                branch_tasks = re.findall(r'(?:^|\/)([0-9a-f]{16})(?:-|_|\s|$)', current_branch)
                
                # Add any new IDs found in branch name
                for task_id in branch_tasks:
                    if task_id not in task_ids:
                        task_ids.append(task_id)
                        print_info(f"Added Asana task {task_id} from branch name: {current_branch}")
            except Exception as e:
                print_warning(f"Could not extract Asana tasks from branch name: {e}")
            
            if task_ids:
                print_info(f"Found Asana tasks: {', '.join(task_ids)}")
                # In a full implementation, we would add comments to Asana tasks here
                
        return task_ids

    def _amend_commit(self):
        """Open the default git editor for editing the commit message.

        This function changes the current working directory to the repository
        path, runs the git command to amend the last commit, and opens the
        default editor for the user to modify the commit message. After the
        operation, it returns to the original directory.
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
