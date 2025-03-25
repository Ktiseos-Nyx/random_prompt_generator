# debug_utils.py

# Example:  Print variable values with a label
def print_debug(label, value):
    """Prints a debug message with a label and the value."""
    print(f"DEBUG: {label}: {value}")

# Example:  Conditional breakpoint (useful for interactive debugging)
def conditional_breakpoint(condition):
    """Sets a breakpoint if the condition is True."""
    if condition:
        breakpoint()  # Requires Python 3.7+