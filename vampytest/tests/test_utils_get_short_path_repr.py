from ..utils import get_short_path_repr

from vampytest import with_parameters, mark_as_test

a_100 = 'a'*100
a_30 = 'a'*30
a_10 = 'a'*10

(
mark_as_test(get_short_path_repr)
@with_parameters('').returning_itself()
@with_parameters('no/game/no/life').returning_itself()
@with_parameters('/no/game/no/life').returning_itself()
@with_parameters('/this/game/no/game/no/life').returning('../no/game/no/life')
@with_parameters(a_100).returning_itself()
@with_parameters('/this/game//no/game/no/life').returning('..//no/game/no/life')
@with_parameters(f'/{a_100}').returning_itself()
@with_parameters(f'{a_10}/{a_100}').returning(f'./{a_100}')
@with_parameters(f'{a_10}/{a_10}').returning(f'./{a_100}')
@with_parameters(f'{a_30}/{a_30}/{a_30}').returning(f'./{a_30}/{a_30}')
@with_parameters(f'{a_30}//{a_30}/{a_30}').returning(f'.//{a_30}/{a_30}')
)
