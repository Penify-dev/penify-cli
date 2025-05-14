import os
import sys
from git import Repo
from tqdm import tqdm
import time

from penify_hook.base_analyzer import BaseAnalyzer
from penify_hook.utils import get_repo_details, recursive_search_git_folder
from .api_client import APIClient
import logging
from .ui_utils import (
    format_highlight, print_info, print_success, print_warning, print_error,
    print_status, create_stage_progress_bar,
    update_stage, format_file_path
)

# Set up logger
logger = logging.getLogger(__name__)

class FileAnalyzerGenHook(BaseAnalyzer):
    def __init__(self, file_path: str, api_client: APIClient):
        self.file_path = file_path
        super().__init__(file_path, api_client)
        


    def process_file(self, file_path, pbar, new_param: str = ""):
        """Processes a file by validating its extension, reading content,
        generating documentation, and writing changes back to the file.  The function
        performs several stages of processing: 1. Validates the file's extension to
        ensure it is supported. 2. Reads the content of the file. 3. Sends the file
        content for documentation generation. 4. Writes the generated documentation
        back to the file if there are changes.
        
        Args:
            file_path (str): The path of the file to be processed.
            pbar (tqdm.tqdm): A progress bar object to update the status of processing stages.
            new_param (str?): An additional parameter for future use. Defaults to an empty string."""
        file_abs_path = os.path.join(os.getcwd(), file_path)
        file_extension = os.path.splitext(file_path)[1].lower()
        
        # --- STAGE 1: Validating ---
        update_stage(pbar, "Validating")        
        if not file_extension:
            print_warning(f"  Empty extension is not supported. Skipping '{self.relative_file_path}'.")
            return False
        
        file_extension = file_extension[1:]  # Remove the leading dot

        if file_extension not in self.supported_file_types:
            print_warning(f"  File type '{file_extension}' is not supported. Skipping '{self.relative_file_path}'.")
            return False

        # Update progress bar to indicate we're moving to next stage
        pbar.update(1)
        
        # --- STAGE 2: Reading content ---
        update_stage(pbar, "Reading content")        
        try:
            with open(file_abs_path, 'r') as file:
                content = file.read()
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            return False

        modified_lines = [i for i in range(len(content.splitlines()))]
        
        # Update progress bar to indicate we're moving to next stage
        pbar.update(1)
        
        # --- STAGE 3: Documenting ---
        update_stage(pbar, "Documenting")
        
        response = self.api_client.send_file_for_docstring_generation(self.relative_file_path, content, modified_lines, self.repo_details)
        
        if response is None:
            return False
            
        if response == content:
            logger.info(f"No changes needed for {file_path}")
            return False
        
        # Update progress bar to indicate we're moving to next stage
        pbar.update(1)
        
        # --- STAGE 4: Writing changes ---
        update_stage(pbar, "Writing changes")
        
        try:
            with open(file_abs_path, 'w') as file:
                file.write(response)
            logger.info(f"Updated file {file_path} with generated documentation")
            
            # Mark final stage as complete
            pbar.update(1)
            return True
        except Exception as e:
            logger.error(f"Error writing file {file_path}: {str(e)}")
            return False
    
    def print_processing(self, file_path):
        """Prints a message indicating that a file is being processed."""
        formatted_path = format_file_path(file_path)
        print(f"\n{format_highlight(f'Processing file: {formatted_path}')}")

    def run(self):
        
        # Create a progress bar with appropriate stages
        """Runs the documentation process with a progress bar.
        
        This method orchestrates the documentation process by creating a progress bar,
        processing the file, and handling exceptions to ensure the progress bar
        completes properly. It updates the progress bar through various stages and
        provides feedback based on the result of the file processing.
        """
        stages = ["Validating", "Reading content", "Documenting", "Writing changes", "Completed"]
        pbar, _ = create_stage_progress_bar(stages, f"Starting documenting")
        
        try:
            # Print a clear indication of which file is being processed
            # self.print_processing(self.file_path)
            
            # Process the file
            result = self.process_file(self.file_path, pbar)
            
            # Ensure all stages are completed
            remaining_steps = len(stages) - pbar.n
            pbar.update(remaining_steps)
            
                
            # Display appropriate message based on result
            remaining = len(stages) - pbar.n
            if remaining > 0:
                pbar.update(remaining)
            update_stage(pbar, "Complete")
            pbar.clear()
            pbar.close()
                
        except Exception as e:
            remaining = len(stages) - pbar.n
            if remaining > 0:
                pbar.update(remaining)
            update_stage(pbar, "Complete")
            pbar.clear()
            pbar.close()
            print_status('error', e)
            sys.exit(1)
            
            # Ensure progress bar completes even on error
        if result:
            print_success(f"\n✓ Documentation updated for {self.relative_file_path}")
        else:
            print_success(f"\n✓ No changes needed for {self.relative_file_path}")
                
