from vampytest import revert, raising

from ..aliases import assert_raises


def test_assert_raises():
    """
    Tests whether `raises` context-assertion succeeds.
    """
    with assert_raises(KeyError):
        raise KeyError


@revert()
def test_assert_raises_reverted():
    """
    Tests whether `raises` context-assertion fails.
    """
    with assert_raises(KeyError):
        raise ValueError


def test_assert_raises_with_subtype():
    """
    Tests whether `raises` context-assertion succeeds on subtype.
    """
    with assert_raises(LookupError):
        raise KeyError


@revert()
def test_assert_raises_with_subtype_reverted():
    """
    Tests whether `raises` context-assertion fails on 3rd type.
    """
    with assert_raises(LookupError):
        raise ValueError


def test_assert_raises_without_subtype():
    """
    Tests whether `raises` context-assertion succeeds on the type without allowing subtypes.
    """
    with assert_raises(LookupError, accept_subtypes = False):
        raise LookupError


@revert()
def test_assert_raises_without_subtype_reverted():
    """
    Tests whether `raises` context-assertion fails on subtype without allowing subtypes.
    """
    with assert_raises(LookupError, accept_subtypes = False):
        raise KeyError


@raising(ValueError)
def test_assert_raises_with_empty_parameter():
    """
    Tests whether `raises` context-assertion raises when empty parameter is given.
    """
    with assert_raises((),):
        pass


def test_assert_raises_matching_instance():
    """
    Tests whether `raises` context-assertion succeeds on matching instances.
    """
    with assert_raises(ValueError(1)):
        raise ValueError(1)


@raising(ValueError)
def test_assert_raises_mismatching_instance():
    """
    Tests whether `raises` context-assertion fails on mismatching instances.
    """
    with assert_raises(ValueError(1)):
        raise ValueError(2)


def test_assert_raises_matching_where():
    """
    Tests whether `raises` context-assertion fails on matching where.
    """
    with assert_raises(ValueError, where = lambda err: err.args == (1,)):
        raise ValueError(1)


@raising(ValueError)
def test_assert_raises_mismatching_where():
    """
    Tests whether `raises` context-assertion fails on mismatching where.
    """
    with assert_raises(ValueError, where = lambda err: err.args == (1,)):
        raise ValueError(2)
