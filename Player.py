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
        self.walk = 0
        self.walk_history = []
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
        
    def percentChange(self, startPoint, currentPoint):
        try:
            if startPoint == 0 :
                startPoint = 1
                currentPoint += 1
            return((currentPoint - startPoint) / abs(startPoint)) * 100.00
        except:
            return 0

    def place_bet(self, scorecard = None):
        self.bet = Bet(2, self.bankerBet)
        if self.verbose: 
            print('{0} bets {1}'.format(self.name, self.bet))
        self.stake -= self.bet.amount

    def update_walk(self, decision):
        if decision == 'B' or decision == 'D':
            self.walk += 1
        elif decision == 'P' or decision == 'p':
            self.walk -= 1

        self.walk_history.append(self.walk)
    
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
        self.update_walk(decision)
        
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


class PatternWinUp1Bettor(Player):
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
        self.name = 'Pattern Up 1'

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


class Banker2of5Bettor(Player):
    '''Player which always bets on Banker. 
    The amount bet is based on a series of five bets (2,3,4,5,6). 
    The series is reset after any two wins. 
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Banker 2of5'
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


class Player2of5Bettor(Player):
    '''Player which always bets on Banker. 
    The amount bet is based on a series of five bets (2,3,4,5,6). 
    The series is reset after any two wins. 
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Player 2of5'
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


class Walk2of5Bettor(Player):
    '''Player which bets on the outcome that has happened most frequently. 
    The amount bet is based on a series of five bets (2,3,4,5,6). 
    The series is reset after any two wins. 
    '''
    def __init__(self):
        super().__init__()
        self.name = 'Walk 2-5'
        self.verbose = False
        if self.verbose : 
            print('Created player {}'.format(self.name))
        self.bet_series = [1,2,3,5,7,9]
        self.series_wins = 0
        self.series_length = 1
        self.walk = 0
        self.trend = 0
        
    def place_bet(self):
# amount to bet
        if self.series_length > 5 or self.series_wins > 2:
            self.series_length = 1
            self.series_wins = 0
            
        self.bet.amount = self.bet_series[self.series_length]
# Which outcome to bet on
        if len(self.walk_history) < 5:
            if self.walk >= 0:
                self.bet.outcome =  self.bankerBet
            elif self.walk < 0:
                self.bet.outcome =  self.playerBet
        else :
            if len(self.stake_history) % 5 == 0:
                self.trend = self.percentChange(self.walk_history[-5],
                                           self.walk_history[-1])
                if self.trend >= 0 :
                    self.bet.outcome = self.bankerBet
                else:
                    self.bet.outcome = self.playerBet

        if self.verbose : 
            print('Series length: {}\t'.format(self.series_length))
            print('Walk = {} Trend = {}'.format(self.walk, self.trend))
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

    def lose(self):
        if self.verbose: 
            print('{} Loses. Stake {}'
                    .format(self.name, self.stake))
        self.stake_history.append(self.stake)
        self.series_length += 1
        if self.series_length > 5 : 
            self.series_length = 1
            self.series_wins = 0
            if self.verbose:
                print('Lost series')

class Stake2of5Bettor(Walk2of5Bettor):
    '''Player which changes outcome to be on based on the net stake after the 
    previous five bets. If the stake has lost money change sides, if not
    continue betting the same outcome.   
    The amount bet is based on a series of five bets (2,3,4,5,6). 
    The series is reset after any two wins. 
    '''
    def __init__(self):
        super().__init__()
        self.verbose = False
        self.name = 'Stake 2of5'
        if self.verbose : 
            print('Created player {}'.format(self.name))

    def place_bet(self):
# amount to bet
        if self.series_length > 5 or self.series_wins > 2:
            self.series_length = 1
            self.series_wins = 0
            
        self.bet.amount = self.bet_series[self.series_length]
# Which outcome to bet on
        if len(self.walk_history) < 5:
            if self.walk >= 0:
                self.bet.outcome =  self.bankerBet
            elif self.walk < 0:
                self.bet.outcome =  self.playerBet
        else:
            if len(self.stake_history) % 5 == 0:
                currentBetOutcome = self.bet.outcome
                self.trend = self.percentChange(self.stake_history[-5],
                                           self.stake_history[-1])
                if self.trend >= 0 :
                    self.bet.outcome = currentBetOutcome
                else:
                    if self.verbose : 
                        print('Switch sides')
                    if currentBetOutcome == self.bankerBet:
                        self.bet.outcome = self.playerBet
                    elif currentBetOutcome == self.playerBet:
                        self.bet.outcome = self.bankerBet

        if self.verbose : 
            print('Series length: {}\t'.format(self.series_length))
            print('Walk = {} Trend = {}'.format(self.walk, self.trend))
            print('{0} has {2} bets {1}'
                    .format(self.name, self.bet, self.stake))
                    
        self.stake -= self.bet.amount


class Pattern2of5Bettor(PatternWinUp1Bettor):
    '''Player which bets that the second previous outcome will occur
    and raises the amount bet by one unit after every win.
    scorecard is a list of previous outcomes (not including ties)
    to be passed to the place_bet() method
    The amount bet is based on a series of five bets (2,3,4,5,6). 
    The series is reset after any two wins or after 5 bets. 
    '''
    def __init__(self):
        super().__init__()
        self.verbose = False
        self.name = 'Pattern 2of5'
        self.bet_series = [1,2,3,4,5,6]
        self.series_wins = 0
        self.series_length = 1
        self.walk = 0
        self.trend = 0
        if self.verbose : 
            print('Created player {}'.format(self.name))

    def place_bet(self):
# amount to bet
        if self.series_length > 5 or self.series_wins > 2:
            self.series_length = 1
            self.series_wins = 0
            
        self.bet.amount = self.bet_series[self.series_length]
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

        if self.verbose : 
            print('Series length: {}\t'.format(self.series_length))
            print('{0} has {2} bets {1}'
                    .format(self.name, self.bet, self.stake))
                    
        self.stake -= self.bet.amount


class Repeat2of5Bettor(Pattern2of5Bettor):
    def __init__(self):
        super().__init__()
        self.name = 'Repeat 2of5'

    def place_bet(self):
# amount to bet
        if self.series_length > 5 or self.series_wins > 2:
            self.series_length = 1
            self.series_wins = 0
            
        self.bet.amount = self.bet_series[self.series_length]
#  choose outcome to bet on
        if len(self.scorecard) < 2:
            self.bet.outcome = self.bankerBet
        else:
            if self.scorecard[-1] == 'B':
                self.bet.outcome = self.bankerBet
            elif self.scorecard[-1] == 'P':
                self.bet.outcome = self.playerBet
            else:
                print('ERROR: You should not be able to get here')

        if self.verbose : 
            print('Series length: {}\t'.format(self.series_length))
            print('{0} has {2} bets {1}'
                    .format(self.name, self.bet, self.stake))
                    
        self.stake -= self.bet.amount
