__all__ = (
    'assert_', 'assert_contains', 'assert_eq', 'assert_equals', 'assert_false', 'assert_id', 'assert_identical',
    'assert_in', 'assert_instance', 'assert_is', 'assert_is_not', 'assert_ne', 'assert_not', 'assert_not_contains',
    'assert_not_eq', 'assert_not_equals', 'assert_not_id', 'assert_not_identical', 'assert_not_in', 'assert_not_is',
    'assert_raises', 'assert_subtype', 'assert_true'
)


from .assertion_contains import AssertionContains
from .assertion_equals import AssertionEquals
from .assertion_false import AssertionValueEvaluationFalse
from .assertion_identical import AssertionIdentical
from .assertion_instance import AssertionInstance
from .assertion_not_contains import AssertionNotContains
from .assertion_not_equals import AssertionNotEquals
from .assertion_not_identical import AssertionNotIdentical
from .assertion_raising import AssertionRaising
from .assertion_subtype import AssertionSubtype
from .assertion_true import AssertionValueEvaluationTrue


def assert_contains(value_0, value_1, *, reverse = False):
    """
    Asserts whether the second value contains the first.
    
    Parameters
    ----------
    value_0 : `object`
        The first value to assert with.
    
    value_1 : `object`
        The second value to assert with.
    
    reverse : `bool` = `False`, Optional (Keyword only)
        Whether the condition should be reversed.
    
    Raises
    ------
    AssertionException
        The condition failed.
    """
    assertion = AssertionContains(value_0, value_1, reverse = reverse)
    return assertion.invoke()


def assert_equals(value_0, value_1, *, reverse = False):
    """
    Asserts whether the two values are equal.
    
    Parameters
    ----------
    value_0 : `object`
        The first value to assert with.
    
    value_1 : `object`
        The second value to assert with.
    
    reverse : `bool` = `False`, Optional (Keyword only)
        Whether the condition should be reversed.
    
    Raises
    ------
    AssertionException
        The condition failed.
    """
    assertion = AssertionEquals(value_0, value_1, reverse = reverse)
    return assertion.invoke()


def assert_false(value, *, reverse = False):
    """
    Asserts whether the value evaluates to `False`.
    
    Parameters
    ----------
    value : `object`
        The value to assert with.
        First value to assert equality with.
    
    reverse : `bool` = `False`, Optional (Keyword only)
        Whether the condition should be reversed.
    
    Raises
    ------
    AssertionException
        The condition failed.
    """
    assertion = AssertionValueEvaluationFalse(value, reverse = reverse)
    return assertion.invoke()


def assert_identical(value_0, value_1, *, reverse = False):
    """
    Asserts whether the two values are identical.
    
    Parameters
    ----------
    value_0 : `object`
        The first value to assert with.
    
    value_1 : `object`
        The second value to assert with.
    
    reverse : `bool` = `False`, Optional (Keyword only)
        Whether the condition should be reversed.
    
    Raises
    ------
    AssertionException
        The condition failed.
    """
    assertion = AssertionIdentical(value_0, value_1, reverse = reverse)
    return assertion.invoke()


def assert_instance(value, accepted_type, *accepted_types, accept_subtypes = True, reverse = False, nullable = False):
    """
    Asserts whether the two values are identical.
    
    Parameters
    ----------
    value : `object`
        Object to check.
    
    accepted_type : `type`
        The type to check.
    
    *accepted_types : `tuple<type, ...>`
        Additional accepted types.
    
    accept_subtypes : `bool` = `True`, Optional (Keyword only)
        Whether instances of subtypes should be accepted.
    
    reverse : `bool` = `False`, Optional (Keyword only)
        Whether the condition should be reversed.
    
    nullable : `bool` = `False`, Optional (Keyword only)
        Whether `value` is accepted even if given as `None`.
    
    Raises
    ------
    AssertionException
        The condition failed.
    """
    assertion = AssertionInstance(
        value,
        accepted_type,
        *accepted_types,
        accept_subtypes = accept_subtypes,
        reverse = reverse,
        nullable = nullable,
    )
    return assertion.invoke()


