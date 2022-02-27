__all__ = ('WrapperCall',)

import reprlib

from ..helpers import hash_dict, hash_set, hash_tuple, try_hash_method, un_nest_exception_types

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
    accept_sub_classes : `bool`
        Whether exception subclasses are accepted as well if ``.is_raising``.
    exceptions : `None`, `set` of ``BaseException``
        The exceptions expected to be raised if ``.is_raising``.
    is_raising : `bool`
        Whether raised exceptions of the test should be checked.
    is_returning : `bool`
        Whether returned value of the test should be checked.
    is_call_with : `bool`
        Whether the test should be called with specific parameters.
    keyword_parameters : `None`, `dict` of (`str`, `Any`) items
        Keyword parameters to call the test with if ``.is_call_with``.
    positional_parameters : `None`, `tuple` of `Any`
        Positional parameter to call the test with if ``.is_call_with``.
    value : `None`, `Any`
        The expected returned value of the test if ``.is_returning``.
    """
    __slots__ = (
        'accept_sub_classes', 'exceptions', 'is_raising', 'is_returning', 'is_call_with', 'keyword_parameters',
        'positional_parameters', 'value'
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
            exceptions = None
            accept_sub_classes = None
        
        else:
            is_raising = True
            exceptions, accept_sub_classes = raising
        
        
        if returning is None:
            is_returning = False
            value = None
        
        else:
            is_returning = True
            value = returning[0]
        
        
        if call_with is None:
            is_call_with = False
            keyword_parameters = None
            positional_parameters = None
        
        else:
            is_call_with = True
            positional_parameters, keyword_parameters = call_with
        
        
        self = object.__new__(cls)
        self.wrapped = wrapped
        
        self.accept_sub_classes = accept_sub_classes
        self.exceptions = exceptions
        self.is_raising = is_raising
        self.is_returning = is_returning
        self.is_call_with = is_call_with
        self.keyword_parameters = keyword_parameters
        self.positional_parameters = positional_parameters
        self.value = value
        
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
                
                repr_parts.append(' exceptions=')
                repr_parts.append(repr(self.exceptions))
                
                repr_parts.append(', accept_sub_classes=')
                repr_parts.append(repr(self.accept_sub_classes))
            
            if is_returning:
                if field_added:
                    repr_parts.append(',')
                else:
                    field_added = True
                
                repr_parts.append(' value=')
                repr_parts.append(reprlib.repr(self.value))
            
            
            if is_call_with:
                positional_parameters = self.positional_parameters
                if positional_parameters:
                    if field_added:
                        repr_parts.append(',')
                    else:
                        field_added = True
                    
                    repr_parts.append(' positional_parameters=')
                    repr_parts.append(reprlib.repr(positional_parameters))
                
                keyword_parameters = self.keyword_parameters
                if keyword_parameters:
                    if field_added:
                        repr_parts.append(',')
                    else:
                        field_added = True
                    
                    repr_parts.append(' keyword_parameters=')
                    repr_parts.append(reprlib.repr(keyword_parameters))
            
        return ''.join(repr_parts)
    
    
    @copy_docs(WrapperBase.__hash__)
    def __hash__(self):
        hash_value = WrapperBase.__hash__(self)
        
        if self.is_raising:
            hash_value ^= hash_set(self.exceptions)
            hash_value ^= self.accept_sub_classes
        
        if self.is_returning:
            hash_value ^= try_hash_method(self.value)
        
        
        if self.is_call_with:
            hash_value ^= hash_tuple(self.positional_parameters)
            hash_value ^= hash_dict(self.keyword_parameters)
        
        
        return hash_value
    
    
    @copy_docs(WrapperBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        is_raising = self.is_raising
        if is_raising != other.is_raising:
            return False
        
        if is_raising:
            if self.exceptions != other.exceptions:
                return False
            
            if self.accept_sub_classes != other.accept_sub_classes:
                return False
        
        is_returning = self.is_returning
        if is_returning != other.is_returning:
            return False
        
        if is_returning:
            if self.value != other.value:
                return False
        
        is_call_with = self.is_call_with
        if is_call_with != other.is_call_with:
            return False
        
        if is_call_with:
            if self.positional_parameters != other.positional_parameters:
                return False
            
            if self.keyword_parameters != other.keyword_parameters:
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
    

    @property
    def raising_key(self):
        """
        Returns the wrapper's raising key.
        
        Returns
        -------
        raising_key : `None`, `tuple` (`set` of ``BaseException``, `bool`)
        """
        if self.is_raising:
            return (self.exceptions, self.accept_sub_classes)
    
    
    @property
    def returning_key(self):
        """
        Returns the wrapper's raising key.
        
        Returns
        -------
        raising_key : `None`, `tuple` (`set` of ``BaseException``, `bool`)
        """
        if self.is_raising:
            return (self.value, )
    
    
    @property
    def call_with_key(self):
        """
        Returns the wrapper's raising key.
        
        Returns
        -------
        call_with_key : `None`, `tuple` (`tuple` of `Any`, `dict` of (`str`, `Any`) items)
        """
        if self.is_call_with:
            return (self.positional_parameters, self.keyword_parameters)
    
    
    def raising_constructor(cls,  *exception_types, accept_sub_classes=True):
        """
        Creates a new raising wrapper.
        
        Parameters
        ----------
        *exception_types : tuple` of (`BaseException`, ...)
            Exception types to expect.
        accept_sub_classes : `bool` = `True`
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
            raising = (exception_types, accept_sub_classes),
        )
    
    
    def raising(self,  *exception_types, accept_sub_classes=True):
        """
        Creates a new raising wrapper extending self.
        
        Parameters
        ----------
        *exception_types : tuple` of (`BaseException`, ...)
            Exception types to expect.
        accept_sub_classes : `bool` = `True`
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
            raising = (exception_types, accept_sub_classes),
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
    
    
    def returning(self, returning):
        """
        Creates a new returning wrapper extending self.
        
        Parameters
        ----------
        returning : `Any`
            The expected value to be returned.
        
        Returns
        -------
        new : ``WrapperCall``
        """
        return type(self)(
            self.wrapped,
            raising = self.raising_key,
            returning = (returning, ),
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
        
        positional_parameters = self.positional_parameters
        keyword_parameters = self.keyword_parameters
        
        if len(positional_parameters) + len(keyword_parameters) != 1:
            raise ValueError(
                f'``.returning_itself`` is only applicable if the wrapper has 1 parameter added; '
                f'self={self!r}.'
            )
        
        if positional_parameters:
            value = positional_parameters[0]
        else:
            value = next(iter(keyword_parameters.values()))
        
        return type(self)(
            self.wrapped,
            raising = self.raising_key,
            returning = (value, ),
            call_with = self.call_with_key,
        )
    
    
    @classmethod
    def call_with_constructor(cls, *positional_parameters, **keyword_parameters):
        """
        Creates new parameterised wrapper.
        
        Parameters
        ----------
        *positional_parameters : `tuple` of `Any`
            Positional parameter to call the test with.
        **keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters to call the test with.
        
        Returns
        -------
        self : ``WrapperCall``
        """
        return cls(
            call_with = (positional_parameters, keyword_parameters),
        )
    
    
    def call_with(self, *positional_parameters, **keyword_parameters):
        """
        Creates a new parameterised wrapper extending self.
        
        Parameters
        ----------
        *positional_parameters : `tuple` of `Any`
            Positional parameter to call the test with.
        **keyword_parameters : `dict` of (`str`, `Any`) items
            Keyword parameters to call the test with.
        
        Returns
        -------
        new : ``WrapperCall``
        """
        return type(self)(
            self.wrapped,
            raising = self.raising_key,
            returning = self.returning_key,
            call_with = (positional_parameters, keyword_parameters),
        )
