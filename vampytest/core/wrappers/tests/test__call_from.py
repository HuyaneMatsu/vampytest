from vampytest import _

from ..aliases import call_from


@call_from([1, 2])
def test__call_from__call_single(value_0):
    """
    Tests whether `call_from` works when calling a single parameter.
    
    Parameters
    ----------
    value_0 : `int`
    """


@call_from([(1, ), (2, )])
def test__call_from__call_single_nested(value_0):
    """
    Tests whether `call_from` works when calling a single nested parameter.
    
    Parameters
    ----------
    value_0 : `int`
    """

@call_from([(1, 2), (2, 3)])
def test__call_from__call_multiple_nested(value_0, value_1):
    """
    Tests whether `call_from` works when calling with nested parameters.
    
    Parameters
    ----------
    value_0 : `int`
    value_1 : `int`
    """

@_(call_from([1, 2]).raising(ValueError))
def test__call_from__call_raise_given(value_0):
    """
    Tests whether `call_from` excepts given exception.
    
    Parameters
    ----------
    value_0 : `int`
    """
    raise ValueError


@_(call_from([ValueError, ValueError]).raising_last())
def test__call_from__raise_last_single():
    """
    Tests whether `call_from` excepts last parameters as exception.
    """
    raise ValueError


@_(call_from([(1, ValueError), (2, ValueError)]).raising_last())
def test__call_from__raise_last_multiple(value_0):
    """
    Tests whether `call_from` excepts last parameters as exception.
    
    Case: With parameters.
    
    Parameters
    ----------
    value_0 : `int`
    """
    raise ValueError


@_(call_from([1, 2]).returning(1))
def test__call_from__return_given(value_0):
    """
    Tests whether `call_from` excepts given return.
    
    Parameters
    ----------
    value_0 : `int`
    """
    return 1


@_(call_from([1, 1]).returning_last())
def test__call_from__return_last_single():
    """
    Tests whether `call_from` excepts last parameter as exception.
    """
    return 1


@_(call_from([(1, 2), (2, 3)]).returning_last())
def test__call_from__return_last_multiple(value_0):
    """
    Tests whether `call_from` excepts last parameter as exception.
    
    Case: With parameters.
    
    Parameters
    ----------
    value_0 : `int`
    """
    return value_0 + 1


@_(call_from([1, 2]).returning_transformed(lambda x: x + 1))
def test__call_from__return_transformed(value_0):
    """
    Tests whether `call_from` excepts the return to be transformed.
    
    Parameters
    ----------
    value_0 : `int`
    """
    return value_0 + 1


@_(call_from([1, 2]).returning_itself())
def test__call_from__return_itself(value_0):
    """
    Tests whether `call_from` excepts the return to same as the parameter.
    
    Parameters
    ----------
    value_0 : `int`
    """
    return value_0
