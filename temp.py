# -*- coding: utf-8 -*-
"""
Created on Fri Oct 16 13:13:22 2015

@author: amaloney
"""


class Bin():
        
    def __init__(self, *argv):
        self.outcomes = frozenset(argv)
        
        print(self.outcomes)
        
    def add(self, outcome):                               
        self.outcomes |= set([outcome])
        
    def __str__(self):
        return '([{}])'.format(', '.join( map(str,self.outcomes)))
    
    
if __name__ == "__main__":
    from baccarat import Outcome
    zero = Outcome("0",35)
    zerozero = Outcome("00",35)

    b0 = Bin(zero)
    print(b0)
    b0.add(zerozero)
    print(b0)
    
    