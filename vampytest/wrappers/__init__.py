"""
Test wrappers used to enhance our test experience.

Examples
--------
```
import vampytest

def test_equals():
    vampytest.assert_equals(5, 5)


def test_raises():
    with vampytest.raises(TypeError):
        'nice' + 69

def test_contains():
    vampytest.assert_contains(range(7), 5)
```
"""

from .base import *


__all__ = (
    *base.__all__,
)
