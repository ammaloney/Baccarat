# -*- coding: utf-8 -*-
"""
Contains the following classes for Baccarat simulation:

Outcome, Table, Game, Bet

@author: amaloney
"""

    
class Outcome():
    """ Outcome contains a single outcome on which a bet can be placed.
    An Outcome will contain the name of the outcome as a String, and the 
    odds that are paid as an integer.
    
    >>> oc1 = Outcome( "Tie", 9 )
    >>> oc2 = Outcome( "Tie", 9 )
    >>> oc3 = Outcome( "dummy", 3)
    >>> oc1 == oc2
    True
    >>> oc1.winAmount(3)
    24
    >>> oc1 == oc3
    False
    
    """
    
    def __init__(self, name, odds):
        self.name = name
        self.odds = odds
        
    def __eq__(self, other):
        if self.name == other.name:
            return True
        else:
            return False
        
    def __str__(self):
        return "{} ({:d}:1)".format(self.name, self.odds)
        
    def __hash__(self):
        return hash(self.name)
    
    def winAmount(self, amount):
        return self.odds * amount

class Bet():
    """Bet contains an Outcome and an amount bet that the outcome will occur.
    
    """
    def __init__(self, anAmount, anOutcome):
        self.amount = anAmount
        self.outcome = anOutcome

    def __str__(self):
        return "{} on {}".format(self.amount, self.outcome.name)

    def winAmount(self):
        return (self.amount * self.outcome.odds) + self.amount

    def pushAmount(self):
        return self.amount


class Table():
    '''
    '''
    def __init__(self):
        self.bets = []




if __name__ == "__main__":
#    import doctest
#    doctest.testmod(verbose=False, optionflags=doctest.ELLIPSIS)
    pass
