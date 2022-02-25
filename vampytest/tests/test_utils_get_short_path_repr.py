from ..utils import get_short_path_repr

from vampytest import call_with, mark_as_test

a_100 = 'a'*100
a_30 = 'a'*30
a_10 = 'a'*10

(
mark_as_test(get_short_path_repr)
@call_with('').returning_itself()
@call_with('no/game/no/life').returning_itself()
@call_with('/no/game/no/life').returning_itself()
@call_with('/this/game/no/game/no/life').returning('../no/game/no/life')
@call_with(a_100).returning_itself()
@call_with('/this/game//no/game/no/life').returning('..//no/game/no/life')
@call_with(f'/{a_100}').returning_itself()
@call_with(f'{a_10}/{a_100}').returning(f'./{a_100}')
@call_with(f'{a_10}/{a_10}').returning(f'./{a_100}')
@call_with(f'{a_30}/{a_30}/{a_30}').returning(f'./{a_30}/{a_30}')
@call_with(f'{a_30}//{a_30}/{a_30}').returning(f'.//{a_30}/{a_30}')
)
