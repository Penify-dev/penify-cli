"""
UI utilities for Penify CLI.

This module provides utility functions for consistent UI formatting,
colored output, and progress indicators across the Penify CLI application.
"""
import os
from colorama import Fore, Style, init
from tqdm import tqdm

# Initialize colorama for cross-platform colored terminal output
init(autoreset=True)

# Color constants for different message types
INFO_COLOR = Fore.CYAN
SUCCESS_COLOR = Fore.GREEN
WARNING_COLOR = Fore.YELLOW
ERROR_COLOR = Fore.RED
HIGHLIGHT_COLOR = Fore.BLUE
NEUTRAL_COLOR = Fore.WHITE

# Status symbols
SUCCESS_SYMBOL = "✓"
WARNING_SYMBOL = "○"
ERROR_SYMBOL = "✗"
PROCESSING_SYMBOL = "⟳"

def format_info(message):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    return f"{INFO_COLOR}{message}{Style.RESET_ALL}"

def format_success(message):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    return f"{SUCCESS_COLOR}{message}{Style.RESET_ALL}"

def format_warning(message):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    return f"{WARNING_COLOR}{message}{Style.RESET_ALL}"

def format_error(message):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    return f"{ERROR_COLOR}{message}{Style.RESET_ALL}"

def format_highlight(message):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    return f"{HIGHLIGHT_COLOR}{message}{Style.RESET_ALL}"

def format_file_path(file_path):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    return f"{WARNING_COLOR}{file_path}{Style.RESET_ALL}"

def print_info(message):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    print(format_info(message))

def print_success(message):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    print(format_success(message))

def print_warning(message):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    print(format_warning(message))

def print_error(message):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    print(format_error(message))

def print_processing(file_path):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    formatted_path = format_file_path(file_path)
    print(f"\n{format_highlight(f'Processing file: {formatted_path}')}")

def print_status(status, message):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    if status == 'success':
        print(f"  {SUCCESS_COLOR}{SUCCESS_SYMBOL} {message}{Style.RESET_ALL}")
    elif status == 'warning':
        print(f"  {NEUTRAL_COLOR}{WARNING_SYMBOL} {message}{Style.RESET_ALL}")
    elif status == 'error':
        print(f"  {ERROR_COLOR}{ERROR_SYMBOL} {message}{Style.RESET_ALL}")
    else:
        print(f"  {PROCESSING_SYMBOL} {message}")

def create_progress_bar(total, desc="Processing", unit="item"):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    return tqdm(
        total=total,
        desc=format_info(desc),
        unit=unit,
        ncols=80,
        ascii=True
    )

def create_stage_progress_bar(stages, desc="Processing"):
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    pbar = tqdm(
        total=len(stages),
        desc=format_info(desc),
        unit="step",
        ncols=80,
        ascii=True
    )
    return pbar, stages

def update_stage(pbar, stage_name):
    # Force refresh with a custom description and ensure it's visible
    """Save the processed files map to a JSON file.
    
    Function parameters should be documented in the ``Args`` section. The name of each parameter is required. The type and
    description of each parameter is optional, but should be included if not obvious.
    
    @type dictionary: dict
    @param dictionary: The processed files map.
    @rtype: bool
    @return: True if successful, False otherwise.
    @return: The return type is optional and may be specified at the beginning of
    @return: the ``Returns`` section followed by a colon.
    @return: The ``Returns`` section may span multiple lines and paragraphs.
    @return: Following lines should be indented to match the first line.
    @return: The ``Returns`` section supports any reStructuredText formatting,
    @return: including literal blocks::
        
        {
        'param1': param1,
        'param2': param2
        }
    """
    pbar.set_postfix_str("")  # Clear any existing postfix
    pbar.set_description_str(f"{format_info(stage_name)}")
    pbar.refresh()  # Force refresh the display
