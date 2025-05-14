# page `md__tmp_github_reposRepoArchDocGenContext_Penify_dev_penify_cli_docs_config_commands` {#md__tmp_github_reposRepoArchDocGenContext_Penify_dev_penify_cli_docs_config_commands}

The `config` command allows you to set up and manage configuration settings for Penify CLI. This document explains all available configuration options and how to use them.

Configuration OverviewPenify CLI stores configuration in a JSON file at `~/.penify/config.json`. The configuration includes:

* LLM (Large Language Model) settings for local commit message generation

* JIRA integration settings for enhanced commit messages

* API tokens and other credentials

Basic Usage
```cpp
# Configure LLM settings
penify config llm

# Configure JIRA integration
penify config jira
```

LLM ConfigurationWeb InterfaceRunning `penify config llm` opens a web interface in your browser where you can configure:

* **Model**: The LLM model to use (e.g., `gpt-3.5-turbo`)

* **API Base URL**: The endpoint URL for your LLM API (e.g., `[https://api.openai.com/v1](https://api.openai.com/v1)`)

* **API Key**: Your authentication key for the LLM API

Supported LLMsPenify CLI supports various LLM providers:

OpenAI

* Model: `gpt-3.5-turbo` or `gpt-4`

* API Base: `[https://api.openai.com/v1](https://api.openai.com/v1)`

* API Key: Your OpenAI API key

Anthropic

* Model: `claude-instant-1` or `claude-2`

* API Base: `[https://api.anthropic.com/v1](https://api.anthropic.com/v1)`

* API Key: Your Anthropic API key

Ollama (Local)

* Model: `llama2` or any model you have installed

* API Base: `[http://localhost:11434](http://localhost:11434)`

* API Key: (leave blank)

Azure OpenAI

* Model: Your deployed model name

* API Base: Your Azure endpoint

* API Key: Your Azure API key

Configuration File StructureAfter configuration, your `~/.penify/config.json` will contain:

```cpp
{
  "llm": {
    "model": "gpt-3.5-turbo",
    "api_base": "https://api.openai.com/v1",
    "api_key": "sk-..."
  }
}
```

JIRA ConfigurationWeb InterfaceRunning `penify config jira` opens a web interface where you can configure:

* **JIRA URL**: Your JIRA instance URL (e.g., `[https://yourcompany.atlassian.net](https://yourcompany.atlassian.net)`)

* **Username**: Your JIRA username (typically your email)

* **API Token**: Your JIRA API token

Creating a JIRA API Token* Log in to [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)

* Click "Create API token"

* Give it a name (e.g., "Penify CLI")

* Copy the generated token and paste it into the configuration

Configuration File StructureAfter configuration, your `~/.penify/config.json` will contain:

```cpp
{
  "jira": {
    "url": "https://yourcompany.atlassian.net",
    "username": "your.email@example.com",
    "api_token": "your-jira-api-token"
  }
}
```

Configuration LocationsPenify CLI looks for configuration in multiple locations:

* Project-specific: `.penify/config.json` in the Git repository root

* User-specific: `~/.penify/config.json` in your home directory

The project-specific configuration takes precedence if both exist.

Environment VariablesYou can override configuration settings using environment variables:

* `PENIFY_API_TOKEN`: Override the stored API token

* `PENIFY_LLM_MODEL`: Override the configured LLM model

* `PENIFY_LLM_API_BASE`: Override the configured LLM API base URL

* `PENIFY_LLM_API_KEY`: Override the configured LLM API key

* `PENIFY_JIRA_URL`: Override the configured JIRA URL

* `PENIFY_JIRA_USER`: Override the configured JIRA username

* `PENIFY_JIRA_TOKEN`: Override the configured JIRA API token

Example: 
```cpp
export PENIFY_LLM_MODEL="gpt-4"
penify commit
```

Command-Line ConfigurationFor advanced users or scripting, you can directly edit the configuration file:

```cpp
# View current configuration
cat ~/.penify/config.json

# Edit configuration with your preferred editor
nano ~/.penify/config.json
```

Sharing ConfigurationYou can share configuration between machines by copying the `.penify/config.json` file. However, be cautious with API keys and credentials.

For team settings, consider:* Using a project-specific `.penify/config.json` with shared settings

* Excluding API keys from shared configuration

* Using environment variables for sensitive credentials

TroubleshootingCommon Issues* **"Error reading configuration file"**

* Check if the file exists: `ls -la ~/.penify`

* Ensure it contains valid JSON: `cat ~/.penify/config.json`

* **"Failed to connect to LLM API"**

* Verify API base URL and API key

* Check network connectivity to the API endpoint

* Ensure your account has access to the specified model

* **"Failed to connect to JIRA"**

* Check JIRA URL format (should include `[https://](https://)`)

* Verify username and API token

* Ensure your JIRA account has API access permissions

