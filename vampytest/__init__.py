__version__ = '0.0.22'

try:
    import scarletio
except ImportError as err:
    raise ImportError(
        'Couldn\'t import scarletio. \n'
        'Are you sure it\'s installed and available on your PYTHONPATH environment variable?\n'
        'Did you forget to activate a virtual environment?\n'
    ) from err

del scarletio


from .core import *

from .return_codes import *


__all__ = (
    *core.__all__,
    
    *return_codes.__all__,
)
