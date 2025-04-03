import os
import sys
import pytest
from unittest.mock import patch, MagicMock, call

from penify_hook.commands.commit_commands import commit_code, setup_commit_parser, handle_commit

class TestCommitCommands:

    @pytest.fixture
    def mock_api_client(self):
        """Mocks an instance of APIClient using unittest.mock.

        This function creates a mock object for APIClient and yields it along
        with the mocked instance. It is useful for testing purposes where real
        API calls should be avoided.

        Yields:
            tuple: A tuple containing the mock of APIClient and the mocked instance of
                APIClient.
        """

        with patch('penify_hook.api_client.APIClient', create=True) as mock:
            api_client_instance = MagicMock()
            mock.return_value = api_client_instance
            yield mock, api_client_instance

    @pytest.fixture
    def mock_llm_client(self):
        """Mock an instance of LLMClient for testing purposes.

        This function yields a mock object representing an instance of
        LLMClient, which can be used to simulate interactions with a language
        model during testing. The mock is patched to replace the actual
        LLMClient class from the penify_hook module.

        Yields:
            tuple: A tuple containing two elements:
                - mock (MagicMock): The mock object for LLMClient.
                - llm_client_instance (MagicMock): An instance of the mocked LLMClient.
        """

        with patch('penify_hook.llm_client.LLMClient', create=True) as mock:
            llm_client_instance = MagicMock()
            mock.return_value = llm_client_instance
            yield mock, llm_client_instance

    @pytest.fixture
    def mock_jira_client(self):
        """Create a mock JIRA client for testing purposes.

        This function yields a tuple containing a mock JIRA client instance and
        its `is_connected` method. The mock client is configured to simulate an
        active connection. This is useful for unit tests that require
        interaction with a JIRA client without making actual network calls.

        Yields:
            tuple: A tuple containing the mocked JIRA client instance and its
                `is_connected` method.
        """

        with patch('penify_hook.jira_client.JiraClient', create=True) as mock:
            jira_instance = MagicMock()
            jira_instance.is_connected.return_value = True
            mock.return_value = jira_instance
            yield mock, jira_instance

    @pytest.fixture
    def mock_commit_doc_gen(self):
        """Mocks the CommitDocGenHook class and returns a MagicMock instance.

        This function uses the `patch` decorator from the `unittest.mock` module
        to create a mock of the `CommitDocGenHook` class. It then sets up this
        mock to return a new `MagicMock` instance when invoked. The function
        yields both the mock object and the mocked instance, allowing for easy
        testing of functions that rely on `CommitDocGenHook`.

        Returns:
            tuple: A tuple containing two elements:
                - mock (patch): The patch object used to mock the `CommitDocGenHook`
                class.
                - doc_gen_instance (MagicMock): The mocked instance of
                `CommitDocGenHook`.
        """

        with patch('penify_hook.commit_analyzer.CommitDocGenHook', create=True) as mock:
            doc_gen_instance = MagicMock()
            mock.return_value = doc_gen_instance
            yield mock, doc_gen_instance

    @pytest.fixture
    def mock_git_folder_search(self):
        """Mock the `recursive_search_git_folder` function to return a predefined
        git folder path.

        This function uses the `patch` decorator from the `unittest.mock` module
        to intercept calls to `penify_hook.utils.recursive_search_git_folder`.
        When called, it will return '/mock/git/folder' instead of performing an
        actual search. This is useful for testing purposes where you need a
        consistent response without interacting with the file system.

        Yields:
            MagicMock: A mock object that simulates the `recursive_search_git_folder` function.
        """

        with patch('penify_hook.utils.recursive_search_git_folder', create=True) as mock:
            mock.return_value = '/mock/git/folder'
            yield mock
            
    @pytest.fixture
    def mock_print_functions(self):
        """Mocks the print functions from `penify_hook.ui_utils` for testing
        purposes.

        This function uses Python's `unittest.mock.patch` to replace the actual
        print functions (`print`, `print_warning`, and `print_error`) with mock
        objects. These mock objects can be used in tests to capture calls made
        to these print functions without actually printing anything.

        Yields:
            tuple: A tuple containing three mock objects corresponding to `print_info`,
                `print_warning`,
                and `print_error`.
        """

        with patch('penify_hook.ui_utils.print_info', create=True) as mock_info, \
             patch('penify_hook.ui_utils.print_warning', create=True) as mock_warning, \
             patch('penify_hook.ui_utils.print_error', create=True) as mock_error:
            yield mock_info, mock_warning, mock_error

    @patch('penify_hook.api_client.APIClient', create=True)
    @patch('penify_hook.llm_client.LLMClient', create=True)
    @patch('penify_hook.commit_analyzer.CommitDocGenHook', create=True)
    @patch('penify_hook.utils.recursive_search_git_folder', create=True)
    @patch('penify_hook.ui_utils.print_info', create=True)
    @patch('penify_hook.ui_utils.print_warning', create=True)
    @patch('penify_hook.ui_utils.print_error', create=True)
    def test_commit_code_with_llm_client(self, mock_error, mock_warning, mock_info, 
                                        mock_git_folder_search, mock_doc_gen, 
                                        mock_llm_client, mock_api_client):
        """Test committing code using an LLM client.

        This function sets up mock objects for various components and then calls
        the `commit_code` function with specified parameters. It verifies that
        the correct mocks are created and called with the appropriate arguments.

        Args:
            mock_error (MagicMock): Mock object for error handling.
            mock_warning (MagicMock): Mock object for warning logging.
            mock_info (MagicMock): Mock object for info logging.
            mock_git_folder_search (MagicMock): Mock object to simulate git folder search.
            mock_doc_gen (MagicMock): Mock object for document generation.
            mock_llm_client (MagicMock): Mock object for LLM client interaction.
            mock_api_client (MagicMock): Mock object for API client interaction.
        """

        # Setup mocks
        api_instance = MagicMock()
        mock_api_client.return_value = api_instance
        
        llm_instance = MagicMock()
        mock_llm_client.return_value = llm_instance
        
        doc_gen_instance = MagicMock()
        mock_doc_gen.return_value = doc_gen_instance
        
        mock_git_folder_search.return_value = '/mock/git/folder'
        
        # Call function with LLM parameters
        commit_code(
            api_url="http://api.example.com",
            token="api-token",
            message="test commit",
            open_terminal=False,
            generate_description=True,
            llm_model="gpt-4",
            llm_api_base="http://llm-api.example.com",
            llm_api_key="llm-api-key"
        )
        
        # Verify calls
        mock_api_client.assert_called_once_with("http://api.example.com", "api-token")
        mock_llm_client.assert_called_once_with(
            model="gpt-4",
            api_base="http://llm-api.example.com",
            api_key="llm-api-key"
        )
        mock_doc_gen.assert_called_once_with('/mock/git/folder', api_instance, llm_instance, None)
        doc_gen_instance.run.assert_called_once_with("test commit", False, True)

    @patch('penify_hook.api_client.APIClient', create=True)
    @patch('penify_hook.llm_client.LLMClient', create=True)
    @patch('penify_hook.jira_client.JiraClient', create=True)
    @patch('penify_hook.commit_analyzer.CommitDocGenHook', create=True)
    @patch('penify_hook.utils.recursive_search_git_folder', create=True)
    @patch('penify_hook.ui_utils.print_info', create=True)
    @patch('penify_hook.ui_utils.print_warning', create=True)
    @patch('penify_hook.ui_utils.print_error', create=True)
    def test_commit_code_with_jira_client(self, mock_error, mock_warning, mock_info,
                                         mock_git_folder_search, mock_doc_gen, 
                                         mock_jira_client, mock_llm_client, mock_api_client):
        """Test committing code using a JIRA client.

        This function tests the commit_code function with various parameters,
        including API and JIRA credentials. It sets up mock objects for
        dependencies such as the JIRA client, LLM client, and doc generator to
        simulate the behavior of the real classes. The function then calls
        commit_code and verifies that the JIRA client and doc generator are
        called with the correct parameters.

        Args:
            mock_error (MagicMock): A MagicMock object for simulating error logging.
            mock_warning (MagicMock): A MagicMock object for simulating warning logging.
            mock_info (MagicMock): A MagicMock object for simulating info logging.
            mock_git_folder_search (MagicMock): A MagicMock object for simulating the git folder search function.
            mock_doc_gen (MagicMock): A MagicMock object for simulating the doc generator function.
            mock_jira_client (MagicMock): A MagicMock object for simulating the JIRA client class.
            mock_llm_client (MagicMock): A MagicMock object for simulating the LLM client class.
            mock_api_client (MagicMock): A MagicMock object for simulating the API client class.
        """

        # Setup mocks
        api_instance = MagicMock()
        mock_api_client.return_value = api_instance
        
        llm_instance = MagicMock()
        mock_llm_client.return_value = llm_instance
        
        jira_instance = MagicMock()
        jira_instance.is_connected.return_value = True
        mock_jira_client.return_value = jira_instance
        
        doc_gen_instance = MagicMock()
        mock_doc_gen.return_value = doc_gen_instance
        
        mock_git_folder_search.return_value = '/mock/git/folder'
        
        # Call function with JIRA parameters
        commit_code(
            api_url="http://api.example.com",
            token="api-token",
            message="test commit",
            open_terminal=False,
            generate_description=True,
            llm_model="gpt-4",
            llm_api_base="http://llm-api.example.com",
            llm_api_key="llm-api-key",
            jira_url="https://jira.example.com",
            jira_user="jira-user",
            jira_api_token="jira-token"
        )
        
        # Verify calls
        mock_jira_client.assert_called_once_with(
            jira_url="https://jira.example.com",
            jira_user="jira-user",
            jira_api_token="jira-token"
        )
        mock_doc_gen.assert_called_once_with('/mock/git/folder', api_instance, llm_instance, jira_instance)

    @patch('penify_hook.api_client.APIClient', create=True)
    @patch('penify_hook.jira_client.JiraClient', create=True)
    @patch('penify_hook.commit_analyzer.CommitDocGenHook', create=True)
    @patch('penify_hook.utils.recursive_search_git_folder', create=True)
    @patch('penify_hook.ui_utils.print_info', create=True)
    @patch('penify_hook.ui_utils.print_warning', create=True)
    @patch('penify_hook.ui_utils.print_error', create=True)
    def test_commit_code_with_jira_connection_failure(self, mock_error, mock_warning, mock_info,
                                                     mock_git_folder_search, mock_doc_gen,
                                                     mock_jira_client, mock_api_client):
        """Test the commit_code function when JIRA connection fails.

        This function tests the scenario where the JIRA connection fails during
        a code commit. It sets up various mocks to simulate different components
        of the system and then calls the `commit_code` function with specific
        parameters. The function is expected to handle the JIRA connection
        failure gracefully by logging an appropriate warning.

        Args:
            mock_error (MagicMock): Mock for error logging.
            mock_warning (MagicMock): Mock for warning logging.
            mock_info (MagicMock): Mock for info logging.
            mock_git_folder_search (MagicMock): Mock for searching the Git folder.
            mock_doc_gen (MagicMock): Mock for generating documentation.
            mock_jira_client (MagicMock): Mock for creating a JIRA client.
            mock_api_client (MagicMock): Mock for creating an API client.
        """

        # Setup mocks
        api_instance = MagicMock()
        mock_api_client.return_value = api_instance
        
        jira_instance = MagicMock()
        jira_instance.is_connected.return_value = False
        mock_jira_client.return_value = jira_instance
        
        doc_gen_instance = MagicMock()
        mock_doc_gen.return_value = doc_gen_instance
        
        mock_git_folder_search.return_value = '/mock/git/folder'
        
        # Call function
        commit_code(
            api_url="http://api.example.com",
            token="api-token",
            message="test commit",
            open_terminal=False,
            generate_description=True,
            llm_model=None,
            jira_url="https://jira.example.com",
            jira_user="jira-user",
            jira_api_token="jira-token"
        )
        
        # Verify JIRA warning
        mock_doc_gen.assert_called_once_with('/mock/git/folder', api_instance, None, None)

    @patch('penify_hook.api_client.APIClient', create=True)
    @patch('penify_hook.commit_analyzer.CommitDocGenHook', create=True)
    @patch('penify_hook.utils.recursive_search_git_folder', create=True)
    @patch('sys.exit')
    @patch('builtins.print')
    def test_commit_code_error_handling(self, mock_print, mock_exit, 
                                       mock_git_folder_search, mock_doc_gen, mock_api_client):
        """Test the error handling in the test_commit_code function.

        This function sets up mocks to simulate exceptions and test the error
        handling of the commit_code function. It verifies that the function
        correctly prints an error message and exits with a status code of 1 when
        an exception occurs during documentation generation.

        Args:
            mock_print (MagicMock): Mock for the print function, used to verify error message output.
            mock_exit (MagicMock): Mock for the sys.exit function, used to verify exit behavior.
            mock_git_folder_search (MagicMock): Mock for the git_folder_search function, returning a mock Git folder
                path.
            mock_doc_gen (MagicMock): Mock for the doc_gen function, simulating an exception during
                documentation generation.
            mock_api_client (MagicMock): Mock for the API client class, not directly used but referenced in the
                function signature.
        """

        # Setup mocks
        mock_doc_gen.side_effect = Exception("Test error")
        mock_git_folder_search.return_value = '/mock/git/folder'
        
        # Call function
        commit_code(
            api_url="http://api.example.com",
            token="api-token",
            message="test commit",
            open_terminal=False,
            generate_description=True
        )
        
        mock_print.assert_called_once_with("Error: Test error")
        mock_exit.assert_called_once_with(1)

    def test_setup_commit_parser(self):
        """Set up the argument parser for the commit command.

        This function configures an argument parser to handle various options
        for committing changes. It adds three arguments: - '-m' or '--message':
        An optional argument to specify a contextual commit message with a
        default value of "N/A". - '-e' or '--terminal': A boolean flag to open
        an edit terminal before committing. - '-d' or '--description': A boolean
        flag that, when set to False, indicates the generation of a commit
        message with title and description.

        Args:
            parser (MagicMock): The argument parser to be configured.
        """

        parser = MagicMock()
        setup_commit_parser(parser)
        
        # Verify parser configuration
        assert parser.add_argument.call_count == 3
        parser.add_argument.assert_any_call("-m", "--message", required=False, help="Commit with contextual commit message.", default="N/A")
        parser.add_argument.assert_any_call("-e", "--terminal", action="store_true", help="Open edit terminal before committing.")
        parser.add_argument.assert_any_call("-d", "--description", action="store_false", help="It will generate commit message with title and description.", default=False)

    @patch('penify_hook.commands.commit_commands.get_token')
    @patch('penify_hook.commands.commit_commands.get_jira_config')
    @patch('penify_hook.commands.commit_commands.get_llm_config')
    @patch('penify_hook.commands.commit_commands.commit_code')
    @patch('penify_hook.commands.commit_commands.print_info')
    @patch('penify_hook.constants.API_URL', "http://api.example.com")
    def test_handle_commit(self, mock_print_info, mock_commit_code, mock_get_token, 
                         mock_get_llm_config, mock_get_jira_config):
        """Test the handle_commit function with various mock objects.

        This function sets up mocks for retrieving LLM configuration, JIRA
        configuration, and commit code. It then creates an argument object and
        calls the handle_commit function. Finally, it verifies that the mock
        functions were called with the expected arguments.

        Args:
            mock_print_info (MagicMock): Mock object for printing information.
            mock_commit_code (MagicMock): Mock object for committing code.
            mock_get_token (MagicMock): Mock object for retrieving API token.
            mock_get_llm_config (MagicMock): Mock object for retrieving LLM configuration.
            mock_get_jira_config (MagicMock): Mock object for retrieving JIRA configuration.
        """

        # Setup mocks
        mock_get_llm_config.return_value = {
            'model': 'test-model',
            'api_base': 'http://llm-api.example.com',
            'api_key': 'llm-key'
        }
        mock_get_token.return_value = 'api-token'
        mock_get_jira_config.return_value = {
            'url': 'https://jira.example.com',
            'username': 'jira-user',
            'api_token': 'jira-token'
        }
        
        # Create args
        args = MagicMock()
        args.message = "test commit"
        args.terminal = True
        args.description = True
        
        # Call function
        handle_commit(args)
        
        # Verify
        mock_print_info.assert_called_with("Generate Commit Description: True")
        mock_commit_code.assert_called_once_with(
            "http://api.example.com", 'api-token', "test commit", True, True,
            'test-model', 'http://llm-api.example.com', 'llm-key',
            'https://jira.example.com', 'jira-user', 'jira-token'
        )
