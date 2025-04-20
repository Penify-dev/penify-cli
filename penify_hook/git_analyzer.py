import os
import re
from git import Repo
from tqdm import tqdm

from penify_hook.base_analyzer import BaseAnalyzer
from penify_hook.utils import get_repo_details, recursive_search_git_folder
from .api_client import APIClient
import logging
from .ui_utils import (
    print_info, print_success, print_warning, print_error,
    print_processing, print_status, create_progress_bar,
    format_file_path
)

# Set up logger
logger = logging.getLogger(__name__)

class GitDocGenHook(BaseAnalyzer):
    def __init__(self, repo_path: str, api_client: APIClient):
        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        
        Parameters
        ----------
        dictionary : dict
            The processed files map.
        
        Returns
        -------
        bool
            True if successful, False otherwise.
        
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

    def get_modified_files_in_last_commit(self):
        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        
        Parameters
        ----------
        dictionary : dict
            The processed files map.
        
        Returns
        -------
        bool
            True if successful, False otherwise.
        
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
        last_commit = self.repo.head.commit
        modified_files = []
        for diff in last_commit.diff('HEAD~1'):
            if diff.a_path not in modified_files:
                modified_files.append(diff.a_path)
        return modified_files

    def get_modified_lines(self, diff_text):
        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        
        Parameters
        ----------
        dictionary : dict
            The processed files map.
        
        Returns
        -------
        bool
            True if successful, False otherwise.
        
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
        modified_lines = []
        current_line = 0
        deletion_start = None

        for line in diff_text.splitlines():
            if line.startswith('@@'):
                # Parse the hunk header
                _, old, new, _ = line.split(' ', 3)
                current_line = int(new.split(',')[0].strip('+'))
                deletion_start = None
            elif line.startswith('-'):
                # This is a deleted line
                if deletion_start is None:
                    deletion_start = current_line
            elif line.startswith('+'):
                # This is an added line
                modified_lines.append(current_line)
                current_line += 1
                if deletion_start is not None:
                    modified_lines.append(deletion_start)
                    deletion_start = None
            else:
                # This is an unchanged line
                current_line += 1
                if deletion_start is not None:
                    modified_lines.append(deletion_start)
                    deletion_start = None

        # Handle case where deletion is at the end of the file
        if deletion_start is not None:
            modified_lines.append(deletion_start)

        return sorted(set(modified_lines))  # Remove duplicates and sort

    def process_file(self, file_path):
        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        
        Parameters
        ----------
        dictionary : dict
            The processed files map.
        
        Returns
        -------
        bool
            True if successful, False otherwise.
        
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
        file_abs_path = os.path.join(self.repo_path, file_path)
        file_extension = os.path.splitext(file_path)[1].lower()

        if not file_extension:
            logger.info(f"File {file_path} has no extension. Skipping.")
            return False
        
        file_extension = file_extension[1:]  # Remove the leading dot

        if file_extension not in self.supported_file_types:
            logger.info(f"File type {file_extension} is not supported. Skipping {file_path}.")
            return False

        with open(file_abs_path, 'r') as file:
            content = file.read()

        # Get the diff of the file in the last commit
        last_commit = self.repo.head.commit
        prev_commit = last_commit.parents[0] if last_commit.parents else last_commit

        # Use git command to get the diff
        diff_text = self.repo.git.diff(prev_commit.hexsha, last_commit.hexsha, '--', file_path)

        if not diff_text:
            logger.info(f"No changes detected for {file_path}")
            return False

        modified_lines = self.get_modified_lines(diff_text)
        # Send data to API
        response = self.api_client.send_file_for_docstring_generation(file_path, content, modified_lines, self.repo_details)
        if response is None:
            return False
        
        if response == content:
            logger.info(f"No changes detected for {file_path}")
            return False
        # If the response is successful, replace the file content
        with open(file_abs_path, 'w') as file:
            file.write(response)
        logger.info(f"Updated file {file_path} with generated documentation")
        return True

    def run(self):
        """Save the processed files map to a JSON file.
        
        Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
        description of each parameter is optional, but should be included if not obvious.
        
        
        Parameters
        ----------
        dictionary : dict
            The processed files map.
        
        Returns
        -------
        bool
            True if successful, False otherwise.
        
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
        logger.info("Starting doc_gen_hook processing")
        print_info("Starting doc_gen_hook processing")
        
        modified_files = self.get_modified_files_in_last_commit()
        changes_made = False
        total_files = len(modified_files)

        with create_progress_bar(total_files, "Processing files", "file") as pbar:
            for file in modified_files:
                print_processing(file)
                logging.info(f"Processing file: {file}")
                try:
                    if self.process_file(file):
                        # Stage the modified file
                        self.repo.git.add(file)
                        changes_made = True
                        print_status('success', "Documentation updated")
                    else:
                        print_status('warning', "No changes needed")
                except Exception as file_error:
                    error_msg = f"Error processing file [{file}]: {file_error}"
                    logger.error(error_msg)
                    print_status('error', error_msg)
                pbar.update(1)  # Update the progress bar

        # If any file was modified, create a new commit
        if changes_made:
            # self.repo.git.commit('-m', 'Auto-commit: Updated files after doc_gen_hook processing.')
            logger.info("Auto-commit created with changes.")
            print_success("\n✓ Auto-commit created with changes")
        else:
            logger.info("doc_gen_hook complete. No changes made.")
            print_info("\n✓ doc_gen_hook complete. No changes made.")