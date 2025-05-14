# page `md__tmp_github_reposRepoArchDocGenContext_Penify_dev_penify_cli_docs_detailed_usage` {#md__tmp_github_reposRepoArchDocGenContext_Penify_dev_penify_cli_docs_detailed_usage}

This document provides in-depth information about all features and capabilities of the Penify CLI tool.

Table of Contents

* Penify CLI - Detailed Usage Guide

* Table of Contents

* Authentication

* Login Process

* API Token Storage

* Token Precedence

* Command Overview

* Commit Message Generation

* Code Documentation Generation

* Use Cases

* Authentication Requirement

* Configuration Settings

* Git Hooks

* Post-Commit Hook

* Custom Hook Location

* Advanced Use Cases

* CI/CD Integration

* Remote Repository Documentation

* Troubleshooting

* Common Issues

* Logs

* Support

AuthenticationLogin ProcessWhen you run `penify login`, the tool:

* Opens your default web browser

* Redirects you to Penify's login page

* Captures the authentication token after successful login

* Saves the token in `~/.penify` file

API Token StorageAPI tokens are stored in your home directory in the `.penify` file. This JSON file contains:

```cpp
{
  "api_keys": "your-api-token",
  "llm": { "model": "...", "api_base": "...", "api_key": "..." },
  "jira": { "url": "...", "username": "...", "api_token": "..." }
}
```

Token Precedence* Environment variable `PENIFY_API_TOKEN` (highest priority)

* Token in `~/.penify` file

Command Overview
```cpp
penify
├── commit        Generate smart commit messages
├── config        Configure local LLM and JIRA
│   ├── llm       Configure local LLM settings
│   └── jira      Configure JIRA integration
├── login         Log in to Penify account
└── docgen        Generate code documentation
    ├── install-hook     Install Git post-commit hook
    └── uninstall-hook   Remove Git post-commit hook
```

Commit Message GenerationThe `commit` command analyzes your staged changes and generates meaningful commit messages. It can:

* Use a local LLM if configured

* Enhance messages with JIRA issue details

* Provide both title and description

For specific options and examples, see [docs/commit-commands.md](#md__tmp_github_reposRepoArchDocGenContext_Penify_dev_penify_cli_docs_commit_commands).

Code Documentation GenerationThe `docgen` command generates documentation for your code:

Use Cases* **Current Git Diff**: Default behavior, documents only changed files

* **Specific File**: Pass a file path with `-l path/to/file.py`

* **Entire Folder**: Pass a folder path with `-l path/to/folder`

Authentication RequirementThis feature requires authentication with a Penify account. Run `penify login` before using documentation features.

Configuration SettingsConfigure local settings using the `config` command:

* **LLM Settings**: Configure a local LLM for commit message generation

* **JIRA Settings**: Set up JIRA integration for enhanced commit messages

For detailed configuration options, see [docs/config-commands.md](#md__tmp_github_reposRepoArchDocGenContext_Penify_dev_penify_cli_docs_config_commands).

Git HooksPenify can install Git hooks to automate documentation generation:

Post-Commit Hook

* **Install**: `penify docgen install-hook`

* **What it does**: Automatically generates documentation for changed files after each commit

* **Uninstall**: `penify docgen uninstall-hook`

Custom Hook LocationYou can specify a custom location for Git hooks:

```cpp
penify docgen install-hook -l /path/to/git/repo
```

Advanced Use CasesCI/CD IntegrationFor CI/CD pipelines:

* Set `PENIFY_API_TOKEN` as an environment variable

* Run commands without requiring interactive login

Remote Repository DocumentationGenerate documentation for an entire repository:

```cpp
git clone https://github.com/user/repo
cd repo
penify docgen -l .
```

TroubleshootingCommon Issues* **API Key Errors**: Ensure you've run `penify login` or set `PENIFY_API_TOKEN`

* **LLM Configuration**: Check your LLM settings with `cat ~/.penify`

* **JIRA Integration**: Verify JIRA credentials in your configuration

LogsFor more detailed logs, you can set the environment variable:

```cpp
export PENIFY_DEBUG=1
```

SupportFor additional help, visit [https://docs.penify.dev/](https://docs.penify.dev/) or contact [support@penify.dev](mailto:support@penify.dev)

