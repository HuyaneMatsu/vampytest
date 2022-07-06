__all__ = ('WrapperCall',)

import reprlib

from ..assertions import AssertionException
from ..helpers import hash_dict, hash_set, hash_tuple, try_hash_method, try_match_exception, un_nest_expected_exceptions
from ..result import Result

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
    calling_keyword_parameters : `None`, `dict` of (`str`, `Any`) items
        Keyword parameters to call the test with if ``.is_call_with``.
    calling_positional_parameters : `None`, `tuple` of `Any`
        Positional parameter to call the test with if ``.is_call_with``.
    is_raising : `bool`
        Whether raised exceptions of the test should be checked.
    is_returning : `bool`
        Whether returned value of the test should be checked.
    is_call_with : `bool`
        Whether the test should be called with specific parameters.
    raising_accept_subtypes : `bool`
        Whether exception subclasses are accepted as well if ``.is_raising``.
    raising_exceptions : `None`, `set` of ``BaseException``
        The raising_exceptions expected to be raised if ``.is_raising``.
    returning_value : `None`, `Any`
        The expected returned value of the test if ``.is_returning``.
    """
    __slots__ = (
        'calling_keyword_parameters', 'calling_positional_parameters', 'is_call_with', 'is_raising', 'is_returning',
        'raising_exceptions', 'raising_accept_subtypes', 'returning_value'
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
            raising_accept_subtypes = None
        
        else:
            is_raising = True
            raising_exceptions, raising_accept_subtypes = raising
        
        
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
        
        self.raising_accept_subtypes = raising_accept_subtypes
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
                
                repr_parts.append(', raising_accept_subtypes=')
                repr_parts.append(repr(self.raising_accept_subtypes))
            
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
            hash_value ^= self.raising_accept_subtypes
        
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
            
            if self.raising_accept_subtypes != other.raising_accept_subtypes:
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
    def context(self, handle):
        call_state = yield None
        
        if self.is_call_with:
            call_state = call_state.with_parameters(
                self.calling_positional_parameters,
                self.calling_keyword_parameters,
            )
        
        result_state = yield call_state
        
        # Ignore `AssertionException`-s.
        if result_state is None:
            raised_exception = None
        else:
            raised_exception = result_state.raised_exception
        
        if (raised_exception is None) or (not isinstance(raised_exception, AssertionException)):
            
            if self.is_raising:
                raising_exceptions = self.raising_exceptions
                raising_accept_subtypes = self.raising_accept_subtypes
                if raised_exception is None:
                    return Result(handle).with_exception(
                        raising_exceptions,
                        None,
                        raising_accept_subtypes,
                    )
                
                if try_match_exception(raising_exceptions, raised_exception, raising_accept_subtypes):
                    if (result_state is not None):
                        result_state = result_state.with_exception(None)
                
                else:
                    return Result(handle).with_exception(
                        raising_exceptions,
                        raised_exception,
                        raising_accept_subtypes,
                    )
            
            elif self.is_returning:
                if (raised_exception is not None):
                    return Result(handle).with_exception(None, raised_exception, False)
                
                if (result_state is None):
                    returned_value = None
                else:
                    returned_value = result_state.returned_value
                
                returning_value = self.returning_value
                
                if returned_value != returning_value:
                    return Result(handle).with_return(returning_value, returned_value)
        
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
            return (self.raising_exceptions, self.raising_accept_subtypes)
    
    
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
    
    
    @classmethod
    def raising_constructor(cls,  *exception_types, raising_accept_subtypes=True):
        """
        Creates a new raising wrapper.
        
        Parameters
        ----------
        *exception_types : tuple` of (`BaseException`, ...)
            Exception types to expect.
        raising_accept_subtypes : `bool` = `True`
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
        exception_types = un_nest_expected_exceptions(exception_types)
        if not exception_types:
            raise ValueError(
                'At least 1 exception is required.'
            )
        
        return cls(
            raising = (exception_types, raising_accept_subtypes),
        )
    
    
    def raising(self,  *exception_types, raising_accept_subtypes=True):
        """
        Creates a new raising wrapper extending self.
        
        Parameters
        ----------
        *exception_types : tuple` of (`BaseException`, ...)
            Exception types to expect.
        raising_accept_subtypes : `bool` = `True`
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
        exception_types = un_nest_expected_exceptions(exception_types)
        if not exception_types:
            raise ValueError(
                'At least 1 exception is required.'
            )
        
        return type(self)(
            self.wrapped,
            raising = (exception_types, raising_accept_subtypes),
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
    
    
    def returning_transformed(self, transformer):
        """
        Creates a new returning wrapper transforming the current parameters of the wrapper.
        
        Parameters
        ----------
        transformer : `callable`
        
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
        
        if calling_positional_parameters is None:
            if calling_keyword_parameters:
                returning_value = transformer()
            else:
                returning_value = transformer(**calling_keyword_parameters)
        
        else:
            if calling_keyword_parameters:
                returning_value = transformer(*calling_positional_parameters)
            else:
                returning_value = transformer(*calling_positional_parameters, **calling_keyword_parameters)
        
        return self.returning(returning_value)
    
    
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
