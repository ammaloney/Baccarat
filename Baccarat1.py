#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Baccarat1.py 

Created on Sun Aug 23 11:30:55 2015
@author: amaloney
"""


import pickle
from CasinoCards import Shoe
from getDecision import getDecision
from Player import BankerFlatBettor, PlayerFlatBettor, Banker3of5Bettor, \
                BankerWinUp1Bettor, PlayerWinUp1Bettor, RepeatWinUp1Bettor, \
                Player3of5Bettor
from Player import Walk3of5Bettor
from baccarat import Outcome, Bet
import matplotlib.pyplot as plt

scorecard = []

def prepareShoe():
    '''Returns an eight deck shoe of CasinoCards and a discard pile.
    '''
    try:
        with open('baccarat_shoe.dat', 'rb') as shoe_file:
            aShoe = pickle.load(shoe_file)
    except:
        print('No shoe file found; creating new shoe.')
        aShoe = Shoe()

    aShoe.shuffle()
    aShoe.cut_cards()
    discards = Shoe()
    discards.cards = []
    return aShoe, discards
    
def burn_top_cards(aShoe, discards):
    '''Before play begins, the dealer deals the first card from the shoe 
    face-up then deals a number of cards face-down depending on the value of
    the first card: for cards Ace through Nine the number of cards dealt equals
    the number of pips on the card; for cards Ten through King ten cards are
    dealt. The cards are then discarded with revealing their value.
    '''
    print(aShoe.cards[-1])
    if aShoe.cards[-1].value == 0:
        aShoe.move_cards(discards, 11)
    else:
        aShoe.move_cards(discards, aShoe.cards[-1].rank + 1)
    
def percentChange(startPoint, currentPoint):
    try:
        if startPoint == 0 :
            startPoint = 1
            currentPoint += 1
        return((currentPoint - startPoint) / abs(startPoint)) * 100.00
    except:
        return 0

def fibonacci(n):
    '''where the fibonacci sequence for parameters 0-7 are:
        0, 1, 1, 2, 3, 5, 8, 13
    '''
    if n == 0:
        return 0
    elif n==1:
        return 1
    else:
        return fibonacci(n-1) + fibonacci(n-2)

def save_shoe(aShoe, discards):
    try:
        with open('baccarat_shoe.dat', 'wb') as shoe_file:
            if len(discards.cards) > 0:
                discards.move_cards(aShoe, len(discards.cards))
            pickle.dump(aShoe, shoe_file)
    except IOError as err:
        print('File error: ' + str(err))
    
if __name__ == '__main__':

    bankerBet = Outcome('B', 1)
    dragonBet = Outcome('D', 40)
    playerBet = Outcome('P', 1)
    pandaBet = Outcome('p', 25)
    tieBet = Outcome('T', 9)
    bets = {'B':'Banker', 'D':'Dragon', 'P':'Player', 'p':'Panda', 'T':'Tie'}
    stake = 0
    walk = 0
#    stakeHistory = []
    scorecard =[]
    BvsP = []
    walkHistory = []
    side = 'P'
    nextBet = Bet(2, bankerBet)
    currentBet = nextBet
    gameShoe, discards = prepareShoe()
    burn_top_cards(gameShoe, discards)
    
    bfb = BankerFlatBettor() 
    pfb = PlayerFlatBettor()
    b3b = Banker3of5Bettor()
    w3b = Walk3of5Bettor()
    p3b = Player3of5Bettor()
    bw1 = BankerWinUp1Bettor()
    pw1 = PlayerWinUp1Bettor()
    rw1 = RepeatWinUp1Bettor()
    players = [b3b, p3b, bw1, pw1]
    
    file = open('data.out', 'a')
    file.seek(0,2)

#----------- Main Game Loop ------------#

    while len(gameShoe.cards) > 16:
# Place bet
        for player in players:
            if isinstance(player, RepeatWinUp1Bettor) :
                player.place_bet(BvsP)
            else:
                player.place_bet()
# Get decision
        decision = getDecision(gameShoe, discards)
# Settle bets
        for player in players:
            player.settle_bets(decision)
      
        if decision == 'B' or decision == 'D':
            walk += 1
            BvsP.append('B')
        elif decision == 'P' or decision == 'p':
            walk -= 1
            BvsP.append('P')

#        stakeHistory.append(stake)
        walkHistory.append(walk)
        scorecard.append(decision)
        file.write(decision)

#-------------- End Main Loop -----------#

    file.write('\n')
    file.close()
    save_shoe(gameShoe, discards)
    
    print('\n', scorecard)
    print('Total hands:', len(scorecard), 'Banker:', scorecard.count('B'),
          'Player:', scorecard.count('P'), 'Tie:', scorecard.count('T'),
          'Panda:', scorecard.count('p'), 'Dragon:', scorecard.count('D'))
    plt.plot(walkHistory, 'yellow', label='BvP')
    for player in players:
        print(player.name,'\t', player.stake,'\t', 
              max(player.stake_history),'\t', min(player.stake_history))
        plt.plot(player.stake_history, label=player.name)
#    plt.plot(pfb.stake_history, 'dodgerblue', label='Player')
#    plt.plot(bfb.stake_history, 'r', label='Banker')
#    plt.plot(b3b.stake_history, 'magenta', label='B3B')
#    plt.plot(w3b.stake_history, 'yellow', label='W3B')

    plt.legend(loc=3)
    plt.show()

#    len(aShoe.cards)
#    len(discards.cards)


    