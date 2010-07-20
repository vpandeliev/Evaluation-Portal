'''
Classes:
    ChoiceList
'''


class ChoiceList(object):

    """ChoiceList object.

    Instantiate by passing a multiline string, with names of each
    choice on single lines. For example,

    >>> choices = ChoiceList('''
    ... First Choice
    ... Second Choice
    ... Final
    ... ''')

    Each choice is assigned an integer identifier. They can be accessed
    as follows:

    >>> choices.FIRST_CHOICE
    1
    >>> choices.SECOND_CHOICE
    2
    >>> choices.FINAL
    3

    See ChoiceList.attributize for exact conversion process.
    
    Also, choices features an 'as_choices' method which returns a list
    of 2-tuples ideal for use in a models or form field. For example:

    >>> choices.as_choices(blank=True)
    ((0, '------'), (1, 'First Choice'), (2, 'Second Choice'), (3, 'Final'))
    >>> choices.as_choices()
    ((1, 'First Choice'), (2, 'Second Choice'), (3, 'Final'))

    >>> choices.verbose(choices.FIRST_CHOICE)
    'First Choice'

    >>> choices.find_match('first CHOICE')
    1
    >>> choices.find_match('not a choice')
    0

    #   class Order(models.Model):
    #       choice = models.IntegerField(choices=choices.as_choices())
    
    """

    def __init__(self, initializer):
        lines = [line.strip() for line in initializer.split('\n') if line.strip()]
        self._verbose = map(self.verbositize, lines)
        self._choices = map(self.attributize, lines)
        for i, attr in enumerate(self._choices):
            setattr(self, attr, i + 1)

    def attributize(self, line):
        return line.upper().replace(' ', '_')

    def verbositize(self, line):
        return line
        
    def as_choices(self, blank=False):
        X = zip(range(1, len(self._verbose) + 1), self._verbose)
        return tuple((blank and [(0, '------')] or []) + X)

    def verbose(self, index):
        return self._verbose[int(index) - 1]

    def tag(self, index):
        return self._choices[int(index) - 1]

    def find_match(self, verbose):
        for v, c, i in zip(self._choices, self._verbose, range(1, len(self._choices) + 1)):
            if verbose.lower() in (v.lower(), c.lower()):
                return i
        return 0

    def add_properties(self, model, field):
        '''Adds methods and properties to a model for a field that uses this.
        
        For example:
            
            class Foo(models.Model):
                animal = models.IntegerField(choices=animals.as_choices())
            animals.add_properties(Foo, 'animal')
        
        Now Foo has a method _animal ideal for use in django admin, and
        also a property animal_verbose which is a short cut for
        animals.verbose(foo.animal)
        '''
        def _get(this):
            return self.verbose(getattr(this, field))
        _get.short_description = field.capitalize()
        _get.admin_order_field = field
        setattr(model, '_%s' % field, _get)
        setattr(model, '%s_verbose' % field, property(_get))


###############################################################################
        
def _test():
    import doctest
    doctest.testmod()

if __name__ == "__main__":
    _test()
