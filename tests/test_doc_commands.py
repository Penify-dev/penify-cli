import pytest
import sys
import os
from argparse import ArgumentParser
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from penify_hook.commands.doc_commands import (
    generate_doc,
    setup_docgen_parser,
    handle_docgen
)


@patch('penify_hook.file_analyzer.FileAnalyzerGenHook')
@patch('penify_hook.git_analyzer.GitDocGenHook')
@patch('penify_hook.folder_analyzer.FolderAnalyzerGenHook')
@patch('penify_hook.api_client.APIClient')
@patch('penify_hook.commands.doc_commands.os.getcwd')
def test_generate_doc_no_location(mock_getcwd, mock_api_client, 
                                 mock_folder_analyzer, mock_file_analyzer, 
                                 mock_git_analyzer):
    """Test function to generate documentation without location information.

    This function sets up mocks for the API client, current working
    directory, and Git analyzer. It then calls the `generate_doc` function
    with a fake API URL and token. The function is expected to initialize
    the API client, configure the Git analyzer, and run it without any
    location information.

    Args:
        mock_getcwd (MagicMock): Mock for os.getcwd().
        mock_api_client (MagicMock): Mock for creating an API client.
        mock_folder_analyzer (MagicMock): Mock for folder analysis.
        mock_file_analyzer (MagicMock): Mock for file analysis.
        mock_git_analyzer (MagicMock): Mock for Git analyzer setup.
    """

    # Setup
    mock_api_instance = MagicMock()
    mock_api_client.return_value = mock_api_instance
    mock_getcwd.return_value = '/fake/current/dir'
    mock_git_instance = MagicMock()
    mock_git_analyzer.return_value = mock_git_instance
    
    # Call function
    generate_doc('http://api.example.com', 'fake-token', None)
    
    # Assertions
    mock_api_client.assert_called_once_with('http://api.example.com', 'fake-token')
    mock_git_analyzer.assert_called_once_with('/fake/current/dir', mock_api_instance)
    mock_git_instance.run.assert_called_once()
    # mock_file_analyzer.assert_not_called()
    # mock_folder_analyzer.assert_not_called()


@patch('penify_hook.git_analyzer.GitDocGenHook')
@patch('penify_hook.folder_analyzer.FolderAnalyzerGenHook')
@patch('penify_hook.api_client.APIClient')
@patch('penify_hook.api_client.APIClient')
def test_generate_doc_file_location(mock_api_client, mock_folder_analyzer, 
                                   mock_file_analyzer, mock_git_analyzer):
    """Test generating a documentation file location.

    This function tests the process of generating a documentation file
    location using mock objects for API client, folder analyzer, file
    analyzer, and Git analyzer. It sets up the necessary mocks, calls the
    `generate_doc` function with specified parameters, and asserts that the
    appropriate methods on the mock objects are called as expected.

    Args:
        mock_api_client (MagicMock): Mock object for the API client.
        mock_folder_analyzer (MagicMock): Mock object for the folder analyzer.
        mock_file_analyzer (MagicMock): Mock object for the file analyzer.
        mock_git_analyzer (MagicMock): Mock object for the Git analyzer.
    """

    # Setup
    mock_api_instance = MagicMock()
    mock_api_client.return_value = mock_api_instance
    mock_file_instance = MagicMock()
    mock_file_analyzer.return_value = mock_file_instance
    
    # Call function
    generate_doc('http://api.example.com', 'fake-token', 'example.py')
    
    # Assertions
    mock_api_client.assert_called_once_with('http://api.example.com', 'fake-token')
    mock_file_analyzer.assert_called_once_with('example.py', mock_api_instance)
    mock_file_instance.run.assert_called_once()
    mock_git_analyzer.assert_not_called()
    mock_folder_analyzer.assert_not_called()


@patch('penify_hook.commands.doc_commands.GitDocGenHook')
@patch('penify_hook.commands.doc_commands.FileAnalyzerGenHook')
@patch('penify_hook.commands.doc_commands.FolderAnalyzerGenHook')
@patch('penify_hook.api_client.APIClient')
def test_generate_doc_folder_location(mock_api_client, mock_folder_analyzer, 
                                     mock_file_analyzer, mock_git_analyzer):
    """Test the function to generate documentation for a folder location.

    This function sets up mock objects for API client, folder analyzer, file
    analyzer, and Git analyzer. It then calls the `generate_doc` function
    with specified parameters and asserts that the correct methods on the
    mock objects were called as expected.

    Args:
        mock_api_client (MagicMock): Mock object for the API client.
        mock_folder_analyzer (MagicMock): Mock object for the folder analyzer.
        mock_file_analyzer (MagicMock): Mock object for the file analyzer.
        mock_git_analyzer (MagicMock): Mock object for the Git analyzer.
    """

    # Setup
    mock_api_instance = MagicMock()
    mock_api_client.return_value = mock_api_instance
    mock_folder_instance = MagicMock()
    mock_folder_analyzer.return_value = mock_folder_instance
    
    # Call function
    generate_doc('http://api.example.com', 'fake-token', 'src')
    
    # Assertions
    mock_api_client.assert_called_once_with('http://api.example.com', 'fake-token')
    mock_folder_analyzer.assert_called_once_with('src', mock_api_instance)
    mock_folder_instance.run.assert_called_once()
    mock_git_analyzer.assert_not_called()
    mock_file_analyzer.assert_not_called()


