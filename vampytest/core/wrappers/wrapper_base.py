__all__ = ('WrapperBase', )

from ..helpers import hash_object

from scarletio import RichAttributeErrorBaseType, include


WrapperChainer = include('WrapperChainer')


class WrapperBase(RichAttributeErrorBaseType):
    """
    Base class for test wrappers defining shared functionality.
    
    Attributes
    ----------
    wrapped : `None`, `Any`
        The wrapped test.
    """
    __slots__ = ('wrapped', )
    
    def __new__(cls):
        """
        Creates a new test wrapper.
        """
        self = object.__new__(cls)
        self.wrapped = None
        return self
    
    
    def __call__(self, to_wrap):
        """
        Calls the wrapper.
        
        Parameters
        ----------
        to_wrap : `Any`
            The object to wrap. It can be either a function or an another wrapper.
        
        Returns
        -------
        to_wrap : ``WrapperBase``
            The same or a newly created wrapper.
        
        Raises
        ------
        RuntimeError
            Wrapper already called.
        """
        if to_wrap is None:
            raise RuntimeError(f'Cannot wrap `None`; self={self!r}.')
        
        
        wrapped = self.wrapped
        
        if isinstance(to_wrap, WrapperBase):
            
            if (wrapped is not None) and (to_wrap.wrapped is not None):
                raise RuntimeError(
                    f'Both self and other wrappers are already wrapped; self = {self!r}; other = {to_wrap!r}.'
                )
            
            if isinstance(to_wrap, WrapperChainer):
                to_wrap.append(self)
                
                if (wrapped is not None):
                    to_wrap(wrapped)
                
                return to_wrap
            
            if wrapped is None:
                wrapped = to_wrap.wrapped
            
            wrapper_chainer = WrapperChainer(wrapped)
            wrapper_chainer.append(self)
            wrapper_chainer.append(to_wrap)
            return wrapper_chainer
        
        
        if (wrapped is not None):
            raise RuntimeError(f'Wrapped already wrapped; self = {self!r}, to_wrap = {to_wrap!r}.')
        
        self.wrapped = to_wrap
        return self
    
    
    def __matmul__(self, other):
        """Returns `self(other)`"""
        return self.__call__(other)
    
    
    def __rmatmul__(self, other):
        """Returns `self(other)`"""
        return self.__call__(other)
        
    
    def _cursed_repr_builder(self):
        """
        Representation builder helper.
        
        This method is a generator.
        
        Examples
        --------
        ```
        for field_added, repr_parts in self._cursed_repr_builder():
            if not field_added:
                repr_parts.append(',')
            
            repr_parts.append(' oh no')
        
        return ''.join(repr_parts)
        ```
        """
        repr_parts = ['<', self.__class__.__name__]
        
        wrapped = self.wrapped
        if (wrapped is None):
            repr_parts.append(' wrapped = ')
            repr_parts.append(repr(wrapped))
            
            field_added = True
        else:
            field_added = False
        
        yield field_added, repr_parts
        
        repr_parts.append('>')
        return ''.join(repr_parts)
    
    
    def __repr__(self):
        """Returns the wrapper's representation."""
        for field_added, repr_parts in self._cursed_repr_builder():
            pass
        
        return ''.join(repr_parts)
    
    
    def __hash__(self):
        """Returns the wrapper's representation."""
        wrapped = self.wrapped
        if wrapped is None:
            hash_value = 0
        else:
            hash_value = hash_object(wrapped)
        
        return hash_value
    
    
    def __eq__(self, other):
        """return whether the two wrappers are equal."""
        if type(self) is not type(other):
            return NotImplemented
        
        if self.wrapped != other.wrapped:
            return False
        
        return True
    
    
    def do_skip(self):
        """
        Whether the test should be skipped.
        
        Returns
        -------
        do_skip : `bool`
        """
        return False
    
    
    def do_revert(self):
        """
        Tests whether the test's result should be reverted.
        
        Returns
        -------
        do_revert : `bool`
        """
        return False
    
    
    def check_conflicts(self):
        """
        Checks whether the wrapper has internal conflict.
        
        Returns
        ------
        wrapper_conflict: `None`, ``WrapperConflict``
        """
        pass
    
    
    def check_conflict_with(self, other):
        """
        Checks whether the wrapper has conflict with the other one.
        
        Returns
        ------
        wrapper_conflict: `None`, ``WrapperConflict``
        """
        pass
    
    
    def has_bound_test(self):
        """
        Returns whether the wrapper wraps a test.
        
        Returns
        -------
        has_bound_test : `bool`
        """
        return (self.wrapped is not None)
    
    
    def unbind_test(self):
        """
        Unbinds the wrappers test.
        
        Returns
        -------
        test : `Any`
        
        Raises
        ------
        RuntimeError
            The wrapper had no test or already unbind.
        """
        wrapped = self.wrapped
        if wrapped is None:
            raise RuntimeError(f'The wrapper had no test or already unbind; self = {self!r}.')
        
        self.wrapped = None
        return wrapped
    
    
    def iter_wrappers(self):
        """
        Iterates over the wrappers encapsulated by this wrapper. This method is used to un-nest wrapper groups if
        required.
        
        This method is an iterable generator.
        
        Yields
        ------
        wrapper : ``WrapperBase``
        """
        yield self
    
    
    def is_ignored_when_testing(self):
        """
        Returns whether the wrapper can be ignore when testing, but is used instead for just pre-checks.
        
        Returns
        -------
        is_ignored_when_testing : `bool`
        """
        return True
    
    
    def is_mutually_exclusive_with(self, other):
        """
        Returns whether the wrapper is mutually exclusive with the other one.
        
        Parameters
        ----------
        other : ``WrapperBase``
        
        Returns
        -------
        is_mutually_exclusive_with : `bool`
        """
        return False
    
    
    def context(self, handle):
        """
        Context over a test handle.
        
        This method is a generator.
        
        Parameters
        ----------
        handle : ``Handle``
            The parent test handle.
        
        Yields
        ------
        step_result : ``Result``, ``CallState``, ``ResultState``
        
        Returns
        -------
        step_result : ``Result``, ``CallState``, ``ResultState``
        
        Example Implementation
        ----------------------
        ```py
        # before first yield we might check the test handle out and return a `Result` if something is wrong.
        
        if everything is not good:
            return Result(handle)....
        
        # If we find everything good, we will get back a `CallState` on our yield
        call_state = yield
        
        # We might modify the parameters of the call state with `.with_parameters` method
        call_state = call_state.with_parameters(positional, keyword)
        
        # If something is wrong, we can return a `Result` again.
        if everything is not good:
            return Result(handle)....
        
        # If everything is good, we yield back our call state. At this time we will get back a `ResultState` on our
        # yield.
        
        result_state = yield call_state
        
        # We might check the result state and modify it, or again return a `Result` if something is wrong.
        
        if everything is not good:
            return Result(handle)....
        
        # To modify the result state, use the `.with_return` or the `.with_exception` methods.
        result_state = result_state.with_return(None)
        result_state = result_state.with_exception(None)
        
        At the end yield back our `result_state`
        yield result_state
        ```
        """
        call_state = yield None
        result_state = yield call_state
        yield result_state
    
    
    def iter_environments(self):
        """
        Iterates over the environments registered to the wrapper.
        
        This method is an iterable generator.
        
        Yields
        ------
        environment : ``DefaultEnvironment``
        """
        return
        yield
