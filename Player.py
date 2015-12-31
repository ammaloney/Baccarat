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
        return "{} on {}".format(self.amount, self.outcome.name)

    def winAmount(self):
        return (self.amount * self.outcome.odds) + self.amount

    def pushAmount(self):
        return self.amount

class Player():
#    def __init__(self, aName, initial_stake=200):
    def __init__(self, aName='Joe'):
        
#        self.stake = initial_stake
        self.stake_history = []
#        self.wlp_history = []
        self.name = aName
        self.stake = 0
    
    def place_bet(self, anAmount=1, anOutcome='bankerBet'):
        self.nextBet = Bet(anAmount, anOutcome)
        self.stake -= int(anAmount)
        return self.nextBet

    def win(self, aBet):
        self.stake += aBet.winAmount
        self.stake_history.append(self.stake)
        
    def lose(self, aBet):
        self.stake_history.append(self.stake)
    
    def push(self, aBet):
        self.stake += aBet.amount
        self.stake_history.append(self.stake)
    