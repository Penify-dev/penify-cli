def setup_config_parser(parent_parser):
    # Config subcommand: Create subparsers for config types
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

    # Config subcommand: azure-devops
    azdo_config_parser = parser.add_parser("azdo-cmd", help="Configure Azure DevOps settings.")
    azdo_config_parser.add_argument("--url", required=True, help="Azure DevOps organization URL (e.g., https://dev.azure.com/organization)")
    azdo_config_parser.add_argument("--project", required=True, help="Azure DevOps project name")
    azdo_config_parser.add_argument("--pat-token", required=True, help="Azure DevOps Personal Access Token")
    azdo_config_parser.add_argument("--verify", action="store_true", help="Verify Azure DevOps connection")

    # Config subcommand: azure-devops-web
    parser.add_parser("azdo", help="Configure Azure DevOps settings through a web interface")

    # Config subcommand: asana
    asana_config_parser = parser.add_parser("asana-cmd", help="Configure Asana settings.")
    asana_config_parser.add_argument("--token", required=True, help="Asana Personal Access Token")
    asana_config_parser.add_argument("--workspace", required=True, help="Asana workspace name or ID")
    asana_config_parser.add_argument("--project", help="Asana project name or ID")
    asana_config_parser.add_argument("--verify", action="store_true", help="Verify Asana connection")

    # Config subcommand: asana-web
    parser.add_parser("asana", help="Configure Asana settings through a web interface")

    # Config subcommand: kanban
    kanban_config_parser = parser.add_parser("kanban-cmd", help="Configure Kanban board settings.")
    kanban_config_parser.add_argument("--tool", required=True, choices=["jira", "azdo", "trello", "github", "asana"], help="Kanban tool to use")
    kanban_config_parser.add_argument("--board-id", required=True, help="ID or name of the Kanban board")
    kanban_config_parser.add_argument("--columns", help="Comma-separated list of column names")

    # Config subcommand: kanban-web
    parser.add_parser("kanban", help="Configure Kanban board settings through a web interface")

    # Config subcommand: github
    github_config_parser = parser.add_parser("github-cmd", help="Configure GitHub settings.")
    github_config_parser.add_argument("--token", required=True, help="GitHub Personal Access Token")
    github_config_parser.add_argument("--owner", help="GitHub repository owner (username or organization)")
    github_config_parser.add_argument("--repo", help="GitHub repository name")
    github_config_parser.add_argument("--verify", action="store_true", help="Verify GitHub connection")

    # Config subcommand: github-web
    parser.add_parser("github", help="Configure GitHub settings through a web interface")

    # Add all other necessary arguments for config command
    
