import pytest
import json
import http.server
import threading
import socketserver
import time
from unittest.mock import patch, MagicMock, mock_open
import webbrowser

from penify_hook.commands.config_commands import config_llm_web, config_jira_web


class TestWebConfig:
    
    @patch('webbrowser.open')
    @patch('socketserver.TCPServer')
    @patch('pkg_resources.resource_filename')
    def test_config_llm_web_server_setup(self, mock_resource_filename, mock_server, mock_webbrowser):
        """Set up and test the web server configuration for an LLM (Large Language
        Model) web interface.

        This function configures a mock web server for testing purposes. It sets
        up resource filenames, mocks server behavior, and verifies that the web
        browser is opened and the server starts correctly. The function uses
        various mocks to simulate external dependencies such as
        `resource_filename` and `server`.

        Args:
            mock_resource_filename (MagicMock): A MagicMock object simulating the `resource_filename` function.
            mock_server (MagicMock): A MagicMock object simulating the context manager for the web server.
            mock_webbrowser (MagicMock): A MagicMock object simulating the `webbrowser` module.
        """

        # Setup mocks
        mock_resource_filename.return_value = 'mock/template/path'
        mock_server_instance = MagicMock()
        mock_server.return_value.__enter__.return_value = mock_server_instance
        
        # Mock the serve_forever method to stop after being called once
        def stop_server_after_call():
            mock_server_instance.shutdown()
        mock_server_instance.serve_forever.side_effect = stop_server_after_call
        
        # Call function with patched webbrowser
        with patch('builtins.print'):  # Suppress print statements
            config_llm_web()
        
        # Verify webbrowser was opened
        mock_webbrowser.assert_called_once()
        assert mock_webbrowser.call_args[0][0].startswith('http://localhost:')
        
        # Verify server was started
        mock_server.assert_called_once()
        mock_server_instance.serve_forever.assert_called_once()

    @patch('webbrowser.open')
    @patch('socketserver.TCPServer')
    @patch('pkg_resources.resource_filename')
    def test_config_jira_web_server_setup(self, mock_resource_filename, mock_server, mock_webbrowser):
        """Test the configuration and setup of a JIRA web server.

        This function tests the entire process of setting up a JIRA web server,
        including mocking necessary resources, configuring the server to shut
        down after handling one request, and verifying that the web browser is
        opened with the correct URL. The function uses several mocks to simulate
        external dependencies such as resource files, servers, and web browsers.

        Args:
            mock_resource_filename (MagicMock): A MagicMock object for simulating the `resource_filename` function.
            mock_server (MagicMock): A MagicMock object for simulating the server setup.
            mock_webbrowser (MagicMock): A MagicMock object for simulating the web browser opening.
        """

        # Setup mocks
        mock_resource_filename.return_value = 'mock/template/path'
        mock_server_instance = MagicMock()
        mock_server.return_value.__enter__.return_value = mock_server_instance
        
        # Mock the serve_forever method to stop after being called once
        def stop_server_after_call():
            mock_server_instance.shutdown()
        mock_server_instance.serve_forever.side_effect = stop_server_after_call
        
        # Call function with patched webbrowser
        with patch('builtins.print'):  # Suppress print statements
            config_jira_web()
        
        # Verify webbrowser was opened
        mock_webbrowser.assert_called_once()
        assert mock_webbrowser.call_args[0][0].startswith('http://localhost:')
        
        # Verify server was started
        mock_server.assert_called_once()
        mock_server_instance.serve_forever.assert_called_once()
