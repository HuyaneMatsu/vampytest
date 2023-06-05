__all__ = ('WrapperCalling',)

import reprlib

from scarletio import copy_docs

from ..contexts import ContextCalling
from ..helpers.hashing import hash_dict, hash_set, hash_tuple, try_hash_method
from ..helpers.un_nesting import un_nest_exceptions

from .wrapper_base import WrapperBase
from .wrapper_conflict import WrapperConflict


MODE_RAISING = 1 << 0
MODE_RETURNING = 1 << 2
MODE_CALL_WITH = 1 << 3


class WrapperCalling(WrapperBase):
    """
    Combined wrapper supporting `call_with`, `returning` and `raising`.
    
    Attributes
    ----------
    wrapped : `object`
        The wrapped test.
    calling_keyword_parameters : `None`, `dict` of (`str`, `object`) items
        Keyword parameters to call the test with if ``.is_call_with``.
    calling_positional_parameters : `None`, `tuple` of `object`
        Positional parameter to call the test with if ``.is_call_with``.
    mode : `int`
        Bitwise flag containing the mode of calling and handling returns.
    raising_accept_subtypes : `bool`
        Whether exception subclasses are accepted as well if ``.is_raising``.
    raising_exceptions : `None`, `set` of ``BaseException``
        The raised exceptions to be expected to be raised if ``.is_raising``.
    raising_where : `None`, `callable`
        Additional check to check the raised exception if ``.is_raising`.
    returning_value : `None`, `object`
        The expected returned value of the test if ``.is_returning``.
    """
    __slots__ = (
        'calling_keyword_parameters', 'calling_positional_parameters', 'mode', 'raising_exceptions',
        'raising_accept_subtypes', 'raising_where', 'returning_value'
    )
    
    def __new__(cls, wrapped = None, *, call_with = None, raising = None, returning = None):
        """
        Creates a new combined test wrapper.
        
        Parameters
        ----------
        wrapped : `None`, `object` = `None`, Optional
            The wrapped test if any.
        call_with : `None`, `tuple` (`tuple` of `object`, `dict` of (`str`, `object`) items) = `None`
                , Optional (Keyword only)
            Whether the test should be called with parameters.
        raising : `None`, `tuple` (`set` of ``BaseException``, `bool`, (`None`, `callable`)) = `None` \
                , Optional (Keyword only)
            Whether the test is raising.
        returning : `None`, `tuple` (`object`) = `None`, Optional (Keyword only)
            Whether the test is returning.
        """
        mode = 0
        
        if raising is None:
            raising_exceptions = None
            raising_accept_subtypes = None
            raising_where = None
        
        else:
            mode |= MODE_RAISING
            raising_exceptions, raising_accept_subtypes, raising_where = raising
        
        
        if returning is None:
            returning_value = None
        
        else:
            mode |= MODE_RETURNING
            returning_value, = returning
        
        
        if call_with is None:
            calling_keyword_parameters = None
            calling_positional_parameters = None
        
        else:
            mode |= MODE_CALL_WITH
            calling_positional_parameters, calling_keyword_parameters = call_with
        
        
        self = object.__new__(cls)
        self.wrapped = wrapped
        
        self.calling_keyword_parameters = calling_keyword_parameters
        self.calling_positional_parameters = calling_positional_parameters
        self.mode = mode
        self.raising_accept_subtypes = raising_accept_subtypes
        self.raising_exceptions = raising_exceptions
        self.raising_where = raising_where
        self.returning_value = returning_value
        
        return self
    
    
    @copy_docs(WrapperBase.__repr__)
    def __repr__(self):
        for field_added, repr_parts in self._cursed_repr_builder():
            
            mode = self.mode
            repr_parts.append(' (')
            type_field_added = False
            
            if mode & MODE_RAISING:
                if type_field_added:
                    repr_parts.append(', ')
                else:
                    type_field_added = True
                
                repr_parts.append('raising')
            
            if mode & MODE_RETURNING:
                if type_field_added:
                    repr_parts.append(', ')
                else:
                    type_field_added = True
            
                repr_parts.append('returning')
            
            if mode & MODE_CALL_WITH:
                if type_field_added:
                    repr_parts.append(', ')
                else:
                    type_field_added = True
            
                repr_parts.append('call_with')
            
            repr_parts.append(')')
            
            
            if mode & MODE_RAISING:
                if field_added:
                    repr_parts.append(',')
                else:
                    field_added = True
                
                repr_parts.append(' raising_exceptions = ')
                repr_parts.append(repr(self.raising_exceptions))
                
                repr_parts.append(', raising_accept_subtypes = ')
                repr_parts.append(repr(self.raising_accept_subtypes))
                
                raising_where = self.raising_where
                if (raising_where is not None):
                    repr_parts.append(', raising_where = ')
                    repr_parts.append(repr(raising_where))
            
            if mode & MODE_RETURNING:
                if field_added:
                    repr_parts.append(',')
                else:
                    field_added = True
                
                repr_parts.append(', returning_value = ')
                repr_parts.append(reprlib.repr(self.returning_value))
            
            if mode & MODE_CALL_WITH:
                calling_positional_parameters = self.calling_positional_parameters
                if calling_positional_parameters:
                    if field_added:
                        repr_parts.append(',')
                    else:
                        field_added = True
                    
                    repr_parts.append(' calling_positional_parameters = ')
                    repr_parts.append(reprlib.repr(calling_positional_parameters))
                
                calling_keyword_parameters = self.calling_keyword_parameters
                if calling_keyword_parameters:
                    if field_added:
                        repr_parts.append(',')
                    else:
                        field_added = True
                    
                    repr_parts.append(' calling_keyword_parameters = ')
                    repr_parts.append(reprlib.repr(calling_keyword_parameters))
            
        return ''.join(repr_parts)
    
    
    @copy_docs(WrapperBase.__hash__)
    def __hash__(self):
        hash_value = WrapperBase.__hash__(self)
        
        if self.is_raising():
            hash_value ^= hash_set(self.raising_exceptions)
            hash_value ^= self.raising_accept_subtypes
            raising_where = self.raising_where
            if (raising_where is not None):
                hash_value ^= try_hash_method(raising_where)
                
        if self.is_returning():
            hash_value ^= try_hash_method(self.returning_value)
        
        if self.is_call_with():
            hash_value ^= hash_tuple(self.calling_positional_parameters)
            hash_value ^= hash_dict(self.calling_keyword_parameters)
        
        return hash_value
    
    
    @copy_docs(WrapperBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        self_mode = self.mode
        if self_mode != other.mode:
            return False
        
        if self_mode & MODE_RAISING:
            if self.raising_exceptions != other.raising_exceptions:
                return False
            
            if self.raising_accept_subtypes != other.raising_accept_subtypes:
                return False
            
            if self.raising_where != other.raising_where:
                return False
        
        if self_mode & MODE_RETURNING:
            if self.returning_value != other.returning_value:
                return False
        
        if self_mode & MODE_CALL_WITH:
            if self.calling_positional_parameters != other.calling_positional_parameters:
                return False
            
            if self.calling_keyword_parameters != other.calling_keyword_parameters:
                return False
        
        return True
    
    
    @copy_docs(WrapperBase.check_conflicts)
    def check_conflicts(self):
        if self.is_raising() and self.is_returning():
            return WrapperConflict(
                self,
                reason = 'A call wrapper cannot be returning & raising at the same time.',
            )
    
    
    @copy_docs(WrapperBase.check_conflict_with)
    def check_conflict_with(self, other):
        if not isinstance(other, type(self)):
            return
        
        
        self_input_field_count = self.is_call_with()
        self_output_field_count = self.is_raising() + self.is_returning()
        
        other_input_count = other.is_call_with()
        other_output_field_count = other.is_raising() + other.is_returning()
        
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
        
        if self.is_call_with() and other.is_call_with():
            return True
        
        return False
    
    
    @copy_docs(WrapperBase.get_context)
    def get_context(self, handle):
        return ContextCalling(handle, self)
    
    
    @property
    def raising_key(self):
        """
        Returns the wrapper's raising key.
        
        Returns
        -------
        raising_key : `None`, `tuple` (`set` of ``BaseException``, `bool`, (`None`, `callable`))
        """
        if self.is_raising():
            return (self.raising_exceptions, self.raising_accept_subtypes, self.raising_where)
    
    
    @property
    def returning_key(self):
        """
        Returns the wrapper's raising key.
        
        Returns
        -------
        returning_key : `None`, `tuple` (`object`)
        """
        if self.is_returning():
            return (self.returning_value, )
    
    
    @property
    def call_with_key(self):
        """
        Returns the wrapper's raising key.
        
        Returns
        -------
        call_with_key : `None`, `tuple` (`tuple` of `object`, `dict` of (`str`, `object`) items)
        """
        if self.is_call_with():
            return (self.calling_positional_parameters, self.calling_keyword_parameters)
    
    
    @classmethod
    def raising_constructor(cls, exception_type, *exception_types, accept_subtypes = True, where = None):
        """
        Creates a new raising wrapper.
        
        Parameters
        ----------
        exception_type : `type<BaseException> | BaseException>
            Exception type to expect.
        *exception_types : `tuple<type<BaseException>, BaseException, ...>`
            Additional exception types.
        accept_subtypes : `bool` = `True`
            Whether subclasses are accepted as well.
        where : `None`, `callable` = `None`, Optional (Keyword only)
            Additional check to check the raised exception.
        
        Raises
        ------
        TypeError
            If an `exception_types`'s type is incorrect.
        ValueError
            If no exception was passed.
        
        Returns
        -------
        self : `instance<self>`
        """
        exception_types = un_nest_exceptions((exception_type, *exception_types))
        if not exception_types:
            raise ValueError(
                'At least 1 exception is required.'
            )
        
        return cls(
            raising = (exception_types, accept_subtypes, where),
        )
    
    
    def raising(self, exception_type, *exception_types, accept_subtypes = True, where = None):
        """
        Creates a new raising wrapper extending self.
        
        Parameters
        ----------
        exception_type : `type<BaseException> | BaseException>
            Exception type to expect.
        *exception_types : `tuple<type<BaseException>, BaseException, ...>`
            Additional exception types.
        accept_subtypes : `bool` = `True`
            Whether subclasses are accepted as well.
        where : `None`, `callable` = `None`, Optional (Keyword only)
            Additional check to check the raised exception.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        TypeError
            If an `exception_types`'s type is incorrect.
        ValueError
            If no exception was passed.
        """
        exception_types = un_nest_exceptions((exception_type, *exception_types))
        if not exception_types:
            raise ValueError(
                'At least 1 exception is required.'
            )
        
        return type(self)(
            self.wrapped,
            raising = (exception_types, accept_subtypes, where),
            returning = self.returning_key,
            call_with = self.call_with_key,
        )
    
    
    @classmethod
    def returning_constructor(cls, returning):
        """
        Creates a new returning wrapper.
        
        Parameters
        ----------
        returning : `object`
            The expected value to be returned.
        
        Returns
        -------
        self : `instance<self>`
        """
        return cls(
            returning = (returning, ),
        )
    
    
    def returning(self, returning_value):
        """
        Creates a new returning wrapper extending self.
        
        Parameters
        ----------
        returning_value : `object`
            The expected value to be returned.
        
        Returns
        -------
        new : `instance<type<self>>`
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
        new : `instance<type<self>>`
        
        Raises
        ------
        ValueError
            The wrapper is not parameterised, or incorrect amount parameters registered.
        """
        if not self.is_call_with():
            raise ValueError(
                f'Call wrapper cannot check for return value if it has no parameters added; self = {self!r}.'
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
        new : `instance<type<self>>`
        
        Raises
        ------
        ValueError
            The wrapper is not parameterised, or incorrect amount parameters registered.
        """
        if not self.is_call_with():
            raise ValueError(
                f'Call wrapper cannot check for return value if it has no parameters added; self = {self!r}.'
            )
        
        calling_positional_parameters = self.calling_positional_parameters
        calling_keyword_parameters = self.calling_keyword_parameters
        
        if len(calling_positional_parameters) + len(calling_keyword_parameters) != 1:
            raise ValueError(
                f'`returning_itself` is only applicable if the wrapper has 1 parameter added; '
                f'self = {self!r}.'
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
        *calling_positional_parameters : `tuple` of `object`
            Positional parameter to call the test with.
        **calling_keyword_parameters : `dict` of (`str`, `object`) items
            Keyword parameters to call the test with.
        
        Returns
        -------
        self : `instance<cls>`
        """
        return cls(
            call_with = (calling_positional_parameters, calling_keyword_parameters),
        )
    
    
    def call_with(self, *calling_positional_parameters, **calling_keyword_parameters):
        """
        Creates a new parameterised wrapper extending self.
        
        Parameters
        ----------
        *calling_positional_parameters : `tuple` of `object`
            Positional parameter to call the test with.
        **calling_keyword_parameters : `dict` of (`str`, `object`) items
            Keyword parameters to call the test with.
        
        Returns
        -------
        new : `instance<type<self>>`
        """
        return type(self)(
            self.wrapped,
            raising = self.raising_key,
            returning = self.returning_key,
            call_with = (calling_positional_parameters, calling_keyword_parameters),
        )
    
    
    def is_raising(self):
        """
        Returns whether raised exceptions of the test should be checked.
        
        Returns
        -------
        is_raising : `bool`
        """
        return True if self.mode & MODE_RAISING else False
    
    
    def is_returning(self):
        """
        Returns whether returned value of the test should be checked.
        
        Returns
        -------
        is_returning : `bool`
        """
        return True if self.mode & MODE_RETURNING else False
    
    
    def is_call_with(self):
        """
        Returns whether the test should be called with specific parameters.
        
        Returns
        -------
        is_call_with : `bool`
        """
        return True if self.mode & MODE_CALL_WITH else False
