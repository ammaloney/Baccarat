# -*- coding: utf-8 -*-
"""
Player.py

I represent a player at a Baccarat table. I know my bankroll and betting
strategy. My betting strategy consists of the outcome I will bet on and
the amount of the bet. 

@author: amaloney
"""


class Bet():
    def __init__(self, anAmount, anOutcome):
        self.amount = anAmount
        self.outcome = anOutcome

    def __str__(self):
        return "{0} on {1}".format(self.amount, self.outcome.name)

    def winAmount(self):
        return (self.amount * self.outcome.odds) + self.amount

    def pushAmount(self):
        return self.amount

class Player():
    def __init__(self, aName='Joe'):
        
        self.stake_history = []
        self.name = aName
        self.stake = 0
        print('Created player {}'.format(self.name))

    def __str__(self):
        ''' Returns a string
        '''
        return '{0}, current stake: {1}\nStake history {2}'.format(self.name,
            self.stake, self.stake_history)
        
    
    def place_bet(self, anAmount=1, anOutcome='bankerBet'):
        self.nextBet = Bet(anAmount, anOutcome)
        print('{0} bets {1}'.format(self.name, self.nextBet))
        self.stake -= anAmount
        return self.nextBet

    def win(self, aBet):
        self.stake += aBet.winAmount()
        self.stake_history.append(self.stake)
        
    def lose(self, aBet):
        self.stake_history.append(self.stake)
    
    def push(self, aBet):
        self.stake += aBet.amount
        self.stake_history.append(self.stake)
    