@patch('sys.exit')
@patch('penify_hook.commands.doc_commands.GitDocGenHook')
@patch('penify_hook.api_client.APIClient')
def test_generate_doc_error_handling(mock_api_client, mock_git_analyzer, mock_exit):
    """Test function to ensure proper error handling during API calls with
    GitAnalyzer.

    This test function is designed to verify that the generate_doc function
    handles exceptions correctly when an error occurs during API interaction
    with GitAnalyzer. It sets up a mock API client and a mock Git analyzer,
    causing the analyzer to raise an exception to simulate a failure
    condition. The function then asserts that the exit code is set to 1 when
    the error handling mechanism is invoked.

    Args:
        mock_api_client (MagicMock): A mock object simulating the API client.
        mock_git_analyzer (MagicMock): A mock object simulating the Git analyzer, configured to raise an
            exception.
        mock_exit (MagicMock): A mock object representing the exit function, which should be called
            with an error code.
    """

    # Setup
    mock_api_instance = MagicMock()
    mock_api_client.return_value = mock_api_instance
    mock_git_analyzer.side_effect = Exception("Test error")
    
    # Call function
    generate_doc('http://api.example.com', 'fake-token', None)
    
    # Assertions
    mock_exit.assert_called_once_with(1)


def test_setup_docgen_parser():
    """Test the setup_docgen_parser function to ensure it properly configures
    the ArgumentParser for docgen options.  It verifies that the parser
    correctly sets up docgen options and handles different subcommands like
    'install-hook' and 'uninstall-hook'.
    """

    parser = ArgumentParser()
    setup_docgen_parser(parser)
    
    # Check that docgen options are properly set up
    args = parser.parse_args(['-l', 'test_location'])
    assert args.location == 'test_location'
    
    # Check install-hook subcommand
    args = parser.parse_args(['install-hook', '-l', 'hook_location'])
    assert args.docgen_subcommand == 'install-hook'
    assert args.location == 'hook_location'
    
    # Check uninstall-hook subcommand
    args = parser.parse_args(['uninstall-hook', '-l', 'hook_location'])
    assert args.docgen_subcommand == 'uninstall-hook'
    assert args.location == 'hook_location'


@patch('penify_hook.commands.doc_commands.install_git_hook')
@patch('penify_hook.commands.doc_commands.uninstall_git_hook')
@patch('penify_hook.commands.doc_commands.generate_doc')
@patch('penify_hook.commands.doc_commands.get_token')
@patch('sys.exit')
def test_handle_docgen_install_hook(mock_exit, mock_get_token, mock_generate_doc, 
                                   mock_uninstall_hook, mock_install_hook):
    """Test the handling of the 'install-hook' subcommand.

    This function sets up a mock environment to simulate the execution of
    the 'install-hook' subcommand. It verifies that the `mock_install_hook`
    is called with the correct arguments while ensuring that
    `mock_generate_doc` and `mock_uninstall_hook` are not called.

    Args:
        mock_exit (MagicMock): Mock object for sys.exit.
        mock_get_token (MagicMock): Mock object to simulate fetching a token.
        mock_generate_doc (MagicMock): Mock object to simulate generating documentation.
        mock_uninstall_hook (MagicMock): Mock object to simulate uninstalling a hook.
        mock_install_hook (MagicMock): Mock object to simulate installing a hook.
    """

    # Setup
    mock_get_token.return_value = 'fake-token'
    
    # Test install-hook subcommand
    args = MagicMock(docgen_subcommand='install-hook', location='hook_location')
    handle_docgen(args)
    mock_install_hook.assert_called_once_with('hook_location', 'fake-token')
    mock_generate_doc.assert_not_called()
    mock_uninstall_hook.assert_not_called()


