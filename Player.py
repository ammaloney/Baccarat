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
        self.status = None
        self.verbose = False
        self.nextBet = Bet(2, self.bankerBet)
        if self.verbose: 
            print('Created player {}'.format(self.name))

    def __str__(self):
        ''' Returns a string
        '''
        return '{0}, current stake: {1}\nStake history {2}'.format(self.name,
            self.stake, self.stake_history)
        
    def place_bet(self, scorecard = None):
        self.nextBet = Bet(2, self.bankerBet)
        if self.verbose: 
            print('{0} bets {1}'.format(self.name, self.nextBet))
        self.stake -= self.nextBet.amount
#        return self.nextBet

    def settle_bets(self, decision):
        if self.nextBet.outcome.name == decision:
            self.win()
        elif decision == 'T' and (self.nextBet.outcome.name != 'p'
                                  or self.nextBet.outcome.name != 'D'):
            self.push()
        elif self.nextBet.outcome.name == 'P' and decision == 'p':
            self.win()
        elif self.nextBet.outcome.name == 'B' and decision == 'D':
            self.push()
        else:
            self.lose()
        
    def win(self):
        self.stake += self.nextBet.winAmount()
        if self.verbose: 
            print('{} Wins {} stake: {}'
                    .format(self.name, self.nextBet.amount, self.stake))
        self.stake_history.append(self.stake)
        self.status = 'W'
        
    def lose(self):
        if self.verbose: 
            print('{} Loses {} Stake {}'
                    .format(self.name, self.nextBet.amount, self.stake))
        self.stake_history.append(self.stake)
        self.status = 'L'
    
    def push(self):
        self.stake += self.nextBet.amount
        if self.verbose: 
            print('{} Pushes {} Stake {}'
                    .format(self.name, self.nextBet.amount, self.stake))
        self.stake_history.append(self.stake)
        self.status = 'T'


class BankerFlatBettor(Player):
    '''Player which always bets 2 units on Banker
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Banker Flat'
        if self.verbose: 
            print('Created player {}'.format(self.name))

    def place_bet(self):
        self.nextBet = Bet(2, self.bankerBet)
        if self.verbose : 
            print('{0} has {2} bets {1}'
                    .format(self.name, self.nextBet, self.stake), end='')
                    
        self.stake -= self.nextBet.amount
        if self.verbose:
            print('\tStake: {}'.format(self.stake))
#        return self.nextBet


class PlayerFlatBettor(Player):
    '''Player which always bets 2 units on Player
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Player Flat'
        if self.verbose: 
            print('Created player {}'.format(self.name))

    def place_bet(self):
        self.nextBet = Bet(2, self.playerBet)
        if self.verbose : 
            print('{0} has {2} bets {1}'
                    .format(self.name, self.nextBet, self.stake), end='')
                    
        self.stake -= self.nextBet.amount
        if self.verbose:
            print('\tStake: {}'.format(self.stake))
#        return self.nextBet


class BankerWinUp1Bettor(BankerFlatBettor):
    '''Player which always bets on Banker and raises the amount
    bet by one unit after every win
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Banker Up 1'
        if self.verbose: 
            print('Created player {}'.format(self.name))

    def place_bet(self):
        if self.status == 'W':
            self.nextBet = Bet((self.nextBet.amount + 1), self.bankerBet)
        elif self.status == 'L':
            self.nextBet = Bet(2, self.bankerBet)

        if self.verbose : 
            print('{0} has {2} bets {1}'
                    .format(self.name, self.nextBet, self.stake), end='')
                    
        self.stake -= self.nextBet.amount
        if self.verbose:
            print('\tStake: {}'.format(self.stake))
#        return self.nextBet


class PlayerWinUp1Bettor(PlayerFlatBettor):
    '''Player which always bets on Player and raises the amount
    bet by one unit after every win
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Player Up 1'
        if self.verbose: 
            print('Created player {}'.format(self.name))

    def place_bet(self):
        if self.status == 'W':
            self.nextBet = Bet((self.nextBet.amount + 1), self.playerBet)
        elif self.status == 'L':
            self.nextBet = Bet(2, self.playerBet)

        if self.verbose : 
            print('{0} has {2} bets {1}'
                    .format(self.name, self.nextBet, self.stake), end='')
                    
        self.stake -= self.nextBet.amount
        if self.verbose:
            print('\tStake: {}'.format(self.stake))
        return self.nextBet


class RepeatWinUp1Bettor(BankerFlatBettor):
    '''Player which bets that the second previous outcome will occur
    and raises the amount bet by one unit after every win.
    BvsP is a list of previous outcomes (not including ties)
    to be passed to the place_bet() method
    '''
    def __init__(self):
        super().__init__()
        self.verbose = False
        self.status = None
        self.name = 'Repeat Up 1'
        if self.verbose: 
            print('Created player {}'.format(self.name))

    def place_bet(self, BvsP):
        if self.status == 'W':
            amount = (self.nextBet.amount + 1)
        elif self.status == 'L' or self.status == None:
            amount = 2

        if len(BvsP) < 3:
            self.nextBet = Bet(amount, self.bankerBet)
            if self.verbose : 
                print('{0} has {2} bets {1}'
                        .format(self.name, self.nextBet, self.stake), end='')
                        
            self.stake -= self.nextBet.amount
            if self.verbose:
                print('\tStake: {}'.format(self.stake))
#            return self.nextBet
        else:
            self.nextBet.outcome.name = BvsP[-2]
            if self.verbose : 
                print('{0} has {2} bets {1}'
                        .format(self.name, self.nextBet, self.stake), end='')
                        
            self.stake -= self.nextBet.amount
            if self.verbose:
                print('\tStake: {}'.format(self.stake))
