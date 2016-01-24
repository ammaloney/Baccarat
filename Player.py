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
    bets = {'B':'Banker', 'D':'Dragon', 'P':'Player', 'p':'Panda', 'T':'Tie'}
    
    def __init__(self, aName='Joe'):
        
        self.stake_history = []
        self.name = aName
        self.stake = 0
        self.status = None
        self.verbose = False
        self.bet = Bet(2, self.bankerBet)
        if self.verbose: 
            print('Created player {}'.format(self.name))

    def __str__(self):
        ''' Returns a string
        '''
        return '{0}, current stake: {1}\nStake history {2}'.format(self.name,
            self.stake, self.stake_history)
        
    def place_bet(self, scorecard = None):
        self.bet = Bet(2, self.bankerBet)
        if self.verbose: 
            print('{0} bets {1}'.format(self.name, self.bet))
        self.stake -= self.bet.amount


    def settle_bets(self, decision):
        if self.verbose == True:
            print('{} wins '.format(self.bets[decision]))

        if decision == 'T':
            if (self.bet.outcome.name == 'p'
                or self.bet.outcome.name == 'D'):
                    self.lose()
            else:
                self.push()
        elif (self.bet.outcome.name == decision or
                self.bet.outcome.name == 'P' and decision == 'p'):
            self.win()
        elif self.bet.outcome.name == 'B' and decision == 'D':
            self.push()
        else:
            self.lose()
        
    def win(self):
        self.stake += self.bet.winAmount()
        if self.verbose: 
            print('{} Wins {} stake: {}'
                    .format(self.name, self.bet.amount, self.stake))
        self.stake_history.append(self.stake)
        self.status = 'W'
        
    def lose(self):
        if self.verbose: 
            print('{} Loses {} Stake {}'
                    .format(self.name, self.bet.amount, self.stake))
        self.stake_history.append(self.stake)
        self.status = 'L'
    
    def push(self):
        self.stake += self.bet.amount
        if self.verbose: 
            print('{} Pushes {} Stake {}'
                    .format(self.name, self.bet.amount, self.stake))
        self.stake_history.append(self.stake)
        self.status = 'T'


class BankerFlatBettor(Player):
    '''Player which always bets 2 units on Banker
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Banker Flat'
        self.verbose = False
        if self.verbose: 
            print('Created player {}'.format(self.name))

    def place_bet(self):
        self.bet = Bet(2, self.bankerBet)
        if self.verbose : 
            print('{0} has {2} bets {1}'
                    .format(self.name, self.bet, self.stake))
      
        self.stake -= self.bet.amount
            

class PlayerFlatBettor(Player):
    '''Player which always bets 2 units on Player
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Player Flat'
        self.verbose = False
        if self.verbose: 
            print('Created player {}'.format(self.name))

    def place_bet(self):
        self.bet = Bet(2, self.playerBet)
        if self.verbose : 
            print('{0} has {2} bets {1}'
                    .format(self.name, self.bet, self.stake))
                    
        self.stake -= self.bet.amount


class BankerWinUp1Bettor(BankerFlatBettor):
    '''Player which always bets on Banker and raises the amount
    bet by one unit after every win
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Banker Up 1'
        self.verbose = False
        if self.verbose: 
            print('Created player {}'.format(self.name))

    def place_bet(self):
        if self.status == 'W':
            self.bet = Bet((self.bet.amount + 1), self.bankerBet)
        elif self.status == 'L' or self.status == None:
            self.bet = Bet(2, self.bankerBet)

        if self.verbose : 
            print('{0} has {2} bets {1}'
                    .format(self.name, self.bet, self.stake))
                    
        self.stake -= self.bet.amount


class PlayerWinUp1Bettor(PlayerFlatBettor):
    '''Player which always bets on Player and raises the amount
    bet by one unit after every win
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Player Up 1'
        self.verbose = False
        self.bet = Bet(2, self.playerBet)
        if self.verbose: 
            print('Created player {}'.format(self.name))

    def place_bet(self):
        if self.status == 'W':
            self.bet = Bet((self.bet.amount + 1), self.playerBet)
        elif self.status == 'L' or self.status == None:
            self.bet = Bet(2, self.playerBet)

        if self.verbose : 
            print('{0} has {2} bets {1}'
                    .format(self.name, self.bet, self.stake))
                    
        self.stake -= self.bet.amount


class RepeatWinUp1Bettor(Player):
    '''Player which bets that the second previous outcome will occur
    and raises the amount bet by one unit after every win.
    scorecard is a list of previous outcomes (not including ties)
    to be passed to the place_bet() method
    '''
    def __init__(self):
        super().__init__()
        self.bet = Bet(2, self.bankerBet)
        self.verbose = False
        self.status = None
        self.scorecard = []
        self.name = 'Repeat Up 1'

        if self.verbose: 
            print('Created player {}'.format(self.name))

    def place_bet(self):
