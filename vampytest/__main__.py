import sys

from .main import execute_from_terminal

def main():
    """
    Executes vampytest from terminal.
    """
    parameters = sys.argv.copy()
    if parameters and parameters[0] == __file__:
        del parameters[0]
    
    execute_from_terminal(parameters)


if __name__ == '__main__':
    main()
