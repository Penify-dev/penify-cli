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
    """Format an informational message with appropriate color.

    Args:
        message (str): The text of the informational message to be formatted.

    Returns:
        str: The formatted informational message with the specified color.
    """
    return f"{INFO_COLOR}{message}{Style.RESET_ALL}"

def format_success(message):
    """Format a success message with appropriate color.

    This function takes a message as input and wraps it in ANSI escape codes
    to display it in green, indicating a successful operation. The
    Style.RESET_ALL is applied at the end to ensure that any subsequent text
    is displayed in the default style.

    Args:
        message (str): The message to be formatted as a success message.

    Returns:
        str: The formatted success message with green color and reset style.
    """
    return f"{SUCCESS_COLOR}{message}{Style.RESET_ALL}"

def format_warning(message):
    """Format a warning message with appropriate color.

    Args:
        message (str): The warning message to be formatted.

    Returns:
        str: The formatted warning message with the specified color.
    """
    return f"{WARNING_COLOR}{message}{Style.RESET_ALL}"

def format_error(message):
    """Format an error message with appropriate color.

    This function takes a plain error message and wraps it in ANSI escape
    codes to apply the specified error color, ensuring that the error
    message is visually distinct when output. The function supports various
    error colors defined by constants like `ERROR_COLOR`.

    Args:
        message (str): The plain text error message to be formatted.

    Returns:
        str: The formatted error message with the error color applied.
    """
    return f"{ERROR_COLOR}{message}{Style.RESET_ALL}"

def format_highlight(message):
    """Format a highlighted message with appropriate color.

    Args:
        message (str): The message to be formatted and highlighted.

    Returns:
        str: The formatted message with applied highlight style.
    """
    return f"{HIGHLIGHT_COLOR}{message}{Style.RESET_ALL}"

def format_file_path(file_path):
    """Format a file path with appropriate color.

    This function takes a file path as input and wraps it in ANSI escape
    codes to apply a warning color. The original file path is then reset to
    default style using Style.RESET_ALL.

    Args:
        file_path (str): The file path to be formatted.

    Returns:
        str: The formatted file path with the warning color applied.
    """
    return f"{WARNING_COLOR}{file_path}{Style.RESET_ALL}"

def print_info(message):
    """Print an informational message with appropriate formatting.

    This function takes a string message as input and prints it in a
    formatted manner. It utilizes the `format_info` function to apply any
    necessary formatting before printing.

    Args:
        message (str): The message to be printed.
    """
    print(format_info(message))

def print_success(message):
    """Print a formatted success message.

    This function takes a string `message` and prints it as a formatted
    success message. The formatting includes adding a prefix "Success: " to
    the message and enclosing it within asterisks for emphasis.

    Args:
        message (str): The message to be printed as a success message.
    """
    print(format_success(message))

def print_warning(message):
    """Print a warning message with appropriate formatting.

    This function takes a warning message as input and prints it with
    formatted output. The formatting may include color, timestamp, or other
    styles to emphasize that it is a warning.

    Args:
        message (str): The warning message to be printed.
    """
    print(format_warning(message))

def print_error(message):
    """Print an error message with appropriate formatting.

    This function takes a string message, formats it as an error message,
    and then prints it. The formatting typically includes prefixing the
    message with "Error: " to clearly indicate that it is an error.

    Args:
        message (str): The error message to be printed.
    """
    print(format_error(message))

def print_processing(file_path):
    """Print a processing message for a specified file.

    This function takes a file path, formats it using `format_file_path`,
    and then prints a formatted message indicating that the file is being
    processed. The formatted path is highlighted using `format_highlight`.

    Args:
        file_path (str): The path of the file to be processed.
    """
    formatted_path = format_file_path(file_path)
    print(f"\n{format_highlight(f'Processing file: {formatted_path}')}")

def print_status(status, message):
    """Print a status message with an appropriate symbol.

    This function takes a status and a message, then prints them with a
    colored symbol that corresponds to the given status. The available
    statuses are 'success', 'warning', 'error', and any other value will
    default to a processing indicator.

    Args:
        status (str): The status type ('success', 'warning', 'error') or another string.
        message (str): The message to be displayed along with the symbol.
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
    """Create a tqdm progress bar with consistent styling.

    Args:
        total (int): Total number of items to process.
        desc (str): Description for the progress bar. Defaults to "Processing".
        unit (str): Unit label for the progress items. Defaults to "item".

    Returns:
        tqdm: A configured tqdm progress bar instance.
    """
    return tqdm(
        total=total,
        desc=format_info(desc),
        unit=unit,
        ncols=80,
        ascii=True
    )

def create_stage_progress_bar(stages, desc="Processing"):
    """Create a tqdm progress bar for processing stages with consistent
    styling.

    This function initializes and returns a tqdm progress bar object for
    tracking the progress through a series of stages. It also provides a
    description for the progress bar to enhance its usability.

    Args:
        stages (list): A list of strings representing individual stages in the process.
        desc (str?): A description for the progress bar. Defaults to "Processing".

    Returns:
        tuple: A tuple containing the tqdm progress bar object and the list of stages.
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
    """Update the progress bar with a new stage name.

    This function updates the provided tqdm progress bar to reflect the
    current stage of a process. It clears any existing postfix and sets a
    new description based on the provided stage name. The display is then
    refreshed to ensure that the update is visible immediately.

    Args:
        pbar (tqdm): The progress bar object to be updated.
        stage_name (str): A string representing the current stage of the process.
    """
    # Force refresh with a custom description and ensure it's visible
    pbar.set_postfix_str("")  # Clear any existing postfix
    pbar.set_description_str(f"{format_info(stage_name)}")
    pbar.refresh()  # Force refresh the display