#  choose outcome to bet on
        if len(self.scorecard) < 2:
            self.bet.outcome = self.bankerBet
        else:
            if self.scorecard[-2] == 'B':
                self.bet.outcome = self.bankerBet
            elif self.scorecard[-2] == 'P':
                self.bet.outcome = self.playerBet
            else:
                print('ERROR: You should not be able to get here')

#   set amount to bet
        if self.status == 'W':
            amount = self.bet.amount + 1
            self.bet.amount = amount
        elif self.status == 'L' or self.status == None:
            self.bet.amount = 2

        if self.verbose : 
            print('{0} has {2} bets {1}'
                    .format(self.name, self.bet, self.stake))

        self.stake -= self.bet.amount

    def settle_bets(self, decision):
        super().settle_bets(decision)

# update scorecard
        if decision != 'T':
            if decision == 'B' or decision == 'D':
                self.scorecard.append('B')
            elif decision == 'P' or decision == 'p':
                self.scorecard.append('P')


class Banker3of5Bettor(Player):
    '''Player which always bets on Banker. 
    The amount bet is based on a series of five bets (2,3,4,5,6). 
    The series is reset after any two wins. 
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Banker 3of5'
        self.verbose = False
        self.bet = Bet(2, self.bankerBet)
        if self.verbose : 
            print('Created player {}'.format(self.name))
        self.bet_series = [1,2,3,4,5,6]
        self.series_wins = 0
        self.series_length = 1
        
    def place_bet(self):
        if self.series_length > 5 or self.series_wins > 2:
            self.series_length = 1
            self.series_wins = 0
            
        self.bet = Bet(self.bet_series[self.series_length], self.bankerBet)

        if self.verbose : 
            print('{0} has {1} bets {2}'
                    .format(self.name, self.stake, self.bet))
        self.stake -= self.bet.amount

    def win(self):
        super().win()
        self.series_wins += 1
        self.series_length += 1
        if self.series_wins > 1:
            self.series_wins = 0
            self.series_length = 1
        if self.series_length > 5:
            self.series_length = 1
            self.series_wins = 0

    def lose(self):
        super().lose()
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
        self.verbose = False
        if self.verbose : 
            print('Created player {}'.format(self.name))
        self.bet_series = [1,2,3,4,5,6]
        self.series_wins = 0
        self.series_length = 1

    def place_bet(self):
        if self.series_length > 5 or self.series_wins > 2:
            self.series_length = 1
            self.series_wins = 0
        self.bet = Bet(self.bet_series[self.series_length], self.playerBet)

        if self.verbose : 
            print('{0} has {2} bets {1}'
                    .format(self.name, self.bet, self.stake))
        self.stake -= self.bet.amount

    def win(self):
        super().win()
        self.series_wins += 1
        self.series_length += 1
        if self.series_wins > 1:
            self.series_wins = 0
            self.series_length = 1
        if self.series_length > 5:
            self.series_length = 1
            self.series_wins = 0

    def lose(self):
        super().lose()
        self.series_length += 1
        if self.series_length > 5 : 
            self.series_length = 1
            self.series_wins = 0
            if self.verbose == True:
                print('Lost Series\n')


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
        self.bet_series = [1,2,3,4,5,6]
        self.series_wins = 0
        self.series_length = 0
        self.walk = 0
        
    def place_bet(self):
        if self.walk >= 0:
            self.bet = Bet(2 + self.series_length, self.bankerBet)
        elif self.walk < 0:
            self.bet = Bet(2 + self.series_length, self.playerBet)

        if self.verbose : 
            print('Series length: {}\t'.format(self.series_length))
            print('Walk = {}'.format(self.walk))
            print('{0} has {2} bets {1}'
                    .format(self.name, self.bet, self.stake))
                    
        self.stake -= self.bet.amount

    def win(self):
        self.stake += self.bet.winAmount()
        if self.verbose: 
            print('{} Wins {} Stake {}'
                    .format(self.name, self.bet.amount, self.stake))
        self.stake_history.append(self.stake)
        self.series_wins += 1
        self.series_length += 1
        if self.series_wins > 1:
            self.series_wins = 0
            self.series_length = 1
        if self.series_length > 5:
            self.series_length = 1
            self.series_wins = 0

        if (self.bet.outcome.name == 'B' or 
            self.bet.outcome.name == 'D'):
            self.walk += 1

        if (self.bet.outcome.name == 'P' or 
            self.bet.outcome.name == 'p'):
            self.walk -= 1
            
        if self.verbose:
            print('Walk = {}'.format(self.walk))

    def lose(self):
        if self.verbose: 
            print('{} Loses. Stake {}'
                    .format(self.name, self.stake))
        self.stake_history.append(self.stake)
        self.series_length += 1
        if self.series_length > 5 : 
            self.series_length = 1
            self.series_wins = 0

        if (self.bet.outcome.name == 'B' or 
            self.bet.outcome.name == 'D'):
            self.walk += 1

        if (self.bet.outcome.name == 'P' or 
            self.bet.outcome.name == 'p'):
            self.walk -= 1

        if self.verbose:
            print('Walk = {}'.format(self.walk))



