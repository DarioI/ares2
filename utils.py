import os

SHELL_STATUS_STOP = 0
SHELL_STATUS_RUN = 1
HISTORY_PATH = os.path.expanduser('~') + os.sep + '.droid_history'

INVERT_CODE = "\033[7m"
BLUE = "\033[34m"
RESET = "\033[0m"
GREEN = "\033[92m"
WHITE = "\033[97m"


def format_command_prompt(command_prompt):
    return INVERT_CODE + BLUE + str(command_prompt) + RESET


def format_directory_string(directory):
    return INVERT_CODE + GREEN + str(directory) + RESET


def decode_string(encoded_string):
    return (encoded_string.split(":&:")[0],
            encoded_string.split(":&:")[1],
            encoded_string.split(":&:")[2])
