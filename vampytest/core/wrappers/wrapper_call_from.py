__all__ = ('WrapperCallingFrom',)

import reprlib
from itertools import repeat

from scarletio import copy_docs

from ..helpers.hashing import hash_set, try_hash_method
from ..helpers.un_nesting import un_nest_exceptions

from .wrapper_base import WrapperBase
from .wrapper_call import WrapperCalling
from .wrapper_conflict import WrapperConflict


MODE_RAISING_GIVEN = 1 << 0
MODE_RAISING_LAST = 1 << 2
MODE_RETURNING_GIVEN = 1 << 3
MODE_RETURNING_LAST = 1 << 4
MODE_RETURNING_TRANSFORMED = 1 << 5
MODE_RETURNING_ITSELF = 1 << 6

MODE_RAISING_ALL = MODE_RAISING_GIVEN | MODE_RAISING_LAST
MODE_RETURNING_ALL = MODE_RETURNING_GIVEN | MODE_RETURNING_LAST | MODE_RETURNING_TRANSFORMED | MODE_RETURNING_ITSELF


class WrapperCallingFrom(WrapperBase):
    """
    Allows to create multiple `call_with`, `returning` and `raising` wrappers at once.
    
    Attributes
    ----------
    wrapped : `object`
        The wrapped test.
    calling_from : `list` of `tuple<object>`
        Values to call the tests from.
    mode : `int`
        Bitwise flag containing the mode of handling returns.
    raising_accept_subtypes : `bool`
        Whether exception subclasses are accepted as well if ``.is_raising``.
    raising_exceptions : `None`, `set` of `BaseException`, `list` of `set` of `BaseException`
        The raised exceptions to be expected to be raised if ``.is_raising``.
    raising_where : `None`, `callable`
        Additional check to check the raised exception if ``.is_raising`.
    returning_value : `None`, `object`, `list` of `object`
        The expected returned value of the test if ``.is_returning``.
    """
    __slots__ = (
        'calling_from', 'mode', 'raising_exceptions', 'raising_accept_subtypes', 'raising_where', 'returning_value'
    )
    
    def __new__(cls, wrapped = None, *, calling_from = None, raising = None, returning = None):
        """
        Creates a new combined test wrapper.
        
        Parameters
        ----------
        wrapped : `None`, `object` = `None`, Optional
            The wrapped test if any.
        calling_from : `list` of `tuple<object>`
            Values to call the tests from.
        raising : `None`, `(int, set<BaseException> | list<set<BaseException>>, bool, None | callable)` = `None` \
                , Optional (Keyword only)
            Whether the test is raising.
        returning : `None`, `(int, object | list<object>)` = `None`, Optional (Keyword only)
            Whether the test is returning.
        """
        mode = 0
        
        if raising is None:
            raising_exceptions = None
            raising_accept_subtypes = None
            raising_where = None
        
        else:
            raising_mode, raising_exceptions, raising_accept_subtypes, raising_where = raising
            mode |= raising_mode
        
        if returning is None:
            returning_value = None
        
        else:
            returning_mode, returning_value = returning
            mode |= returning_mode
        
        
        self = object.__new__(cls)
        self.wrapped = wrapped
        self.calling_from = calling_from
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
            
            if mode & MODE_RAISING_ALL:
                if field_added:
                    repr_parts.append(',')
                else:
                    field_added = True
                
                if mode & MODE_RAISING_GIVEN:
                    raising_mode = 'given'
                elif mode & MODE_RAISING_LAST:
                    raising_mode = 'last'
                else:
                    raising_mode = 'unknown'
                
                repr_parts.append(' raising_mode = ')
                repr_parts.append(raising_mode)
                
                repr_parts.append(', raising_exceptions = ')
                repr_parts.append(repr(self.raising_exceptions))
                
                repr_parts.append(', raising_accept_subtypes = ')
                repr_parts.append(repr(self.raising_accept_subtypes))
                
                raising_where = self.raising_where
                if (raising_where is not None):
                    repr_parts.append(', raising_where = ')
                    repr_parts.append(repr(raising_where))
            
            if mode & MODE_RETURNING_ALL:
                if field_added:
                    repr_parts.append(',')
                else:
                    field_added = True
                
                if mode & MODE_RETURNING_GIVEN:
                    returning_mode = 'given'
                elif mode & MODE_RETURNING_LAST:
                    returning_mode = 'last'
                elif mode & MODE_RETURNING_TRANSFORMED:
                    returning_mode = 'transformed'
                elif mode & MODE_RETURNING_ITSELF:
                    returning_mode = 'itself'
                else:
                    returning_mode = 'unknown'
                
                repr_parts.append(' returning_mode = ')
                repr_parts.append(returning_mode)
                
                repr_parts.append(', returning_value = ')
                repr_parts.append(reprlib.repr(self.returning_value))
        
        
        return ''.join(repr_parts)
    
    
    @copy_docs(WrapperBase.__hash__)
    def __hash__(self):
        hash_value = WrapperBase.__hash__(self)
        
        hash_value ^= try_hash_method(self.calling_from)
        
        if self.is_raising():
            hash_value ^= hash_set(self.raising_exceptions)
            hash_value ^= self.raising_accept_subtypes
            raising_where = self.raising_where
            if (raising_where is not None):
                hash_value ^= try_hash_method(raising_where)
        
        if self.is_returning():
            returning_value = self.returning_value
            if (returning_value is not None):
                hash_value ^= try_hash_method(returning_value)
        
        return hash_value
    
    
    @copy_docs(WrapperBase.__eq__)
    def __eq__(self, other):
        if type(self) is not type(other):
            return NotImplemented
        
        self_mode = self.mode
        if self_mode != other.mode:
            return False
        
        if self.calling_from != other.calling_from:
            return False
        
        if self_mode & MODE_RAISING_ALL:
            if self.raising_exceptions != other.raising_exceptions:
                return False
            
            if self.raising_accept_subtypes != other.raising_accept_subtypes:
                return False
            
            if self.raising_where != other.raising_where:
                return False
        
        if self_mode & MODE_RETURNING_ALL:
            if self.returning_value != other.returning_value:
                return False
        
        return True
    
    
    @copy_docs(WrapperBase.check_conflicts)
    def check_conflicts(self):
        if self.is_raising() and self.is_returning():
            return WrapperConflict(
                self,
                reason = 'A call-from wrapper cannot be returning & raising at the same time.',
            )
    
    
    # We cant have conflicts
    # @copy_docs(WrapperBase.check_conflict_with)
    # def check_conflict_with(self, other):
    #    pass
    
    
    @copy_docs(WrapperBase.is_ignored_when_testing)
    def is_ignored_when_testing(self):
        return False
    
    
    @copy_docs(WrapperBase.is_mutually_exclusive_with)
    def is_mutually_exclusive_with(self, other):
        if type(self) is type(other):
            return True
        
        if isinstance(other, WrapperCalling):
            if other.is_call_with():
                return True
            
            return False
        
        return False
    
    
    @copy_docs(WrapperBase.iter_wrappers)
    def iter_wrappers(self):
        mode = self.mode
        if mode & MODE_RAISING_ALL:
            if mode & MODE_RAISING_GIVEN:
                raising_key_iterator = repeat(
                    (self.raising_exceptions, self.raising_accept_subtypes, self.raising_where),
                )
            else:
                raising_key_iterator = zip(
                    self.raising_exceptions, repeat(self.raising_accept_subtypes), repeat(self.raising_where)
                )
        else:
            raising_key_iterator = repeat(None)
        
        if mode & MODE_RETURNING_ALL:
            if mode & MODE_RETURNING_GIVEN:
                returning_key_iterator = repeat((self.returning_value,),)
            else:
                returning_key_iterator = zip(self.returning_value)
        else:
            returning_key_iterator = repeat(None)
        
        for calling_with_key, raising_key, returning_key in zip(
            self.calling_from, raising_key_iterator, returning_key_iterator
        ):
            yield WrapperCalling(
                None, call_with = (calling_with_key, {}), raising = raising_key, returning = returning_key
            )
    
    
    @property
    def raising_key(self):
        """
        Returns the wrapper's raising key.
        
        Returns
        -------
        raising_key : `None`, `tuple` (`int`, (`None`, `set` of `BaseException`), `bool`, (`None`, `callable`))
        """
        raising_mode = self.mode & MODE_RAISING_ALL
        if raising_mode:
            return (raising_mode, self.raising_exceptions, self.raising_accept_subtypes, self.raising_where)
    
    
    @property
    def returning_key(self):
        """
        Returns the wrapper's raising key.
        
        Returns
        -------
        returning_key : `None`, `tuple` (`int`, `object`)
        """
        returning_mode = self.mode & MODE_RETURNING_ALL
        if returning_mode:
            return (returning_mode, self.returning_value)
    
    
    
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
            - If an `exception_types`'s type is incorrect.
        ValueError
            - If no exception was passed.
        """
        exception_types = un_nest_exceptions((exception_type, *exception_types))
        if not exception_types:
            raise ValueError(
                'At least 1 exception is required.'
            )
        
        return type(self)(
            self.wrapped,
            calling_from = self.calling_from,
            raising = (MODE_RAISING_GIVEN, exception_types, accept_subtypes, where),
            returning = self.returning_key,
        )
    
    
    def raising_last(self, *, accept_subtypes = True, where = None):
        """
        Creates a new raising last wrapper extending self.
        
        Note that this also removes the last parameter when calling.
        
        Parameters
        ----------
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
            - If an `exception_types`'s type is incorrect.
        ValueError
            - If an item has no parameters.
        """
        calling_from = self.calling_from
        if any(len(item) < 1 for item in calling_from):
            raise ValueError(
                f'`raising_last` is only applicable if the wrapper has at least 1 for each call; '
                f'self = {self!r}.'
            )
        
        raises = [un_nest_exceptions(item[-1]) for item in calling_from]
        if any((not raises) for raises in raises):
            raise ValueError(
                'At least 1 exception is required for each case.'
            )
        
        calling_from = [item[:-1] for item in calling_from]
        
        return type(self)(
            self.wrapped,
            calling_from = calling_from,
            raising = (MODE_RAISING_LAST, raises, accept_subtypes, where),
            returning = self.returning_key,
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
            calling_from = self.calling_from,
            raising = self.raising_key,
            returning = (MODE_RETURNING_GIVEN, returning_value),
        )
    
    
    def returning_last(self):
        """
        Creates a new returning last wrapper extending self.
        
        Note that this also removes the last parameter when calling.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        ValueError
            - If an item has no parameters.
        """
        calling_from = self.calling_from
        if any(len(item) < 1 for item in calling_from):
            raise ValueError(
                f'`returning_last` is only applicable if the wrapper has at least 1 for each call; '
                f'self = {self!r}.'
            )
        
        returns = [item[-1] for item in calling_from]
        calling_from = [item[:-1] for item in calling_from]
        
        return type(self)(
            self.wrapped,
            calling_from = calling_from,
            raising = self.raising_key,
            returning = (MODE_RETURNING_LAST, returns),
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
        """
        calling_from = self.calling_from
        
        returns = [transformer(*item) for item in calling_from]
        
        return type(self)(
            self.wrapped,
            calling_from = self.calling_from,
            raising = self.raising_key,
            returning = (MODE_RETURNING_TRANSFORMED, returns),
        )
    
    
    def returning_itself(self):
        """
        Creates a new retuning wrapper checking for whether the input value matches the returned one.
        
        Returns
        -------
        new : `instance<type<self>>`
        
        Raises
        ------
        ValueError
            - If an item stores incorrect amount parameters.
        """
        calling_from = self.calling_from
        if any(len(item) != 1 for item in calling_from):
            raise ValueError(
                f'`returning_itself` is only applicable if the wrapper has 1 parameter added for each call; '
                f'self = {self!r}.'
            )
        
        returns = [item[0] for item in calling_from]
        
        return type(self)(
            self.wrapped,
            calling_from = calling_from,
            raising = self.raising_key,
            returning = (MODE_RETURNING_ITSELF, returns),
        )
    
    
    @classmethod
    def calling_from_constructor(cls, calling_from):
        """
        Creates new parameterised wrapper.
        
        Parameters
        ----------
        calling_from : `iterable`
            Iterable to call the test from.
        
        Returns
        -------
        self : `instance<cls>`
        """
        if not hasattr(calling_from, '__iter__'):
            raise TypeError(
                f'`calling_from` must be iterable, got {calling_from.__class__.__name__}; {calling_from!r}.'
            )
        
        items = []
        
        for item in calling_from:
            if isinstance(item, tuple):
                items.append(item)
            else:
                items.append((item,),)
        
        
        return cls(
            calling_from = items,
        )
    
    
    def is_raising(self):
        """
        Returns whether raised exceptions of the test should be checked.
        
        Returns
        -------
        is_raising : `bool`
        """
        return True if self.mode & MODE_RAISING_ALL else False
    
    
    def is_returning(self):
        """
        Returns whether returned value of the test should be checked.
        
        Returns
        -------
        is_returning : `bool`
        """
        return True if self.mode & MODE_RETURNING_ALL else False
