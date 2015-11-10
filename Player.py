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

    def loseAmount(self):
        return self.amount

class Player():
    def __init__(self, aName, initial_stake=200):
        
        self.stake = initial_stake
        self.stake_history = []
        self.name = aName
    
    def place_bet(self, anOutcome, anAmount):
        self.bet_on = anOutcome
        self.bet_amount = anAmount
        