def assert_not_contains(value_0, value_1, *, reverse = False):
    """
    Asserts whether the second value not contains the first one.
    
    Parameters
    ----------
    value_0 : `object`
        The first value to assert with.
    
    value_1 : `object`
        The second value to assert with.
    
    reverse : `bool` = `False`, Optional (Keyword only)
        Whether the condition should be reversed.
    
    Raises
    ------
    AssertionException
        The condition failed.
    """
    assertion = AssertionNotContains(value_0, value_1, reverse = reverse)
    return assertion.invoke()


def assert_not_equals(value_0, value_1, *, reverse = False):
    """
    Asserts not equality.
    
    Parameters
    ----------
    value_0 : `object`
        The first value to assert with.
    
    value_1 : `object`
        The second value to assert with.
    
    reverse : `bool` = `False`, Optional (Keyword only)
        Whether the condition should be reversed.
    
    Raises
    ------
    AssertionException
        The condition failed.
    """
    assertion = AssertionNotEquals(value_0, value_1, reverse = reverse)
    return assertion.invoke()


def assert_not_identical(value_0, value_1, *, reverse = False):
    """
    Asserts whether two objects are not identical.
    
    Parameters
    ----------
    value_0 : `object`
        The first value to assert with.
    
    value_1 : `object`
        The second value to assert with.
    
    reverse : `bool` = `False`, Optional (Keyword only)
        Whether the condition should be reversed.
    
    Raises
    ------
    AssertionException
        The condition failed.
    """
    assertion = AssertionNotIdentical(value_0, value_1, reverse = reverse)
    return assertion.invoke()


def assert_raises(expected_exception, *expected_exceptions, accept_subtypes = True, where = None):
    """
    Context manager, which checks for exception raise.
    
    Parameters
    ----------
    expected_exception : `type<BaseException> | instance<BaseException>˙
        The expected exception to be raised.
    
    *expected_exceptions : ˙tuple<type<BaseException> | instance<BaseException>>˙
        Additional expected exceptions.
    
    accept_subtypes : `bool` = `True`, Optional (Keyword only)
        Whether subclasses are accepted as well.
    
    where : `None | (BaseException) -> bool` = `None`, Optional (Keyword only)
        Additional check to check the raised exception.
    
    Returns
    -------
    assertion : ``AssertionRaising``
    """
    return AssertionRaising(
        expected_exception,
        *expected_exceptions,
        accept_subtypes = accept_subtypes,
        where = where,
    )


def assert_subtype(value, accepted_type, *accepted_types, reverse = False, nullable = False):
    """
    Asserts whether the first object is instance of the second one.
    
    Parameters
    ----------
    value : `object`
        Object to check.
    
    accepted_type : `type`
        Type to check.
    
    *accepted_types : `tuple<type>`
        Additional types to check.
    
    reverse : `bool` = `False`, Optional (Keyword only)
        Whether the condition should be reversed.
    
    nullable : `bool` = `False`, Optional (Keyword only)
        Whether `value` is accepted even if given as `None`.
    
    Raises
    ------
    AssertionException
        The condition failed.
    """
    assertion = AssertionSubtype(
        value,
        accepted_type,
        *accepted_types,
        reverse = reverse,
        nullable = nullable,
    )
    return assertion.invoke()


def assert_true(value, *, reverse = False):
    """
    Asserts whether the value evaluates to `True`.
    
    Parameters
    ----------
    value : `object`
        The value to assert with.
    
    reverse : `bool` = `False`, Optional (Keyword only)
        Whether the condition should be reversed.
    
    Raises
    ------
    AssertionException
        The condition failed.
    """
    assertion = AssertionValueEvaluationTrue(value, reverse = reverse)
    return assertion.invoke()


assert_ = assert_true
assert_eq = assert_equals
assert_id = assert_identical
assert_in = assert_contains
assert_is = assert_identical
assert_is_not = assert_not_identical
assert_ne = assert_not_equals
assert_not = assert_false
assert_not_eq = assert_not_equals
assert_not_id = assert_not_identical
assert_not_in = assert_not_contains
assert_not_is = assert_not_identical
