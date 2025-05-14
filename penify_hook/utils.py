import logging
import os
import re

from git import Repo
logger = logging.getLogger(__name__)


class GitRepoNotFoundError(Exception):
    pass


def get_repo_details(repo: Repo):
    """Determine the details of a repository including its remote URL, hosting
    service, organization name, and repository name.
    
    This function extracts the remote URL from the given Git repository object and
    determines the hosting service (e.g., GitHub, Azure DevOps, Bitbucket, GitLab).
    It then parses the URL to extract the organization name and repository name. If
    the URL does not match any known hosting service pattern, it sets the hosting
    service as "Unknown". The function handles exceptions that may occur during
    this process and logs an error message if needed.
    
    Args:
        repo (Repo): A GitPython Repo object representing the local git repository.
    
    Returns:
        dict: A dictionary containing the organization name, repository name, and hosting
            service.
    """
    remote_url = None
    hosting_service = "Unknown"
    org_name = None
    repo_name = None

    try:
        # Get the remote URL
        remote = repo.remotes.origin.url
        remote_url = remote

        # Determine the hosting service based on the URL
        if "github.com" in remote:
            hosting_service = "GITHUB"
            match = re.match(r".*github\.com[:/](.*?)/(.*?)(\.git)?$", remote)
        elif "dev.azure.com" in remote:
            hosting_service = "AZUREDEVOPS"
            match = re.match(r".*dev\.azure\.com/(.*?)/(.*?)/_git/(.*?)(\.git)?$", remote)
        elif "visualstudio.com" in remote:
            hosting_service = "AZUREDEVOPS"
            match = re.match(r".*@(.*?)\.visualstudio\.com/(.*?)/_git/(.*?)(\.git)?$", remote)
        elif "bitbucket.org" in remote:
            hosting_service = "BITBUCKET"
            match = re.match(r".*bitbucket\.org[:/](.*?)/(.*?)(\.git)?$", remote)
        elif "gitlab.com" in remote:
            hosting_service = "GITLAB"
            match = re.match(r".*gitlab\.com[:/](.*?)/(.*?)(\.git)?$", remote)
        else:
            hosting_service = "Unknown Hosting Service"
            match = None

        if match:
            org_name = match.group(1)
            repo_name = match.group(2)
            
            # For Azure DevOps, adjust the group indices
            if hosting_service == "AZUREDEVOPS":
                repo_name = match.group(3)

    except Exception as e:
        logger.error(f"Error determining GIT provider: {e}")

    return {
        "organization_name": org_name,
        "repo_name": repo_name,
        "vendor": hosting_service
    }

def recursive_search_git_folder(folder_path):
    """Recursively searches for a .git folder starting from the given directory."""
    if os.path.isdir(folder_path):
        if '.git' in os.listdir(folder_path):
            return folder_path
        # reached the root of the filesystem
        elif folder_path == os.path.dirname(folder_path):
            return None
        else:
            return recursive_search_git_folder(os.path.dirname(folder_path))
        
def find_git_parent(path):

    """Traverse up from the given path to find the nearest directory containing a .git
    subdirectory."""
    current_dir = os.path.abspath(path)

    while current_dir != os.path.dirname(current_dir):  # Traverse up to the root directory
        if os.path.isdir(os.path.join(current_dir, ".git")):
            return current_dir  # Return the parent folder containing the .git directory
        current_dir = os.path.dirname(current_dir)
    
    raise GitRepoNotFoundError(f"No Git repository found in the path or any of its parent directories: {path}")
