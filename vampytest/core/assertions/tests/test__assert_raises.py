from ...utils import _
from ...wrappers import call_from

from ..exception import AssertionException
from ..top_level import assert_raises


class TestException(Exception):
    __slots__ = ('message',)
    __init__ = object.__init__
    
    def __new__(cls, message):
        self = Exception.__new__(cls, message)
        self.message = message
        return self
    
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        return self.message == other.message
    
    
    def __hash__(self):
        return hash(self.message)


def _iter_options():
    yield None, (ValueError, ), {}, True
    yield ValueError(), (ValueError, ), {}, False
    
    # expected_exceptions
    yield None, (ValueError, IndexError), {}, True
    yield ValueError(), (ValueError, IndexError), {}, False

    # accept_subtypes
    yield KeyError(), (LookupError, ), {}, False
    yield LookupError, (LookupError, ), {}, False
    yield KeyError(), (LookupError, ), {'accept_subtypes': False}, True
    yield LookupError, (LookupError, ), {'accept_subtypes': False}, False
    
    # instance
    yield TestException('nyan'), (TestException('nyan'), ), {}, False
    yield TestException('nyan'), (TestException('mrrr'), ), {}, True
    
    # where
    yield ValueError(), (ValueError, ), {'where': lambda exception: not exception.args}, False
    yield ValueError('nyan',), (ValueError, ), {'where': lambda exception: not exception.args}, True


@_(call_from(_iter_options()).returning_last())
def test__assert_raises(exception, expected_exceptions, keyword_parameters):
    """
    Tests whether ``assert_raises`` works as intended.
    
    Parameters
    ----------
    value : `None | BaseException`
        Exception to raise if any.
    
    expected_exceptions : `expected_exceptions : ˙tuple<type<BaseException> | instance<BaseException>>`
        Expected exceptions.
    
    keyword_parameters : `dict<str, object>`
        Additional keyword parameters to pass to the assertion.
    
    Returns
    -------
    failed : `bool`
    """
    try:
        with assert_raises(*expected_exceptions, **keyword_parameters):
            if (exception is not None):
                raise exception
    except AssertionException:
        failed = True
    else:
        failed = False
    
    return failed
