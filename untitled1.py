# -*- coding: utf-8 -*-
"""
Created on Fri Jan  8 10:19:58 2016

@author: amaloney
"""
class Player:
    def __init__(self, aName = 'Joe'):
        
        self.stake_history = []
        self.name = aName
        self.stake = 0
        print('Created a player named {}'.format(self.name)

    def place_bet(self, anAmount, anOutcome):
        self.nextBet = Bet(anAmount, anOutcome)
        print('{0} bets {1}'.format(self.name, self.nextBet))
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

class BankBettor(Player):
    def __init__(self, name = 'Bank Bettor'):
        self.name = name
