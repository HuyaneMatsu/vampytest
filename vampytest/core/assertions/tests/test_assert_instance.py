from .. import assert_instance

from vampytest import revert, raising


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
    assert_instance(True, int, accept_subtypes=False)


def test_assert_instance_nullable_0():
    """
    Tests whether `instance` assertion succeeds when nullable.
    """
    assert_instance(1, int, nullable=True)


def test_assert_instance_nullable_1():
    """
    Tests whether `instance` assertion succeeds when nullable + giving null.
    """
    assert_instance(None, int, nullable=True)
