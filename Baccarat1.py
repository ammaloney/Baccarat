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
import Player
#from Player import BankerFlatBettor, PlayerFlatBettor, Banker3of5Bettor, \
#                BankerWinUp1Bettor, PlayerWinUp1Bettor, RepeatWinUp1Bettor, \
#                Player3of5Bettor
#from Player import Walk3of5Bettor
#from baccarat import Outcome        #, Bet
import matplotlib.pyplot as plt


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
#    stake = 0
    walk = 0
    walkHistory = []
    scorecard = []
    
    gameShoe, discards = prepareShoe()
    burn_top_cards(gameShoe, discards)

    bfb = Player.BankerFlatBettor() 
    pfb = Player.PlayerFlatBettor()
    b3b = Player.Banker3of5Bettor()
    p3b = Player.Player3of5Bettor()
    w3b = Player.Walk3of5Bettor()
    bw1 = Player.BankerWinUp1Bettor()
    pw1 = Player.PlayerWinUp1Bettor()
    rw1 = Player.RepeatWinUp1Bettor()
    players = [w3b, rw1, b3b, bw1, p3b, pw1]

    file = open('data.out', 'a')
    file.seek(0,2)

#----------- Main Game Loop ------------#

    while len(gameShoe.cards) > 16:
# Place bet
        for player in players:
            player.place_bet()
# Get decision
        decision = getDecision(gameShoe, discards)
# Settle bets
        for player in players:
            player.settle_bets(decision)

        if decision == 'B' or decision == 'D':
            walk += 1
        elif decision == 'P' or decision == 'p':
            walk -= 1

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
    plt.plot(walkHistory, 'yellow', label='Walk', marker = '.', markersize=7)
    for player in players:
        print(player.name,'Stake:', player.stake,'Max:', 
              max(player.stake_history),'Min:', min(player.stake_history))
        plt.plot(player.stake_history, marker = '.', 
                 markersize=7, label=player.name)

    plt.legend(loc=3)
    plt.show()


    