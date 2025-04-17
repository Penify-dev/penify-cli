import json
import os
import sys
from typing import Dict, Optional, List, Any, Union
import litellm

class LLMClient:
    """
    Client for interacting with LLM models using LiteLLM.
    """
    
    def __init__(self, model: str = None, api_base: str = None, api_key: str = None):
        # Configure litellm if parameters are provided
        """Initialize the LLM client.
        
        This function configures and initializes the LLM client with the provided model, API base URL, and API key. If any of
        these parameters are provided, they will be used to set environment variables for interacting with the LLM service.
        
        Args:
            model (str?): The LLM model to use (e.g., "gpt-4", "ollama/llama2", etc.). Defaults to None.
            api_base (str?): The base URL for API requests (e.g., "http://localhost:11434" for Ollama). Defaults to None.
            api_key (str?): The API key for the LLM service. Defaults to None.
        """
        self.model = model
        if api_base:
            os.environ["OPENAI_API_BASE"] = api_base
        if api_key:
            os.environ["OPENAI_API_KEY"] = api_key
    
    def generate_commit_summary(self, diff: str, message: str, generate_description: bool, repo_details: Dict, jira_context: Dict = None) -> Dict:
        """Generate a concise and descriptive commit summary using the LLM.
        
        This function generates a concise and descriptive commit summary based on the provided Git diff, user instructions,
        repository details, and optional JIRA context. It constructs a prompt for the LLM to produce a commit title and an
        optional detailed description, adhering to Semantic Commit Messages guidelines. If the JIRA context is provided, it
        enriches the prompt with relevant issue information.
        
        Args:
            diff (str): Git diff of changes.
            message (str): User-provided commit message or instructions.
            generate_description (bool): Flag indicating whether to include a detailed description in the summary.
            repo_details (Dict): Details about the repository.
            jira_context (Dict?): Optional JIRA issue context to enhance the summary. Defaults to None.
        
        Returns:
            Dict: A dictionary containing the title and description for the commit. If generate_description is False,
            the 'description' key may be absent.
        
        Raises:
            ValueError: If the LLM model is not configured.
        """
        if not self.model:
            raise ValueError("LLM model not configured. Please provide a model when initializing LLMClient.")
        
        # Limit diff size to avoid token limits
        max_diff_chars = 10000
        if len(diff) > max_diff_chars:
            diff = diff[:max_diff_chars] + f"\n... (diff truncated, total {len(diff)} characters)"
        
        # Create prompt for the LLM
        prompt = f"""
        Based on the Git diff below, generate a concise and descriptive commit summary.
                
        User instructions: {message}
        """
        
        # Add JIRA context if available
        if jira_context and jira_context.get('primary_issue'):
            primary = jira_context['primary_issue']
            prompt += f"""
            
            JIRA ISSUE INFORMATION:
            Issue Key: {primary['key']}
            Summary: {primary['summary']}
            Type: {primary['type']}
            Status: {primary['status']}
            """
            
            if 'description' in primary and primary['description']:
                # Include a condensed version of the description
                description = primary['description']
                if len(description) > 500:
                    description = description[:500] + "..."
                prompt += f"Description: {description}\n"
                
            if 'acceptance_criteria' in primary:
                prompt += f"Acceptance Criteria: {primary['acceptance_criteria']}\n"
                
            prompt += """
            
            Please make sure your commit message addresses the business requirements in the JIRA issue
            while accurately describing the technical changes in the diff.
            """
                
        prompt += f"""
        
        Git diff:
        ```
        {diff}
        ```
        
        Please provide:
        1. A short, focused commit title (50-72 characters) in a Semantic Commit Messages format. Format: <type>(<scope>): <subject>
        {'2. A detailed description that explains what was changed, why it was changed in both business and technical aspects, and any important context' if generate_description else ''}

        List of Semantic Commit Message types that you can use:
        feat: (new feature for the user, not a new feature for build script)
        fix: (bug fix for the user, not a fix to a build script)
        docs: (changes to the documentation)
        style: (formatting, missing semi colons, etc; no production code change)
        refactor: (refactoring production code, eg. renaming a variable)
        test: (adding missing tests, refactoring tests; no production code change)
        chore: (updating grunt tasks etc; no production code change)
        
        Format your response as valid JSON with 'title' {"and 'description'" if generate_description else ''} keys.
        """
        
        try:
            # Call the LLM using litellm
            response = litellm.completion(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.2,
                max_tokens=800  # Increased token limit to accommodate detailed descriptions
            )            
            content = response.choices[0].message.content
            
            # Extract JSON from the response
            try:
                # Try to parse the entire content as JSON
                result = json.loads(content)
                if not isinstance(result, dict) or 'title' not in result or 'description' not in result:
                    raise ValueError("Invalid JSON structure")
                    
            except json.JSONDecodeError:
                # If that fails, try to extract JSON from the content
                import re
                json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    result = json.loads(json_match.group(1))
                else:
                    # Last resort: extract title and description directly
                    lines = content.split('\n')
                    title = next((line for line in lines if line.strip()), "Generated commit").strip()
                    description = "\n".join(line for line in lines[1:] if line.strip())
                    result = {
                        "title": title,
                        "description": description
                    }
            
            if not generate_description and 'description' in result:
                # If description is missing and user requested it, add a placeholder
                del result['description']
            return result
            
        except Exception as e:
            sys.exit(f"Error generating commit summary: {e}")
            # Fallback to a basic summary if LLM fails
            print(f"Error generating commit summary with LLM: {e}")
            return {
                "title": "Update code",
            }
