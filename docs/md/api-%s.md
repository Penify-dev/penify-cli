# Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`namespace `[`penify_hook::api_client`](#namespacepenify__hook_1_1api__client) | 
`namespace `[`penify_hook::base_analyzer`](#namespacepenify__hook_1_1base__analyzer) | 
`namespace `[`penify_hook::commands::auth_commands`](#namespacepenify__hook_1_1commands_1_1auth__commands) | 
`namespace `[`penify_hook::commands::commit_commands`](#namespacepenify__hook_1_1commands_1_1commit__commands) | 
`namespace `[`penify_hook::commands::config_commands`](#namespacepenify__hook_1_1commands_1_1config__commands) | 
`namespace `[`penify_hook::commands::doc_commands`](#namespacepenify__hook_1_1commands_1_1doc__commands) | 
`namespace `[`penify_hook::commands::hook_commands`](#namespacepenify__hook_1_1commands_1_1hook__commands) | 
`namespace `[`penify_hook::commit_analyzer`](#namespacepenify__hook_1_1commit__analyzer) | 
`namespace `[`penify_hook::config_command`](#namespacepenify__hook_1_1config__command) | 
`namespace `[`penify_hook::file_analyzer`](#namespacepenify__hook_1_1file__analyzer) | 
`namespace `[`penify_hook::folder_analyzer`](#namespacepenify__hook_1_1folder__analyzer) | 
`namespace `[`penify_hook::git_analyzer`](#namespacepenify__hook_1_1git__analyzer) | 
`namespace `[`penify_hook::jira_client`](#namespacepenify__hook_1_1jira__client) | 
`namespace `[`penify_hook::llm_client`](#namespacepenify__hook_1_1llm__client) | 
`namespace `[`penify_hook::login_command`](#namespacepenify__hook_1_1login__command) | 
`namespace `[`penify_hook::main`](#namespacepenify__hook_1_1main) | 
`namespace `[`penify_hook::ui_utils`](#namespacepenify__hook_1_1ui__utils) | UI utilities for Penify CLI.
`namespace `[`penify_hook::utils`](#namespacepenify__hook_1_1utils) | 
`namespace `[`tests::test_commit_commands`](#namespacetests_1_1test__commit__commands) | 
`namespace `[`tests::test_config_commands`](#namespacetests_1_1test__config__commands) | 
`namespace `[`tests::test_doc_commands`](#namespacetests_1_1test__doc__commands) | 
`namespace `[`tests::test_web_config`](#namespacetests_1_1test__web__config) | 
`class `[`Exception`](#classException) | 

# namespace `penify_hook::api_client` {#namespacepenify__hook_1_1api__client}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`penify_hook::api_client::APIClient`](#classpenify__hook_1_1api__client_1_1APIClient) | 

# class `penify_hook::api_client::APIClient` {#classpenify__hook_1_1api__client_1_1APIClient}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`api_url`](#classpenify__hook_1_1api__client_1_1APIClient_1a130cf688ed35dc0e8cbd8320b6b2d872) | 
`public  `[`AUTH_TOKEN`](#classpenify__hook_1_1api__client_1_1APIClient_1a5bb502603717946ad710b49ad9d95237) | 
`public  `[`BEARER_TOKEN`](#classpenify__hook_1_1api__client_1_1APIClient_1a7d7e2cf42c54eb4f25adee96a09ee7b0) | 
`public def `[`__init__`](#classpenify__hook_1_1api__client_1_1APIClient_1ad9cb741a8baf2d13f845e25a36311086)`(self,`[`api_url`](#classpenify__hook_1_1api__client_1_1APIClient_1a130cf688ed35dc0e8cbd8320b6b2d872)`,str api_token,str bearer_token)` | 
`public def `[`send_file_for_docstring_generation`](#classpenify__hook_1_1api__client_1_1APIClient_1ac5aad61508c2cafdf6e88e6c7d6c82b3)`(self,file_name,content,line_numbers,repo_details)` | Send file content and modified lines to the API and return modified content.
`public def `[`generate_commit_summary`](#classpenify__hook_1_1api__client_1_1APIClient_1a7ff74798e7d428b4e2f20095287eb2ce)`(self,git_diff,str instruction,repo_details,dict jira_context)` | Generates a commit summary by sending a POST request to the API endpoint.
`public list[str] `[`get_supported_file_types`](#classpenify__hook_1_1api__client_1_1APIClient_1a5d2b4a26b24352d951ea79ecc4ff3402)`(self)` | Retrieve supported file types from the API or return a default list.
`public def `[`generate_commit_summary_with_llm`](#classpenify__hook_1_1api__client_1_1APIClient_1ac0ada470b897935f9fb372cd0e7e51e3)`(self,diff,message,bool generate_description,repo_details,`[`LLMClient`](#classpenify__hook_1_1llm__client_1_1LLMClient)` llm_client,jira_context)` | Generates a commit summary using a local LLM client; falls back to API on
`public def `[`get_api_key`](#classpenify__hook_1_1api__client_1_1APIClient_1ad15b790608e703c8c122aa2ead7dfa99)`(self)` | Fetch an API key from a specified URL using a Bearer token.

## Members

#### `public  `[`api_url`](#classpenify__hook_1_1api__client_1_1APIClient_1a130cf688ed35dc0e8cbd8320b6b2d872) {#classpenify__hook_1_1api__client_1_1APIClient_1a130cf688ed35dc0e8cbd8320b6b2d872}

#### `public  `[`AUTH_TOKEN`](#classpenify__hook_1_1api__client_1_1APIClient_1a5bb502603717946ad710b49ad9d95237) {#classpenify__hook_1_1api__client_1_1APIClient_1a5bb502603717946ad710b49ad9d95237}

#### `public  `[`BEARER_TOKEN`](#classpenify__hook_1_1api__client_1_1APIClient_1a7d7e2cf42c54eb4f25adee96a09ee7b0) {#classpenify__hook_1_1api__client_1_1APIClient_1a7d7e2cf42c54eb4f25adee96a09ee7b0}

#### `public def `[`__init__`](#classpenify__hook_1_1api__client_1_1APIClient_1ad9cb741a8baf2d13f845e25a36311086)`(self,`[`api_url`](#classpenify__hook_1_1api__client_1_1APIClient_1a130cf688ed35dc0e8cbd8320b6b2d872)`,str api_token,str bearer_token)` {#classpenify__hook_1_1api__client_1_1APIClient_1ad9cb741a8baf2d13f845e25a36311086}

#### `public def `[`send_file_for_docstring_generation`](#classpenify__hook_1_1api__client_1_1APIClient_1ac5aad61508c2cafdf6e88e6c7d6c82b3)`(self,file_name,content,line_numbers,repo_details)` {#classpenify__hook_1_1api__client_1_1APIClient_1ac5aad61508c2cafdf6e88e6c7d6c82b3}

Send file content and modified lines to the API and return modified content.

#### `public def `[`generate_commit_summary`](#classpenify__hook_1_1api__client_1_1APIClient_1a7ff74798e7d428b4e2f20095287eb2ce)`(self,git_diff,str instruction,repo_details,dict jira_context)` {#classpenify__hook_1_1api__client_1_1APIClient_1a7ff74798e7d428b4e2f20095287eb2ce}

Generates a commit summary by sending a POST request to the API endpoint.

This function constructs a payload containing the git diff and any additional
instructions provided. It then sends this payload to a specified API endpoint
to generate a summary of the commit. If the request is successful, it returns
the response from the API; otherwise, it returns None. The function also
handles optional repository details and JIRA context if they are provided.

Args:
    git_diff (str): The git diff of the commit.
    instruction (str): Additional instruction for the commit. Defaults to "".
    repo_details (dict): Details of the git repository. Defaults to None.
    jira_context (dict): JIRA issue details to enhance the commit summary. Defaults to None.

Returns:
    dict: The response from the API if the request is successful, None otherwise.

#### `public list[str] `[`get_supported_file_types`](#classpenify__hook_1_1api__client_1_1APIClient_1a5d2b4a26b24352d951ea79ecc4ff3402)`(self)` {#classpenify__hook_1_1api__client_1_1APIClient_1a5d2b4a26b24352d951ea79ecc4ff3402}

Retrieve supported file types from the API or return a default list.

#### `public def `[`generate_commit_summary_with_llm`](#classpenify__hook_1_1api__client_1_1APIClient_1ac0ada470b897935f9fb372cd0e7e51e3)`(self,diff,message,bool generate_description,repo_details,`[`LLMClient`](#classpenify__hook_1_1llm__client_1_1LLMClient)` llm_client,jira_context)` {#classpenify__hook_1_1api__client_1_1APIClient_1ac0ada470b897935f9fb372cd0e7e51e3}

Generates a commit summary using a local LLM client; falls back to API on
error.

#### `public def `[`get_api_key`](#classpenify__hook_1_1api__client_1_1APIClient_1ad15b790608e703c8c122aa2ead7dfa99)`(self)` {#classpenify__hook_1_1api__client_1_1APIClient_1ad15b790608e703c8c122aa2ead7dfa99}

Fetch an API key from a specified URL using a Bearer token.

# namespace `penify_hook::base_analyzer` {#namespacepenify__hook_1_1base__analyzer}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`penify_hook::base_analyzer::BaseAnalyzer`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer) | 

# class `penify_hook::base_analyzer::BaseAnalyzer` {#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`folder_path`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1aa67c06dd12b1bafaeaee81c41dcb7e25) | 
`public  `[`repo_path`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a957e81a1ab561f6cecfbe999e7b85499) | 
`public  `[`repo`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a3a9ddfa1dfba81fe21214fe486389369) | 
`public  `[`repo_details`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a9cca3465b0cc00d78324b0a9eac1d7f5) | 
`public  `[`relative_file_path`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1ab702c0c3ba81d159d7c3bcd7ea2abba4) | 
`public  `[`api_client`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a81e9c55709205aaf4ebbe2b41683baf2) | 
`public  `[`supported_file_types`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a0cac0310ec635aa64a34857cf30ce1eb) | 
`public def `[`__init__`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1ab1296a3d1e9070d891801876b66f7344)`(self,str folder_path,`[`APIClient`](#classpenify__hook_1_1api__client_1_1APIClient)` api_client)` | 

## Members

#### `public  `[`folder_path`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1aa67c06dd12b1bafaeaee81c41dcb7e25) {#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1aa67c06dd12b1bafaeaee81c41dcb7e25}

#### `public  `[`repo_path`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a957e81a1ab561f6cecfbe999e7b85499) {#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a957e81a1ab561f6cecfbe999e7b85499}

#### `public  `[`repo`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a3a9ddfa1dfba81fe21214fe486389369) {#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a3a9ddfa1dfba81fe21214fe486389369}

#### `public  `[`repo_details`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a9cca3465b0cc00d78324b0a9eac1d7f5) {#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a9cca3465b0cc00d78324b0a9eac1d7f5}

#### `public  `[`relative_file_path`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1ab702c0c3ba81d159d7c3bcd7ea2abba4) {#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1ab702c0c3ba81d159d7c3bcd7ea2abba4}

#### `public  `[`api_client`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a81e9c55709205aaf4ebbe2b41683baf2) {#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a81e9c55709205aaf4ebbe2b41683baf2}

#### `public  `[`supported_file_types`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a0cac0310ec635aa64a34857cf30ce1eb) {#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1a0cac0310ec635aa64a34857cf30ce1eb}

#### `public def `[`__init__`](#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1ab1296a3d1e9070d891801876b66f7344)`(self,str folder_path,`[`APIClient`](#classpenify__hook_1_1api__client_1_1APIClient)` api_client)` {#classpenify__hook_1_1base__analyzer_1_1BaseAnalyzer_1ab1296a3d1e9070d891801876b66f7344}

# namespace `penify_hook::commands::auth_commands` {#namespacepenify__hook_1_1commands_1_1auth__commands}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`save_credentials`](#namespacepenify__hook_1_1commands_1_1auth__commands_1aa3956ca1749d4218ea1dc6e5b6218b24)`(api_key)`            | Save the API key in a priority-based manner.
`public def `[`login`](#namespacepenify__hook_1_1commands_1_1auth__commands_1a78f375c58bb6f69f98675e6a9ac84655)`(api_url,dashboard_url)`            | Open the login page in a web browser and capture the token via redirect.

## Members

#### `public def `[`save_credentials`](#namespacepenify__hook_1_1commands_1_1auth__commands_1aa3956ca1749d4218ea1dc6e5b6218b24)`(api_key)` {#namespacepenify__hook_1_1commands_1_1auth__commands_1aa3956ca1749d4218ea1dc6e5b6218b24}

Save the API key in a priority-based manner.

This function attempts to save the API key in two locations, based on priority:
1. In a `.env` file located in the root of the Git repository if one is found.
2. In a global `.penify` file located in the user's home directory as a
fallback.  The function first tries to locate the Git repository using
`recursive_search_git_folder`. If a Git repository is found, it reads the
existing `.env` file (if present), updates or adds the API key under the key
`PENIFY_API_TOKEN`, and writes the updated content back. If any error occurs
during this process, it falls back to saving the credentials in the global
`.penify` file. The function handles exceptions and prints appropriate error
messages.

Args:
    api_key (str): The API key to save.

Returns:
    bool: True if the API key is saved successfully, False otherwise.

#### `public def `[`login`](#namespacepenify__hook_1_1commands_1_1auth__commands_1a78f375c58bb6f69f98675e6a9ac84655)`(api_url,dashboard_url)` {#namespacepenify__hook_1_1commands_1_1auth__commands_1a78f375c58bb6f69f98675e6a9ac84655}

Open the login page in a web browser and capture the token via redirect.

# namespace `penify_hook::commands::commit_commands` {#namespacepenify__hook_1_1commands_1_1commit__commands}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`commit_code`](#namespacepenify__hook_1_1commands_1_1commit__commands_1a62564c4e8ad59fc46d56cb0f9122a71a)`(api_url,token,message,open_terminal,generate_description,llm_model,llm_api_base,llm_api_key,jira_url,jira_user,jira_api_token)`            | Enhance Git commits with AI-powered commit messages.
`public def `[`setup_commit_parser`](#namespacepenify__hook_1_1commands_1_1commit__commands_1a8627583116eb78e31a4d3cdc16d2f15c)`(parser)`            | Sets up an argument parser for generating smart commit messages.
`public def `[`handle_commit`](#namespacepenify__hook_1_1commands_1_1commit__commands_1af4f739f524c38b437e4e47673d683e23)`(args)`            | Handle commit functionality by processing arguments and invoking the

## Members

#### `public def `[`commit_code`](#namespacepenify__hook_1_1commands_1_1commit__commands_1a62564c4e8ad59fc46d56cb0f9122a71a)`(api_url,token,message,open_terminal,generate_description,llm_model,llm_api_base,llm_api_key,jira_url,jira_user,jira_api_token)` {#namespacepenify__hook_1_1commands_1_1commit__commands_1a62564c4e8ad59fc46d56cb0f9122a71a}

Enhance Git commits with AI-powered commit messages.

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

#### `public def `[`setup_commit_parser`](#namespacepenify__hook_1_1commands_1_1commit__commands_1a8627583116eb78e31a4d3cdc16d2f15c)`(parser)` {#namespacepenify__hook_1_1commands_1_1commit__commands_1a8627583116eb78e31a4d3cdc16d2f15c}

Sets up an argument parser for generating smart commit messages.

#### `public def `[`handle_commit`](#namespacepenify__hook_1_1commands_1_1commit__commands_1af4f739f524c38b437e4e47673d683e23)`(args)` {#namespacepenify__hook_1_1commands_1_1commit__commands_1af4f739f524c38b437e4e47673d683e23}

Handle commit functionality by processing arguments and invoking the
appropriate commands.

# namespace `penify_hook::commands::config_commands` {#namespacepenify__hook_1_1commands_1_1config__commands}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public None `[`load_env_files`](#namespacepenify__hook_1_1commands_1_1config__commands_1aabe277132ce0bc0aacef951cf1dee2ae)`()`            | Load environment variables from .env files in various locations with proper
`public Path `[`get_penify_config`](#namespacepenify__hook_1_1commands_1_1config__commands_1a6559a82d0bf727703d550d1003d3ed20)`()`            | Returns the path to the `config.json` file within the `.penify` directory,
`public Any `[`get_env_var_or_default`](#namespacepenify__hook_1_1commands_1_1config__commands_1a3caf2b062dd33b1f1d7ddc7224f0ff87)`(str env_var,Any default)`            | Get environment variable or return default value.
`public def `[`save_llm_config`](#namespacepenify__hook_1_1commands_1_1config__commands_1a4617bc5956e502c9555dc0dda0376df4)`(model,api_base,api_key)`            | Save LLM configuration settings to an .env file.
`public def `[`save_jira_config`](#namespacepenify__hook_1_1commands_1_1config__commands_1ab2486ac2bf16b4a671e49625bfa4f9b4)`(url,username,api_token)`            | Save JIRA configuration settings to a .env file.
`public Dict[str, str] `[`get_llm_config`](#namespacepenify__hook_1_1commands_1_1config__commands_1a6492bc8e7df6e38bb06ad05e572d4cc0)`()`            | Retrieve LLM configuration from environment variables.
`public Dict[str, str] `[`get_jira_config`](#namespacepenify__hook_1_1commands_1_1config__commands_1a15bf3685c4dcb5c15ba6a4055e484cf2)`()`            | Retrieve JIRA configuration from environment variables.
`public def `[`config_llm_web`](#namespacepenify__hook_1_1commands_1_1config__commands_1a185dfc34a655ed80e6c95939b6f3c35c)`()`            | Starts an HTTP server for configuring LLM settings via a web interface.
`public def `[`config_jira_web`](#namespacepenify__hook_1_1commands_1_1config__commands_1af115198ea5d6808ccb98733957f50b06)`()`            | Starts a web server for configuring JIRA settings.
`public Optional[str] `[`get_token`](#namespacepenify__hook_1_1commands_1_1config__commands_1a5503d51c905e2f1b299b12d2a73bd812)`()`            | Retrieves an API token using a prioritized method.

## Members

#### `public None `[`load_env_files`](#namespacepenify__hook_1_1commands_1_1config__commands_1aabe277132ce0bc0aacef951cf1dee2ae)`()` {#namespacepenify__hook_1_1commands_1_1config__commands_1aabe277132ce0bc0aacef951cf1dee2ae}

Load environment variables from .env files in various locations with proper
priority.

This function loads environment variables from .env files located in different
directories, prioritizing the current directory over the Git repo root and the
user home directory. The loading process ensures that later files override
earlier ones.

#### `public Path `[`get_penify_config`](#namespacepenify__hook_1_1commands_1_1config__commands_1a6559a82d0bf727703d550d1003d3ed20)`()` {#namespacepenify__hook_1_1commands_1_1config__commands_1a6559a82d0bf727703d550d1003d3ed20}

Returns the path to the `config.json` file within the `.penify` directory,
creating it if necessary.

#### `public Any `[`get_env_var_or_default`](#namespacepenify__hook_1_1commands_1_1config__commands_1a3caf2b062dd33b1f1d7ddc7224f0ff87)`(str env_var,Any default)` {#namespacepenify__hook_1_1commands_1_1config__commands_1a3caf2b062dd33b1f1d7ddc7224f0ff87}

Get environment variable or return default value.

#### `public def `[`save_llm_config`](#namespacepenify__hook_1_1commands_1_1config__commands_1a4617bc5956e502c9555dc0dda0376df4)`(model,api_base,api_key)` {#namespacepenify__hook_1_1commands_1_1config__commands_1a4617bc5956e502c9555dc0dda0376df4}

Save LLM configuration settings to an .env file.

This function saves the LLM configuration following a specific priority: 1. Git
repo root .env (if inside a git repo) 2. User home directory .env  It handles
the detection of the Git repo root, reads the existing .env content, updates it
with the new LLM configuration, and writes it back to the file. It also reloads
the environment variables to make changes immediately available.

Args:
    model (str): The name of the language model.
    api_base (str): The base URL for the API.
    api_key (str): The API key for authentication.

Returns:
    bool: True if the configuration is saved successfully, False otherwise.

#### `public def `[`save_jira_config`](#namespacepenify__hook_1_1commands_1_1config__commands_1ab2486ac2bf16b4a671e49625bfa4f9b4)`(url,username,api_token)` {#namespacepenify__hook_1_1commands_1_1config__commands_1ab2486ac2bf16b4a671e49625bfa4f9b4}

Save JIRA configuration settings to a .env file.

This function saves JIRA configuration following these steps: 1. Determine the
target .env file location based on whether the current directory is inside a
Git repository. 2. If inside a Git repo, use the Git repo root's .env file;
otherwise, use the user home directory's .env file. 3. Read the existing
content of the .env file (if it exists) to preserve other settings. 4. Update
the .env content with the new JIRA configuration. 5. Write the updated content
back to the .env file. 6. Optionally, reload environment variables to make
changes immediately available.

Args:
    url (str): The JIRA URL to be saved in the .env file.
    username (str): The JIRA username to be saved in the .env file.
    api_token (str): The JIRA API token to be saved in the .env file.

Returns:
    bool: True if the configuration was successfully saved, False otherwise.

#### `public Dict[str, str] `[`get_llm_config`](#namespacepenify__hook_1_1commands_1_1config__commands_1a6492bc8e7df6e38bb06ad05e572d4cc0)`()` {#namespacepenify__hook_1_1commands_1_1config__commands_1a6492bc8e7df6e38bb06ad05e572d4cc0}

Retrieve LLM configuration from environment variables.

#### `public Dict[str, str] `[`get_jira_config`](#namespacepenify__hook_1_1commands_1_1config__commands_1a15bf3685c4dcb5c15ba6a4055e484cf2)`()` {#namespacepenify__hook_1_1commands_1_1config__commands_1a15bf3685c4dcb5c15ba6a4055e484cf2}

Retrieve JIRA configuration from environment variables.

#### `public def `[`config_llm_web`](#namespacepenify__hook_1_1commands_1_1config__commands_1a185dfc34a655ed80e6c95939b6f3c35c)`()` {#namespacepenify__hook_1_1commands_1_1config__commands_1a185dfc34a655ed80e6c95939b6f3c35c}

Starts an HTTP server for configuring LLM settings via a web interface.

#### `public def `[`config_jira_web`](#namespacepenify__hook_1_1commands_1_1config__commands_1af115198ea5d6808ccb98733957f50b06)`()` {#namespacepenify__hook_1_1commands_1_1config__commands_1af115198ea5d6808ccb98733957f50b06}

Starts a web server for configuring JIRA settings.

#### `public Optional[str] `[`get_token`](#namespacepenify__hook_1_1commands_1_1config__commands_1a5503d51c905e2f1b299b12d2a73bd812)`()` {#namespacepenify__hook_1_1commands_1_1config__commands_1a5503d51c905e2f1b299b12d2a73bd812}

Retrieves an API token using a prioritized method.

This function first attempts to load environment variables from all `.env`
files and checks if the `PENIFY_API_TOKEN` environment variable is set. If
found, it returns the token. If not, it looks for the API key in a
configuration file named 'api_keys'. If both methods fail, it returns None.

Returns:
    str or None: The API token if found, otherwise None.

# namespace `penify_hook::commands::doc_commands` {#namespacepenify__hook_1_1commands_1_1doc__commands}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`generate_doc`](#namespacepenify__hook_1_1commands_1_1doc__commands_1a4daac68bc563432bf25c85dc78081a25)`(api_url,token,location)`            | Generates documentation based on the given parameters.
`public def `[`setup_docgen_parser`](#namespacepenify__hook_1_1commands_1_1doc__commands_1acc7f4ead1b11951d885fa5c151c2cbe0)`(parser)`            | Configure a parser for generating documentation using Git commands.
`public def `[`handle_docgen`](#namespacepenify__hook_1_1commands_1_1doc__commands_1a2006ab13bff718ef783868a910c0b704)`(args)`            | Handle document generation and hook management based on subcommands.

## Members

#### `public def `[`generate_doc`](#namespacepenify__hook_1_1commands_1_1doc__commands_1a4daac68bc563432bf25c85dc78081a25)`(api_url,token,location)` {#namespacepenify__hook_1_1commands_1_1doc__commands_1a4daac68bc563432bf25c85dc78081a25}

Generates documentation based on the given parameters.

This function initializes an API client using the provided API URL and token.
It then generates documentation by analyzing the specified location, which can
be a folder, a file, or the current working directory if no location is
provided. The function handles different types of analysis based on the input
location and reports any errors encountered during the process.

Args:
    api_url (str): The URL of the API to connect to for documentation generation.
    token (str): The authentication token for accessing the API.
    location (str?): The path to a specific file or folder to analyze. If not provided,
        the current working directory is used.

#### `public def `[`setup_docgen_parser`](#namespacepenify__hook_1_1commands_1_1doc__commands_1acc7f4ead1b11951d885fa5c151c2cbe0)`(parser)` {#namespacepenify__hook_1_1commands_1_1doc__commands_1acc7f4ead1b11951d885fa5c151c2cbe0}

Configure a parser for generating documentation using Git commands.

#### `public def `[`handle_docgen`](#namespacepenify__hook_1_1commands_1_1doc__commands_1a2006ab13bff718ef783868a910c0b704)`(args)` {#namespacepenify__hook_1_1commands_1_1doc__commands_1a2006ab13bff718ef783868a910c0b704}

Handle document generation and hook management based on subcommands.

# namespace `penify_hook::commands::hook_commands` {#namespacepenify__hook_1_1commands_1_1hook__commands}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`install_git_hook`](#namespacepenify__hook_1_1commands_1_1hook__commands_1adff8f5d3bf1c3795974a391ee95b72b2)`(location,token)`            | Install a post-commit Git hook that generates documentation for changed files.
`public def `[`uninstall_git_hook`](#namespacepenify__hook_1_1commands_1_1hook__commands_1a81543eb5fa835fd1237f24e8bce6201d)`(location)`            | Uninstalls the post-commit hook from the specified location.

## Members

#### `public def `[`install_git_hook`](#namespacepenify__hook_1_1commands_1_1hook__commands_1adff8f5d3bf1c3795974a391ee95b72b2)`(location,token)` {#namespacepenify__hook_1_1commands_1_1hook__commands_1adff8f5d3bf1c3795974a391ee95b72b2}

Install a post-commit Git hook that generates documentation for changed files.

#### `public def `[`uninstall_git_hook`](#namespacepenify__hook_1_1commands_1_1hook__commands_1a81543eb5fa835fd1237f24e8bce6201d)`(location)` {#namespacepenify__hook_1_1commands_1_1hook__commands_1a81543eb5fa835fd1237f24e8bce6201d}

Uninstalls the post-commit hook from the specified location.

# namespace `penify_hook::commit_analyzer` {#namespacepenify__hook_1_1commit__analyzer}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`penify_hook::commit_analyzer::CommitDocGenHook`](#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook) | 

# class `penify_hook::commit_analyzer::CommitDocGenHook` {#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook}

```
class penify_hook::commit_analyzer::CommitDocGenHook
  : public penify_hook.base_analyzer.BaseAnalyzer
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`llm_client`](#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1ad93360e31f2ec58a0d7c9f08b219028a) | 
`public def `[`__init__`](#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1af127d86729e226d74dbeb095b008db3e)`(self,str repo_path,`[`APIClient`](#classpenify__hook_1_1api__client_1_1APIClient)` api_client,`[`llm_client`](#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1ad93360e31f2ec58a0d7c9f08b219028a)`,jira_client)` | 
`public dict `[`get_summary`](#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1a8496194276441fa2eb2fa014eaab9a37)`(self,str instruction,bool generate_description)` | Generate a summary for the commit based on the staged changes.
`public def `[`run`](#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1a6370a03f7ed9175ef6f81e931a105ea9)`(self,Optional msg,bool edit_commit_message,bool generate_description)` | Run the post-commit hook.
`public tuple `[`process_jira_integration`](#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1adda13cc121d96342476ccf72b63a007f)`(self,str title,str description,str msg)` | Process JIRA integration by extracting issue keys from commit message

## Members

#### `public  `[`llm_client`](#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1ad93360e31f2ec58a0d7c9f08b219028a) {#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1ad93360e31f2ec58a0d7c9f08b219028a}

#### `public def `[`__init__`](#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1af127d86729e226d74dbeb095b008db3e)`(self,str repo_path,`[`APIClient`](#classpenify__hook_1_1api__client_1_1APIClient)` api_client,`[`llm_client`](#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1ad93360e31f2ec58a0d7c9f08b219028a)`,jira_client)` {#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1af127d86729e226d74dbeb095b008db3e}

#### `public dict `[`get_summary`](#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1a8496194276441fa2eb2fa014eaab9a37)`(self,str instruction,bool generate_description)` {#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1a8496194276441fa2eb2fa014eaab9a37}

Generate a summary for the commit based on the staged changes.

This function retrieves the differences of the staged changes in the repository
and generates a commit summary using the provided instruction. If there are no
changes staged for commit, an exception is raised. If a JIRA client is
connected, it will attempt to extract issue keys from the current branch and
use them to fetch context. The summary can be generated either with a Language
Model (LLM) client or through the API client.

Args:
    instruction (str): A string containing instructions for generating the commit summary.
    generate_description (bool): Whether to include detailed descriptions in the summary.

Raises:
    ValueError: If there are no changes staged for commit.

#### `public def `[`run`](#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1a6370a03f7ed9175ef6f81e931a105ea9)`(self,Optional msg,bool edit_commit_message,bool generate_description)` {#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1a6370a03f7ed9175ef6f81e931a105ea9}

Run the post-commit hook.

This method processes the modified files from the last commit, stages them, and
creates an auto-commit with an optional message. It also handles JIRA
integration if available. If there is an error generating the commit summary,
an exception is raised.

Args:
    msg (Optional[str]): An optional message to include in the commit.
    edit_commit_message (bool): A flag indicating whether to open the git commit
        edit terminal after committing.
    generate_description (bool): A flag indicating whether to include a description
        in the commit message.

#### `public tuple `[`process_jira_integration`](#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1adda13cc121d96342476ccf72b63a007f)`(self,str title,str description,str msg)` {#classpenify__hook_1_1commit__analyzer_1_1CommitDocGenHook_1adda13cc121d96342476ccf72b63a007f}

Process JIRA integration by extracting issue keys from commit message
components and branch name.

This function looks for JIRA issue keys in the provided commit title,
description, original user message, and the active branch name. It uses these
keys to update the commit message with JIRA information and adds comments to
the corresponding JIRA issues. If no keys are found, it logs a warning.

Args:
    title (str): The generated commit title.
    description (str): The generated commit description.
    msg (str): The original user message that might contain JIRA references.

Returns:
    tuple: A tuple containing the updated commit title and description with included JIRA
        information.

# namespace `penify_hook::config_command` {#namespacepenify__hook_1_1config__command}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`setup_config_parser`](#namespacepenify__hook_1_1config__command_1a4f3eb92164a69df1446d745f8a09285e)`(parent_parser)`            | Set up configuration parsers with subcommands for LLM and JIRA settings.
`public def `[`handle_config`](#namespacepenify__hook_1_1config__command_1a240e5331681eb574ac319d7458783bde)`(args)`            | Handle configuration settings based on the specified config type.

## Members

#### `public def `[`setup_config_parser`](#namespacepenify__hook_1_1config__command_1a4f3eb92164a69df1446d745f8a09285e)`(parent_parser)` {#namespacepenify__hook_1_1config__command_1a4f3eb92164a69df1446d745f8a09285e}

Set up configuration parsers with subcommands for LLM and JIRA settings.

#### `public def `[`handle_config`](#namespacepenify__hook_1_1config__command_1a240e5331681eb574ac319d7458783bde)`(args)` {#namespacepenify__hook_1_1config__command_1a240e5331681eb574ac319d7458783bde}

Handle configuration settings based on the specified config type.

This function processes different types of configurations such as LLM (Language
Model) and JIRA. It saves configurations, sets up web-based configurations, and
verifies JIRA connections. Depending on the `args.config_type`, it imports
necessary modules, handles configuration saving or setup, and optionally
verifies JIRA connectivity.

Args:
    args (argparse.Namespace): Command-line arguments containing the type of configuration to handle.

# namespace `penify_hook::file_analyzer` {#namespacepenify__hook_1_1file__analyzer}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`penify_hook::file_analyzer::FileAnalyzerGenHook`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook) | 

# class `penify_hook::file_analyzer::FileAnalyzerGenHook` {#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook}

```
class penify_hook::file_analyzer::FileAnalyzerGenHook
  : public penify_hook.base_analyzer.BaseAnalyzer
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`file_path`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a9b03b88a9ce1b9af945279375048dc32) | 
`public def `[`__init__`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a190c473090b2a07e7cb43073a3211c4b)`(self,str file_path,`[`APIClient`](#classpenify__hook_1_1api__client_1_1APIClient)` api_client)` | 
`public def `[`process_file`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a2cc6c22ef588fccf3eed9bbc57fb6d6e)`(self,`[`file_path`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a9b03b88a9ce1b9af945279375048dc32)`,pbar,str new_param)` | Processes a file by validating its extension, reading content,
`public def `[`print_processing`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a6ab39391dfb7686f2a2d21a702dd3073)`(self,`[`file_path`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a9b03b88a9ce1b9af945279375048dc32)`)` | Prints a message indicating that a file is being processed.
`public def `[`run`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a4f4dffbc432fac3e259d957dd1e187f1)`(self)` | Runs the documentation process with a progress bar.

## Members

#### `public  `[`file_path`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a9b03b88a9ce1b9af945279375048dc32) {#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a9b03b88a9ce1b9af945279375048dc32}

#### `public def `[`__init__`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a190c473090b2a07e7cb43073a3211c4b)`(self,str file_path,`[`APIClient`](#classpenify__hook_1_1api__client_1_1APIClient)` api_client)` {#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a190c473090b2a07e7cb43073a3211c4b}

#### `public def `[`process_file`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a2cc6c22ef588fccf3eed9bbc57fb6d6e)`(self,`[`file_path`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a9b03b88a9ce1b9af945279375048dc32)`,pbar,str new_param)` {#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a2cc6c22ef588fccf3eed9bbc57fb6d6e}

Processes a file by validating its extension, reading content,
generating documentation, and writing changes back to the file.  The function
performs several stages of processing: 1. Validates the file's extension to
ensure it is supported. 2. Reads the content of the file. 3. Sends the file
content for documentation generation. 4. Writes the generated documentation
back to the file if there are changes.

Args:
    file_path (str): The path of the file to be processed.
    pbar (tqdm.tqdm): A progress bar object to update the status of processing stages.
    new_param (str?): An additional parameter for future use. Defaults to an empty string.

#### `public def `[`print_processing`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a6ab39391dfb7686f2a2d21a702dd3073)`(self,`[`file_path`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a9b03b88a9ce1b9af945279375048dc32)`)` {#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a6ab39391dfb7686f2a2d21a702dd3073}

Prints a message indicating that a file is being processed.

#### `public def `[`run`](#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a4f4dffbc432fac3e259d957dd1e187f1)`(self)` {#classpenify__hook_1_1file__analyzer_1_1FileAnalyzerGenHook_1a4f4dffbc432fac3e259d957dd1e187f1}

Runs the documentation process with a progress bar.

This method orchestrates the documentation process by creating a progress bar,
processing the file, and handling exceptions to ensure the progress bar
completes properly. It updates the progress bar through various stages and
provides feedback based on the result of the file processing.

# namespace `penify_hook::folder_analyzer` {#namespacepenify__hook_1_1folder__analyzer}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`penify_hook::folder_analyzer::FolderAnalyzerGenHook`](#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook) | 

# class `penify_hook::folder_analyzer::FolderAnalyzerGenHook` {#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook}

```
class penify_hook::folder_analyzer::FolderAnalyzerGenHook
  : public penify_hook.base_analyzer.BaseAnalyzer
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`dir_path`](#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook_1a53f73d69cc0f00763ee4830e4f0f7393) | 
`public def `[`__init__`](#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook_1a1bb0358140931d82c7616f12efe31821)`(self,str dir_path,`[`APIClient`](#classpenify__hook_1_1api__client_1_1APIClient)` api_client)` | 
`public def `[`list_all_files_in_dir`](#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook_1a70b845318fc7ac3b607daf26378e19ec)`(self,str dir_path)` | List all non-hidden files in a directory and its subdirectories.
`public def `[`run`](#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook_1afd189d1b8c773bf710a899eb21fd76cc)`(self)` | Run the post-commit hook and process files with a progress bar.

## Members

#### `public  `[`dir_path`](#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook_1a53f73d69cc0f00763ee4830e4f0f7393) {#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook_1a53f73d69cc0f00763ee4830e4f0f7393}

#### `public def `[`__init__`](#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook_1a1bb0358140931d82c7616f12efe31821)`(self,str dir_path,`[`APIClient`](#classpenify__hook_1_1api__client_1_1APIClient)` api_client)` {#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook_1a1bb0358140931d82c7616f12efe31821}

#### `public def `[`list_all_files_in_dir`](#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook_1a70b845318fc7ac3b607daf26378e19ec)`(self,str dir_path)` {#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook_1a70b845318fc7ac3b607daf26378e19ec}

List all non-hidden files in a directory and its subdirectories.

This function recursively traverses the specified directory and its
subdirectories, collecting paths of all non-hidden files. It filters out hidden
directories and files (those starting with a dot) to ensure only visible files
are returned.

Args:
    dir_path (str): The path to the directory whose files and subdirectory files need to be listed.

#### `public def `[`run`](#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook_1afd189d1b8c773bf710a899eb21fd76cc)`(self)` {#classpenify__hook_1_1folder__analyzer_1_1FolderAnalyzerGenHook_1afd189d1b8c773bf710a899eb21fd76cc}

Run the post-commit hook and process files with a progress bar.

# namespace `penify_hook::git_analyzer` {#namespacepenify__hook_1_1git__analyzer}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`penify_hook::git_analyzer::GitDocGenHook`](#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook) | 

# class `penify_hook::git_analyzer::GitDocGenHook` {#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook}

```
class penify_hook::git_analyzer::GitDocGenHook
  : public penify_hook.base_analyzer.BaseAnalyzer
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`__init__`](#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a92275fddb43dbef6dfdb6c1ed6e96d0c)`(self,str repo_path,`[`APIClient`](#classpenify__hook_1_1api__client_1_1APIClient)` api_client)` | 
`public def `[`get_modified_files_in_last_commit`](#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a17549766100e91eb94b5f1a1d34bf481)`(self)` | Get the list of files modified in the last commit.
`public def `[`get_modified_lines`](#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a974d2f51315ed6a1965a7fd7e2ced0cd)`(self,diff_text)` | Extract modified line numbers from a diff text.
`public def `[`process_file`](#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a05313caa22b173ce75638f0db08eeb85)`(self,file_path)` | Processes a file by checking its type, reading its content, and sending it to
`public def `[`run`](#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a3beba14e92d717391a74bb70b1fab0ae)`(self)` | Run the post-commit hook.

## Members

#### `public def `[`__init__`](#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a92275fddb43dbef6dfdb6c1ed6e96d0c)`(self,str repo_path,`[`APIClient`](#classpenify__hook_1_1api__client_1_1APIClient)` api_client)` {#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a92275fddb43dbef6dfdb6c1ed6e96d0c}

#### `public def `[`get_modified_files_in_last_commit`](#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a17549766100e91eb94b5f1a1d34bf481)`(self)` {#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a17549766100e91eb94b5f1a1d34bf481}

Get the list of files modified in the last commit.

#### `public def `[`get_modified_lines`](#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a974d2f51315ed6a1965a7fd7e2ced0cd)`(self,diff_text)` {#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a974d2f51315ed6a1965a7fd7e2ced0cd}

Extract modified line numbers from a diff text.

This function processes a diff text to identify and extract the line numbers
that have been modified. It distinguishes between added and deleted lines and
keeps track of the current line number as it parses through the diff. The
function handles hunk headers and ensures that any deletions at the end of the
file are also captured.

Args:
    diff_text (str): A string containing the diff text to be processed.

#### `public def `[`process_file`](#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a05313caa22b173ce75638f0db08eeb85)`(self,file_path)` {#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a05313caa22b173ce75638f0db08eeb85}

Processes a file by checking its type, reading its content, and sending it to
an API.

This method constructs the absolute path of the specified file and verifies if
the file has a valid extension. If the file type is supported, it reads the
content of the file and retrieves the differences from the last commit in the
repository. If changes are detected, it sends the file content along with the
modified lines to an API for further processing. If the API response indicates
no changes, the original file will not be overwritten.

Args:
    file_path (str): The relative path to the file to be processed.

#### `public def `[`run`](#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a3beba14e92d717391a74bb70b1fab0ae)`(self)` {#classpenify__hook_1_1git__analyzer_1_1GitDocGenHook_1a3beba14e92d717391a74bb70b1fab0ae}

Run the post-commit hook.

This method retrieves the list of modified files from the last commit and
processes each file. It stages any files that have been modified during
processing and creates an auto-commit if changes were made. A progress bar is
displayed to indicate the processing status of each file. The method handles
any exceptions that occur during file processing, printing an error message for
each file that fails to process. If any modifications are made to the files, an
auto-commit is created to save those changes.

# namespace `penify_hook::jira_client` {#namespacepenify__hook_1_1jira__client}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`penify_hook::jira_client::JiraClient`](#classpenify__hook_1_1jira__client_1_1JiraClient) | Client for interacting with JIRA API

# class `penify_hook::jira_client::JiraClient` {#classpenify__hook_1_1jira__client_1_1JiraClient}

Client for interacting with JIRA API

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`jira_url`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a3c0cfecff02a75cb7001509a595b8197) | 
`public  `[`jira_user`](#classpenify__hook_1_1jira__client_1_1JiraClient_1ae56104d5aa7bda7bb26d169c4b46038c) | 
`public  `[`jira_api_token`](#classpenify__hook_1_1jira__client_1_1JiraClient_1afc5c90e53b702f9fc27e2ee7d3f991b9) | 
`public  `[`jira_client`](#classpenify__hook_1_1jira__client_1_1JiraClient_1aefb3f96c79358cf3a95d96d3747235b6) | 
`public def `[`__init__`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a47efc1ec07389c960f2dfb37ba8c09f5)`(self,str jira_url,str jira_user,str jira_api_token)` | Initialize the JIRA client.
`public bool `[`is_connected`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a00d0f9ae006313a21576362d26ac5ec8)`(self)` | Check if the JIRA client is connected.
`public List[str] `[`extract_issue_keys_from_branch`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a093d6456fe053ef7a7862d5d6851910c)`(self,str branch_name)` | Extracts unique JIRA issue keys from a branch name.
`public List[str] `[`extract_issue_keys`](#classpenify__hook_1_1jira__client_1_1JiraClient_1ad2823ad1d3baaedd38039913c3a97fd7)`(self,str text)` | Extract unique JIRA issue keys from the given text.
`public Optional[Dict[str, Any]] `[`get_issue_details`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a65f6924819084b7c8d268956a784804a)`(self,str issue_key)` | Retrieve details of a JIRA issue based on its key.
`public bool `[`add_comment`](#classpenify__hook_1_1jira__client_1_1JiraClient_1aa1f374116c64cd5f1492ec7f7e40f9c1)`(self,str issue_key,str comment)` | Adds a comment to a JIRA issue.
`public bool `[`update_issue_status`](#classpenify__hook_1_1jira__client_1_1JiraClient_1aca8837552d37bfd611de23441a240826)`(self,str issue_key,str transition_name)` | Update the status of a JIRA issue.
`public tuple `[`format_commit_message_with_jira_info`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a49ea1149758f7f5212149d357b13cc23)`(self,str commit_title,str commit_description,List issue_keys)` | Format commit message with JIRA issue information.
`public Dict[str, Any] `[`get_detailed_issue_context`](#classpenify__hook_1_1jira__client_1_1JiraClient_1aa967169a4b7970c67c0947b9ac56f746)`(self,str issue_key)` | Retrieve comprehensive details about a JIRA issue including context for better
`public Dict[str, Any] `[`get_commit_context_from_issues`](#classpenify__hook_1_1jira__client_1_1JiraClient_1afb41ce6f13c30b1265d439ddf04bf2cd)`(self,List issue_keys)` | Gather contextual information from JIRA issues to improve commit messages.
`public tuple `[`enhance_commit_message`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a70d2c5a6432aa6f238da0ff65d49a760)`(self,str title,str description,List issue_keys)` | Enhance a commit message with business and technical context from JIRA issues.

## Members

#### `public  `[`jira_url`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a3c0cfecff02a75cb7001509a595b8197) {#classpenify__hook_1_1jira__client_1_1JiraClient_1a3c0cfecff02a75cb7001509a595b8197}

#### `public  `[`jira_user`](#classpenify__hook_1_1jira__client_1_1JiraClient_1ae56104d5aa7bda7bb26d169c4b46038c) {#classpenify__hook_1_1jira__client_1_1JiraClient_1ae56104d5aa7bda7bb26d169c4b46038c}

#### `public  `[`jira_api_token`](#classpenify__hook_1_1jira__client_1_1JiraClient_1afc5c90e53b702f9fc27e2ee7d3f991b9) {#classpenify__hook_1_1jira__client_1_1JiraClient_1afc5c90e53b702f9fc27e2ee7d3f991b9}

#### `public  `[`jira_client`](#classpenify__hook_1_1jira__client_1_1JiraClient_1aefb3f96c79358cf3a95d96d3747235b6) {#classpenify__hook_1_1jira__client_1_1JiraClient_1aefb3f96c79358cf3a95d96d3747235b6}

#### `public def `[`__init__`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a47efc1ec07389c960f2dfb37ba8c09f5)`(self,str jira_url,str jira_user,str jira_api_token)` {#classpenify__hook_1_1jira__client_1_1JiraClient_1a47efc1ec07389c960f2dfb37ba8c09f5}

Initialize the JIRA client.

Args:
    jira_url: Base URL for JIRA instance (e.g., "https://your-domain.atlassian.net")
    jira_user: JIRA username or email
    jira_api_token: JIRA API token

#### `public bool `[`is_connected`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a00d0f9ae006313a21576362d26ac5ec8)`(self)` {#classpenify__hook_1_1jira__client_1_1JiraClient_1a00d0f9ae006313a21576362d26ac5ec8}

Check if the JIRA client is connected.

#### `public List[str] `[`extract_issue_keys_from_branch`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a093d6456fe053ef7a7862d5d6851910c)`(self,str branch_name)` {#classpenify__hook_1_1jira__client_1_1JiraClient_1a093d6456fe053ef7a7862d5d6851910c}

Extracts unique JIRA issue keys from a branch name.

#### `public List[str] `[`extract_issue_keys`](#classpenify__hook_1_1jira__client_1_1JiraClient_1ad2823ad1d3baaedd38039913c3a97fd7)`(self,str text)` {#classpenify__hook_1_1jira__client_1_1JiraClient_1ad2823ad1d3baaedd38039913c3a97fd7}

Extract unique JIRA issue keys from the given text.

#### `public Optional[Dict[str, Any]] `[`get_issue_details`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a65f6924819084b7c8d268956a784804a)`(self,str issue_key)` {#classpenify__hook_1_1jira__client_1_1JiraClient_1a65f6924819084b7c8d268956a784804a}

Retrieve details of a JIRA issue based on its key.

This function fetches detailed information about a specified JIRA issue using
the provided issue key. It first checks if the JIRA client is connected; if
not, it logs a warning and returns `None`. If connected, it attempts to
retrieve the issue from the JIRA server. On success, it constructs and returns
a dictionary containing various details such as the issue's key, summary,
status, description, assignee, reporter, type, priority, and URL. Errors during
this process are logged, and `None` is returned.

Args:
    issue_key (str): The JIRA issue key (e.g., "PROJECT-123").

#### `public bool `[`add_comment`](#classpenify__hook_1_1jira__client_1_1JiraClient_1aa1f374116c64cd5f1492ec7f7e40f9c1)`(self,str issue_key,str comment)` {#classpenify__hook_1_1jira__client_1_1JiraClient_1aa1f374116c64cd5f1492ec7f7e40f9c1}

Adds a comment to a JIRA issue.

#### `public bool `[`update_issue_status`](#classpenify__hook_1_1jira__client_1_1JiraClient_1aca8837552d37bfd611de23441a240826)`(self,str issue_key,str transition_name)` {#classpenify__hook_1_1jira__client_1_1JiraClient_1aca8837552d37bfd611de23441a240826}

Update the status of a JIRA issue.

This method checks if the JIRA client is connected, retrieves available
transitions for the given issue, finds the transition ID by name, and updates
the issue's status accordingly. If any step fails or the specified transition
is not found, appropriate logs are generated, and False is returned.

Args:
    issue_key (str): The key of the JIRA issue to be updated.
    transition_name (str): The name of the desired transition.

Returns:
    bool: True if the status was successfully updated, False otherwise.

#### `public tuple `[`format_commit_message_with_jira_info`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a49ea1149758f7f5212149d357b13cc23)`(self,str commit_title,str commit_description,List issue_keys)` {#classpenify__hook_1_1jira__client_1_1JiraClient_1a49ea1149758f7f5212149d357b13cc23}

Format commit message with JIRA issue information.

This function updates the provided commit title and description by
incorporating JIRA issue keys. If no issue keys are supplied, it extracts them
from the commit title and description. It then formats the commit title to
include the first issue key if not already present and appends detailed
information about each issue to the commit description.

Args:
    commit_title (str): The original commit title.
    commit_description (str): The original commit description.
    issue_keys (List[str]?): A list of JIRA issue keys to include in the commit message. If not
        provided, issue keys will be extracted from both the title and the description.

Returns:
    tuple: A tuple containing the updated commit title and description with JIRA
        information included.

#### `public Dict[str, Any] `[`get_detailed_issue_context`](#classpenify__hook_1_1jira__client_1_1JiraClient_1aa967169a4b7970c67c0947b9ac56f746)`(self,str issue_key)` {#classpenify__hook_1_1jira__client_1_1JiraClient_1aa967169a4b7970c67c0947b9ac56f746}

Retrieve comprehensive details about a JIRA issue including context for better
commit messages.

This function fetches detailed information from a specified JIRA issue and
constructs a dictionary containing various context fields such as the issue
summary, description, type, status, priority, comments, URL, and additional
custom fields like acceptance criteria and sprint information. It handles
errors by logging appropriate warnings or errors.

Args:
    issue_key (str): The JIRA issue key (e.g., "PROJECT-123").

Returns:
    Dict[str, Any]: A dictionary containing business and technical context from the issue.

#### `public Dict[str, Any] `[`get_commit_context_from_issues`](#classpenify__hook_1_1jira__client_1_1JiraClient_1afb41ce6f13c30b1265d439ddf04bf2cd)`(self,List issue_keys)` {#classpenify__hook_1_1jira__client_1_1JiraClient_1afb41ce6f13c30b1265d439ddf04bf2cd}

Gather contextual information from JIRA issues to improve commit messages.

This function processes a list of JIRA issue keys, retrieves detailed context
for each issue, and aggregates it into a dictionary that can be used to enhance
commit messages. It first retrieves the primary issue (the first key in the
list) and then gathers basic details for any related issues. The resulting
context includes information from both the primary and related issues, along
with all issue keys.

Args:
    issue_keys: List of JIRA issue keys to gather information from

Returns:
    Dict containing business and technical context from the issues

#### `public tuple `[`enhance_commit_message`](#classpenify__hook_1_1jira__client_1_1JiraClient_1a70d2c5a6432aa6f238da0ff65d49a760)`(self,str title,str description,List issue_keys)` {#classpenify__hook_1_1jira__client_1_1JiraClient_1a70d2c5a6432aa6f238da0ff65d49a760}

Enhance a commit message with business and technical context from JIRA issues.

This function first checks if the list of issue keys is empty or if there is no
connection. If so, it returns the original title and description without
modification. It then retrieves context information from the specified JIRA
issues. If the primary issue is missing, it formats the commit message with
basic JIRA info.  The function enhances the commit title by prefixing it with
the primary issue key if not already included. It appends a business context
section to the description, including details like issue type, status,
priority, sprint, acceptance criteria, and a condensed issue description. If
comments are available, they are added as technical notes. Finally, related
issues are listed.

Args:
    title (str): Original commit title.
    description (str): Original commit description.
    issue_keys (List[str]): List of JIRA issue keys to include in the enhanced commit message.

Returns:
    tuple: A tuple containing the enhanced commit title and description with added
        context from JIRA issues.

# namespace `penify_hook::llm_client` {#namespacepenify__hook_1_1llm__client}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`penify_hook::llm_client::LLMClient`](#classpenify__hook_1_1llm__client_1_1LLMClient) | Client for interacting with LLM models using LiteLLM.

# class `penify_hook::llm_client::LLMClient` {#classpenify__hook_1_1llm__client_1_1LLMClient}

Client for interacting with LLM models using LiteLLM.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public  `[`model`](#classpenify__hook_1_1llm__client_1_1LLMClient_1abc2cb6b1d6d9b5dc16401ca078ec8c10) | 
`public def `[`__init__`](#classpenify__hook_1_1llm__client_1_1LLMClient_1a76d92354f585ab4bb291169f9f530764)`(self,str model,str api_base,str api_key)` | Initialize the LLM client.
`public def `[`litellm`](#classpenify__hook_1_1llm__client_1_1LLMClient_1ad6f06658ca922793f879474f2234518e)`(self)` | Returns the litellm module, loading it if necessary.
`public Dict `[`generate_commit_summary`](#classpenify__hook_1_1llm__client_1_1LLMClient_1a2ad3014dac466ee1d8e00306d0cf2000)`(self,str diff,str message,bool generate_description,Dict repo_details,Dict jira_context)` | Generate a concise and descriptive commit summary based on Git diff, user

## Members

#### `public  `[`model`](#classpenify__hook_1_1llm__client_1_1LLMClient_1abc2cb6b1d6d9b5dc16401ca078ec8c10) {#classpenify__hook_1_1llm__client_1_1LLMClient_1abc2cb6b1d6d9b5dc16401ca078ec8c10}

#### `public def `[`__init__`](#classpenify__hook_1_1llm__client_1_1LLMClient_1a76d92354f585ab4bb291169f9f530764)`(self,str model,str api_base,str api_key)` {#classpenify__hook_1_1llm__client_1_1LLMClient_1a76d92354f585ab4bb291169f9f530764}

Initialize the LLM client.

Args:
    model: LLM model to use (e.g., "gpt-4", "ollama/llama2", etc.)
    api_base: Base URL for API requests (e.g., "http://localhost:11434" for Ollama)
    api_key: API key for the LLM service

#### `public def `[`litellm`](#classpenify__hook_1_1llm__client_1_1LLMClient_1ad6f06658ca922793f879474f2234518e)`(self)` {#classpenify__hook_1_1llm__client_1_1LLMClient_1ad6f06658ca922793f879474f2234518e}

Returns the litellm module, loading it if necessary.

#### `public Dict `[`generate_commit_summary`](#classpenify__hook_1_1llm__client_1_1LLMClient_1a2ad3014dac466ee1d8e00306d0cf2000)`(self,str diff,str message,bool generate_description,Dict repo_details,Dict jira_context)` {#classpenify__hook_1_1llm__client_1_1LLMClient_1a2ad3014dac466ee1d8e00306d0cf2000}

Generate a concise and descriptive commit summary based on Git diff, user
instructions, repository details, and optional JIRA context.

This function constructs a prompt for an LLM to produce a commit title and, if
requested, a detailed description. The summary adheres to Semantic Commit
Messages guidelines. If JIRA context is provided, it enriches the prompt with
relevant issue information.

Args:
    diff (str): Git diff of changes.
    message (str): User-provided commit message or instructions.
    generate_description (bool): Flag indicating whether to include a detailed description in the summary.
    repo_details (Dict): Details about the repository.
    jira_context (Dict?): Optional JIRA issue context to enhance the summary.

Returns:
    Dict: A dictionary containing the title and description for the commit. If
        `generate_description` is False, the 'description' key may be absent.

Raises:
    ValueError: If the LLM model is not configured.

# namespace `penify_hook::login_command` {#namespacepenify__hook_1_1login__command}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`setup_login_parser`](#namespacepenify__hook_1_1login__command_1aae63db4c484797bead34b7d874020c6a)`(parser)`            | Set up command-line arguments for login.
`public def `[`handle_login`](#namespacepenify__hook_1_1login__command_1ae4bf932fbafeff834b0a0c5a37f74ccd)`(args)`            | Initiates a user login process using predefined constants and the `login`

## Members

#### `public def `[`setup_login_parser`](#namespacepenify__hook_1_1login__command_1aae63db4c484797bead34b7d874020c6a)`(parser)` {#namespacepenify__hook_1_1login__command_1aae63db4c484797bead34b7d874020c6a}

Set up command-line arguments for login.

#### `public def `[`handle_login`](#namespacepenify__hook_1_1login__command_1ae4bf932fbafeff834b0a0c5a37f74ccd)`(args)` {#namespacepenify__hook_1_1login__command_1ae4bf932fbafeff834b0a0c5a37f74ccd}

Initiates a user login process using predefined constants and the `login`
function.

# namespace `penify_hook::main` {#namespacepenify__hook_1_1main}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`main`](#namespacepenify__hook_1_1main_1a16838b20df4bd14ee4b5e1dd2906738f)`()`            | Main function to handle command-line interface (CLI) interactions with Penify

## Members

#### `public def `[`main`](#namespacepenify__hook_1_1main_1a16838b20df4bd14ee4b5e1dd2906738f)`()` {#namespacepenify__hook_1_1main_1a16838b20df4bd14ee4b5e1dd2906738f}

Main function to handle command-line interface (CLI) interactions with Penify
services.

This tool provides a command-line interface for generating smart commit
messages, configuring local-LLM and JIRA, and generating code documentation. It
supports basic commands that do not require login and advanced commands that
require user authentication. The `--version` flag can be used to display the
version information.

# namespace `penify_hook::ui_utils` {#namespacepenify__hook_1_1ui__utils}

UI utilities for Penify CLI.

This module provides utility functions for consistent UI formatting,
colored output, and progress indicators across the Penify CLI application.

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`format_info`](#namespacepenify__hook_1_1ui__utils_1a92c3e466d1912058167be2eacf85b9f6)`(message)`            | Format an informational message with appropriate color.
`public def `[`format_success`](#namespacepenify__hook_1_1ui__utils_1a532cdb4de7c679ce8b29c3e9116c4776)`(message)`            | Formats a success message with green color and reset style.
`public def `[`format_warning`](#namespacepenify__hook_1_1ui__utils_1a0a6fd2613c6fe053b6e4356cd9e5cda2)`(message)`            | Format a warning message with appropriate color.
`public def `[`format_error`](#namespacepenify__hook_1_1ui__utils_1a4dd934568897433fa73f9cc182ac4a3e)`(message)`            | Format an error message with the specified error color.
`public def `[`format_highlight`](#namespacepenify__hook_1_1ui__utils_1adcb97fc26b405d2b9cdf5eb7aecc5452)`(message)`            | Format a highlighted message with appropriate color.
`public def `[`format_file_path`](#namespacepenify__hook_1_1ui__utils_1af3441fb3c2c3850b8b3b6455a9fdaba4)`(file_path)`            | Format a file path with a warning color.
`public def `[`print_info`](#namespacepenify__hook_1_1ui__utils_1a811f0adf6e9bf71510c379b6fa155e44)`(message)`            | Prints an informational message with formatting.
`public def `[`print_success`](#namespacepenify__hook_1_1ui__utils_1a2b16aa6b68a9edea5f29f84f1c4be79a)`(message)`            | Prints a formatted success message.
`public def `[`print_warning`](#namespacepenify__hook_1_1ui__utils_1a1ffbb9671dbe233770268e2dd66a67fa)`(message)`            | Prints a warning message with formatted output.
`public def `[`print_error`](#namespacepenify__hook_1_1ui__utils_1a6f0acd7dd91abfe67d0807803bc3b65f)`(message)`            | Print an error message with appropriate formatting.
`public def `[`print_processing`](#namespacepenify__hook_1_1ui__utils_1adfcbbfe39029ab6d1dd33e7bf75ae115)`(file_path)`            | Print a processing message for a specified file.
`public def `[`print_status`](#namespacepenify__hook_1_1ui__utils_1aa6e684c00e26199440137a87ed9b195c)`(status,message)`            | Print a status message with an appropriate symbol.
`public def `[`create_progress_bar`](#namespacepenify__hook_1_1ui__utils_1a12b92532b1458af94f3649d411b5505c)`(total,desc,unit)`            | Create a tqdm progress bar with consistent styling.
`public def `[`create_stage_progress_bar`](#namespacepenify__hook_1_1ui__utils_1a3da02cd1140179a9ce60f62c85fccfef)`(stages,desc)`            | Create a tqdm progress bar for processing stages with consistent styling.
`public def `[`update_stage`](#namespacepenify__hook_1_1ui__utils_1a5a7340d0fc60fb80f17514d60bf45f1d)`(pbar,stage_name)`            | Update the progress bar with a new stage name.

## Members

#### `public def `[`format_info`](#namespacepenify__hook_1_1ui__utils_1a92c3e466d1912058167be2eacf85b9f6)`(message)` {#namespacepenify__hook_1_1ui__utils_1a92c3e466d1912058167be2eacf85b9f6}

Format an informational message with appropriate color.

#### `public def `[`format_success`](#namespacepenify__hook_1_1ui__utils_1a532cdb4de7c679ce8b29c3e9116c4776)`(message)` {#namespacepenify__hook_1_1ui__utils_1a532cdb4de7c679ce8b29c3e9116c4776}

Formats a success message with green color and reset style.

#### `public def `[`format_warning`](#namespacepenify__hook_1_1ui__utils_1a0a6fd2613c6fe053b6e4356cd9e5cda2)`(message)` {#namespacepenify__hook_1_1ui__utils_1a0a6fd2613c6fe053b6e4356cd9e5cda2}

Format a warning message with appropriate color.

#### `public def `[`format_error`](#namespacepenify__hook_1_1ui__utils_1a4dd934568897433fa73f9cc182ac4a3e)`(message)` {#namespacepenify__hook_1_1ui__utils_1a4dd934568897433fa73f9cc182ac4a3e}

Format an error message with the specified error color.

#### `public def `[`format_highlight`](#namespacepenify__hook_1_1ui__utils_1adcb97fc26b405d2b9cdf5eb7aecc5452)`(message)` {#namespacepenify__hook_1_1ui__utils_1adcb97fc26b405d2b9cdf5eb7aecc5452}

Format a highlighted message with appropriate color.

#### `public def `[`format_file_path`](#namespacepenify__hook_1_1ui__utils_1af3441fb3c2c3850b8b3b6455a9fdaba4)`(file_path)` {#namespacepenify__hook_1_1ui__utils_1af3441fb3c2c3850b8b3b6455a9fdaba4}

Format a file path with a warning color.

#### `public def `[`print_info`](#namespacepenify__hook_1_1ui__utils_1a811f0adf6e9bf71510c379b6fa155e44)`(message)` {#namespacepenify__hook_1_1ui__utils_1a811f0adf6e9bf71510c379b6fa155e44}

Prints an informational message with formatting.

#### `public def `[`print_success`](#namespacepenify__hook_1_1ui__utils_1a2b16aa6b68a9edea5f29f84f1c4be79a)`(message)` {#namespacepenify__hook_1_1ui__utils_1a2b16aa6b68a9edea5f29f84f1c4be79a}

Prints a formatted success message.

#### `public def `[`print_warning`](#namespacepenify__hook_1_1ui__utils_1a1ffbb9671dbe233770268e2dd66a67fa)`(message)` {#namespacepenify__hook_1_1ui__utils_1a1ffbb9671dbe233770268e2dd66a67fa}

Prints a warning message with formatted output.

#### `public def `[`print_error`](#namespacepenify__hook_1_1ui__utils_1a6f0acd7dd91abfe67d0807803bc3b65f)`(message)` {#namespacepenify__hook_1_1ui__utils_1a6f0acd7dd91abfe67d0807803bc3b65f}

Print an error message with appropriate formatting.

#### `public def `[`print_processing`](#namespacepenify__hook_1_1ui__utils_1adfcbbfe39029ab6d1dd33e7bf75ae115)`(file_path)` {#namespacepenify__hook_1_1ui__utils_1adfcbbfe39029ab6d1dd33e7bf75ae115}

Print a processing message for a specified file.

#### `public def `[`print_status`](#namespacepenify__hook_1_1ui__utils_1aa6e684c00e26199440137a87ed9b195c)`(status,message)` {#namespacepenify__hook_1_1ui__utils_1aa6e684c00e26199440137a87ed9b195c}

Print a status message with an appropriate symbol.

#### `public def `[`create_progress_bar`](#namespacepenify__hook_1_1ui__utils_1a12b92532b1458af94f3649d411b5505c)`(total,desc,unit)` {#namespacepenify__hook_1_1ui__utils_1a12b92532b1458af94f3649d411b5505c}

Create a tqdm progress bar with consistent styling.

#### `public def `[`create_stage_progress_bar`](#namespacepenify__hook_1_1ui__utils_1a3da02cd1140179a9ce60f62c85fccfef)`(stages,desc)` {#namespacepenify__hook_1_1ui__utils_1a3da02cd1140179a9ce60f62c85fccfef}

Create a tqdm progress bar for processing stages with consistent styling.

#### `public def `[`update_stage`](#namespacepenify__hook_1_1ui__utils_1a5a7340d0fc60fb80f17514d60bf45f1d)`(pbar,stage_name)` {#namespacepenify__hook_1_1ui__utils_1a5a7340d0fc60fb80f17514d60bf45f1d}

Update the progress bar with a new stage name.

# namespace `penify_hook::utils` {#namespacepenify__hook_1_1utils}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`get_repo_details`](#namespacepenify__hook_1_1utils_1ae236f3c4c8bf5dcddbb92b4c2065eea3)`(Repo repo)`            | Determine the details of a repository including its remote URL, hosting
`public def `[`recursive_search_git_folder`](#namespacepenify__hook_1_1utils_1a95c3f9c80860d6a2e2d061d2fb660a3f)`(folder_path)`            | Recursively searches for a .git folder starting from the given directory.
`public def `[`find_git_parent`](#namespacepenify__hook_1_1utils_1a4ec5335a4026c22a34a3a8ccf665a5f2)`(path)`            | Traverse up from the given path to find the nearest directory containing a .git
`class `[`penify_hook::utils::GitRepoNotFoundError`](#classpenify__hook_1_1utils_1_1GitRepoNotFoundError) | 

## Members

#### `public def `[`get_repo_details`](#namespacepenify__hook_1_1utils_1ae236f3c4c8bf5dcddbb92b4c2065eea3)`(Repo repo)` {#namespacepenify__hook_1_1utils_1ae236f3c4c8bf5dcddbb92b4c2065eea3}

Determine the details of a repository including its remote URL, hosting
service, organization name, and repository name.

This function extracts the remote URL from the given Git repository object and
determines the hosting service (e.g., GitHub, Azure DevOps, Bitbucket, GitLab).
It then parses the URL to extract the organization name and repository name. If
the URL does not match any known hosting service pattern, it sets the hosting
service as "Unknown". The function handles exceptions that may occur during
this process and logs an error message if needed.

Args:
    repo (Repo): A GitPython Repo object representing the local git repository.

Returns:
    dict: A dictionary containing the organization name, repository name, and hosting
        service.

#### `public def `[`recursive_search_git_folder`](#namespacepenify__hook_1_1utils_1a95c3f9c80860d6a2e2d061d2fb660a3f)`(folder_path)` {#namespacepenify__hook_1_1utils_1a95c3f9c80860d6a2e2d061d2fb660a3f}

Recursively searches for a .git folder starting from the given directory.

#### `public def `[`find_git_parent`](#namespacepenify__hook_1_1utils_1a4ec5335a4026c22a34a3a8ccf665a5f2)`(path)` {#namespacepenify__hook_1_1utils_1a4ec5335a4026c22a34a3a8ccf665a5f2}

Traverse up from the given path to find the nearest directory containing a .git
subdirectory.

# class `penify_hook::utils::GitRepoNotFoundError` {#classpenify__hook_1_1utils_1_1GitRepoNotFoundError}

```
class penify_hook::utils::GitRepoNotFoundError
  : public Exception
```  

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------

## Members

# namespace `tests::test_commit_commands` {#namespacetests_1_1test__commit__commands}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`tests::test_commit_commands::TestCommitCommands`](#classtests_1_1test__commit__commands_1_1TestCommitCommands) | 

# class `tests::test_commit_commands::TestCommitCommands` {#classtests_1_1test__commit__commands_1_1TestCommitCommands}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`mock_api_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1abcd2354a2af4afe19e57877628d3acc2)`(self)` | Mocks an instance of APIClient using unittest.mock.
`public def `[`mock_llm_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a20e78370ff5bd6223cc1dd4323a86ea4)`(self)` | Mock an instance of LLMClient for testing purposes.
`public def `[`mock_jira_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a05adaa9a713ff1be657455d0667bc6be)`(self)` | Create a mock JIRA client for testing purposes.
`public def `[`mock_commit_doc_gen`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1aa9b25a4bf692b8736164695072a398f6)`(self)` | Mocks the CommitDocGenHook class and returns a MagicMock instance.
`public def `[`mock_git_folder_search`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a2842f456a8c0f1bf0f4def17c183c04e)`(self)` | Mock the `recursive_search_git_folder` function to return a predefined
`public def `[`mock_print_functions`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1afafbae3c9aeb0e50a75996256c02c8be)`(self)` | Mocks the print functions from `penify_hook.ui_utils` for testing
`public def `[`test_commit_code_with_llm_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1acc4b1e4189792a3f7c11d2a745f479c0)`(self,mock_error,mock_warning,mock_info,`[`mock_git_folder_search`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a2842f456a8c0f1bf0f4def17c183c04e)`,mock_doc_gen,`[`mock_llm_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a20e78370ff5bd6223cc1dd4323a86ea4)`,`[`mock_api_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1abcd2354a2af4afe19e57877628d3acc2)`)` | Test committing code using an LLM client.
`public def `[`test_commit_code_with_jira_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1af9c09013055ec39ddde86b487aefcf8b)`(self,mock_error,mock_warning,mock_info,`[`mock_git_folder_search`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a2842f456a8c0f1bf0f4def17c183c04e)`,mock_doc_gen,`[`mock_jira_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a05adaa9a713ff1be657455d0667bc6be)`,`[`mock_llm_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a20e78370ff5bd6223cc1dd4323a86ea4)`,`[`mock_api_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1abcd2354a2af4afe19e57877628d3acc2)`)` | Test committing code using a JIRA client.
`public def `[`test_commit_code_with_jira_connection_failure`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1acea0d934ee0f2b914b0b893736e8fe4e)`(self,mock_error,mock_warning,mock_info,`[`mock_git_folder_search`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a2842f456a8c0f1bf0f4def17c183c04e)`,mock_doc_gen,`[`mock_jira_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a05adaa9a713ff1be657455d0667bc6be)`,`[`mock_api_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1abcd2354a2af4afe19e57877628d3acc2)`)` | Test the commit_code function when JIRA connection fails.
`public def `[`test_commit_code_error_handling`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a43c2ff3707124aa48e8eb581106b8691)`(self,mock_print,mock_exit,`[`mock_git_folder_search`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a2842f456a8c0f1bf0f4def17c183c04e)`,mock_doc_gen,`[`mock_api_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1abcd2354a2af4afe19e57877628d3acc2)`)` | Test the error handling in the test_commit_code function.
`public def `[`test_setup_commit_parser`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a4d04b125e102190a768f65f1948f15bc)`(self)` | Set up the argument parser for the commit command.
`public def `[`test_handle_commit`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1ac13e368262340af98b30fd8ebdac6597)`(self,mock_print_info,mock_commit_code,mock_get_token,mock_get_llm_config,mock_get_jira_config)` | Test the handle_commit function with various mock objects.

## Members

#### `public def `[`mock_api_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1abcd2354a2af4afe19e57877628d3acc2)`(self)` {#classtests_1_1test__commit__commands_1_1TestCommitCommands_1abcd2354a2af4afe19e57877628d3acc2}

Mocks an instance of APIClient using unittest.mock.

This function creates a mock object for APIClient and yields it along
with the mocked instance. It is useful for testing purposes where real
API calls should be avoided.

Yields:
    tuple: A tuple containing the mock of APIClient and the mocked instance of
        APIClient.

#### `public def `[`mock_llm_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a20e78370ff5bd6223cc1dd4323a86ea4)`(self)` {#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a20e78370ff5bd6223cc1dd4323a86ea4}

Mock an instance of LLMClient for testing purposes.

This function yields a mock object representing an instance of
LLMClient, which can be used to simulate interactions with a language
model during testing. The mock is patched to replace the actual
LLMClient class from the penify_hook module.

Yields:
    tuple: A tuple containing two elements:
        - mock (MagicMock): The mock object for LLMClient.
        - llm_client_instance (MagicMock): An instance of the mocked LLMClient.

#### `public def `[`mock_jira_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a05adaa9a713ff1be657455d0667bc6be)`(self)` {#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a05adaa9a713ff1be657455d0667bc6be}

Create a mock JIRA client for testing purposes.

This function yields a tuple containing a mock JIRA client instance and
its `is_connected` method. The mock client is configured to simulate an
active connection. This is useful for unit tests that require
interaction with a JIRA client without making actual network calls.

Yields:
    tuple: A tuple containing the mocked JIRA client instance and its
        `is_connected` method.

#### `public def `[`mock_commit_doc_gen`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1aa9b25a4bf692b8736164695072a398f6)`(self)` {#classtests_1_1test__commit__commands_1_1TestCommitCommands_1aa9b25a4bf692b8736164695072a398f6}

Mocks the CommitDocGenHook class and returns a MagicMock instance.

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

#### `public def `[`mock_git_folder_search`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a2842f456a8c0f1bf0f4def17c183c04e)`(self)` {#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a2842f456a8c0f1bf0f4def17c183c04e}

Mock the `recursive_search_git_folder` function to return a predefined
git folder path.

This function uses the `patch` decorator from the `unittest.mock` module
to intercept calls to `penify_hook.utils.recursive_search_git_folder`.
When called, it will return '/mock/git/folder' instead of performing an
actual search. This is useful for testing purposes where you need a
consistent response without interacting with the file system.

Yields:
    MagicMock: A mock object that simulates the `recursive_search_git_folder` function.

#### `public def `[`mock_print_functions`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1afafbae3c9aeb0e50a75996256c02c8be)`(self)` {#classtests_1_1test__commit__commands_1_1TestCommitCommands_1afafbae3c9aeb0e50a75996256c02c8be}

Mocks the print functions from `penify_hook.ui_utils` for testing
purposes.

This function uses Python's `unittest.mock.patch` to replace the actual
print functions (`print`, `print_warning`, and `print_error`) with mock
objects. These mock objects can be used in tests to capture calls made
to these print functions without actually printing anything.

Yields:
    tuple: A tuple containing three mock objects corresponding to `print_info`,
        `print_warning`,
        and `print_error`.

#### `public def `[`test_commit_code_with_llm_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1acc4b1e4189792a3f7c11d2a745f479c0)`(self,mock_error,mock_warning,mock_info,`[`mock_git_folder_search`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a2842f456a8c0f1bf0f4def17c183c04e)`,mock_doc_gen,`[`mock_llm_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a20e78370ff5bd6223cc1dd4323a86ea4)`,`[`mock_api_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1abcd2354a2af4afe19e57877628d3acc2)`)` {#classtests_1_1test__commit__commands_1_1TestCommitCommands_1acc4b1e4189792a3f7c11d2a745f479c0}

Test committing code using an LLM client.

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

#### `public def `[`test_commit_code_with_jira_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1af9c09013055ec39ddde86b487aefcf8b)`(self,mock_error,mock_warning,mock_info,`[`mock_git_folder_search`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a2842f456a8c0f1bf0f4def17c183c04e)`,mock_doc_gen,`[`mock_jira_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a05adaa9a713ff1be657455d0667bc6be)`,`[`mock_llm_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a20e78370ff5bd6223cc1dd4323a86ea4)`,`[`mock_api_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1abcd2354a2af4afe19e57877628d3acc2)`)` {#classtests_1_1test__commit__commands_1_1TestCommitCommands_1af9c09013055ec39ddde86b487aefcf8b}

Test committing code using a JIRA client.

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

#### `public def `[`test_commit_code_with_jira_connection_failure`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1acea0d934ee0f2b914b0b893736e8fe4e)`(self,mock_error,mock_warning,mock_info,`[`mock_git_folder_search`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a2842f456a8c0f1bf0f4def17c183c04e)`,mock_doc_gen,`[`mock_jira_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a05adaa9a713ff1be657455d0667bc6be)`,`[`mock_api_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1abcd2354a2af4afe19e57877628d3acc2)`)` {#classtests_1_1test__commit__commands_1_1TestCommitCommands_1acea0d934ee0f2b914b0b893736e8fe4e}

Test the commit_code function when JIRA connection fails.

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

#### `public def `[`test_commit_code_error_handling`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a43c2ff3707124aa48e8eb581106b8691)`(self,mock_print,mock_exit,`[`mock_git_folder_search`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a2842f456a8c0f1bf0f4def17c183c04e)`,mock_doc_gen,`[`mock_api_client`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1abcd2354a2af4afe19e57877628d3acc2)`)` {#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a43c2ff3707124aa48e8eb581106b8691}

Test the error handling in the test_commit_code function.

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

#### `public def `[`test_setup_commit_parser`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a4d04b125e102190a768f65f1948f15bc)`(self)` {#classtests_1_1test__commit__commands_1_1TestCommitCommands_1a4d04b125e102190a768f65f1948f15bc}

Set up the argument parser for the commit command.

This function configures an argument parser to handle various options
for committing changes. It adds three arguments: - '-m' or '--message':
An optional argument to specify a contextual commit message with a
default value of "N/A". - '-e' or '--terminal': A boolean flag to open
an edit terminal before committing. - '-d' or '--description': A boolean
flag that, when set to False, indicates the generation of a commit
message with title and description.

Args:
    parser (MagicMock): The argument parser to be configured.

#### `public def `[`test_handle_commit`](#classtests_1_1test__commit__commands_1_1TestCommitCommands_1ac13e368262340af98b30fd8ebdac6597)`(self,mock_print_info,mock_commit_code,mock_get_token,mock_get_llm_config,mock_get_jira_config)` {#classtests_1_1test__commit__commands_1_1TestCommitCommands_1ac13e368262340af98b30fd8ebdac6597}

Test the handle_commit function with various mock objects.

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

# namespace `tests::test_config_commands` {#namespacetests_1_1test__config__commands}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`tests::test_config_commands::TestConfigCommands`](#classtests_1_1test__config__commands_1_1TestConfigCommands) | 

# class `tests::test_config_commands::TestConfigCommands` {#classtests_1_1test__config__commands_1_1TestConfigCommands}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`test_get_penify_config_existing_dir`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a2e8162082bcdd5652bb37bdb14cf453a)`(self,mock_file_open,mock_makedirs,mock_path,mock_git_folder)` | Test the get_penify_config function when the .penify config directory
`public def `[`test_get_penify_config_new_dir`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a33d4760eee3b67e1cde3aed755ebb948)`(self,mock_file_open,mock_makedirs,mock_path,mock_git_folder)` | Test the behavior of get_penify_config when the .penify directory does
`public def `[`test_get_llm_config_exists`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1adf9f2233a3f4cc5725b9d4f05758b167)`(self,mock_file_open,mock_get_config)` | Test the get_llm_config function when the configuration file exists.
`public def `[`test_get_llm_config_empty`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1abd12f028b89aa9cd1152c0b9ece5d3cd)`(self,mock_file_open,mock_get_config)` | Test the behavior of get_llm_config when called with an empty
`public def `[`test_get_llm_config_invalid_json`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a473984d31452b56acd6ce4011a1248bd)`(self,mock_print,mock_file_open,mock_get_config)` | Test function to verify the behavior of get_llm_config when reading an
`public def `[`test_get_jira_config_exists`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1aee37b97432821d19758c6325d4c74bcf)`(self,mock_file_open,mock_get_config)` | Test that get_jira_config returns the correct JIRA configuration when
`public def `[`test_save_llm_config_success`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1acd8df8219441b9e9871b903a681400d9)`(self,mock_print,mock_json_dump,mock_file_open,mock_get_config)` | Test the save_llm_config function successfully.
`public def `[`test_save_llm_config_failure`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a73a264dfb21e16003e095b79f6eab2ac)`(self,mock_print,mock_file_open,mock_get_config)` | Test function to verify that the save_llm_config function returns False
`public def `[`test_save_jira_config_success`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1af8d62310da2d768e21770f8f01ff5375)`(self,mock_print,mock_json_dump,mock_file_open,mock_path)` | Test the save_jira_config function to ensure it saves JIRA configuration
`public def `[`test_get_token_from_env`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a3355f7d313bebaa71694387cf2bc5232)`(self,mock_file_open,mock_path,mock_getenv)` | Test retrieving a token from the environment variable.
`public def `[`test_get_token_from_config`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a6c0207be563c3de59a6d16277805114c)`(self,mock_file_open,mock_path,mock_getenv)` | Test retrieving a token from the configuration.
`public def `[`test_get_token_not_found`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a400ca5d9fcdc159714e8df54920f9436)`(self,mock_file_open,mock_path,mock_getenv)` | Test the get_token function when the API token environment variable is

## Members

#### `public def `[`test_get_penify_config_existing_dir`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a2e8162082bcdd5652bb37bdb14cf453a)`(self,mock_file_open,mock_makedirs,mock_path,mock_git_folder)` {#classtests_1_1test__config__commands_1_1TestConfigCommands_1a2e8162082bcdd5652bb37bdb14cf453a}

Test the get_penify_config function when the .penify config directory
exists.

It should not create a new directory and assert that all mocked
functions were called correctly.

Args:
    mock_file_open (MagicMock): A MagicMock object simulating the open() function.
    mock_makedirs (MagicMock): A MagicMock object simulating the os.makedirs() function.
    mock_path (MagicMock): A MagicMock object simulating the Path class from pathlib module.
    mock_git_folder (MagicMock): A MagicMock object simulating the git_folder_search() function.

#### `public def `[`test_get_penify_config_new_dir`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a33d4760eee3b67e1cde3aed755ebb948)`(self,mock_file_open,mock_makedirs,mock_path,mock_git_folder)` {#classtests_1_1test__config__commands_1_1TestConfigCommands_1a33d4760eee3b67e1cde3aed755ebb948}

Test the behavior of get_penify_config when the .penify directory does
not exist.

This function mocks various system calls to simulate a scenario where
the .penify directory is not present. It then asserts that the
appropriate actions are taken to create the directory and write an empty
JSON file.

Args:
    mock_file_open (MagicMock): A MagicMock object simulating the `open` function.
    mock_makedirs (MagicMock): A MagicMock object simulating the `os.makedirs` function.
    mock_path (MagicMock): A MagicMock object simulating the `Path` class from `pathlib`.
    mock_git_folder (MagicMock): A MagicMock object simulating a git folder search function.

#### `public def `[`test_get_llm_config_exists`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1adf9f2233a3f4cc5725b9d4f05758b167)`(self,mock_file_open,mock_get_config)` {#classtests_1_1test__config__commands_1_1TestConfigCommands_1adf9f2233a3f4cc5725b9d4f05758b167}

Test the get_llm_config function when the configuration file exists.

This function sets up a mock configuration file that exists and returns
it when called. It then calls the get_llm_config function and asserts
that it returns the correct configuration dictionary. Additionally, it
checks that the mock_file_open function was called with the correct
arguments.

Args:
    mock_file_open (MagicMock): A mock for the open() function.
    mock_get_config (MagicMock): A mock for the get_config() function.

#### `public def `[`test_get_llm_config_empty`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1abd12f028b89aa9cd1152c0b9ece5d3cd)`(self,mock_file_open,mock_get_config)` {#classtests_1_1test__config__commands_1_1TestConfigCommands_1abd12f028b89aa9cd1152c0b9ece5d3cd}

Test the behavior of get_llm_config when called with an empty
configuration file.

This function sets up a mock configuration file that exists but returns
no content. It then calls the `get_llm_config` function and asserts that
it returns an empty dictionary and that the file open method was called
exactly once with the correct arguments.

Args:
    mock_file_open (MagicMock): A MagicMock object simulating the built-in open function.
    mock_get_config (MagicMock): A MagicMock object simulating the get_config function.

#### `public def `[`test_get_llm_config_invalid_json`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a473984d31452b56acd6ce4011a1248bd)`(self,mock_print,mock_file_open,mock_get_config)` {#classtests_1_1test__config__commands_1_1TestConfigCommands_1a473984d31452b56acd6ce4011a1248bd}

Test function to verify the behavior of get_llm_config when reading an
invalid JSON file.

It sets up a mock configuration file that exists but contains invalid
JSON. The function is expected to handle this gracefully by printing an
error message and returning an empty dictionary.

Args:
    mock_print (MagicMock): Mock for the print function.
    mock_file_open (MagicMock): Mock for the open function.
    mock_get_config (MagicMock): Mock for the get_config function, which returns the mock configuration
        file.

#### `public def `[`test_get_jira_config_exists`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1aee37b97432821d19758c6325d4c74bcf)`(self,mock_file_open,mock_get_config)` {#classtests_1_1test__config__commands_1_1TestConfigCommands_1aee37b97432821d19758c6325d4c74bcf}

Test that get_jira_config returns the correct JIRA configuration when
the configuration file exists.

It sets up a mock for the configuration file to simulate its existence
and verifies that the function reads from the correct file and returns
the expected JIRA configuration dictionary. Additionally, it checks that
the mock file open is called with the appropriate arguments.

Args:
    mock_file_open (MagicMock): A mock for the `open` function.
    mock_get_config (MagicMock): A mock for the `get_config` function, which is expected to return a mock
        configuration file object.

Returns:
    None: This test function does not explicitly return anything. Its assertions
        serve as the verification of its correctness.

#### `public def `[`test_save_llm_config_success`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1acd8df8219441b9e9871b903a681400d9)`(self,mock_print,mock_json_dump,mock_file_open,mock_get_config)` {#classtests_1_1test__config__commands_1_1TestConfigCommands_1acd8df8219441b9e9871b903a681400d9}

Test the save_llm_config function successfully.

This function tests that the save_llm_config function correctly saves an
LLM configuration and handles various mock objects and side effects. It
ensures that the function returns True upon successful execution, writes
the expected configuration to a file, and prints a confirmation message.

Args:
    mock_print (MagicMock): A mock object for the print function.
    mock_json_dump (MagicMock): A mock object for json.dump.
    mock_file_open (MagicMock): A mock object for file opening.
    mock_get_config (MagicMock): A mock object to return a configuration file mock.

#### `public def `[`test_save_llm_config_failure`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a73a264dfb21e16003e095b79f6eab2ac)`(self,mock_print,mock_file_open,mock_get_config)` {#classtests_1_1test__config__commands_1_1TestConfigCommands_1a73a264dfb21e16003e095b79f6eab2ac}

Test function to verify that the save_llm_config function returns False
and prints an error message when it fails to save the LLM configuration
due to a permission error.

It sets up a mock configuration file that exists and calls the
save_llm_config function with valid parameters. The function is expected
to return False and print "Error saving LLM configuration: Permission
denied" in case of a failure.

Args:
    self (TestLLMConfig): An instance of the test class.
    mock_print (MagicMock): A MagicMock object representing the print function, which will be used
        to assert that it was called with the expected error message.
    mock_file_open (MagicMock): A MagicMock object representing the open function, which is not used in
        this test but is included as a parameter for completeness.
    mock_get_config (MagicMock): A MagicMock object representing the get_config function, which will be
        used to return the mock configuration file.

#### `public def `[`test_save_jira_config_success`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1af8d62310da2d768e21770f8f01ff5375)`(self,mock_print,mock_json_dump,mock_file_open,mock_path)` {#classtests_1_1test__config__commands_1_1TestConfigCommands_1af8d62310da2d768e21770f8f01ff5375}

Test the save_jira_config function to ensure it saves JIRA configuration
successfully.

This function sets up mocks for various dependencies and tests the
functionality of saving a JIRA configuration. It asserts that the
function returns `True`, the JSON dump is called with the correct
configuration, and the print statement contains the expected message.

Args:
    mock_print (MagicMock): Mock for the print function.
    mock_json_dump (MagicMock): Mock for the json.dump function.
    mock_file_open (MagicMock): Mock for the open function.
    mock_path (MagicMock): Mock for the path module.

#### `public def `[`test_get_token_from_env`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a3355f7d313bebaa71694387cf2bc5232)`(self,mock_file_open,mock_path,mock_getenv)` {#classtests_1_1test__config__commands_1_1TestConfigCommands_1a3355f7d313bebaa71694387cf2bc5232}

Test retrieving a token from the environment variable.

This function tests the behavior of `get_token` when an environment
variable is set. It verifies that if the 'PENIFY_API_TOKEN' environment
variable exists, the function returns its value without attempting to
read a file.

Args:
    mock_file_open (MagicMock): A MagicMock object for simulating file operations.
    mock_path (MagicMock): A MagicMock object for simulating path operations.
    mock_getenv (MagicMock): A MagicMock object for simulating environment variable retrieval.

#### `public def `[`test_get_token_from_config`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a6c0207be563c3de59a6d16277805114c)`(self,mock_file_open,mock_path,mock_getenv)` {#classtests_1_1test__config__commands_1_1TestConfigCommands_1a6c0207be563c3de59a6d16277805114c}

Test retrieving a token from the configuration.

This function sets up mocks for environment variables and configuration
files, calls the `get_token` function, and asserts its behavior. It
verifies that when the environment variable is not found, the function
reads a token from a configuration file located in the user's home
directory.

Args:
    mock_file_open (MagicMock): A mock for the `open` function.
    mock_path (MagicMock): A mock for the `pathlib.Path` class.
    mock_getenv (MagicMock): A mock for the `os.getenv` function.

#### `public def `[`test_get_token_not_found`](#classtests_1_1test__config__commands_1_1TestConfigCommands_1a400ca5d9fcdc159714e8df54920f9436)`(self,mock_file_open,mock_path,mock_getenv)` {#classtests_1_1test__config__commands_1_1TestConfigCommands_1a400ca5d9fcdc159714e8df54920f9436}

Test the get_token function when the API token environment variable is
not found.

This function tests the scenario where the `PENIFY_API_TOKEN`
environment variable is not set. It mocks the environment variable to
return `None`, and verifies that the function returns `None`. The test
also checks that the environment variable is accessed once and that a
file open operation is attempted on a configuration file located in the
user's home directory.

Args:
    mock_file_open (MagicMock): Mock for the built-in `open` function.
    mock_path (MagicMock): Mock for the `pathlib.Path` module.
    mock_getenv (MagicMock): Mock for the `os.getenv` function.

Returns:
    None: The function does not return anything; it asserts conditions to verify
        correctness.

# namespace `tests::test_doc_commands` {#namespacetests_1_1test__doc__commands}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`test_generate_doc_no_location`](#namespacetests_1_1test__doc__commands_1a806110833eb0aad547156faf014b31d8)`(mock_getcwd,mock_api_client,mock_folder_analyzer,mock_file_analyzer,mock_git_analyzer)`            | Test function to generate documentation without location information.
`public def `[`test_generate_doc_file_location`](#namespacetests_1_1test__doc__commands_1a0e74c920f258f442914771164fe26b45)`(mock_api_client,mock_folder_analyzer,mock_file_analyzer,mock_git_analyzer)`            | Test generating a documentation file location.
`public def `[`test_generate_doc_folder_location`](#namespacetests_1_1test__doc__commands_1a4bb75610e40d94d42bc169b25403c186)`(mock_api_client,mock_folder_analyzer,mock_file_analyzer,mock_git_analyzer)`            | Test the function to generate documentation for a folder location.
`public def `[`test_generate_doc_error_handling`](#namespacetests_1_1test__doc__commands_1aec76cc25c23476794234cdadbcaef0c0)`(mock_api_client,mock_git_analyzer,mock_exit)`            | Generate a documentation string for the provided code snippet using
`public def `[`test_setup_docgen_parser`](#namespacetests_1_1test__doc__commands_1a0f27751d0ba2acfe40ef7e85bccf47d7)`()`            | Test the setup_docgen_parser function to ensure it properly configures
`public def `[`test_handle_docgen_install_hook`](#namespacetests_1_1test__doc__commands_1ab74688baa8c9b5ba302c2877a9789d05)`(mock_exit,mock_get_token,mock_generate_doc,mock_uninstall_hook,mock_install_hook)`            | Test the handling of the 'install-hook' subcommand.
`public def `[`test_handle_docgen_uninstall_hook`](#namespacetests_1_1test__doc__commands_1a1458af9ad0128c3ca1263b552fd5e482)`(mock_exit,mock_get_token,mock_generate_doc,mock_uninstall_hook,mock_install_hook)`            | Test the uninstall-hook subcommand of the handle_docgen function.
`public def `[`test_handle_docgen_generate`](#namespacetests_1_1test__doc__commands_1ab158ffa48469b6c097a7a55fcb20c21a)`(mock_get_token,mock_generate_doc,mock_uninstall_hook,mock_install_hook)`            | Test the direct documentation generation functionality.
`public def `[`test_handle_docgen_no_token`](#namespacetests_1_1test__doc__commands_1af9b01e5fc89255cac96747fa081c442c)`(mock_exit,mock_get_token)`            | Test the behavior of the `handle_docgen` function when no token is
`public def `[`test_generate_doc_with_file_exception`](#namespacetests_1_1test__doc__commands_1a335e7fd4912192c7276cf31bbebc6eb0)`(mock_api_client,mock_getcwd)`            | Generate documentation from a Python source file.
`public def `[`test_generate_doc_with_folder_exception`](#namespacetests_1_1test__doc__commands_1a64165ddfdb3071a88422f080f0e529a3)`(mock_api_client,mock_getcwd)`            | Generate documentation from a given API endpoint and save it to a

## Members

#### `public def `[`test_generate_doc_no_location`](#namespacetests_1_1test__doc__commands_1a806110833eb0aad547156faf014b31d8)`(mock_getcwd,mock_api_client,mock_folder_analyzer,mock_file_analyzer,mock_git_analyzer)` {#namespacetests_1_1test__doc__commands_1a806110833eb0aad547156faf014b31d8}

Test function to generate documentation without location information.

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

#### `public def `[`test_generate_doc_file_location`](#namespacetests_1_1test__doc__commands_1a0e74c920f258f442914771164fe26b45)`(mock_api_client,mock_folder_analyzer,mock_file_analyzer,mock_git_analyzer)` {#namespacetests_1_1test__doc__commands_1a0e74c920f258f442914771164fe26b45}

Test generating a documentation file location.

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

#### `public def `[`test_generate_doc_folder_location`](#namespacetests_1_1test__doc__commands_1a4bb75610e40d94d42bc169b25403c186)`(mock_api_client,mock_folder_analyzer,mock_file_analyzer,mock_git_analyzer)` {#namespacetests_1_1test__doc__commands_1a4bb75610e40d94d42bc169b25403c186}

Test the function to generate documentation for a folder location.

It sets up mock objects for API client, folder analyzer, file analyzer,
and Git analyzer, then calls the `generate_doc` function with specified
parameters. Finally, it asserts that the correct methods on the mock
objects were called as expected.

Args:
    mock_api_client (MagicMock): Mock object for the API client.
    mock_folder_analyzer (MagicMock): Mock object for the folder analyzer.
    mock_file_analyzer (MagicMock): Mock object for the file analyzer.
    mock_git_analyzer (MagicMock): Mock object for the Git analyzer.

#### `public def `[`test_generate_doc_error_handling`](#namespacetests_1_1test__doc__commands_1aec76cc25c23476794234cdadbcaef0c0)`(mock_api_client,mock_git_analyzer,mock_exit)` {#namespacetests_1_1test__doc__commands_1aec76cc25c23476794234cdadbcaef0c0}

Generate a documentation string for the provided code snippet using
Google Docstring style.

Short one line description: Test function to ensure proper error
handling during API calls with GitAnalyzer.  Multiline long description:
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

#### `public def `[`test_setup_docgen_parser`](#namespacetests_1_1test__doc__commands_1a0f27751d0ba2acfe40ef7e85bccf47d7)`()` {#namespacetests_1_1test__doc__commands_1a0f27751d0ba2acfe40ef7e85bccf47d7}

Test the setup_docgen_parser function to ensure it properly configures
the ArgumentParser for docgen options.

It verifies that the parser correctly sets up docgen options and handles
different subcommands like 'install-hook' and 'uninstall-hook'.

#### `public def `[`test_handle_docgen_install_hook`](#namespacetests_1_1test__doc__commands_1ab74688baa8c9b5ba302c2877a9789d05)`(mock_exit,mock_get_token,mock_generate_doc,mock_uninstall_hook,mock_install_hook)` {#namespacetests_1_1test__doc__commands_1ab74688baa8c9b5ba302c2877a9789d05}

Test the handling of the 'install-hook' subcommand.

This function sets up a mock environment where it simulates the
execution of the 'install-hook' subcommand. It verifies that the
`mock_install_hook` is called with the correct arguments, while
`mock_generate_doc` and `mock_uninstall_hook` are not called.

Args:
    mock_exit (MagicMock): Mock object for sys.exit.
    mock_get_token (MagicMock): Mock object to simulate fetching a token.
    mock_generate_doc (MagicMock): Mock object to simulate generating documentation.
    mock_uninstall_hook (MagicMock): Mock object to simulate uninstalling a hook.
    mock_install_hook (MagicMock): Mock object to simulate installing a hook.

#### `public def `[`test_handle_docgen_uninstall_hook`](#namespacetests_1_1test__doc__commands_1a1458af9ad0128c3ca1263b552fd5e482)`(mock_exit,mock_get_token,mock_generate_doc,mock_uninstall_hook,mock_install_hook)` {#namespacetests_1_1test__doc__commands_1a1458af9ad0128c3ca1263b552fd5e482}

Test the uninstall-hook subcommand of the handle_docgen function.
This test case sets up a mock environment and verifies that the
uninstall-hook is called with the correct location, while generate_doc
and install_hook are not called.

Args:
    mock_exit (MagicMock): A mock for the exit function.
    mock_get_token (MagicMock): A mock for the get_token function.
    mock_generate_doc (MagicMock): A mock for the generate_doc function.
    mock_uninstall_hook (MagicMock): A mock for the uninstall_hook function.
    mock_install_hook (MagicMock): A mock for the install_hook function.

#### `public def `[`test_handle_docgen_generate`](#namespacetests_1_1test__doc__commands_1ab158ffa48469b6c097a7a55fcb20c21a)`(mock_get_token,mock_generate_doc,mock_uninstall_hook,mock_install_hook)` {#namespacetests_1_1test__doc__commands_1ab158ffa48469b6c097a7a55fcb20c21a}

Test the direct documentation generation functionality.

This function tests the `handle_docgen` function when no subcommand is
provided. It verifies that the document generation hook is called and
the uninstall and install hooks are not called.

Args:
    mock_get_token (MagicMock): Mocked function to get authentication token.
    mock_generate_doc (MagicMock): Mocked function for generating documentation.
    mock_uninstall_hook (MagicMock): Mocked function for uninstalling the document generation hook.
    mock_install_hook (MagicMock): Mocked function for installing the document generation hook.

#### `public def `[`test_handle_docgen_no_token`](#namespacetests_1_1test__doc__commands_1af9b01e5fc89255cac96747fa081c442c)`(mock_exit,mock_get_token)` {#namespacetests_1_1test__doc__commands_1af9b01e5fc89255cac96747fa081c442c}

Test the behavior of the `handle_docgen` function when no token is
provided.

This function asserts that if no token is returned by `mock_get_token`,
the `handle_docgen` function will call `mock_exit` with a status code of
1.

Args:
    mock_exit (MagicMock): A MagicMock object simulating the `exit` function.
    mock_get_token (MagicMock): A MagicMock object simulating the `get_token` function.

#### `public def `[`test_generate_doc_with_file_exception`](#namespacetests_1_1test__doc__commands_1a335e7fd4912192c7276cf31bbebc6eb0)`(mock_api_client,mock_getcwd)` {#namespacetests_1_1test__doc__commands_1a335e7fd4912192c7276cf31bbebc6eb0}

Generate documentation from a Python source file.

This function reads a Python file and generates a docstring based on its
content. It uses mock objects to simulate API calls and directory
operations during testing.

Args:
    mock_api_client (unittest.mock.MagicMock): A mock object for simulating API client behavior.
    mock_getcwd (unittest.mock.MagicMock): A mock object for simulating the current working directory function.

#### `public def `[`test_generate_doc_with_folder_exception`](#namespacetests_1_1test__doc__commands_1a64165ddfdb3071a88422f080f0e529a3)`(mock_api_client,mock_getcwd)` {#namespacetests_1_1test__doc__commands_1a64165ddfdb3071a88422f080f0e529a3}

Generate documentation from a given API endpoint and save it to a
folder.

This function fetches data from the specified API endpoint, processes
it, and saves the generated documentation in the provided folder. If an
error occurs during the fetching process, a SystemExit exception is
raised with an appropriate message.

Args:
    api_url (str): The URL of the API endpoint from which data will be fetched.
    token (str): The authentication token required to access the API.
    folder_path (str): The path to the folder where the documentation will be saved.

# namespace `tests::test_web_config` {#namespacetests_1_1test__web__config}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`class `[`tests::test_web_config::TestWebConfig`](#classtests_1_1test__web__config_1_1TestWebConfig) | 

# class `tests::test_web_config::TestWebConfig` {#classtests_1_1test__web__config_1_1TestWebConfig}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------
`public def `[`test_config_llm_web_server_setup`](#classtests_1_1test__web__config_1_1TestWebConfig_1afc6440352201d207ea8b4d26f8ccfa35)`(self,mock_resource_filename,mock_server,mock_webbrowser)` | Set up and test the web server configuration for an LLM (Large Language
`public def `[`test_config_jira_web_server_setup`](#classtests_1_1test__web__config_1_1TestWebConfig_1a06e600222e426b003850509cb1d3190a)`(self,mock_resource_filename,mock_server,mock_webbrowser)` | Test the configuration and setup of a JIRA web server.

## Members

#### `public def `[`test_config_llm_web_server_setup`](#classtests_1_1test__web__config_1_1TestWebConfig_1afc6440352201d207ea8b4d26f8ccfa35)`(self,mock_resource_filename,mock_server,mock_webbrowser)` {#classtests_1_1test__web__config_1_1TestWebConfig_1afc6440352201d207ea8b4d26f8ccfa35}

Set up and test the web server configuration for an LLM (Large Language
Model) web interface.

This function configures a mock web server for testing purposes,
including setting up resource filenames, mocking server behavior, and
verifying that the web browser is opened and the server starts
correctly. The function uses various mocks to simulate external
dependencies such as `resource_filename` and `server`.

Args:
    mock_resource_filename (MagicMock): A MagicMock object simulating the `resource_filename` function.
    mock_server (MagicMock): A MagicMock object simulating the context manager for the web server.
    mock_webbrowser (MagicMock): A MagicMock object simulating the `webbrowser` module.

#### `public def `[`test_config_jira_web_server_setup`](#classtests_1_1test__web__config_1_1TestWebConfig_1a06e600222e426b003850509cb1d3190a)`(self,mock_resource_filename,mock_server,mock_webbrowser)` {#classtests_1_1test__web__config_1_1TestWebConfig_1a06e600222e426b003850509cb1d3190a}

Test the configuration and setup of a JIRA web server.

This function tests the entire process of setting up a JIRA web server,
including mocking necessary resources, configuring the server to shut
down after handling one request, and verifying that the web browser is
opened with the correct URL. The function uses several mocks to simulate
external dependencies such as resource files, servers, and web browsers.

Args:
    mock_resource_filename (MagicMock): A MagicMock object for simulating the `resource_filename` function.
    mock_server (MagicMock): A MagicMock object for simulating the server setup.
    mock_webbrowser (MagicMock): A MagicMock object for simulating the web browser opening.

# class `Exception` {#classException}

## Summary

 Members                        | Descriptions                                
--------------------------------|---------------------------------------------

## Members

Generated by [Moxygen](https://sourcey.com/moxygen)