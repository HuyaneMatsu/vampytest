__all__ = ('EventHandlerManager',)

from scarletio import CallableAnalyzer, RichAttributeErrorBaseType

from ..events import EventBase


class EventHandlerManager(RichAttributeErrorBaseType):
    """
    Event handler for handling test runner events.
    
    Attributes
    -----------
    _event_handlers_by_identifier : `dict` of (`int`, `callable`) items
        The registered event handlers.
    """
    __slots__ = ('_event_handlers_by_identifier',)
    
    def __new__(cls):
        """
        Creates a new event handler.
        """
        self = object.__new__(cls)
        self._event_handlers_by_identifier = {}
        return self
    
    
    def events(self, event_handler):
        """
        Can be sued to register event handlers by either using it as a decorator, or just calling it.
        
        Parameters
        ----------
        event_handler : `callable`
            the function to add as an event handler.
        
        Returns
        -------
        event_handler : `callable`
        
        Raises
        ------
        TypeError
            - If `event`'s types is incorrect.
        """
        analyzer = CallableAnalyzer(event_handler)
        
        event_parameter = None
        
        for parameter in analyzer.iter_non_reserved_parameters():
            if parameter.is_keyword_only() or parameter.is_args() or parameter.is_kwargs():
                raise TypeError(
                    f'Event handlers do not support keyword only, args or kwargs parameters, '
                    f'got event_handler= {event_handler!r} with parameter= {parameter!r}.'
                )
            
            if event_parameter is None:
                event_parameter = parameter
            
            else:
                if not parameter.has_default():
                    raise TypeError(
                        f'To event handlers only 1 parameter is passed, but the given one expects more, '
                        f'got event_handler = {event_handler!r} with parameter = {parameter!r}.'
                    )
        
        
        if (event_parameter is None):
            raise TypeError(
                f'To event handlers 1 parameter is passed, but the given one expects zero, '
                f'got event_handler= {event_handler!r}.'
            )
        
        if not event_parameter.has_annotation:
            raise TypeError(
                'Event handler\'s event parameter should be annotated with an event\'s type, '
                f'got event_handler = {event_handler!r} with parameter = {event_parameter!r}.'
            )
        
        annotation = event_parameter.annotation
        if (not isinstance(annotation, type)) or (not issubclass(annotation, EventBase)):
            raise TypeError(
                'Event handler\'s event parameter should be annotated with an event\'s type, '
                f'got event_handler= {event_handler!r} with parameter= {event_parameter!r}; annotation= {annotation!r}.'
            )
        
        if annotation.identifier == EventBase.identifier:
            raise TypeError(
                'Event handler\'s event parameter is annotated with a base event type, '
                f'got event_handler= {event_handler!r} with parameter= {event_parameter!r}; annotation= {annotation!r}.'
            )
        
        # Register event handler
        event_handlers_by_identifier = self._event_handlers_by_identifier
        try:
            event_handlers = event_handlers_by_identifier[annotation.identifier]
        except KeyError:
            event_handlers = []
            event_handlers_by_identifier[annotation.identifier] = event_handlers
        
        event_handlers.append(event_handler)
        
        
        return event_handler
    
    
    def iter_handlers_for_event(self, event):
        """
        Iterates over the event handler which should be called with the given event.
        
        This method is an iterable generator.
        
        Parameters
        ----------
        event : ``EventBase``
            Event instance.
        
        Yields
        ------
        event_handler : `callable`
        """
        try:
            event_handlers = self._event_handlers_by_identifier[event.identifier]
        except KeyError:
            pass
        else:
            yield from event_handlers
    
    
    def copy(self):
        """
        Copies the event handler manager returning a new one.
        
        Returns
        -------
        new : ``EventHandlerManager``
        """
        event_handlers_by_identifier = {}
        
        for event_identifier, event_handlers in self._event_handlers_by_identifier.items():
            event_handlers_by_identifier[event_identifier] = event_handlers.copy()
        
        new = object.__new__(type(self))
        new._event_handlers_by_identifier = event_handlers_by_identifier
        return new
