import vampytest

THRESHOLD = 10


# section 0

@vampytest._(vampytest.named('over threshold').call_with(THRESHOLD + 1).returning(True))
@vampytest._(vampytest.named('at threshold').call_with(THRESHOLD).returning(True))
@vampytest._(vampytest.named('under threshold').call_with(THRESHOLD - 1).returning(False))
def test_over_or_equal_to_threshold__section_0(value):
    return value >= THRESHOLD


# section 1

def _iter_options():
    yield (
        'over threshold',
        THRESHOLD + 1,
        True,
    )
    
    yield (
        'at threshold',
        THRESHOLD,
        True,
    )
    
    yield (
        'under threshold',
        THRESHOLD - 1,
        False,
    )


@vampytest._(vampytest.call_from(_iter_options()).named_first().returning_last())
def test_over_or_equal_to_threshold__section_1(value):
    return value >= THRESHOLD