@patch('penify_hook.commands.doc_commands.install_git_hook')
@patch('penify_hook.commands.doc_commands.uninstall_git_hook')
@patch('penify_hook.commands.doc_commands.generate_doc')
@patch('penify_hook.commands.doc_commands.get_token')
@patch('sys.exit')
def test_handle_docgen_uninstall_hook(mock_exit, mock_get_token, mock_generate_doc, 
                                     mock_uninstall_hook, mock_install_hook):
    """Test the uninstall-hook subcommand of the handle_docgen function.

    This function sets up a mock environment and verifies that the
    uninstall-hook is called with the correct location, while generate_doc
    and install_hook are not called.

    Args:
        mock_exit (MagicMock): A mock for the exit function.
        mock_get_token (MagicMock): A mock for the get_token function.
        mock_generate_doc (MagicMock): A mock for the generate_doc function.
        mock_uninstall_hook (MagicMock): A mock for the uninstall_hook function.
        mock_install_hook (MagicMock): A mock for the install_hook function.
    """

    # Setup
    mock_get_token.return_value = 'fake-token'
    
    # Test uninstall-hook subcommand
    args = MagicMock(docgen_subcommand='uninstall-hook', location='hook_location')
    handle_docgen(args)
    mock_uninstall_hook.assert_called_once_with('hook_location')
    mock_generate_doc.assert_not_called()
    mock_install_hook.assert_not_called()


@patch('penify_hook.commands.doc_commands.install_git_hook')
@patch('penify_hook.commands.doc_commands.uninstall_git_hook')
@patch('penify_hook.commands.doc_commands.generate_doc')
@patch('penify_hook.commands.doc_commands.get_token')
def test_handle_docgen_generate(mock_get_token, mock_generate_doc, 
                               mock_uninstall_hook, mock_install_hook):
    """Test the direct documentation generation functionality.

    This function tests the `handle_docgen` function when no subcommand is
    provided. It verifies that the document generation hook is called and
    the uninstall and install hooks are not called.

    Args:
        mock_get_token (MagicMock): Mocked function to get authentication token.
        mock_generate_doc (MagicMock): Mocked function for generating documentation.
        mock_uninstall_hook (MagicMock): Mocked function for uninstalling the document generation hook.
        mock_install_hook (MagicMock): Mocked function for installing the document generation hook.
    """

    # Setup
    mock_get_token.return_value = 'fake-token'
    
    # Test direct documentation generation
    args = MagicMock(docgen_subcommand=None, location='doc_location')
    handle_docgen(args)
    mock_generate_doc.assert_called_once()
    mock_install_hook.assert_not_called()
    mock_uninstall_hook.assert_not_called()


@patch('penify_hook.commands.doc_commands.get_token')
@patch('sys.exit')
def test_handle_docgen_no_token(mock_exit, mock_get_token):
    """Test the behavior of the `handle_docgen` function when no token is
    provided.

    This function asserts that if no token is returned by `mock_get_token`,
    the `handle_docgen` function will call `mock_exit` with a status code of
    1.

    Args:
        mock_exit (MagicMock): A MagicMock object simulating the `exit` function.
        mock_get_token (MagicMock): A MagicMock object simulating the `get_token` function.
    """

    # Test with no token
    mock_get_token.return_value = None
    args = MagicMock(docgen_subcommand=None, location='doc_location')
    handle_docgen(args)
    mock_exit.assert_called_once_with(1)


@patch('penify_hook.commands.doc_commands.os.getcwd')
@patch('penify_hook.api_client.APIClient')
def test_generate_doc_with_file_exception(mock_api_client, mock_getcwd):
    """Test generating documentation from a Python source file with an
    exception.

    This function reads a Python file and attempts to generate a docstring
    based on its content. It uses mock objects to simulate API calls and
    directory operations during testing. If an exception occurs during the
    process, it raises a SystemExit with status code 1.

    Args:
        mock_api_client (unittest.mock.MagicMock): A mock object for simulating API client behavior.
        mock_getcwd (unittest.mock.MagicMock): A mock object for simulating the current working directory function.
    """

    # Setup
    mock_api_client.side_effect = Exception("API error")
    mock_getcwd.return_value = '/fake/current/dir'
    
    # Test file location with exception
    with pytest.raises(SystemExit):
        generate_doc('http://api.example.com', 'fake-token', 'example.py')


@patch('penify_hook.commands.doc_commands.os.getcwd')
@patch('penify_hook.api_client.APIClient')
def test_generate_doc_with_folder_exception(mock_api_client, mock_getcwd):
    """Test that a SystemExit exception is raised when an error occurs during
    the fetching process.

    This function tests the behavior of the `generate_doc` function when an
    error occurs during the fetching process. It sets up a mock API client
    to simulate a failure and checks if a SystemExit exception is raised
    with the appropriate message.

    Args:
        mock_api_client (MagicMock): A mock object for the API client, simulating an error.
        mock_getcwd (MagicMock): A mock object for `os.getcwd`, returning a fake directory path.
    """

    # Setup
    mock_api_client.side_effect = Exception("API error")
    mock_getcwd.return_value = '/fake/current/dir'
    
    # Test folder location with exception
    with pytest.raises(SystemExit):
        generate_doc('http://api.example.com', 'fake-token', 'src_folder')
