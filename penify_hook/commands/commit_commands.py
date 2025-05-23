import os
import sys
import argparse

from penify_hook.ui_utils import print_info, print_warning


def commit_code(api_url, token, message, open_terminal, generate_description,
               llm_model=None, llm_api_base=None, llm_api_key=None,
               jira_url=None, jira_user=None, jira_api_token=None):

    """Enhance Git commits with AI-powered commit messages.
    
    This function allows for the generation of enhanced commit messages using
    natural language processing models and optionally integrates with JIRA for
    additional context. It processes the current Git folder to find relevant files
    and generates a detailed commit message based on the provided parameters.
    
    Args:
        api_url (str): URL of the API endpoint.
        token (str): Authentication token for the API.
        message (str): Initial commit message provided by the user.
        open_terminal (bool): Whether to open the terminal after committing.
        generate_description (bool): Whether to generate a detailed description in the commit message.
        llm_model (str?): The language model to use for generating the commit message. Defaults to None.
        llm_api_base (str?): Base URL of the LLM API. Defaults to None.
        llm_api_key (str?): API key for accessing the LLM service. Defaults to None.
        jira_url (str?): URL of the JIRA instance. Defaults to None.
        jira_user (str?): Username for authenticating with JIRA. Defaults to None.
        jira_api_token (str?): API token for accessing JIRA. Defaults to None.
    """
    from penify_hook.ui_utils import print_error
    from penify_hook.utils import recursive_search_git_folder
    from ..commit_analyzer import CommitDocGenHook
    from ..api_client import APIClient

    # Try importing optional dependencies
    try:
        from ..llm_client import LLMClient
    except ImportError:
        LLMClient = None

    try:
        from ..jira_client import JiraClient
    except ImportError:
        JiraClient = None
    # Create API client
    api_client = APIClient(api_url, token)
    
    # Initialize LLM client if LLM parameters are provided and LLMClient is available
    llm_client = None
    if LLMClient is not None and llm_model:
        try:
            llm_client = LLMClient(
                model=llm_model,
                api_base=llm_api_base,
                api_key=llm_api_key
            )
            print_info(f"Using LLM model: {llm_model}")
        except Exception as e:
            print_error(f"Error initializing LLM client: {e}")
            print_error("Falling back to API for commit summary generation")
    else:
        if not token:
            print_error("No LLM model or API token provided. Please provide an LLM model or API token.")
    
    # Initialize JIRA client if parameters are provided and JiraClient is available
    jira_client = None
    if JiraClient is not None and jira_url and jira_user and jira_api_token:
        try:
            jira_client = JiraClient(
                jira_url=jira_url,
                jira_user=jira_user,
                jira_api_token=jira_api_token
            )
            if jira_client.is_connected():
                print_info(f"Connected to JIRA: {jira_url}")
            else:
                print_warning(f"Failed to connect to JIRA: {jira_url}")
                jira_client = None
        except Exception as e:
            print_warning(f"Error initializing JIRA client: {e}")
            jira_client = None
    
    try:
        # Pass the LLM client and JIRA client to CommitDocGenHook
        gf_path = recursive_search_git_folder(os.getcwd())
        analyzer = CommitDocGenHook(gf_path, api_client, llm_client, jira_client)
        analyzer.run(message, open_terminal, generate_description)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)





def setup_commit_parser(parser):

    """Sets up an argument parser for generating smart commit messages."""
    commit_parser_description = """
It generates smart commit messages. By default, it will just generate just the Title of the commit message.
1. If you have not configured LLM, it will give an error. You either need to configure LLM or use the API key.
2. If you have not configured JIRA. It will not enhance the commit message with JIRA issue details.
3. For more information, visit https://penify.wiki/dcsgc1
"""
    parser.help = "Generate smart commit messages using local-LLM(no login required)."
    parser.description = commit_parser_description
    parser.formatter_class = argparse.RawDescriptionHelpFormatter
    
    # Add the message argument with better help
    parser.add_argument("-m", "--message", required=False, help="Commit with contextual commit message.", default="N/A")
    parser.add_argument("-e", "--terminal", action="store_true", help="Open edit terminal before committing.")
    parser.add_argument("-d", "--description", action="store_false", help="It will generate commit message with title and description.", default=False)
    
def handle_commit(args):

    """Handle commit functionality by processing arguments and invoking the
    appropriate commands."""
    from penify_hook.commands.commit_commands import commit_code
    from penify_hook.commands.config_commands import get_jira_config, get_llm_config, get_token
    from penify_hook.constants import API_URL

    # Only import dependencies needed for commit functionality here
    open_terminal = args.terminal
    generate_description = args.description
    print_info(f"Generate Commit Description: {generate_description}")        
    # Try to get from config
    llm_config = get_llm_config()
    llm_model = llm_config.get('model')
    llm_api_base = llm_config.get('api_base') 
    llm_api_key = llm_config.get('api_key')
    token = get_token()



    # Try to get from config
    jira_config = get_jira_config()
    jira_url = jira_config.get('url')
    jira_user = jira_config.get('username')
    jira_api_token = jira_config.get('api_token')


    commit_code(API_URL, token, args.message, open_terminal, generate_description,
                llm_model, llm_api_base, llm_api_key,
                jira_url, jira_user, jira_api_token)