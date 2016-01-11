# -*- coding: utf-8 -*-
"""
Player.py

This module implements the base class and subclasses of Player.

@author: amaloney
"""

from baccarat import Outcome, Bet

class Player():
    """Base class to represent a player at a gambling table.
    I know my name and current stake and keep a history of my stake.
    place_bet() is where the betting strategy is implemented
    and will be over-ridden by subclasses.

    """
    def __init__(self, aName='Joe'):
        
        self.stake_history = []
        self.name = aName
        self.stake = 0
        self.status = None
        print('Created player {}'.format(self.name))

    def __str__(self):
        ''' Returns a string
        '''
        return '{0}, current stake: {1}\nStake history {2}'.format(self.name,
            self.stake, self.stake_history)
        
    def place_bet(self):
        bankerBet = Outcome('B', 1)
        self.nextBet = Bet(2, bankerBet)
#        print('{0} bets {1}'.format(self.name, self.nextBet))
        self.stake -= self.nextBet.amount
        return self.nextBet

    def win(self, aBet):
        self.stake += 2     # subclasses will override this
#        self.stake += aBet.winAmount()
        self.stake_history.append(self.stake)
        self.status = 'W'
        
    def lose(self, aBet):
        self.stake -= self.nextBet.amount
        self.stake_history.append(self.stake)
        self.status = 'L'
    
    def push(self, aBet):
#        self.stake += aBet.amount
        self.stake_history.append(self.stake)
        self.status = 'P'


class BankerFlatBettor(Player):
    pass