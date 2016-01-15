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
    bankerBet = Outcome('B', 1)
    dragonBet = Outcome('D', 40)
    playerBet = Outcome('P', 1)
    pandaBet = Outcome('p', 25)
    tieBet = Outcome('T', 9)
    
    def __init__(self, aName='Joe'):
        
        self.stake_history = []
        self.name = aName
        self.stake = 0
        self.wl_list = []
        self.status = None
        self.verbose = False
        if self.verbose: print('Created player {}'.format(self.name))

    def __str__(self):
        ''' Returns a string
        '''
        return '{0}, current stake: {1}\nStake history {2}'.format(self.name,
            self.stake, self.stake_history)
        
    def place_bet(self):
        self.nextBet = Bet(2, self.bankerBet)
        if self.verbose: print('\n{0} bets {1}'.format(self.name, self.nextBet))
        self.stake -= self.nextBet.amount
        return self.nextBet

    def win(self, aBet):
        self.stake += aBet.winAmount()
        if self.verbose: print('{} Wins {}'.format(self.name, aBet.winAmount()))
        self.stake_history.append(self.stake)
        self.status = 'W'
        self.wl_list.append(self.status)
        
    def lose(self, aBet):
        if self.verbose: print('{} Loses {}'.format(self.name, aBet.amount))
        self.stake_history.append(self.stake)
        self.status = 'L'
        self.wl_list.append(self.status)
    
    def push(self, aBet):
        self.stake += aBet.amount
        if self.verbose: print('{} Pushes {}'.format(self.name, aBet.amount))
        self.stake_history.append(self.stake)


class BankerFlatBettor(Player):
    def __init__(self):
        super().__init__()
        self.name = 'Banker Flat'
        if self.verbose: print('Created player {}'.format(self.name))

    def place_bet(self):
        self.nextBet = Bet(2, self.bankerBet)
        if self.verbose : print('{0} bets {1}'.format(self.name, self.nextBet))
        self.stake -= self.nextBet.amount
        return self.nextBet


class PlayerFlatBettor(Player):
    def __init__(self):
        super().__init__()
        self.name = 'Player Flat'
        if self.verbose: print('Created player {}'.format(self.name))

    def place_bet(self):
        self.nextBet = Bet(2, self.playerBet)
        if self.verbose : print('{0} bets {1}'.format(self.name, self.nextBet))
        self.stake -= self.nextBet.amount
        return self.nextBet


class Banker3of5Bettor(Player):
    def __init__(self):
        super().__init__()
        self.name = 'Banker 3of5'
        if self.verbose : print('Created player {}'.format(self.name))
        self.series_wins = 0
        self.series_length = 0
        
    def place_bet(self):
        if self.series_length > 5 or self.series_wins > 2:
            self.series_length = 0
            self.series_wins = 0
        self.nextBet = Bet(2 + self.series_length, self.bankerBet)
        if self.verbose: print('{0} bets {1}'.format(self.name, self.nextBet))
        self.stake -= self.nextBet.amount
        return self.nextBet

    def win(self, aBet):
        self.stake += aBet.winAmount()
        if self.verbose: print('{} Wins {}'.format(self.name, aBet.winAmount()))
        self.stake_history.append(self.stake)
        self.series_length += 1
        self.series_wins += 1

    def lose(self, aBet):
        if self.verbose: print('{} Loses {}'.format(self.name, aBet.amount))
        self.stake_history.append(self.stake)
        self.series_length += 1
        if self.series_length > 5 : print('Lost Series')