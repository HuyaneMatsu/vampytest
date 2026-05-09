from ..path_repr import get_short_path_repr

from vampytest import _, call_with

a_100 = 'a' * 100
a_30 = 'a' * 30
a_10 = 'a' * 10


@_(call_with('').returning_itself())
@_(call_with('no/game/no/life').returning_itself())
@_(call_with('/no/game/no/life').returning_itself())
@_(call_with('/this/game/no/game/no/life').returning('../no/game/no/life'))
@_(call_with(a_100).returning_itself())
@_(call_with('/this/game//no/game/no/life').returning('..//no/game/no/life'))
@_(call_with(f'/{a_100}').returning_itself())
@_(call_with(f'{a_10}/{a_100}').returning(f'./{a_100}'))
@_(call_with(f'{a_10}/{a_100}').returning(f'./{a_100}'))
@_(call_with(f'{a_30}/{a_30}/{a_30}').returning(f'./{a_30}/{a_30}'))
@_(call_with(f'{a_30}//{a_30}/{a_30}').returning(f'.//{a_30}/{a_30}'))
def test_get_short_path_repr(input_value):
    return get_short_path_repr(input_value)
