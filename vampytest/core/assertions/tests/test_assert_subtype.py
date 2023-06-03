from vampytest import reverse, raising

from ..aliases import assert_subtype


def test_assert_subtype():
    """
    Tests whether `subtype` assertion succeeds.
    """
    assert_subtype(bool, int)


@reverse()
def test_assert_subtype_reversed():
    """
    Tests whether `subtype` assertion fails.
    """
    assert_subtype(bool, str)


@raising(TypeError)
def test_assert_subtype_incorrect_type():
    """
    Tests whether `subtype` assertion raises when type parameter is incorrect.
    """
    assert_subtype(bool, 1)


@reverse()
def test_assert_subtype_incorrect_checked():
    """
    Tests whether `subtype` assertion fails when the checked value's type is incorrect.
    """
    assert_subtype(1, int)


def test_assert_subtype_nullable__0():
    """
    Tests whether `subtype` assertion succeeds when nullable.
    """
    assert_subtype(bool, int, nullable = True)


def test_assert_subtype_nullable__1():
    """
    Tests whether `subtype` assertion succeeds when nullable + giving null.
    """
    assert_subtype(None, int, nullable = True)


def test_assert_subtype_multiple_types__0():
    """
    Tests whether `subtype` assertion succeeds when multiple types are given.
    """
    assert_subtype(int, str, int)


def test_assert_subtype_multiple_types__1():
    """
    Tests whether `subtype` assertion succeeds when multiple types are given as a tuple.
    """
    assert_subtype(int, (str, int))


@raising(ValueError)
def test_assert_subtype_with_empty_parameter():
    """
    Tests whether `subtype` assertion raises when empty type parameter is given.
    """
    assert_subtype(int, ())
