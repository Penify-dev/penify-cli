# page `md__tmp_github_reposRepoArchDocGenContext_Penify_dev_penify_cli_docs_commit_commands` {#md__tmp_github_reposRepoArchDocGenContext_Penify_dev_penify_cli_docs_commit_commands}

The `commit` command allows you to generate smart, AI-powered commit messages for your Git changes. This document explains all available options and combinations.

Basic Usage
```cpp
penify commit
```

By default, this command:

* Analyzes your staged Git changes

* Generates a concise commit title only

* Uses local LLM if configured, or falls back to Penify API

Command Options<tt>-m, --message</tt>Provide context for the commit message generation:

```cpp
penify commit -m "Fix login flow"
```

This hint helps the AI understand your intention and improves the quality of the generated message.

<tt>-e, --terminal</tt>Open an editor to review and edit the generated commit message before committing:

```cpp
penify commit -e
```

This opens your default Git editor with the generated message for review.

<tt>-d, --description</tt>Generate a detailed commit message with both title and description:

```cpp
penify commit -d
```

Without this flag, only the commit title is generated.

Option CombinationsYou can combine these options for different workflows:

Generate Title Only with Context
```cpp
penify commit -m "Update login UI"
```

Generate Title and Description with Context
```cpp
penify commit -m "Update login UI" -d
```

Generate and Edit Full Commit Message
```cpp
penify commit -d -e
```

Generate, Edit, and Provide Context
```cpp
penify commit -m "Refactor authentication" -d -e
```

LLM and JIRA IntegrationUsing Local LLMIf you've configured a local LLM using `penify config llm`, the commit command will automatically use it for message generation.

Benefits:

* Privacy: your code changes don't leave your machine

* Speed: no network latency

* Works offline

JIRA EnhancementIf you've configured JIRA integration using `penify config jira`, the commit command will:

* Detect JIRA issue references in your changes

* Fetch issue details from your JIRA instance

* Include issue information in the commit message

* Format the commit message according to JIRA's smart commit format

Example output: 
```cpp
PROJ-123: Fix authentication bug in login flow

- Updated OAuth token validation
- Fixed session timeout handling
- Added unit tests for edge cases

[PROJ-123]
```

Configuration RequirementsFor the `commit` command to work:

* You must have configured either:

* Local LLM via `penify config llm`, OR

* Logged in via `penify login`

* For JIRA enhancement (optional):

* Configure JIRA via `penify config jira`

ExamplesBasic Commit with Default Settings
```cpp
# Stage your changes
git add .

# Generate commit message
penify commit

# Commit with the generated message
git commit -m "Generated message here"
```

Full Workflow with All Features
```cpp
# Stage your changes
git add .

# Generate detailed commit message with JIRA integration, 
# provide context, and open editor for review
penify commit -m "Fix login issue" -d -e

# The commit is automatically completed after you save and exit the editor
```

TroubleshootingCommon Issues* **"No LLM model or API token provided"**

* Run `penify config llm` to configure a local LLM, or

* Run `penify login` to authenticate with Penify

* **"Failed to connect to JIRA"**

* Check your JIRA configuration with `cat ~/.penify`

* Verify your network connection

* Ensure your JIRA credentials are valid

* **"Error initializing LLM client"**

* Verify your LLM configuration settings

* Ensure the LLM API is accessible

