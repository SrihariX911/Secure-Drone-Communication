from ast import literal_eval

# Function to process input and convert strings to ASCII values
def string_to_ascii(input_value):
    """
    Converts a string to a list of ASCII values or validates a list of numbers.

    Parameters:
        input_value (str or list): The input value to process. 
                                   - If a string, it will be converted to ASCII values.
                                   - If a list, it must contain only numbers.

    Returns:
        list: A list of ASCII values if input is a string, or the same list if it contains only numbers.

    Raises:
        ValueError: If the input is neither a string nor a list of numbers.
    """
    if isinstance(input_value, list):
        # Check if all elements in the list are numbers
        if all(isinstance(item, (int, float)) for item in input_value):
            return input_value  # Return the list as is if valid
        else:
            raise ValueError("List input must contain only numbers.")
    elif isinstance(input_value, str):
        # Convert string to a list of ASCII values
        return [ord(char) for char in input_value]
    else:
        raise ValueError("Input must be a list of numbers or a string.")

# Example usage
msg = "dheeraj"
ascii_values = string_to_ascii(msg)
print("ASCII values:", ascii_values)
