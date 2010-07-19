class Immutable(object):
    '''
    >>> class Foo(Immutable):
    ...     @mutator
    ...     def change(self):
    ...         print 'Changing...'
    >>> foo = Foo()
    >>> foo.change()
    Changing...
    >>> foo.freeze()
    >>> try:
    ...     foo.change()
    ... except Immutable.MutatorCalledOnFrozenObject:
    ...     print 'Exception raised'
    Exception raised
    '''
    
    is_frozen = property(lambda self: getattr(self, '_frozen', False))
    
    def freeze(self):
        self._frozen = True
    
    class MutatorCalledOnFrozenObject(Exception): pass
    

def mutator(method):
    '''
    Mark a method as a mutator. Once an object is frozen,
    the method will raise an exception.
    '''
    def wrapper(self, *args, **kwargs):
        if self.is_frozen:
            raise Immutable.MutatorCalledOnFrozenObject()
        return method(self, *args, **kwargs)
    wrapper.__name__ = method.__name__
    return wrapper
