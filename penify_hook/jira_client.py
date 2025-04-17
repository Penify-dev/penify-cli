import re
import logging
from typing import Optional, Dict, List, Any

from penify_hook.ui_utils import print_info, print_success
try:
    from jira import JIRA
    JIRA_AVAILABLE = True
except ImportError:
    JIRA_AVAILABLE = False
    
class JiraClient:
    """
    Client for interacting with JIRA API
    """
    
    def __init__(self, jira_url: str = None, jira_user: str = None, jira_api_token: str = None):
        """Initialize the JIRA client.
        
        Args:
            jira_url (str): Base URL for JIRA instance (e.g., "https://your-domain.atlassian.net")
            jira_user (str): JIRA username or email
            jira_api_token (str): JIRA API token
        """
        self.jira_url = jira_url
        self.jira_user = jira_user
        self.jira_api_token = jira_api_token
        self.jira_client = None
        
        if not JIRA_AVAILABLE:
            logging.warning("JIRA package not available. JIRA integration will not work.")
            return
        
        if jira_url and jira_user and jira_api_token:
            try:
                self.jira_client = JIRA(
                    server=jira_url,
                    basic_auth=(jira_user, jira_api_token)
                )
                logging.info("JIRA client initialized successfully")
            except Exception as e:
                logging.error(f"Failed to initialize JIRA client: {e}")
                self.jira_client = None
    
    def is_connected(self) -> bool:
        """Check if the JIRA client is connected.
        
        This function verifies whether the JIRA client has successfully established a connection. It returns `True` if the
        client is connected, and `False` otherwise.
        
        Returns:
            bool: True if the JIRA client is connected, False otherwise
        """
        return self.jira_client is not None
    
    def extract_issue_keys_from_branch(self, branch_name: str) -> List[str]:
        # Common JIRA issue key pattern: PROJECT-123
        """Extracts JIRA issue keys from a branch name.
        
        This function searches through a given git branch name to find and return any JIRA issue keys that match the pattern.
        Common conventions for JIRA issue keys in branch names include: - feature/PROJECT-123-description -
        bugfix/PROJECT-123-fix-something - hotfix/PROJECT-123/short-desc
        
        Args:
            branch_name (str): The name of the git branch to search for JIRA issue keys.
        
        Returns:
            List[str]: A list of unique JIRA issue keys found in the branch name.
        
        Examples:
            extract_issue_keys_from_branch("feature/PROJ-456-add-new-feature")
            # Output: ['PROJ-456']
        """
        pattern = r'[A-Z][A-Z0-9_]+-[0-9]+'
        matches = re.findall(pattern, branch_name)
        if matches:
            print_info(f"Fetching relevant JIRA issues")
        return list(set(matches))  # Remove duplicates
    
    def extract_issue_keys(self, text: str) -> List[str]:
        # Common JIRA issue key pattern: PROJECT-123
        """Extract JIRA issue keys from a given text.
        
        This function searches through the provided text to find and return all unique JIRA issue keys. A JIRA issue key
        typically follows the pattern of PROJECT-123, where PROJECT is alphanumeric and consists of at least one uppercase
        letter followed by one or more alphanumeric characters, and 123 is a numeric sequence.
        
        Args:
            text (str): The text in which to search for JIRA issue keys.
        
        Returns:
            List[str]: A list of unique JIRA issue keys found in the text.
        """
        pattern = r'[A-Z][A-Z0-9_]+-[0-9]+'
        matches = re.findall(pattern, text)
        return list(set(matches))  # Remove duplicates
    
    def get_issue_details(self, issue_key: str) -> Optional[Dict[str, Any]]:
        """Retrieve details of a JIRA issue based on its key.
        
        This function fetches detailed information about a specified JIRA issue using the provided issue key.  It checks if the
        JIRA client is connected before attempting to retrieve the issue. If the client is not connected,  it logs a warning and
        returns `None`. The function then attempts to fetch the issue from the JIRA server and constructs  a dictionary
        containing various details about the issue such as its key, summary, status, description, assignee, reporter,  type,
        priority, and URL. If any errors occur during this process, they are logged, and `None` is returned.
        
        Args:
            issue_key (str): The JIRA issue key (e.g., "PROJECT-123").
        
        Returns:
            Dict[str, Any] or None: A dictionary containing the details of the JIRA issue if found, otherwise `None`.
        """
        if not self.is_connected():
            logging.warning("JIRA client not connected")
            return None
        
        try:
            issue = self.jira_client.issue(issue_key)
            return {
                'key': issue.key,
                'summary': issue.fields.summary,
                'status': issue.fields.status.name,
                'description': issue.fields.description,
                'assignee': issue.fields.assignee.displayName if issue.fields.assignee else None,
                'reporter': issue.fields.reporter.displayName if issue.fields.reporter else None,
                'type': issue.fields.issuetype.name,
                'priority': issue.fields.priority.name if hasattr(issue.fields, 'priority') and issue.fields.priority else None,
                'url': f"{self.jira_url}/browse/{issue.key}"
            }
        except Exception as e:
            logging.error(f"Error fetching issue {issue_key}: {e}")
            return None
    
    def add_comment(self, issue_key: str, comment: str) -> bool:
        """Add a comment to a JIRA issue.
        
        Args:
            issue_key (str): The JIRA issue key, e.g., "PROJECT-123".
            comment (str): The text of the comment to be added.
        
        Returns:
            bool: True if the comment was added successfully, False otherwise.
        """
        if not self.is_connected():
            logging.warning("JIRA client not connected")
            return False
        
        try:
            self.jira_client.add_comment(issue_key, comment)
            logging.info(f"Comment added to {issue_key}")
            return True
        except Exception as e:
            logging.error(f"Error adding comment to {issue_key}: {e}")
            return False
    
    def update_issue_status(self, issue_key: str, transition_name: str) -> bool:
        """Update the status of a JIRA issue.
        
        This function updates the status of a specified JIRA issue by transitioning it to a new state based on the provided
        transition name. It first checks if the JIRA client is connected and then attempts to find the appropriate transition ID
        from the available transitions. If found, it applies the transition and logs the update. If any errors occur during the
        process, it logs an error message.
        
        Args:
            issue_key (str): The key of the JIRA issue to be updated.
            transition_name (str): The name of the desired transition.
        
        Returns:
            bool: True if the status was successfully updated, False otherwise.
        """
        if not self.is_connected():
            logging.warning("JIRA client not connected")
            return False
        
        try:
            # Get available transitions
            transitions = self.jira_client.transitions(issue_key)
            
            # Find the transition ID based on name
            transition_id = None
            for t in transitions:
                if t['name'].lower() == transition_name.lower():
                    transition_id = t['id']
                    break
            
            if transition_id:
                self.jira_client.transition_issue(issue_key, transition_id)
                logging.info(f"Updated {issue_key} status to {transition_name}")
                return True
            else:
                logging.warning(f"Transition '{transition_name}' not found for {issue_key}")
                return False
                
        except Exception as e:
            logging.error(f"Error updating status for {issue_key}: {e}")
            return False
            
    def format_commit_message_with_jira_info(self, commit_title: str, commit_description: str, issue_keys: List[str] = None) -> tuple:
        # If no issue keys provided, extract them from title and description
        """Format commit message with JIRA issue information.
        
        Args:
            commit_title (str): The original commit title.
            commit_description (str): The original commit description.
            issue_keys (List[str]?): A list of JIRA issue keys to include in the commit message. If not
                provided, issue keys will be extracted from both the title and the
                description.
        
        Returns:
            tuple: A tuple containing the updated commit title and description with JIRA
                information included.
        """
        if not issue_keys:
            title_keys = self.extract_issue_keys(commit_title)
            desc_keys = self.extract_issue_keys(commit_description)
            issue_keys = list(set(title_keys + desc_keys))
            
        if not issue_keys or not self.is_connected():
            return commit_title, commit_description
            
        # Format the title to include the issue key if not already there
        updated_title = commit_title
        if issue_keys and not any(key in commit_title for key in issue_keys):
            # Add the first issue key to the title
            updated_title = f"{issue_keys[0]}: {commit_title}"
            
        # Add issue details to the description
        updated_description = commit_description
        
        issue_details_section = "\n\n## Related JIRA Issues\n\n"
        has_issue_details = False
        
        for issue_key in issue_keys:
            details = self.get_issue_details(issue_key)
            if details:
                has_issue_details = True
                issue_details_section += (
                    f"* **[{details['key']}]({details['url']})**: {details['summary']}\n"
                    f"  * Status: {details['status']}\n"
                    f"  * Type: {details['type']}\n"
                )
                
        if has_issue_details:
            updated_description += issue_details_section
            
        return updated_title, updated_description

    def get_detailed_issue_context(self, issue_key: str) -> Dict[str, Any]:
        """Retrieve comprehensive details about a JIRA issue including context for better commit messages.
        
        This function fetches detailed information from a specified JIRA issue and constructs a dictionary containing various
        context fields such as the issue summary, description, type, status, priority, comments, URL, and additional custom
        fields like acceptance criteria and sprint information. If any errors occur during the fetching process, appropriate
        warnings or errors are logged.
        
        Args:
            issue_key (str): The JIRA issue key (e.g., "PROJECT-123").
        
        Returns:
            Dict[str, Any]: A dictionary containing business and technical context from the issue.
        """
        if not self.is_connected():
            logging.warning("JIRA client not connected")
            return {}
        
        try:
            issue = self.jira_client.issue(issue_key)
            
            # Get issue history and comments for context
            comments = []
            try:
                for comment in self.jira_client.comments(issue):
                    comments.append(comment.body)
            except Exception as e:
                logging.warning(f"Could not fetch comments for {issue_key}: {e}")
            
            # Build a comprehensive context object
            context = {
                'key': issue.key,
                'summary': issue.fields.summary,
                'description': issue.fields.description or "",
                'type': issue.fields.issuetype.name,
                'status': issue.fields.status.name,
                'priority': issue.fields.priority.name if hasattr(issue.fields, 'priority') and issue.fields.priority else "None",
                'comments': comments[:3],  # Limit to latest 3 comments
                'url': f"{self.jira_url}/browse/{issue.key}"
            }
            
            # Add acceptance criteria if available (common custom fields)
            # Field names may vary by JIRA instance
            acceptance_criteria = None
            try:
                for field_name in ['customfield_10001', 'acceptance_criteria', 'customfield_10207']:
                    if hasattr(issue.fields, field_name):
                        field_value = getattr(issue.fields, field_name)
                        if field_value:
                            acceptance_criteria = field_value
                            break
            except Exception:
                pass
                
            if acceptance_criteria:
                context['acceptance_criteria'] = acceptance_criteria
                
            # Try to extract sprint information
            try:
                sprint_field = None
                for field_name in dir(issue.fields):
                    if 'sprint' in field_name.lower():
                        sprint_field = field_name
                        break
                
                if sprint_field:
                    sprint_value = getattr(issue.fields, sprint_field)
                    if sprint_value:
                        if isinstance(sprint_value, list) and len(sprint_value) > 0:
                            context['sprint'] = sprint_value[0]
                        else:
                            context['sprint'] = str(sprint_value)
            except Exception as e:
                logging.debug(f"Could not extract sprint information: {e}")
            
            return context
            
        except Exception as e:
            logging.error(f"Error fetching detailed information for {issue_key}: {e}")
            return {}

    def get_commit_context_from_issues(self, issue_keys: List[str]) -> Dict[str, Any]:
        """Gather contextual information from JIRA issues to improve commit messages.
        
        This function processes a list of JIRA issue keys, retrieves detailed context for each issue, and aggregates it into a
        dictionary that can be used to enhance commit messages. It first retrieves the primary issue (the first key in the list)
        and then gathers basic details for any related issues. The resulting context includes information from both the primary
        and related issues, along with all issue keys.
        
        Args:
            issue_keys: List of JIRA issue keys to gather information from
        
        Returns:
            Dict containing business and technical context from the issues
        """
        if not issue_keys or not self.is_connected():
            return {}
            
        # Get the primary issue (first in the list)
        primary_issue = self.get_detailed_issue_context(issue_keys[0])
        
        # Get basic info for related issues
        related_issues = []
        for key in issue_keys[1:]:  # Skip the first one as it's the primary
            details = self.get_issue_details(key)
            if details:
                related_issues.append(details)
                
        # Build context dictionary for commit message enhancement
        context = {
            'primary_issue': primary_issue,
            'related_issues': related_issues,
            'all_keys': issue_keys
        }
        
        return context

    def enhance_commit_message(self, title: str, description: str, issue_keys: List[str]) -> tuple:
        """Enhance a commit message with business and technical context from JIRA issues.
        
        Args:
            title (str): Original commit title.
            description (str): Original commit description.
            issue_keys (List[str]): List of JIRA issue keys to include in the enhanced commit message.
        
        Returns:
            tuple: A tuple containing the enhanced commit title and description with added context from JIRA issues.
        """
        if not issue_keys or not self.is_connected():
            return title, description
            
        # Get context information from issues
        context = self.get_commit_context_from_issues(issue_keys)
        if not context or not context.get('primary_issue'):
            return self.format_commit_message_with_jira_info(title, description, issue_keys)
        
        # Get primary issue
        primary = context['primary_issue']
        
        # Enhance title with primary issue key and summary if not already included
        enhanced_title = title
        if not any(key in title for key in issue_keys):
            key = primary['key']
            # Keep original title, but prefix with issue key
            enhanced_title = f"{key}: {title}"
        
        # Enhance description with business and technical context
        enhanced_description = description
        
        # Add business context section
        business_section = "\n\n## Business Context\n\n"
        business_section += f"**Issue**: [{primary['key']}]({primary['url']}) - {primary['summary']}\n"
        business_section += f"**Type**: {primary['type']}\n"
        business_section += f"**Status**: {primary['status']}\n"
        business_section += f"**Priority**: {primary['priority']}\n"
        
        if 'sprint' in primary:
            business_section += f"**Sprint**: {primary['sprint']}\n"
            
        if 'acceptance_criteria' in primary:
            business_section += f"\n**Acceptance Criteria**:\n{primary['acceptance_criteria']}\n"
            
        if primary.get('description'):
            # Include a condensed version of the description if it's not too long
            desc = primary['description']
            if len(desc) > 300:
                desc = desc[:300] + "..."
            business_section += f"\n**Issue Description**:\n{desc}\n"
        
        # Add technical context from comments if available
        if primary.get('comments'):
            tech_section = "\n## Technical Notes\n\n"
            
            # Extract technical details from comments (often devs discuss implementation details here)
            for comment in primary['comments']:
                if len(comment) > 200:  # Only include shorter technical notes
                    comment = comment[:200] + "..."
                tech_section += f"- {comment}\n\n"
            
            if len(tech_section) > 50:  # Only add if there's substantial content
                enhanced_description += business_section + tech_section
            else:
                enhanced_description += business_section
        else:
            enhanced_description += business_section
            
        # Add related issues section
        if context.get('related_issues'):
            related_section = "\n## Related Issues\n\n"
            for issue in context['related_issues']:
                related_section += f"- [{issue['key']}]({issue['url']}): {issue['summary']} ({issue['status']})\n"
            
            enhanced_description += related_section
            
        return enhanced_title, enhanced_description
