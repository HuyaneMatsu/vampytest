__all__ = ()

from scarletio import HIGHLIGHT_TOKEN_TYPES

from ...assertions import (
    AssertionContains, AssertionEquals, AssertionIdentical, AssertionInstance, AssertionNotContains, AssertionNotEquals,
    AssertionNotIdentical, AssertionRaising, AssertionSubtype, AssertionValueEvaluationFalse,
    AssertionValueEvaluationTrue
)

from .parameter_rendering import (
    _produce_variable_assignation, _produce_bool_non_default, _produce_parameter_representation,
    _produce_types_parameter_representation,
)


def _produce_operation_contains():
    """
    Produces a contains operator.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    # `in`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_WORD, 'in'


def _produce_operation_equals():
    """
    Produces an equality operator.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    # `==`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR, '=='


def _produce_operation_identical():
    """
    Produces an identity operator.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    # `is`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_WORD, 'is'


def _produce_nullable():
    """
    Produces a nullability operation. Invoked by other producers.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    # `value is None or `
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'value'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_WORD, 'is'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_BUILTIN_CONSTANT, 'None'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_WORD, 'or'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '


def _produce_operation_instance(nullable, accept_subtypes):
    """
    Produces an instance check operation.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    nullable : `bool`
        Whether the checked value is nullable.
    
    accept_subtypes : `bool`
        Whether sub-types are also accepted.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    if nullable:
        yield from _produce_nullable()
    
    if accept_subtypes:
        # `isinstance(value, expected_types)`
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE, 'isinstance'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, '('
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'value'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ','
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'expected_types'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ')'
    
    else:
        # `type(value) in expected_types`
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE, 'type'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, '('
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'value'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ')'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_WORD, 'in'
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
        yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'expected_types'


def _produce_operation_evaluation_false():
    """
    Produces an evaluation to false operation.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    # `not bool(value)`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_WORD, 'not'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE, 'bool'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, '('
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'value'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ')'


def _produce_operation_not_contains():
    """
    Produces a not contains operator.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    # `not in`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_WORD, 'not'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_WORD, 'in'


def _produce_operation_not_equals():
    """
    Produces a not equality operator.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    # `!=`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR, '!='


def _produce_operation_not_identical():
    """
    Produces a not identity operator.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    # `is not`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_WORD, 'is'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_WORD, 'not'


def _produce_operation_try_expect():
    """
    Produces a try-except clause representation.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    # `try except`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_KEYWORD, 'try'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_KEYWORD, 'except'


def _produce_operation_subtype(nullable):
    """
    Produces an subtype check operation.
    
    This function is an iterable generator.
    
    Parameters
    ----------
    nullable : `bool`
        Whether the checked value is nullable.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    if nullable:
        # `value is None or `
        yield from _produce_nullable()
    
    # `isinstance(value, type)`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE, 'isinstance'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, '('
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'value'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ','
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE, 'type'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ')'
    
    # ` and `
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_WORD, 'and'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    
    # `issubclass(value, expected_types)`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE, 'issubclass'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, '('
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'value'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ','
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'expected_types'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ')'


def _produce_operation_evaluation_true():
    """
    Produces an evaluation to true operation.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    # `bool(value)`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_BUILTIN_VARIABLE, 'bool'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, '('
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'value'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_PUNCTUATION, ')'


def _produce_operation_unknown():
    """
    Produces an unknown operation.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    # `unknown`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_NON_SPACE_UNIDENTIFIED, 'unknown'


def _produce_one_sided_operation(operation_producer):
    """
    Shortcut for rendering a full one sided operation.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    operation_producer : `iterable<(int, str)>`
        Operation producer.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_variable_assignation('operation')
    yield from operation_producer
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'


def _produce_two_sided_operation(operation_producer):
    """
    Shortcut for rendering a two sided operation.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    operation_producer : `iterable<(int, str)>`
        Operation producer.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_variable_assignation('operation')
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'value_0'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield from operation_producer
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' '
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'value_1'
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_LINE_BREAK, '\n'


def _produce_one_sided_assertion(assertion, operation_producer):
    """
    Shortcut for rendering a one sided assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionConditionalBase1Value``
        The assertion to render.
    
    operation_producer : `iterable<(int, str)>`
        Operation producer.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_one_sided_operation(operation_producer)
    yield from _produce_parameter_representation('value', assertion.value_0)
    yield from _produce_bool_non_default('reverse', assertion.reverse, False)


