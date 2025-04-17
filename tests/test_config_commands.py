import os
import json
import pytest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path

from penify_hook.commands.config_commands import (
    get_penify_config, 
    get_llm_config, 
    get_jira_config, 
    save_llm_config, 
    save_jira_config,
    get_token
)

class TestConfigCommands:
    
    @patch('penify_hook.commands.config_commands.recursive_search_git_folder')  # Updated patch path here
    @patch('penify_hook.commands.config_commands.Path')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_penify_config_existing_dir(self, mock_file_open, mock_makedirs, mock_path, mock_git_folder):

        # Mock git folder search
        """Test the get_penify_config function when the .penify config directory exists.
        
        It should not create a new directory and assert that all mocked functions were called correctly.
        
        Args:
            mock_file_open (MagicMock): A MagicMock object simulating the open() function.
            mock_makedirs (MagicMock): A MagicMock object simulating the os.makedirs() function.
            mock_path (MagicMock): A MagicMock object simulating the Path class from pathlib module.
            mock_git_folder (MagicMock): A MagicMock object simulating the git_folder_search() function.
        """
        mock_git_folder.return_value = '/mock/git/folder'
        
        # Mock Path operations
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.__truediv__.return_value = mock_path_instance
        
        # Path exists for .penify dir
        mock_path_instance.exists.return_value = True
        
        # Call function
        result = get_penify_config()
        
        # Assertions
        mock_git_folder.assert_called_once_with(os.getcwd())
        mock_path.assert_called_once_with('/mock/git/folder')
        mock_path_instance.__truediv__.assert_called_with('.penify')
        assert mock_makedirs.call_count == 0  # Should not create directory
        
    @patch('penify_hook.utils.recursive_search_git_folder')
    @patch('penify_hook.commands.config_commands.Path')
    @patch('os.makedirs')
    @patch('builtins.open', new_callable=mock_open)
    def test_get_penify_config_new_dir(self, mock_file_open, mock_makedirs, mock_path, mock_git_folder):

        # Mock git folder search
        """Test the behavior of get_penify_config when the .penify directory does not exist.
        
        Mock various system calls to simulate a scenario where the .penify directory is not present. Assert that the appropriate
        actions are taken to create the directory and write an empty JSON file.
        
        Args:
            mock_file_open (MagicMock): A MagicMock object simulating the `open` function.
            mock_makedirs (MagicMock): A MagicMock object simulating the `os.makedirs` function.
            mock_path (MagicMock): A MagicMock object simulating the `Path` class from `pathlib`.
            mock_git_folder (MagicMock): A MagicMock object simulating a git folder search function.
        """
        mock_git_folder.return_value = '/mock/git/folder'
        
        # Mock Path operations
        mock_path_instance = MagicMock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.__truediv__.return_value = mock_path_instance
        
        # Path doesn't exist for .penify dir
        mock_path_instance.exists.side_effect = [False, False]
        
        # Call function
        result = get_penify_config()
        
        # Assertions
        mock_makedirs.assert_called_with(mock_path_instance, exist_ok=True)
        mock_file_open.assert_called_once()
        mock_file_open().write.assert_called_once_with('{}')
        
    @patch('penify_hook.commands.config_commands.get_penify_config')
    @patch('builtins.open', new_callable=mock_open, read_data='{"llm": {"model": "gpt-4", "api_base": "https://api.openai.com", "api_key": "test-key"}}')
    def test_get_llm_config_exists(self, mock_file_open, mock_get_config):

        # Setup mock
        """Test the get_llm_config function when the configuration file exists.
        
        This function sets up a mock configuration file that exists and returns it when called. It then calls the get_llm_config
        function and asserts that it returns the correct configuration dictionary. Additionally, it checks that the
        mock_file_open function was called with the correct arguments.
        
        Args:
            mock_file_open (MagicMock): A mock for the open() function.
            mock_get_config (MagicMock): A mock for the get_config() function.
        """
        mock_config_file = MagicMock()
        mock_config_file.exists.return_value = True
        mock_get_config.return_value = mock_config_file
        
        # Call function
        result = get_llm_config()
        
        # Assertions
        assert result == {
            'model': 'gpt-4', 
            'api_base': 'https://api.openai.com', 
            'api_key': 'test-key'
        }
        mock_file_open.assert_called_once_with(mock_config_file, 'r')
        
    @patch('penify_hook.commands.config_commands.get_penify_config')
    @patch('builtins.open', new_callable=mock_open, read_data='{}')
    def test_get_llm_config_empty(self, mock_file_open, mock_get_config):

        # Setup mock
        """Test the behavior of get_llm_config when called with an empty configuration file.
        
        This function sets up a mock configuration file that exists but returns no content. It then calls the `get_llm_config`
        function and asserts that it returns an empty dictionary and that the file open method was called exactly once with the
        correct arguments.
        
        Args:
            mock_file_open (MagicMock): A MagicMock object simulating the built-in open function.
            mock_get_config (MagicMock): A MagicMock object simulating the get_config function.
        """
        mock_config_file = MagicMock()
        mock_config_file.exists.return_value = True
        mock_get_config.return_value = mock_config_file
        
        # Call function
        result = get_llm_config()
        
        # Assertions
        assert result == {}
        mock_file_open.assert_called_once_with(mock_config_file, 'r')
        
    @patch('penify_hook.commands.config_commands.get_penify_config')
    @patch('builtins.open', new_callable=mock_open, read_data='invalid json')
    @patch('builtins.print')
    def test_get_llm_config_invalid_json(self, mock_print, mock_file_open, mock_get_config):

        # Setup mock
        """Test function to verify the behavior of get_llm_config when reading an invalid JSON file.
        
        It sets up a mock configuration file that exists but contains invalid JSON. The function is expected to handle this
        gracefully by printing an error message and returning an empty dictionary.
        """
        mock_config_file = MagicMock()
        mock_config_file.exists.return_value = True
        mock_get_config.return_value = mock_config_file
        
        # Call function
        result = get_llm_config()
        
        # Assertions
        assert result == {}
        mock_print.assert_called_once()
        assert 'Error reading .penify config file' in mock_print.call_args[0][0]
        
    @patch('penify_hook.commands.config_commands.get_penify_config')
    @patch('builtins.open', new_callable=mock_open, read_data='{"jira": {"url": "https://jira.example.com", "username": "user", "api_token": "token"}}')
    def test_get_jira_config_exists(self, mock_file_open, mock_get_config):

        # Setup mock
        """Test that get_jira_config returns the correct JIRA configuration when
        the configuration file exists.  This function sets up a mock for the configuration file to simulate its existence and
        verifies that the function reads from the correct file and returns the expected JIRA configuration dictionary. It also
        checks that the mock file open is called with the appropriate arguments.
        
        Args:
            mock_file_open (MagicMock): A mock for the `open` function.
            mock_get_config (MagicMock): A mock for the `get_config` function, which is expected to return a mock
                configuration file object.
        
        Returns:
            None: This test function does not explicitly return anything. Its assertions serve as the verification of its correctness.
        """
        mock_config_file = MagicMock()
        mock_config_file.exists.return_value = True
        mock_get_config.return_value = mock_config_file
        
        # Call function
        result = get_jira_config()
        
        # Assertions
        assert result == {
            'url': 'https://jira.example.com',
            'username': 'user', 
            'api_token': 'token'
        }
        mock_file_open.assert_called_once_with(mock_config_file, 'r')
        
    @patch('penify_hook.commands.config_commands.get_penify_config')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('builtins.print')
    def test_save_llm_config_success(self, mock_print, mock_json_dump, mock_file_open, mock_get_config):

        # Setup mock
        """Test the save_llm_config function successfully.
        
        This function tests that the save_llm_config function correctly saves an LLM configuration and handles various mock
        objects and side effects. It ensures that the function returns True upon successful execution, writes the expected
        configuration to a file, and prints a confirmation message.
        
        Args:
            mock_print (MagicMock): A mock object for the print function.
            mock_json_dump (MagicMock): A mock object for json.dump.
            mock_file_open (MagicMock): A mock object for file opening.
            mock_get_config (MagicMock): A mock object to return a configuration file mock.
        """
        mock_config_file = MagicMock()
        mock_get_config.return_value = mock_config_file
        mock_file_open.return_value.__enter__.return_value = mock_file_open
        
        # Mock json.load to return empty dict when reading
        with patch('json.load', return_value={}):
            # Call function
            result = save_llm_config("gpt-4", "https://api.openai.com", "test-key")
            
            # Assertions
            assert result == True
            mock_json_dump.assert_called_once()
            expected_config = {
                'llm': {
                    'model': 'gpt-4',
                    'api_base': 'https://api.openai.com',
                    'api_key': 'test-key'
                }
            }
            assert mock_json_dump.call_args[0][0] == expected_config
            mock_print.assert_called_once()
            assert 'configuration saved' in mock_print.call_args[0][0]
        
    @patch('penify_hook.commands.config_commands.get_penify_config')
    @patch('builtins.open', side_effect=IOError("Permission denied"))
    @patch('builtins.print')
    def test_save_llm_config_failure(self, mock_print, mock_file_open, mock_get_config):

        # Setup mock
        """Test function to verify that the save_llm_config function returns False and prints an error message when it fails to
        save the LLM configuration due to a permission error.
        
        It sets up a mock configuration file that exists and calls the save_llm_config function with valid parameters. The
        function is expected to return False and print "Error saving LLM configuration: Permission denied" in case of a failure.
        
        Args:
            self (TestLLMConfig): An instance of the test class.
            mock_print (MagicMock): A MagicMock object representing the print function, which will be used to assert that it was called with the expected
                error message.
            mock_file_open (MagicMock): A MagicMock object representing the open function, which is not used in this test but is included as a parameter for
                completeness.
            mock_get_config (MagicMock): A MagicMock object representing the get_config function, which will be used to return the mock configuration file.
        """
        mock_config_file = MagicMock()
        mock_config_file.exists.return_value = True
        mock_get_config.return_value = mock_config_file
    
        # Call function
        result = save_llm_config("gpt-4", "https://api.openai.com", "test-key")
        
        # Assert
        assert result is False
        mock_print.assert_called_with("Error saving LLM configuration: Permission denied")
        
    @patch('penify_hook.commands.config_commands.Path')
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    @patch('builtins.print')
    def test_save_jira_config_success(self, mock_print, mock_json_dump, mock_file_open, mock_path):

        # Setup mock
        """Test the save_jira_config function to ensure it saves JIRA configuration successfully.
        
        This function sets up mocks for various dependencies and tests the functionality of saving a JIRA configuration.  It
        asserts that the function returns `True`, the JSON dump is called with the correct configuration,  and the print
        statement contains the expected message.
        
        Args:
            mock_print (MagicMock): Mock for the print function.
            mock_json_dump (MagicMock): Mock for the json.dump function.
            mock_file_open (MagicMock): Mock for the open function.
            mock_path (MagicMock): Mock for the path module.
        """
        mock_home_dir = MagicMock()
        mock_path.home.return_value = mock_home_dir
        mock_home_dir.__truediv__.return_value = mock_home_dir
        mock_home_dir.exists.return_value = True
        
        # Mock json.load to return empty dict when reading
        with patch('json.load', return_value={}):
            # Call function
            result = save_jira_config("https://jira.example.com", "user", "token")
            
            # Assertions
            assert result == True
            mock_json_dump.assert_called_once()
            expected_config = {
                'jira': {
                    'url': 'https://jira.example.com',
                    'username': 'user',
                    'api_token': 'token'
                }
            }
            assert mock_json_dump.call_args[0][0] == expected_config
            mock_print.assert_called_once()
            assert 'configuration saved' in mock_print.call_args[0][0]
            
    @patch('os.getenv')
    @patch('penify_hook.commands.config_commands.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='{"api_keys": "config-token"}')
    def test_get_token_from_env(self, mock_file_open, mock_path, mock_getenv):

        # Setup mock for env var
        """Test retrieving a token from the environment variable.
        
        This function tests the behavior of `get_token` when an environment variable is set. It verifies that if the
        'PENIFY_API_TOKEN' environment variable exists, the function returns its value without attempting to read a file.
        """
        mock_getenv.return_value = "env-token"
        
        # Call function
        result = get_token()
        
        # Assertions
        assert result == "env-token"
        mock_getenv.assert_called_once_with('PENIFY_API_TOKEN')
        # File should not be read if env var exists
        assert mock_file_open.call_count == 0
        
    @patch('os.getenv')
    @patch('penify_hook.commands.config_commands.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='{"api_keys": "config-token"}')
    def test_get_token_from_config(self, mock_file_open, mock_path, mock_getenv):

        # Setup mock for env var (not found)
        """Test retrieving a token from the configuration.
        
        This function sets up mocks for environment variables and configuration files, calls the `get_token` function, and
        asserts its behavior. It verifies that when the environment variable is not found, the function reads a token from a
        configuration file located in the user's home directory.
        
        Args:
            mock_file_open (MagicMock): A mock for the `open` function.
            mock_path (MagicMock): A mock for the `pathlib.Path` class.
            mock_getenv (MagicMock): A mock for the `os.getenv` function.
        """
        mock_getenv.return_value = None
        
        # Setup mock for config file
        mock_home_dir = MagicMock()
        mock_path.home.return_value = mock_home_dir
        mock_home_dir.__truediv__.return_value = mock_home_dir
        mock_home_dir.exists.return_value = True
        
        # Call function
        result = get_token()
        
        # Assertions
        assert result == "config-token"
        mock_getenv.assert_called_once_with('PENIFY_API_TOKEN')
        mock_file_open.assert_called_once_with(mock_home_dir, 'r')
        
    @patch('os.getenv')
    @patch('penify_hook.commands.config_commands.Path')
    @patch('builtins.open', new_callable=mock_open, read_data='{"other_key": "value"}')
    def test_get_token_not_found(self, mock_file_open, mock_path, mock_getenv):

        # Setup mock for env var (not found)
        """Test the get_token function when the API token environment variable is not found.
        
        This function tests the scenario where the `PENIFY_API_TOKEN` environment variable is not set. It mocks the environment
        variable to return `None`, and verifies that the function returns `None`. The test also checks that the environment
        variable is accessed once and that a file open operation is attempted on a configuration file located in the user's home
        directory.
        
        Args:
            mock_file_open (MagicMock): Mock for the built-in `open` function.
            mock_path (MagicMock): Mock for the `pathlib.Path` module.
            mock_getenv (MagicMock): Mock for the `os.getenv` function.
        
        Returns:
            None: The function does not return anything; it asserts conditions to verify correctness.
        """
        mock_getenv.return_value = None
        
        # Setup mock for config file
        mock_home_dir = MagicMock()
        mock_path.home.return_value = mock_home_dir
        mock_home_dir.__truediv__.return_value = mock_home_dir
        mock_home_dir.exists.return_value = True
        
        # Call function
        result = get_token()
        
        # Assertions
        assert result is None
        mock_getenv.assert_called_once_with('PENIFY_API_TOKEN')
        mock_file_open.assert_called_once_with(mock_home_dir, 'r')
