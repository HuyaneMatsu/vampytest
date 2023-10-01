import sys

from scarletio import get_short_executable

from .main import execute_from_terminal


def __main__():
    """
    Executes vampytest from terminal.
    """
    parameters = sys.argv.copy()
    
    if parameters and ((parameters[0] == __file__) or (parameters[0] != get_short_executable())):
        del parameters[0]
    
    execute_from_terminal(parameters)


if __name__ == '__main__':
    __main__()
