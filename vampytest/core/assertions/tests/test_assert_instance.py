from vampytest import revert, raising

from ..aliases import assert_instance


def test_assert_instance():
    """
    Tests whether `instance` assertion succeeds.
    """
    assert_instance(1, int)


@revert()
def test_assert_instance_reverted():
    """
    Tests whether `instance` assertion fails.
    """
    assert_instance(1, str)


@raising(TypeError)
def test_assert_instance_incorrect_type():
    """
    Tests whether `instance` assertion raises when type parameter is incorrect.
    """
    assert_instance(1, 1)


def test_assert_instance_subtype():
    """
    Tests whether `instance` assertion succeeds.
    """
    assert_instance(True, int)


@revert()
def test_assert_instance_subtype_reverted():
    """
    Tests whether `instance` assertion fails when subtypes are not allowed.
    """
    assert_instance(True, int, accept_subtypes = False)


def test_assert_instance_nullable__0():
    """
    Tests whether `instance` assertion succeeds when nullable.
    """
    assert_instance(1, int, nullable = True)


def test_assert_instance_nullable__1():
    """
    Tests whether `instance` assertion succeeds when nullable + giving null.
    """
    assert_instance(None, int, nullable = True)


def test_assert_instance_multiple_types__0():
    """
    Tests whether `instance` assertion succeeds when multiple types are given.
    """
    assert_instance(1, str, int)


def test_assert_instance_multiple_types__1():
    """
    Tests whether `instance` assertion succeeds when multiple types are given as a tuple.
    """
    assert_instance(1, (str, int))


@raising(ValueError)
def test_assert_instance_with_empty_parameter():
    """
    Tests whether `instance` assertion raises when empty type parameter is given.
    """
    assert_instance(int, ())
