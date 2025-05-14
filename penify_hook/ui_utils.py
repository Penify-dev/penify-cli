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
    """Format an informational message with appropriate color."""
    return f"{INFO_COLOR}{message}{Style.RESET_ALL}"

def format_success(message):
    """Formats a success message with green color and reset style."""
    return f"{SUCCESS_COLOR}{message}{Style.RESET_ALL}"

def format_warning(message):
    """Format a warning message with appropriate color."""
    return f"{WARNING_COLOR}{message}{Style.RESET_ALL}"

def format_error(message):
    """Format an error message with the specified error color."""
    return f"{ERROR_COLOR}{message}{Style.RESET_ALL}"

def format_highlight(message):
    """Format a highlighted message with appropriate color."""
    return f"{HIGHLIGHT_COLOR}{message}{Style.RESET_ALL}"

def format_file_path(file_path):
    """Format a file path with a warning color."""
    return f"{WARNING_COLOR}{file_path}{Style.RESET_ALL}"

def print_info(message):
    """Prints an informational message."""
    print(format_info(message))

def print_success(message):
    """Prints a formatted success message."""
    print(format_success(message))

def print_warning(message):
    """Prints a formatted warning message."""
    print(format_warning(message))

def print_error(message):
    """Prints an error message with formatting."""
    print(format_error(message))

def print_processing(file_path):
    """Prints a processing message for a specified file."""
    formatted_path = format_file_path(file_path)
    print(f"\n{format_highlight(f'Processing file: {formatted_path}')}")

def print_status(status, message):
    """Print a status message with an appropriate symbol."""
    if status == 'success':
        print(f"  {SUCCESS_COLOR}{SUCCESS_SYMBOL} {message}{Style.RESET_ALL}")
    elif status == 'warning':
        print(f"  {NEUTRAL_COLOR}{WARNING_SYMBOL} {message}{Style.RESET_ALL}")
    elif status == 'error':
        print(f"  {ERROR_COLOR}{ERROR_SYMBOL} {message}{Style.RESET_ALL}")
    else:
        print(f"  {PROCESSING_SYMBOL} {message}")

def create_progress_bar(total, desc="Processing", unit="item"):
    """Create a tqdm progress bar with consistent styling."""
    return tqdm(
        total=total,
        desc=format_info(desc),
        unit=unit,
        ncols=80,
        ascii=True
    )

def create_stage_progress_bar(stages, desc="Processing"):
    """Create a tqdm progress bar for processing stages with consistent styling."""
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
    """Update the progress bar with a new stage name."""
    pbar.set_postfix_str("")  # Clear any existing postfix
    pbar.set_description_str(f"{format_info(stage_name)}")
    pbar.refresh()  # Force refresh the display
