# page `md__tmp_github_reposRepoArchDocGenContext_Penify_dev_penify_cli_docs_example_workflows` {#md__tmp_github_reposRepoArchDocGenContext_Penify_dev_penify_cli_docs_example_workflows}

This document demonstrates how to use Penify CLI in real-world development workflows to improve your productivity.

Workflow 1: Efficient Git Commits with AISetupFirst, configure your local LLM for offline operation:

```cpp
penify config llm
```

Configure your JIRA integration for enhanced commit messages:

```cpp
penify config jira
```

Daily Workflow* Make your code changes as usual

* When ready to commit, use Penify to generate a smart commit message:

```cpp
penify commit
```

* Review and confirm the generated commit message

* Git commit and push as usual

Benefits

* Consistent and descriptive commit messages

* Automatic inclusion of relevant JIRA ticket information

* Time saved from writing detailed commit messages

Workflow 2: Documentation Generation PipelineSetupLogin to Penify to access advanced documentation features:

```cpp
penify login
```

Install the Git hook for automatic documentation generation:

```cpp
penify docgen install-hook
```

Daily Workflow* Make your code changes as usual

* Commit your changes

* Documentation is automatically generated for changed files

* Review the generated documentation

Manual DocumentationFor specific files or folders:

```cpp
penify docgen -l src/components/authentication
```

Benefits

* Always up-to-date documentation

* Consistent documentation style

* Time saved from writing detailed documentation

Workflow 3: Code Review EnhancementSetupEnsure you're logged into Penify:

```cpp
penify login
```

Workflow* Before submitting a PR, generate documentation for changed files:

```cpp
penify docgen
```

* Include the generated documentation in your PR

* Reviewers can better understand your changes with the AI-generated explanations

Benefits

* Improved PR quality

* Faster code reviews

* Better team understanding of code changes

Workflow 4: Onboarding New Team MembersFor Team LeadsGenerate comprehensive documentation for the entire codebase:

```cpp
penify docgen -l .
```

For New Team MembersGenerate focused documentation for components you're working on:

```cpp
penify docgen -l src/components/my-feature
```

Benefits

* Faster onboarding

* Better understanding of code structure

* Reduced questions to senior team members

Workflow 5: Legacy Code UnderstandingWhen working with unfamiliar legacy code:

```cpp
# Document a specific complex file
penify docgen -l src/legacy/complex_module.py

# Document an entire legacy component
penify docgen -l src/legacy/old_component
```

Benefits

* Quickly understand complex legacy systems

* Reduce time spent deciphering undocumented code

* Make safer changes to legacy systems

