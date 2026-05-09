from os import getcwd as get_current_working_directory
from sys import argv as COMMAND_LINE_PARAMETERS, path as SYSTEM_PATHS

# When you run `python3 -m vampytest`, the current working directory is added as the first parameter;
# We do not want that, because it makes local directories importable before other packages.
CURRENT_WORKING_DIRECTORY = get_current_working_directory()
if (len(SYSTEM_PATHS) > 1) and (SYSTEM_PATHS[0] == CURRENT_WORKING_DIRECTORY):
    del SYSTEM_PATHS[0]


from scarletio import get_short_executable

from .main import execute_from_parameters


def __main__():
    """
    Executes vampytest from terminal.
    """
    parameters = COMMAND_LINE_PARAMETERS.copy()
    
    if parameters and ((parameters[0] == __file__) or (parameters[0] != get_short_executable())):
        del parameters[0]
    
    return_code = execute_from_parameters(parameters)
    raise SystemExit(return_code)


if __name__ == '__main__':
    __main__()
