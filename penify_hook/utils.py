import logging
import os
import re

from git import Repo
logger = logging.getLogger(__name__)


class GitRepoNotFoundError(Exception):
    pass


def get_repo_details(repo: Repo):
    """Get details of a Git repository, including its hosting service,
    organization name, and repository name.

    This function extracts these details from the remote URL of the provided
    Git repository. It supports popular platforms like GitHub, Azure DevOps,
    Bitbucket, and GitLab. If the hosting service cannot be determined, it
    defaults to "Unknown Hosting Service".

    Args:
        repo (Repo): The GitPython Repo object representing the repository.

    Returns:
        dict: A dictionary containing keys for 'organization_name', 'repo_name', and
            'vendor' which represent the organization name, repository name, and
            hosting service respectively.
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
    """Recursively search for the .git folder in the specified directory and
    return its parent directory.

    Args:
        folder_path (str): The path of the directory to search for the .git folder.

    Returns:
        str: The path of the directory containing the .git folder. If no .git folder
            is found, returns None.
    """
    if os.path.isdir(folder_path):
        if '.git' in os.listdir(folder_path):
            return folder_path
        # reached the root of the filesystem
        elif folder_path == os.path.dirname(folder_path):
            return None
        else:
            return recursive_search_git_folder(os.path.dirname(folder_path))
        
def find_git_parent(path):
    """Find the parent directory of a Git repository.

    This function traverses up the directory structure from the given path
    to locate the nearest parent directory that contains a `.git` folder. If
    such a directory is found, it returns the path to that directory. If no
    Git repository is found in the specified path or any of its parent
    directories, it raises a custom exception.

    Args:
        path (str): The path from which to start searching for the Git repository.

    Returns:
        str: The absolute path to the parent directory containing the `.git` folder.

    Raises:
        GitRepoNotFoundError: If no Git repository is found in the specified path or any of its parent
            directories.
    """

    current_dir = os.path.abspath(path)

    while current_dir != os.path.dirname(current_dir):  # Traverse up to the root directory
        if os.path.isdir(os.path.join(current_dir, ".git")):
            return current_dir  # Return the parent folder containing the .git directory
        current_dir = os.path.dirname(current_dir)
    
    raise GitRepoNotFoundError(f"No Git repository found in the path or any of its parent directories: {path}")
