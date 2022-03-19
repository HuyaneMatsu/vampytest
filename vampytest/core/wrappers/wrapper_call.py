__all__ = ('WrapperCall',)

import reprlib

from ..helpers import hash_dict, hash_set, hash_tuple, try_hash_method, un_nest_exception_types
from ..test_result import TestResult

from .wrapper_conflict import WrapperConflict
from .wrapper_base import WrapperBase

from scarletio import copy_docs


class WrapperCall(WrapperBase):
    """
    Combined wrapper supporting `call_with`, `returning` and `raising`.
    
    Attributes
    ----------
    wrapped : `Any`
        The wrapped test.
    raising_exceptions_exact_type : `bool`
        Whether exception subclasses are accepted as well if ``.is_raising``.
    raising_exceptions : `None`, `set` of ``BaseException``
        The raising_exceptions expected to be raised if ``.is_raising``.
    is_raising : `bool`
        Whether raised raising_exceptions of the test should be checked.
    is_returning : `bool`
        Whether returned value of the test should be checked.
    is_call_with : `bool`
        Whether the test should be called with specific parameters.
    calling_keyword_parameters : `None`, `dict` of (`str`, `Any`) items
        Keyword parameters to call the test with if ``.is_call_with``.
    calling_positional_parameters : `None`, `tuple` of `Any`
        Positional parameter to call the test with if ``.is_call_with``.
    returning_value : `None`, `Any`
        The expected returned value of the test if ``.is_returning``.
    """
    __slots__ = (
        'calling_keyword_parameters', 'calling_positional_parameters', 'is_call_with', 'is_raising', 'is_returning',
        'raising_exceptions', 'raising_exceptions_exact_type', 'returning_value'
    )
    
    def __new__(cls, wrapped=None, *, raising=None, returning=None, call_with=None):
        """
        Creates a new combined test wrapper.
        
        Parameters
        ----------
        wrapped : `None`, `Any` = `None`, Optional
            The wrapped test if any.
        raising : `None`, `tuple` (`set` of ``BaseException``, `bool`) = `None`, Optional (Keyword only)
            Whether the test is raising.
        returning : `None`, `tuple` (`Any`) = `None`, Optional (Keyword only)
            Whether the test is returning.
        call_with : `None`, `tuple` (`tuple` of `Any`, `dict` of (`str`, `Any`) items) = `None`
                , Optional (Keyword only)
            Whether the test should be called with parameters.
        """
        if raising is None:
            is_raising = False
            raising_exceptions = None
            raising_exceptions_exact_type = None
        
        else:
            is_raising = True
            raising_exceptions, raising_exceptions_exact_type = raising
        
        
        if returning is None:
            is_returning = False
            returning_value = None
        
        else:
            is_returning = True
            returning_value = returning[0]
        
        
        if call_with is None:
            is_call_with = False
            calling_keyword_parameters = None
            calling_positional_parameters = None
        
        else:
            is_call_with = True
            calling_positional_parameters, calling_keyword_parameters = call_with
        
        
        self = object.__new__(cls)
        self.wrapped = wrapped
        
        self.raising_exceptions_exact_type = raising_exceptions_exact_type
        self.raising_exceptions = raising_exceptions
        self.is_raising = is_raising
        self.is_returning = is_returning
        self.is_call_with = is_call_with
        self.calling_keyword_parameters = calling_keyword_parameters
        self.calling_positional_parameters = calling_positional_parameters
        self.returning_value = returning_value
        
        return self
    
    
    @copy_docs(WrapperBase.__repr__)
    def __repr__(self):
        for field_added, repr_parts in self._cursed_repr_builder():
            
            repr_parts.append(' (')
            type_field_added = False
            
            is_raising = self.is_raising
            if is_raising:
                if type_field_added:
                    repr_parts.append(', ')
                else:
                    type_field_added = True
                
                repr_parts.append('raising')
            
            
            is_returning = self.is_returning
            if is_returning:
                if type_field_added:
                    repr_parts.append(', ')
                else:
                    type_field_added = True
            
                repr_parts.append('returning')
            
            is_call_with = self.is_call_with
            
            if is_call_with:
                if type_field_added:
                    repr_parts.append(', ')
                else:
                    type_field_added = True
            
                repr_parts.append('call_with')
            
            repr_parts.append(')')
            
            
            if is_raising:
                if field_added:
                    repr_parts.append(',')
                else:
                    field_added = True
                
                repr_parts.append(' raising_exceptions=')
                repr_parts.append(repr(self.raising_exceptions))
                
                repr_parts.append(', raising_exceptions_exact_type=')
                repr_parts.append(repr(self.raising_exceptions_exact_type))
            
            if is_returning:
                if field_added:
                    repr_parts.append(',')
                else:
                    field_added = True
                
                repr_parts.append(' self.returning_value=')
                repr_parts.append(reprlib.repr(self.returning_value))
            
            
            if is_call_with:
                calling_positional_parameters = self.calling_positional_parameters
                if calling_positional_parameters:
                    if field_added:
                        repr_parts.append(',')
                    else:
                        field_added = True
                    
                    repr_parts.append(' calling_positional_parameters=')
                    repr_parts.append(reprlib.repr(calling_positional_parameters))
                
                calling_keyword_parameters = self.calling_keyword_parameters
                if calling_keyword_parameters:
                    if field_added:
                        repr_parts.append(',')
                    else:
                        field_added = True
                    
                    repr_parts.append(' calling_keyword_parameters=')
                    repr_parts.append(reprlib.repr(calling_keyword_parameters))
            
        return ''.join(repr_parts)
    
    
    @copy_docs(WrapperBase.__hash__)
    def __hash__(self):
        hash_value = WrapperBase.__hash__(self)
        
        if self.is_raising:
            hash_value ^= hash_set(self.raising_exceptions)
            hash_value ^= self.raising_exceptions_exact_type
        
        if self.is_returning:
            hash_value ^= try_hash_method(self.returning_value)
        
        
        if self.is_call_with:
            hash_value ^= hash_tuple(self.calling_positional_parameters)
            hash_value ^= hash_dict(self.calling_keyword_parameters)
        
        
        return hash_value
    
    
    @copy_docs(WrapperBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        is_raising = self.is_raising
        if is_raising != other.is_raising:
            return False
        
        if is_raising:
            if self.raising_exceptions != other.raising_exceptions:
                return False
            
            if self.raising_exceptions_exact_type != other.raising_exceptions_exact_type:
                return False
        
        is_returning = self.is_returning
        if is_returning != other.is_returning:
            return False
        
        if is_returning:
            if self.returning_value != other.returning_value:
                return False
        
        is_call_with = self.is_call_with
        if is_call_with != other.is_call_with:
            return False
        
        if is_call_with:
            if self.calling_positional_parameters != other.calling_positional_parameters:
                return False
            
            if self.calling_keyword_parameters != other.calling_keyword_parameters:
                return False
        
        return True
    
    
    @copy_docs(WrapperBase.check_conflicts)
    def check_conflicts(self):
        if self.is_raising and self.is_returning:
            return WrapperConflict(
                self,
                reason = 'A call wrapper cannot be returning & raising at the same time.',
            )
    
    
    @copy_docs(WrapperBase.check_conflict_with)
    def check_conflict_with(self, other):
        if not isinstance(other, type(self)):
            return
        
        
        self_input_field_count = self.is_call_with
        self_output_field_count = self.is_raising + self.is_returning
        
        other_input_count = other.is_call_with
        other_output_field_count = other.is_raising + other.is_returning
        
        if (self_input_field_count + self_output_field_count) == (other_input_count + other_output_field_count):
            # Both defined input and output, so we accept both.
            return
        
        
        if (self_input_field_count + self_output_field_count) != (other_input_count + other_output_field_count):
            # Both should define input and output at the same time if any does.
            return WrapperConflict(
                self,
                other,
                reason = (
                    'Call wrappers must be either just parameterising / returning / raising, or '
                    'parameterising & (returning / raising) at the same time.'
                )
            )
        
        
        if (self_output_field_count + other_output_field_count) == 2:
            return WrapperConflict(
                self,
                other,
                reason = 'Just returning / raising wrappers cannot be combined.'
            )
    
    
    @copy_docs(WrapperBase.is_ignored_when_testing)
    def is_ignored_when_testing(self):
        return False
    
    
    @copy_docs(WrapperBase.is_mutually_exclusive_with)
    def is_mutually_exclusive_with(self, other):
        if type(self) is not type(other):
            return False
        
        if self.is_call_with and other.is_call_with:
            return True
        
        return False
    
    
    @copy_docs(WrapperBase.context)
    def context(self, test_handle):
        call_state = yield None
        
        if self.is_call_with:
            call_state = call_state.with_parameters(
                self.calling_positional_parameters,
                self.calling_keyword_parameters,
            )
        
        result_state = yield call_state
        
        if self.is_raising:
            raised_exception = result_state.raised_exception
            raising_exceptions = self.raising_exceptions
            raising_exceptions_exact_type = self.raising_exceptions_exact_type
            if raised_exception is None:
                return TestResult(test_handle).with_exception(
                    raising_exceptions,
                    None,
                    raising_exceptions_exact_type,
                )
            
            if raising_exceptions_exact_type:
                for exception in raising_exceptions:
                    if isinstance(raised_exception, exception):
                        passed = True
                        break
                else:
                    passed = False
            
            else:
                for exception in raising_exceptions:
                    if type(raised_exception) is exception:
                        passed = True
                        break
                else:
                    passed = False
            
            if not passed:
                return TestResult(test_handle).with_exception(
                    raising_exceptions,
                    raised_exception,
                    raising_exceptions_exact_type,
                )
            
            if passed:
                result_state = result_state.with_exception(None)
        
        elif self.is_returning:
            raised_exception = result_state.raised_exception
            if (raised_exception is not None):
                return TestResult(test_handle).with_exception(None, raised_exception, False)
            
            returned_value = result_state.returned
            returning_value = self.returning_value
            
            if returned_value != returning_value:
                return TestResult(test_handle).with_exception(None, raised_exception, False)
        
        yield result_state
    
    
    @property
    def raising_key(self):
        """
        Returns the wrapper's raising key.
        
        Returns
        -------
        raising_key : `None`, `tuple` (`set` of ``BaseException``, `bool`)
        """
        if self.is_raising:
            return (self.raising_exceptions, self.raising_exceptions_exact_type)
    
    
    @property
    def returning_key(self):
        """
        Returns the wrapper's raising key.
        
        Returns
        -------
        raising_key : `None`, `tuple` (`set` of ``BaseException``, `bool`)
        """
        if self.is_raising:
            return (self.returning_value, )
    
    
    @property
    def call_with_key(self):
        """
        Returns the wrapper's raising key.
        
        Returns
        -------
        call_with_key : `None`, `tuple` (`tuple` of `Any`, `dict` of (`str`, `Any`) items)
        """
        if self.is_call_with:
            return (self.calling_positional_parameters, self.calling_keyword_parameters)
    
    
    def raising_constructor(cls,  *exception_types, raising_exceptions_exact_type=True):
        """
        Creates a new raising wrapper.
        
        Parameters
        ----------
        *exception_types : tuple` of (`BaseException`, ...)
            Exception types to expect.
        raising_exceptions_exact_type : `bool` = `True`
            Whether subclasses are accepted as well.
        
        Raises
        ------
        TypeError
            If an `exception_types`'s type is incorrect.
        ValueError
            If no exception was passed.
        
        Returns
        -------
        new : ``WrapperCall``
        """
        exception_types = un_nest_exception_types(exception_types)
        if not exception_types:
            raise ValueError('At least 1 exception is required.')
        
        return cls(
            raising = (exception_types, raising_exceptions_exact_type),
        )
    
    
    def raising(self,  *exception_types, raising_exceptions_exact_type=True):
        """
        Creates a new raising wrapper extending self.
        
        Parameters
        ----------
        *exception_types : tuple` of (`BaseException`, ...)
            Exception types to expect.
        raising_exceptions_exact_type : `bool` = `True`
            Whether subclasses are accepted as well.
        
        Raises
        ------
        TypeError
            If an `exception_types`'s type is incorrect.
        ValueError
            If no exception was passed.
        
        Returns
        -------
        new : ``WrapperCall``
        """
        exception_types = un_nest_exception_types(exception_types)
        if not exception_types:
            raise ValueError('At least 1 exception is required.')
        
        return type(self)(
            self.wrapped,
            raising = (exception_types, raising_exceptions_exact_type),
            returning = self.returning_key,
            call_with = self.call_with_key,
        )
    
    
    @classmethod
    def returning_constructor(cls, returning):
        """
        Creates a new returning wrapper.
        
        Parameters
        ----------
        returning : `Any`
            The expected value to be returned.
        
        Returns
        -------
        self : ``WrapperCall``
        """
        return cls(
            returning = (returning, ),
        )
    
    
    def returning(self, returning_value):
        """
        Creates a new returning wrapper extending self.
        
        Parameters
        ----------
        returning_value : `Any`
            The expected value to be returned.
        
        Returns
        -------
        new : ``WrapperCall``
        """
        return type(self)(
            self.wrapped,
            raising = self.raising_key,
            returning = (returning_value, ),
            call_with = self.call_with_key,
        )
    
    
    def returning_itself(self):
        """
        Creates a new retuning wrapper checking for whether the input value matches the returned one.
        
        Returns
        -------
        new : ``WrapperCall``
        
        Raises
        ------
        ValueError
            The wrapper is not parameterised, or incorrect amount parameters registered.
        """
        if not self.is_call_with:
            raise ValueError(
                f'Call wrapper cannot check for return value if it has no parameters added; self={self!r}.'
            )
        
        calling_positional_parameters = self.calling_positional_parameters
        calling_keyword_parameters = self.calling_keyword_parameters
        
        if len(calling_positional_parameters) + len(calling_keyword_parameters) != 1:
            raise ValueError(
                f'``.returning_itself`` is only applicable if the wrapper has 1 parameter added; '
                f'self={self!r}.'
            )
        
        if calling_positional_parameters:
            returning_value = calling_positional_parameters[0]
        else:
            returning_value = next(iter(calling_keyword_parameters.values()))
        
        return type(self)(
            self.wrapped,
            raising = self.raising_key,
            returning = (returning_value, ),
            call_with = self.call_with_key,
        )
    
    
    @classmethod
    def call_with_constructor(cls, *calling_positional_parameters, **calling_keyword_parameters):
        """
        Creates new parameterised wrapper.
        
        Parameters
        ----------
        *calling_positional_parameters : `tuple` of `Any`
            Positional parameter to call the test with.
        **calling_keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters to call the test with.
        
        Returns
        -------
        self : ``WrapperCall``
        """
        return cls(
            call_with = (calling_positional_parameters, calling_keyword_parameters),
        )
    
    
    def call_with(self, *calling_positional_parameters, **calling_keyword_parameters):
        """
        Creates a new parameterised wrapper extending self.
        
        Parameters
        ----------
        *calling_positional_parameters : `tuple` of `Any`
            Positional parameter to call the test with.
        **calling_keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters to call the test with.
        
        Returns
        -------
        new : ``WrapperCall``
        """
        return type(self)(
            self.wrapped,
            raising = self.raising_key,
            returning = self.returning_key,
            call_with = (calling_positional_parameters, calling_keyword_parameters),
        )
