import re
from random import random
from choices import *


class BoggleDice(object):
    
    '''
    >>> len(BoggleDice().shuffle().split())
    16
    
    >>> d = BoggleDice()
    >>> d.shuffle() != d.shuffle()
    True
    >>> len(d.shuffle().split())
    16
    
    >>> w = BoggleDice("""
    ...     AAAAAA AAAAAA AAAAAA AAAAAA
    ...     AAAAAA AAAAAA AAAAAA AAAAAA
    ...     BBBBBB BBBBBB BBBBBB BBBBBB
    ...     BBBBBB BBBBBB BBBBBB QQQQQQ
    ... """).shuffle()
    >>> w.count('A')
    8
    >>> w.count('B')
    7
    >>> w.count('Qu')
    1
    
    >>> w = BoggleDice("""
    ...     AAAAAA AAAAAA AAAAAA AAAAAA
    ...     AAAAAA AAAAAA AAAAAA AAAAAA
    ...     AAAAAA AAAAAA AAAAAA AAAAAA
    ...     AAAAAA AAAAAA AAAAAA AAAAAA        
    ...     """, special_die="BBBBBB").shuffle()
    >>> w.count('A')
    15
    >>> w.count('*B')
    1
    '''
    
    default_dice = '''
        AAEEGN ELRTTY AOOTTW ABBJOO
        EHRTVW CIMOTU DISTTY EIOSST
        DELRVY ACHOPS HIMNQU EEINSU
        EEGHNW AFFKPS HLNNRZ DEILRX
    '''
            
    def __init__(self, dice=None, special_die=None):
        self._dice = [d.strip() for d in (dice or self.default_dice).strip().split()]
        self._special = special_die
    
    def __iter__(self):
        dice = list(self._dice)
        if self._special:
            i = int(random() * len(dice))
            dice[i] = '*' + self._special
        while dice:
            i = int(random() * len(dice))
            die = dice.pop(i)
            c = self.roll(die.lstrip('*'))
            if c == 'Q':
                c = 'Qu'
            if die.startswith('*'):
                # Special die
                c = '*' + c
            yield c 
    
    def shuffle(self):
        return ' '.join(list(self))
        
    @staticmethod
    def roll(die):
        i = int(random() * len(die))
        return die[i]
        

class LogicMode(object):
    
    def __init__(self):
        self._mode_map = {
            boggle_modes.NORMAL: self.normal,
            boggle_modes.MASTER: self.master,
            boggle_modes.CHALLENGE_CUBE: self.challenge_cube,
            }
            
    def __getitem__(self, mode):
        return self._mode_map[mode]


class Scoring(LogicMode):
    
    _scores = (
        0,
        0, 0, 1, 1,
        2, 3, 5, 11,
        11, 11, 11, 11,
        11, 11, 11, 11,
        )
    
    def normal(self, word):
        return self._scores[len(word)]

    def master(self, word):
        return self.normal(word)

    def challenge_cube(self, word):
        return self.normal(word)
scoring = Scoring()


class Shuffler(LogicMode):

    def normal(self):
        return BoggleDice().shuffle()

    def master(self):
        return BoggleDice("""
            AAEEGN ELRTTY AOOTTW ABBJOO
            EHRTVW CIMOTU DISTTY EIOSST
            DELRVY ACHOPS HIMNQU EEINSU
            EEGHNW AFFKPS HLNNRZ DEILRX
        """).shuffle()

    def challenge_cube(self):
        return BoggleDice(special_die="QQQQQQ").shuffle()
shuffler = Shuffler()


def _test():
    import doctest
    doctest.testmod()
 
if __name__ == "__main__":
    _test()