def _produce_two_sided_assertion(assertion, operation_producer):
    """
    Shortcut for rendering a two sided assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionConditionalBase2Value``
        The assertion to render.
    
    operation_producer : `iterable<(int, str)>`
        Operation producer.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_two_sided_operation(operation_producer)
    yield from _produce_parameter_representation('value_0', assertion.value_0)
    yield from _produce_parameter_representation('value_1', assertion.value_1)
    yield from _produce_bool_non_default('reverse', assertion.reverse, False)


def _produce_assertion_contains(assertion):
    """
    Renders a contains assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionContains``
        The assertion to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_two_sided_assertion(assertion, _produce_operation_contains())


def _produce_assertion_equals(assertion):
    """
    Renders an equals assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionEquals``
        The assertion to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_two_sided_assertion(assertion, _produce_operation_equals())


def _produce_assertion_evaluation_false(assertion):
    """
    Renders a false evaluation assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionValueEvaluationFalse``
        The assertion to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    return _produce_one_sided_assertion(assertion, _produce_operation_evaluation_false())


def _produce_assertion_identical(assertion):
    """
    Renders an identical assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionIdentical``
        The assertion to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_two_sided_assertion(assertion, _produce_operation_identical())


def _produce_assertion_instance(assertion):
    """
    Renders an instance check assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionInstance``
        The assertion to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_one_sided_operation(
        _produce_operation_instance(assertion.nullable, assertion.accept_subtypes)
    )
    yield from _produce_parameter_representation('value', assertion.value_0)
    yield from _produce_types_parameter_representation('expected_types', assertion.value_1)
    yield from _produce_bool_non_default('nullable', assertion.nullable, False)
    yield from _produce_bool_non_default('accept_subtypes', assertion.accept_subtypes, True)
    yield from _produce_bool_non_default('reverse', assertion.reverse, False)


def _produce_assertion_not_contains(assertion):
    """
    Renders a not contains assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionNotContains``
        The assertion to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_two_sided_assertion(assertion, _produce_operation_not_contains())


def _produce_assertion_not_equals(assertion):
    """
    Renders a not equals assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionNotEquals``
        The assertion to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_two_sided_assertion(assertion, _produce_operation_not_equals())



def _produce_assertion_not_identical(assertion):
    """
    Renders a not identical assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionNotIdentical``
        The assertion to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_two_sided_assertion(assertion, _produce_operation_not_identical())


def _produce_assertion_raising(assertion):
    """
    Renders a raising assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionRaising``
        The assertion to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_one_sided_operation(_produce_operation_try_expect())
    yield from _produce_types_parameter_representation('expected_exceptions', assertion.expected_exceptions)
    yield from _produce_bool_non_default('accept_subtypes', assertion.accept_subtypes, True)
    
    where = assertion.where
    if (where is not None):
        yield from _produce_parameter_representation('where', where)


def _produce_assertion_subtype(assertion):
    """
    Renders a sub-type assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionSubtype``
        The assertion to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_one_sided_operation(_produce_operation_subtype(assertion.nullable))
    yield from _produce_parameter_representation('value', assertion.value_0)
    yield from _produce_types_parameter_representation('expected_types', assertion.value_1)
    yield from _produce_bool_non_default('nullable', assertion.nullable, False)
    yield from _produce_bool_non_default('reverse', assertion.reverse, False)


def _produce_assertion_evaluation_true(assertion):
    """
    Renders a truth evaluation assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionValueEvaluationTrue``
        The assertion to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_one_sided_assertion(assertion, _produce_operation_evaluation_true())


def _produce_assertion_unknown(assertion):
    """
    Renders an unknown assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionBase``
        The assertion to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from _produce_one_sided_operation(_produce_operation_unknown())
    yield from _produce_parameter_representation('type', type(assertion))


ASSERTION_RENDERERS = {
    AssertionContains : _produce_assertion_contains,
    AssertionEquals : _produce_assertion_equals,
    AssertionValueEvaluationFalse : _produce_assertion_evaluation_false,
    AssertionIdentical : _produce_assertion_identical,
    AssertionInstance : _produce_assertion_instance,
    AssertionNotContains : _produce_assertion_not_contains,
    AssertionNotEquals : _produce_assertion_not_equals,
    AssertionNotIdentical : _produce_assertion_not_identical,
    AssertionRaising : _produce_assertion_raising,
    AssertionSubtype : _produce_assertion_subtype,
    AssertionValueEvaluationTrue : _produce_assertion_evaluation_true,
}


def produce_assertion(assertion):
    """
    Renders the given assertion.
    
    This functions is an iterable generator.
    
    Parameters
    ----------
    assertion : ``AssertionBase``
        The assertion to render.
    
    Yields
    -------
    token_type_and_part : `(int, str)`
    """
    yield from ASSERTION_RENDERERS.get(type(assertion), _produce_assertion_unknown)(assertion)
