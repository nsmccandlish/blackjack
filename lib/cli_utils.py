from typing import Set


def get_user_input_integer(message: str, min_value=None, max_value=None) -> int:
    # Get an integer input from the user
    # TODO: add 'help' option, always available?
    while True:
        value = input(message)
        try:
            return _validate_integer_input(value, min_value, max_value)
        except ValueError as e:
            print(f"Error: {e}\n")


def _validate_integer_input(value: str, min_value=0, max_value=None) -> int:
    value.strip()
    try:
        value = int(value)
    except ValueError:
        raise ValueError(f"{value} is not a valid integer.")

    if min_value is not None and value < min_value:
        raise ValueError(f"Input may not be less than {min_value}.")

    if max_value is not None and value > max_value:
        raise ValueError(f"Input may not be greater than {max_value}.")

    return value


def get_user_string_input(message: str, input_options: Set[str]) -> str:
    # If all input options have a unique first character, let the user type that instead
    option_first_chars = {option[0]: option for option in input_options}
    allow_first_chars = bool(len(option_first_chars) == len(input_options))

    # TODO: add 'help' option, always available?
    while True:
        value = input(message)
        if value.lower() in input_options:
            return value.lower()
        elif allow_first_chars and value.lower() in option_first_chars:
            return option_first_chars.get(value.lower())

        print(f"Error: '{value}' it not a valid option.\n")


def make_string_green(message):
    return f"\033[92m{message}\033[0m"
