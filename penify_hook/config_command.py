


def setup_config_parser(parent_parser):

    # Config subcommand: Create subparsers for config types
    """Set up configuration parsers with subcommands for LLM and JIRA settings."""
    parser = parent_parser.add_subparsers(title="config_type", dest="config_type")

    # Config subcommand: llm
    llm_config_parser = parser.add_parser("llm-cmd", help="Configure LLM settings.")
    llm_config_parser.add_argument("--model", required=True, help="LLM model to use")
    llm_config_parser.add_argument("--api-base", help="API base URL for the LLM service")
    llm_config_parser.add_argument("--api-key", help="API key for the LLM service")

    # Config subcommand: llm-web
    parser.add_parser("llm", help="Configure LLM settings through a web interface")

    # Config subcommand: jira
    jira_config_parser = parser.add_parser("jira-cmd", help="Configure JIRA settings.")
    jira_config_parser.add_argument("--url", required=True, help="JIRA base URL")
    jira_config_parser.add_argument("--username", required=True, help="JIRA username or email")
    jira_config_parser.add_argument("--api-token", required=True, help="JIRA API token")
    jira_config_parser.add_argument("--verify", action="store_true", help="Verify JIRA connection")

    # Config subcommand: jira-web
    parser.add_parser("jira", help="Configure JIRA settings through a web interface")

    # Add all other necessary arguments for config command
    
def handle_config(args):

    # Only import dependencies needed for config functionality here
    
    

    """Handle configuration settings based on the specified config type.
    
    This function processes different types of configurations such as LLM (Language
    Model) and JIRA. It saves configurations, sets up web-based configurations, and
    verifies JIRA connections. Depending on the `args.config_type`, it imports
    necessary modules, handles configuration saving or setup, and optionally
    verifies JIRA connectivity.
    
    Args:
        args (argparse.Namespace): Command-line arguments containing the type of configuration to handle.
    """
    if args.config_type == "llm-cmd":
        from penify_hook.commands.config_commands import save_llm_config
        save_llm_config(args.model, args.api_base, args.api_key)
        print(f"LLM configuration set: Model={args.model}, API Base={args.api_base or 'default'}")

    elif args.config_type == "llm":
        from penify_hook.commands.config_commands import config_llm_web
        config_llm_web()

    elif args.config_type == "jira-cmd":
        from penify_hook.commands.config_commands import save_jira_config
        save_jira_config(args.url, args.username, args.api_token)
        print(f"JIRA configuration set: URL={args.url}, Username={args.username}")
        from penify_hook.jira_client import JiraClient  # Import moved here

        # Verify connection if requested
        if args.verify:
            if JiraClient:
                jira_client = JiraClient(
                    jira_url=args.url,
                    jira_user=args.username,
                    jira_api_token=args.api_token
                )
                if jira_client.is_connected():
                    print("JIRA connection verified successfully!")
                else:
                    print("Failed to connect to JIRA. Please check your credentials.")
            else:
                print("JIRA package not installed. Cannot verify connection.")

    elif args.config_type == "jira":
        from penify_hook.commands.config_commands import config_jira_web
        config_jira_web()

    else:
        print("Please specify a config type: llm, jira")
        return 1
    
    return 0