#            return self.nextBet
    def settle_bets(self, decision):
        Player.settle_bets(self, decision)
        


class Banker3of5Bettor(Player):
    '''Player which always bets on Banker. 
    The amount bet is based on a series of five bets (2,3,4,5,6). 
    The series is reset after any two wins. 
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Banker 3of5'
        self.verbose = False
        if self.verbose : 
            print('Created player {}'.format(self.name))
        self.series_wins = 0
        self.series_length = 1
        
    def place_bet(self):
        if self.series_length > 5 or self.series_wins > 2:
            self.series_length = 1
            self.series_wins = 0
        self.nextBet = Bet(1 + self.series_length, self.bankerBet)
        if self.verbose : 
            print('{0} has {2} bets {1}'
                    .format(self.name, self.nextBet, self.stake), end='')
                    
        self.stake -= self.nextBet.amount
        if self.verbose:
            print('\tStake: {}'.format(self.stake))
        return self.nextBet

    def win(self):
        self.stake += self.nextBet.winAmount()
        if self.verbose: 
            print('{} Wins {} Stake {}'
                    .format(self.name, self.nextBet.amount, self.stake))
        self.stake_history.append(self.stake)
        self.series_wins += 1
        self.series_length += 1
        if self.series_wins > 1:
            self.series_wins = 0
            self.series_length = 1
        if self.series_length > 5:
            self.series_length = 1
            self.series_wins = 0

    def lose(self):
        if self.verbose: 
            print('{} Loses. Stake {}'
                    .format(self.name, self.stake))
        self.stake_history.append(self.stake)
        self.series_length += 1
        if self.series_length > 5 : 
            self.series_length = 1
            self.series_wins = 0
        

class Player3of5Bettor(Player):
    '''Player which always bets on Banker. 
    The amount bet is based on a series of five bets (2,3,4,5,6). 
    The series is reset after any two wins. 
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Player 3of5'
        if self.verbose : 
            print('Created player {}'.format(self.name))
        self.series_wins = 0
        self.series_length = 1
        
    def place_bet(self):
        if self.series_length > 5 or self.series_wins > 2:
            self.series_length = 1
            self.series_wins = 0
        self.nextBet = Bet(1 + self.series_length, self.playerBet)
        if self.verbose : 
            print('{0} has {2} bets {1}'
                    .format(self.name, self.nextBet, self.stake), end='')
                    
        self.stake -= self.nextBet.amount
        if self.verbose:
            print('\tStake: {}'.format(self.stake))
        return self.nextBet

    def win(self):
        self.stake += self.nextBet.winAmount()
        if self.verbose: 
            print('{} Wins {} Stake {}'
                    .format(self.name, self.nextBet.amount, self.stake))
        self.stake_history.append(self.stake)
        self.series_wins += 1
        self.series_length += 1
        if self.series_wins > 1:
            self.series_wins = 0
            self.series_length = 1
        if self.series_length > 5:
            self.series_length = 1
            self.series_wins = 0

    def lose(self):
        if self.verbose: 
            print('{} Loses. Stake {}'
                    .format(self.name, self.stake))
        self.stake_history.append(self.stake)
        self.series_length += 1
        if self.series_length > 4 : 
            self.series_length = 0
            self.series_wins = 0
        

class Walk3of5Bettor(Player):
    '''Player which bets on the outcome that has happened most frequently. 
    The amount bet is based on a series of five bets (2,3,4,5,6). 
    The series is reset after any two wins. 
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Walk 3-5'
        self.verbose = False
        if self.verbose : 
            print('Created player {}'.format(self.name))
        self.series_wins = 0
        self.series_length = 0
        self.walk = 0
        
    def place_bet(self):
        if self.walk >= 0:
            self.nextBet = Bet(2 + self.series_length, self.bankerBet)
        elif self.walk < 0:
            self.nextBet = Bet(2 + self.series_length, self.playerBet)

        if self.verbose : 
            print('Series length: {}\t'.format(self.series_length), end='')
            print('Walk = {}'.format(self.walk))
            print('{0} has {2} bets {1}'
                    .format(self.name, self.nextBet, self.stake), end='')
                    
        self.stake -= self.nextBet.amount
        if self.verbose:
            print('\tStake: {}'.format(self.stake))
        return self.nextBet

    def win(self):
        self.stake += self.nextBet.winAmount()
        if self.verbose: 
            print('{} Wins {} Stake {}'
            .format(self.name, self.nextBet.amount, self.stake), end=' ')
        self.stake_history.append(self.stake)
        self.series_wins += 1
        self.series_length += 1
        if self.series_wins > 1:
            self.series_wins = 0
            self.series_length = 0

        if self.series_length > 4:
            self.series_length = 0
            self.series_wins = 0

        if self.nextBet.outcome.name == 'B' or \
            self.nextBet.outcome.name == 'D':
            self.walk += 1

        if self.nextBet.outcome.name == 'P' or \
            self.nextBet.outcome.name == 'p':
            self.walk -= 1
            
        if self.verbose:
            print('Walk = {}'.format(self.walk))

    def lose(self):
        if self.verbose: 
            print('{} Loses. Stake {}'
                    .format(self.name, self.stake), end=' ')
        self.stake_history.append(self.stake)
        self.series_length += 1
        if self.series_length > 4: 
            self.series_length = 0
            self.series_wins = 0
        if self.nextBet.outcome.name == 'B' or \
            self.nextBet.outcome.name == 'D':
            self.walk += 1
        if self.nextBet.outcome.name == 'P' or \
            self.nextBet.outcome.name == 'p':
            self.walk -= 1
        if self.verbose:
            print('Walk = {}'.format(self.walk))



