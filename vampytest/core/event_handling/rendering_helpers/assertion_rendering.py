__all__ = ()

from scarletio import HIGHLIGHT_TOKEN_TYPES, add_highlighted_part_into, add_highlighted_parts_into

from ...assertions import (
    AssertionContains, AssertionEquals, AssertionIdentical, AssertionInstance, AssertionNotContains, AssertionNotEquals,
    AssertionNotIdentical, AssertionRaising, AssertionSubtype, AssertionValueEvaluationFalse,
    AssertionValueEvaluationTrue
)

from .parameter_rendering import (
    _produce_variable_assignation, _render_bool_non_default_into, _render_parameter_representation_into,
    _render_types_parameter_representation_into,
)


def _produce_operation_contains():
    """
    Produces a contains operator.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type, part : `(int, str)`
    """
    # `in`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_WORD, 'in'


def _produce_operation_equals():
    """
    Produces an equality operator.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type, part : `(int, str)`
    """
    # `==`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR, '=='


def _produce_operation_identical():
    """
    Produces an identity operator.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type, part : `(int, str)`
    """
    # `is`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR_WORD, 'is'


def _produce_nullable():
    """
    Produces a nullability operation. Invoked by other producers.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type, part : `(int, str)`
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
    token_type, part : `(int, str)`
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
    token_type, part : `(int, str)`
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
    token_type, part : `(int, str)`
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
    token_type, part : `(int, str)`
    """
    # `!=`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPECIAL_OPERATOR, '!='


def _produce_operation_not_identical():
    """
    Produces a not identity operator.
    
    This function is an iterable generator.
    
    Yields
    -------
    token_type, part : `(int, str)`
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
    token_type, part : `(int, str)`
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
    token_type, part : `(int, str)`
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
    token_type, part : `(int, str)`
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
    token_type, part : `(int, str)`
    """
    # `unknown`
    yield HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_NON_SPACE_UNIDENTIFIED, 'unknown'


def _render_one_sided_operation_into(operation_producer, highlighter, into):
    """
    Shortcut for rendering a full one sided operation.
    
    Parameters
    ----------
    operation_producer : `iterable<(int, str)>`
        Operation producer.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    into = add_highlighted_parts_into(_produce_variable_assignation('operation'), highlighter, into)
    into = add_highlighted_parts_into(operation_producer, highlighter, into)
    into.append('\n')
    return into


def _render_two_sided_operation_into(operation_producer, highlighter, into):
    """
    Shortcut for rendering a two sided operation.
    
    Parameters
    ----------
    operation_producer : `iterable<(int, str)>`
        Operation producer.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    into = add_highlighted_parts_into(_produce_variable_assignation('operation'), highlighter, into)
    into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'value_0', highlighter, into)
    into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' ', highlighter, into)
    into = add_highlighted_parts_into(operation_producer, highlighter, into)
    into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_SPACE, ' ', highlighter, into)
    into = add_highlighted_part_into(HIGHLIGHT_TOKEN_TYPES.TOKEN_TYPE_IDENTIFIER_VARIABLE, 'value_1', highlighter, into)
    into.append('\n')
    return into


def _render_one_sided_assertion_into(assertion, operation_producer, highlighter, into):
    """
    Shortcut for rendering a one sided assertion.
    
    Parameters
    ----------
    assertion : ``AssertionConditionalBase1Value``
        The assertion to render.
    
    operation_producer : `iterable<(int, str)>`
        Operation producer.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    into = _render_one_sided_operation_into(operation_producer, highlighter, into)
    into = _render_parameter_representation_into('value', assertion.value_0, highlighter, into)
    into = _render_bool_non_default_into('reverse', assertion.reverse, False, highlighter, into)
    return into


def _render_two_sided_assertion_into(assertion, operation_producer, highlighter, into):
    """
    Shortcut for rendering a two sided assertion.
    
    Parameters
    ----------
    assertion : ``AssertionConditionalBase2Value``
        The assertion to render.
    
    operation_producer : `iterable<(int, str)>`
        Operation producer.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    into = _render_two_sided_operation_into(operation_producer, highlighter, into)
    into = _render_parameter_representation_into('value_0', assertion.value_0, highlighter, into)
    into = _render_parameter_representation_into('value_1', assertion.value_1, highlighter, into)
    into = _render_bool_non_default_into('reverse', assertion.reverse, False, highlighter, into)
    return into

def _render_assertion_contains_into(assertion, highlighter, into):
    """
    Renders a contains assertion.
    
    Parameters
    ----------
    assertion : ``AssertionContains``
        The assertion to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    return _render_two_sided_assertion_into(assertion, _produce_operation_contains(), highlighter, into)


def _render_assertion_equals_into(assertion, highlighter, into):
    """
    Renders an equals assertion.
    
    Parameters
    ----------
    assertion : ``AssertionEquals``
        The assertion to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    return _render_two_sided_assertion_into(assertion, _produce_operation_equals(), highlighter, into)


def _render_assertion_evaluation_false_into(assertion, highlighter, into):
    """
    Renders a false evaluation assertion.
    
    Parameters
    ----------
    assertion : ``AssertionValueEvaluationFalse``
        The assertion to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    return _render_one_sided_assertion_into(assertion, _produce_operation_evaluation_false(), highlighter, into)


def _render_assertion_identical_into(assertion, highlighter, into):
    """
    Renders an identical assertion.
    
    Parameters
    ----------
    assertion : ``AssertionIdentical``
        The assertion to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    return _render_two_sided_assertion_into(assertion, _produce_operation_identical(), highlighter, into)