def handle_config(args):
    # Only import dependencies needed for config functionality here
    
    

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
    
    elif args.config_type == "azdo-cmd":
        from penify_hook.commands.config_commands import save_azdo_config
        save_azdo_config(args.url, args.project, args.pat_token)
        print(f"Azure DevOps configuration set: URL={args.url}, Project={args.project}")
        
        # Verify connection if requested
        if args.verify:
            try:
                # Verify connection by importing necessary packages
                try:
                    from azure.devops.connection import Connection
                    from msrest.authentication import BasicAuthentication
                    
                    # Create a connection to Azure DevOps
                    credentials = BasicAuthentication('', args.pat_token)
                    connection = Connection(base_url=args.url, creds=credentials)
                    
                    # Test the connection by getting projects
                    core_client = connection.clients.get_core_client()
                    project = core_client.get_project(args.project)
                    
                    if project:
                        print("Azure DevOps connection verified successfully!")
                    else:
                        print(f"Project {args.project} not found. Please check your project name.")
                except ImportError:
                    print("Azure DevOps packages not installed. Run 'pip install azure-devops' to enable verification.")
            except Exception as e:
                print(f"Failed to connect to Azure DevOps: {str(e)}")
    
    elif args.config_type == "azdo":
        from penify_hook.commands.config_commands import config_azdo_web
        config_azdo_web()
    
    elif args.config_type == "asana-cmd":
        from penify_hook.commands.config_commands import save_asana_config
        save_asana_config(args.token, args.workspace, args.project)
        print(f"Asana configuration set: Workspace={args.workspace}, Project={args.project or 'Not specified'}")
        
        # Verify connection if requested
        if args.verify:
            try:
                import asana
                
                # Create Asana client
                client = asana.Client.access_token(args.token)
                
                # Verify token by attempting to get user info
                me = client.users.me()
                print(f"Asana connection verified successfully! Connected as: {me['name']} ({me['email']})")
                
                # Try to get workspace info if specified
                if args.workspace:
                    try:
                        # Check if workspace ID is directly provided or need to search by name
                        if args.workspace.isdigit():
                            workspace = client.workspaces.find_by_id(args.workspace)
                        else:
                            workspaces = list(client.workspaces.find_all())
                            workspace = next((w for w in workspaces if w['name'].lower() == args.workspace.lower()), None)
                            
                        if workspace:
                            print(f"Workspace found: {workspace['name']}")
                        else:
                            print(f"Workspace '{args.workspace}' not found. Please check the workspace name or ID.")
                    except Exception as workspace_e:
                        print(f"Error finding workspace: {str(workspace_e)}")
                
                # Try to get project info if both workspace and project are specified
                if args.project and args.workspace and workspace:
                    try:
                        # Get projects in the workspace
                        projects = list(client.projects.find_all({'workspace': workspace['gid']}))
                        project = next((p for p in projects if p['name'].lower() == args.project.lower() or p['gid'] == args.project), None)
                        
                        if project:
                            print(f"Project found: {project['name']}")
                        else:
                            print(f"Project '{args.project}' not found in workspace '{workspace['name']}'. Please check the project name or ID.")
                    except Exception as project_e:
                        print(f"Error finding project: {str(project_e)}")
                
            except ImportError:
                print("Asana package not installed. Run 'pip install asana' to enable verification.")
            except Exception as e:
                print(f"Failed to connect to Asana: {str(e)}")
    
    elif args.config_type == "asana":
        from penify_hook.commands.config_commands import config_asana_web
        config_asana_web()
    
    elif args.config_type == "kanban-cmd":
        from penify_hook.commands.config_commands import save_kanban_config
        save_kanban_config(args.tool, args.board_id, args.columns)
        print(f"Kanban configuration set: Tool={args.tool}, Board ID={args.board_id}")
        
    elif args.config_type == "kanban":
        from penify_hook.commands.config_commands import config_kanban_web
        config_kanban_web()
    
    elif args.config_type == "github-cmd":
        from penify_hook.commands.config_commands import save_github_config
        save_github_config(args.token, args.owner, args.repo)
        print(f"GitHub configuration set: Owner={args.owner or 'Not specified'}, Repo={args.repo or 'Not specified'}")
        
        # Verify connection if requested
        if args.verify:
            try:
                import requests
                headers = {
                    'Authorization': f'token {args.token}',
                    'Accept': 'application/vnd.github.v3+json'
                }
                
                if args.owner and args.repo:
                    # Verify specific repository access
                    response = requests.get(f"https://api.github.com/repos/{args.owner}/{args.repo}", headers=headers)
                    if response.status_code == 200:
                        print(f"GitHub connection verified successfully! Access to {args.owner}/{args.repo} confirmed.")
                    else:
                        print(f"Failed to access {args.owner}/{args.repo}. Status code: {response.status_code}")
                else:
                    # Verify general access
                    response = requests.get("https://api.github.com/user", headers=headers)
                    if response.status_code == 200:
                        user_data = response.json()
                        print(f"GitHub connection verified successfully! Connected as: {user_data.get('login')}")
                    else:
                        print(f"Failed to connect to GitHub. Status code: {response.status_code}")
            except Exception as e:
                print(f"Error verifying GitHub connection: {str(e)}")
    
    elif args.config_type == "github":
        from penify_hook.commands.config_commands import config_github_web
        config_github_web()

    else:
        print("Please specify a config type: llm, jira, azdo, asana, kanban, github")
        return 1
    
    return 0
