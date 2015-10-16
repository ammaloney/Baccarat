# -*- coding: utf-8 -*-
"""
Contains the following classes for Baccarat simulation:

Bin, Outcome, Table, Game, Bet

@author: amaloney
"""

class Bin():
    """ Bin contains a collection of Outcomes which reflect the winning bets 
    that are paid for a particular bin on a Roulette wheel. 
    In Roulette, each spin of the wheel has a number of Outcomes. 
    Example: A spin of 1, selects the "1" bin with the following winning 
    Outcomes: "1", "Red", "Odd", "Low", "Column 1", "Dozen 1-12", "Split 1-2",
    "Split 1-4", "Street 1-2-3", "Corner 1-2-4-5", "Five Bet", 
    "Line 1-2-3-4-5-6", and "00-0-1-2-3". 
    These are collected into a single Bin.
    """
    pass
#    def __init__(self, *outcomes):
#        for anOutcome in outcomes:
#            self.outcomes = outcomes
    
class Outcome():
    """ Outcome contains a single outcome on which a bet can be placed.
    An Outcome will contain the name of the outcome as a String, and the 
    odds that are paid as an integer.
    
    >>> oc1 = Outcome( "Any Craps", 8 )
    >>> oc2 = Outcome( "Any Craps", 8 )
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
        
    def winAmount(self, amount):
        return self.odds * amount


if __name__ == "__main__":
    import doctest
    doctest.testmod()
