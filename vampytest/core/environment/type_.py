__all__ = ('EnvironmentType',)

from enum import Enum


class EnvironmentType(Enum):
    """
    Represents an environment's type.
    
    Environment types are detected from test type.
    
    Options
    -------
    +-----------------------+
    | Name                  |
    +=======================+
    | none                  |
    +-----------------------+
    | generator             |
    +-----------------------+
    | coroutine             |
    +-----------------------+
    | coroutine_generator   |
    +-----------------------+
    """
    none = 0
    default = 1
    generator = 2
    coroutine = 3
    coroutine_generator = 4