def _render_assertion_instance_into(assertion, highlighter, into):
    """
    Renders an instance check assertion.
    
    Parameters
    ----------
    assertion : ``AssertionInstance``
        The assertion to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    into = _render_one_sided_operation_into(
        _produce_operation_instance(assertion.nullable, assertion.accept_subtypes), highlighter, into
    )
    into = _render_parameter_representation_into('value', assertion.value_0, highlighter, into)
    into = _render_types_parameter_representation_into('expected_types', assertion.value_1, highlighter, into)
    into = _render_bool_non_default_into('nullable', assertion.nullable, False, highlighter, into)
    into = _render_bool_non_default_into('accept_subtypes', assertion.accept_subtypes, True, highlighter, into)
    into = _render_bool_non_default_into('reverse', assertion.reverse, False, highlighter, into)
    return into


def _render_assertion_not_contains_into(assertion, highlighter, into):
    """
    Renders a not contains assertion.
    
    Parameters
    ----------
    assertion : ``AssertionNotContains``
        The assertion to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    return _render_two_sided_assertion_into(assertion, _produce_operation_not_contains(), highlighter, into)


def _render_assertion_not_equals_into(assertion, highlighter, into):
    """
    Renders a not equals assertion.
    
    Parameters
    ----------
    assertion : ``AssertionNotEquals``
        The assertion to render.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    Returns
    -------
    into : `list<str>`
    """
    return _render_two_sided_assertion_into(assertion, _produce_operation_not_equals(), highlighter, into)



def _render_assertion_not_identical_into(assertion, highlighter, into):
    """
    Renders a not identical assertion.
    
    Parameters
    ----------
    assertion : ``AssertionNotIdentical``
        The assertion to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    return _render_two_sided_assertion_into(assertion, _produce_operation_not_identical(), highlighter, into)


def _render_assertion_raising_into(assertion, highlighter, into):
    """
    Renders a raising assertion.
    
    Parameters
    ----------
    assertion : ``AssertionRaising``
        The assertion to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    into = _render_one_sided_operation_into(_produce_operation_try_expect(), highlighter, into)
    into = _render_types_parameter_representation_into(
        'expected_exceptions', assertion.expected_exceptions, highlighter, into
    )
    into = _render_bool_non_default_into(
        'accept_subtypes', assertion.accept_subtypes, True, highlighter, into
    )
    
    where = assertion.where
    if (where is not None):
        into = _render_parameter_representation_into('where', where, highlighter, into)
    
    return into


def _render_assertion_subtype_into(assertion, highlighter, into):
    """
    Renders a sub-type assertion.
    
    Parameters
    ----------
    assertion : ``AssertionSubtype``
        The assertion to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    into = _render_one_sided_operation_into(_produce_operation_subtype(assertion.nullable), highlighter, into)
    into = _render_parameter_representation_into('value', assertion.value_0, highlighter, into)
    into = _render_types_parameter_representation_into('expected_types', assertion.value_1, highlighter, into)
    into = _render_bool_non_default_into('nullable', assertion.nullable, False, highlighter, into)
    into = _render_bool_non_default_into('reverse', assertion.reverse, False, highlighter, into)
    return into


def _render_assertion_evaluation_true_into(assertion, highlighter, into):
    """
    Renders a truth evaluation assertion.
    
    Parameters
    ----------
    assertion : ``AssertionValueEvaluationTrue``
        The assertion to render.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    Returns
    -------
    into : `list<str>`
    """
    return _render_one_sided_assertion_into(assertion, _produce_operation_evaluation_true(), highlighter, into)


def _render_assertion_unknown(assertion, highlighter, into):
    """
    Renders an unknown assertion.
    
    Parameters
    ----------
    assertion : ``AssertionBase``
        The assertion to render.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    Returns
    -------
    into : `list<str>`
    """
    into = _render_one_sided_operation_into(_produce_operation_unknown(), highlighter, into)
    into = _render_parameter_representation_into('type', type(assertion), highlighter, into)
    return into


ASSERTION_RENDERERS = {
    AssertionContains : _render_assertion_contains_into,
    AssertionEquals : _render_assertion_equals_into,
    AssertionValueEvaluationFalse : _render_assertion_evaluation_false_into,
    AssertionIdentical : _render_assertion_identical_into,
    AssertionInstance : _render_assertion_instance_into,
    AssertionNotContains : _render_assertion_not_contains_into,
    AssertionNotEquals : _render_assertion_not_equals_into,
    AssertionNotIdentical : _render_assertion_not_identical_into,
    AssertionRaising : _render_assertion_raising_into,
    AssertionSubtype : _render_assertion_subtype_into,
    AssertionValueEvaluationTrue : _render_assertion_evaluation_true_into,
}


def render_assertion_into(assertion, highlighter, into):
    """
    Renders the given assertion.
    
    Parameters
    ----------
    assertion : ``AssertionBase``
        The assertion to render.
    
    into : `list<str>`
        A list to extend with the rendered strings.
    
    highlighter : `None | HighlightFormatterContext`
        Highlighter to use.
    
    Returns
    -------
    into : `list<str>`
    """
    return ASSERTION_RENDERERS.get(type(assertion), _render_assertion_unknown)(assertion, highlighter, into)
