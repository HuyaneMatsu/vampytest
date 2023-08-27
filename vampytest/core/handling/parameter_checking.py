__all__ = ()

from scarletio import CallableAnalyzer

from .parameter_mismatch import ParameterMismatch


def iter_parameters_to_pass(positional_parameters, keyword_parameters):
    """
    Iterates over given parameters.
    
    Parameters
    ----------
    positional_parameters : `None | list<object>`
        Positional parameters to call the test with.
    keyword_parameters : `None | dict<str, object> items
        Keyword parameters to call the test with.
    
    This function is an iterable generator.
    
    Yields
    ------
    is_positional : `bool`
        Whether the parameter is a keyword one.
    positional_parameter / keyword_parameter : `object` / `(str, object)`
        They positional or keyword parameter item described by `is_positional`.
    """
    if (positional_parameters is not None):
        for positional_parameter in positional_parameters:
            yield True, positional_parameter
    
    if (keyword_parameters is not None):
        for keyword_parameter in keyword_parameters.items():
            yield False, keyword_parameter


def exhaust_next_positional_parameter(parameters):
    """
    Exhausts and removes (if applicable) the next positional parameter.
    
    Parameters
    ----------
    parameters : `list<Parameter>`
        Parameters to exhaust from.
    
    Returns
    -------
    success : `bool`
    """
    if not parameters:
        return False
    
    parameter = parameters[0]
    if parameter.is_args():
        return True
    
    if parameter.is_positional():
        del parameters[0]
        return True
    
    return False


def exhaust_keyword_parameter(parameters, name):
    """
    Exhausts and removes (if applicable) the a keyword parameter defined by the given name.
    
    Parameters
    ----------
    parameters : `list<Parameter>`
        Parameters to exhaust from.
    name : `str`
        The parameter's name.
    
    Returns
    -------
    success : `bool`
    """
    for index, parameter in enumerate(parameters):
        if parameter.is_keyword():
            if parameter.name == name:
                del parameters[index]
                return True
            
            continue
        
        if parameter.is_kwargs():
            return True
    
    return False


def collect_unsatisfied_parameters(parameters):
    """
    Collects the unsatisfied parameters from the given parameters list.
    
    Parameters
    ----------
    parameters : `list<Parameter>`
        Parameters to collect from.
    
    Returns
    -------
    unsatisfied_parameters : `None | list<Parameter>`
    """
    unsatisfied_parameters = None
    
    for parameter in parameters:
        if parameter.has_default or parameter.is_args() or parameter.is_kwargs():
            continue
        
        if unsatisfied_parameters is None:
            unsatisfied_parameters = []
        
        unsatisfied_parameters.append(parameter)
    
    return unsatisfied_parameters


def check_parameter_mismatch(test, positional_parameters, keyword_parameters):
    """
    Checks whether there is parameter mismatch between the test and the parameters to pass into it.
    
    Parameters
    ----------
    test : `FunctionType`
        The test to check.
    positional_parameters : `None | list<object`
        Positional parameters to call the test with.
    keyword_parameters : `None | dict<str, object>`
        Keyword parameters to call the test with.
    
    Returns
    -------
    parameter_mismatch : `None`, ``ParameterMismatch``
    """
    analyzer = CallableAnalyzer(test)
    original_parameters = analyzer.parameters
    if original_parameters is None:
        original_parameters = []
    else:
        original_parameters = [*original_parameters]
    
    parameters = original_parameters.copy()
    
    
    extra_positional_parameters = None
    extra_keyword_parameters = None
    
    for is_positional, parameter_value in iter_parameters_to_pass(positional_parameters, keyword_parameters):
        if is_positional:
            if exhaust_next_positional_parameter(parameters):
                continue
            
            if extra_positional_parameters is None:
                extra_positional_parameters = []
            
            extra_positional_parameters.append(parameter_value)
        
        else:
            if exhaust_keyword_parameter(parameters, parameter_value[0]):
                continue
            
            if extra_keyword_parameters is None:
                extra_keyword_parameters = {}
            
            extra_keyword_parameters[parameter_value[0]] = parameter_value[1]
    
    
    unsatisfied_parameters = collect_unsatisfied_parameters(parameters)
    
    if (
        (unsatisfied_parameters is None) and
        (extra_positional_parameters is None) and
        (extra_keyword_parameters is None)
    ):
        return None
    
    return ParameterMismatch(
        original_parameters, 
        positional_parameters,
        keyword_parameters,
        unsatisfied_parameters,
        extra_positional_parameters,
        extra_keyword_parameters,
    )
