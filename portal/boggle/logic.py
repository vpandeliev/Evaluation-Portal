import re
from random import random


_scores = (
    0,
    0, 0, 1, 1,
    2, 3, 5, 11,
    11, 11, 11, 11,
    11, 11, 11, 11,
    )
    

def score_for_word(word):
    return _scores[len(word)]


class BoggleDice(object):
    
    '''
    >>> dice = BoggleDice()
    >>> len(list(dice))
    16
    '''
    
    dice = (
        'AAEEGN',
        'ELRTTY',
        'AOOTTW',
        'ABBJOO',
        'EHRTVW',
        'CIMOTU',
        'DISTTY',
        'EIOSST',
        'DELRVY',
        'ACHOPS',
        'HIMNQU',
        'EEINSU',
        'EEGHNW',
        'AFFKPS',
        'HLNNRZ',
        'DEILRX',
        )
    
    def __init__(self):
        self.dice = list(self.dice)
    
    def __iter__(self):
        while self.dice:
            i = int(random() * len(self.dice))
            yield self.roll(self.dice.pop(i))
    
    @staticmethod
    def roll(die):
        i = int(random() * len(die))
        return die[i]

        
_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
_freq = 'EEEEEEEEEEEEEEEEEEEEEEEIIIIIIIIIIIIIIIIISSSSSSSSSSSSSSSSAAAAAAAAAAAAAAAARRRRRRRRRRRRRRRNNNNNNNNNNNNNNNTTTTTTTTTTTTTOOOOOOOOOOOOLLLLLLLLLLLCCCCCCCCDDDDDDDUUUUUUGGGGGGPPPPPPMMMMMMHHHHBBBBYYYFFFVVKKWWZXJQ'


def random_letter():
    a = _freq
    i = int(random() * len(a))
    return a[i]


def get_shuffled_board():
    '''
    A 4x4 board such as this:
        A G I X
        A B T S
        P Q Z I
        O D X L
    Is represented as this:
        "AGIXABTSPQZIODXL"
    '''
    return ''.join(list(BoggleDice()))


class Board(object):
    
    def __init__(self, cells):
        self._cells = cells
    
    def __getitem__(self, item):
        assert re.match(r'\d\d', item), 'Invalid cell %s' % item
        i, j = map(int, item)
        return self._cells[i*4+j]
