# -*- coding: utf-8 -*-
"""
Baccarat1.py 

Created on Sun Aug 23 11:30:55 2015
@author: amaloney
"""


import pickle
from CasinoCards import Shoe
from getDecision import getDecision
from Player import BankerFlatBettor, PlayerFlatBettor, Banker3of5Bettor
from Player import Walk3of5Bettor
from baccarat import Outcome, Bet
import matplotlib.pyplot as plt

scorecard = []

def prepareShoe():
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
    print(aShoe.cards[-1])
    if aShoe.cards[-1].value == 0:
        aShoe.move_cards(discards, 11)
    else:
        aShoe.move_cards(discards, aShoe.cards[-1].rank + 1)
    
def percentChange(startPoint, currentPoint):
    try:
        return((currentPoint - startPoint) / abs(startPoint)) * 100.00
    except:
        return 0

def fibonacci(n):
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
    stakeHistory = []
    scorecard =[]
    temp = []
    walkHistory = []
    side = 'P'
    nextBet = Bet(2, bankerBet)
    currentBet = nextBet
    gameShoe, discards = prepareShoe()
    burn_top_cards(gameShoe, discards)
    file = open('data.out', 'a')
    file.seek(0,2)
    bfb = BankerFlatBettor() 
    pfb = PlayerFlatBettor()
    b3b = Banker3of5Bettor()
    w3b = Walk3of5Bettor()
    players = [bfb, pfb, b3b, w3b]
    
    while len(gameShoe.cards) > 16:
# Place bet
        for player in players:
            player.place_bet()

# Get decision
        decision = getDecision(gameShoe, discards)
        
# Settle bets
        for player in players:
            if player.nextBet.outcome.name == decision:
                player.win(player.nextBet)
            elif decision == 'T' and (player.nextBet.outcome.name != 'p'
                                      or player.nextBet.outcome.name != 'D'):
                player.push(player.nextBet)
            elif player.nextBet.outcome.name == 'P' and decision == 'p':
                player.win(player.nextBet)
            elif player.nextBet.outcome.name == 'B' and decision == 'D':
                player.push(player.nextBet)
            else:
                player.lose(player.nextBet)
            
        if decision == 'B' or decision == 'D':
            walk += 1
        elif decision == 'P' or decision == 'p':
            walk -= 1

        stakeHistory.append(stake)
        walkHistory.append(walk)
        scorecard.append(decision)
        file.write(decision)

    file.write('\n')
    file.close()
    save_shoe(gameShoe, discards)
    
    print('\n', scorecard)
    print('Total hands:', len(scorecard), 'Banker:', scorecard.count('B'),
          'Player:', scorecard.count('P'), 'Tie:', scorecard.count('T'),
          'Panda:', scorecard.count('p'), 'Dragon:', scorecard.count('D'))
    for player in players:
        print(player.name, player.stake, 
              max(player.stake_history), min(player.stake_history))
    plt.plot(walkHistory, 'g', label='BvP')
    plt.plot(pfb.stake_history, 'dodgerblue', label='Player')
    plt.plot(bfb.stake_history, 'r', label='Banker')
    plt.plot(b3b.stake_history, 'magenta', label='B3B')
    plt.plot(w3b.stake_history, 'y', label='W3B')

#    plt.legend()
    plt.show()

#    len(aShoe.cards)
#    len(discards.cards)


    