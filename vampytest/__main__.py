import sys

from scarletio import get_short_executable

from .main import execute_from_parameters


def __main__():
    """
    Executes vampytest from terminal.
    """
    parameters = sys.argv.copy()
    
    if parameters and ((parameters[0] == __file__) or (parameters[0] != get_short_executable())):
        del parameters[0]
    
    return_code = execute_from_parameters(parameters)
    raise SystemExit(return_code)


if __name__ == '__main__':
    __main__()
