# -*- coding: utf-8 -*-
"""
Baccarat1.py 

Created on Sun Aug 23 11:30:55 2015
@author: amaloney
"""


import pickle
from CasinoCards import Shoe
from getDecision import getDecision
from Player import Player
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
    banker_bettor = Player('banker_bettor')
    bet2onBanker = Bet(2, bankerBet)
    player_bettor = Player('player_bettor')
    bet2onPlayer = Bet(2, playerBet)
    
    while len(gameShoe.cards) > 16:
#        Place bet
        banker_bettor.nextBet = bet2onBanker
        player_bettor.nextBet = bet2onPlayer
        
        if len(temp) < 3:
            nextBet.outcome.name = 'B'
        else:
            nextBet.outcome.name = temp[-2]
        
        currentBet = nextBet
#        print('\nYou bet {}'.format(currentBet))
        
#        Get decision
        decision = getDecision(gameShoe, discards)
        
#        settle bets
        if decision != 'T':
            if decision == 'D':
                temp.append('B')
                banker_bettor.push(bet2onBanker)
                player_bettor.lose(bet2onPlayer)
#                print('Dragon', end = ' ')
                if currentBet.outcome.name == decision:
#                    print('You win {}'.format(
#                        currentBet.amount * currentBet.outcome.odds))
                    stake += currentBet.amount * currentBet.outcome.odds
#                elif currentBet.outcome.name == 'B':
#                    print('Banker bets push')
            elif decision == 'B':
                temp.append('B')
                banker_bettor.win(bet2onBanker)
                player_bettor.lose(bet2onPlayer)
                walk += 1
#                print('Banker Wins', end = ' ')
                if currentBet.outcome.name == decision:
#                    print('You win {}'.format(currentBet.amount))
                    stake += currentBet.amount
                    nextBet.amount += 1
                else:
                    stake -= currentBet.amount
                    nextBet.amount = 2
            elif decision == 'p':
                temp.append('P')
                walk -= 1
                banker_bettor.lose(bet2onBanker)
                player_bettor.win(bet2onPlayer)
#                print('Panda', end = ' ')
                if currentBet.outcome.name == decision:
#                    print('You win {}'.format(
#                        currentBet.amount * currentBet.outcome.odds))
                    stake += currentBet.amount * currentBet.outcome.odds
                    nextBet.amount += 1
                elif currentBet.outcome.name == 'P':
#                    print('Panda - pay Player and Panda bets')
                    stake += currentBet.amount
                    nextBet.amount += 1
                else:
                    stake -= currentBet.amount
                    nextBet.amount = 2
            elif decision == 'P':
                temp.append('P')
                banker_bettor.lose(bet2onBanker)
                player_bettor.win(bet2onPlayer)
                walk -= 1
#                print('Player Wins', end = ' ')
                if currentBet.outcome.name == decision:
#                    print('You win {}'.format(currentBet.amount))
                    stake += currentBet.amount
                    nextBet.amount += 1
                else:
                    stake -= currentBet.amount
                    nextBet.amount = 2
        else:
            banker_bettor.push(bet2onBanker)
            player_bettor.push(bet2onPlayer)
#            print('The hand is a tie')

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
    print('repeat ', stake)
    print('banker_bettor ', banker_bettor.stake)
    print('player_bettor ', player_bettor.stake)
    plt.plot(stakeHistory, 'magenta', label='Stake')
    plt.plot(walkHistory, 'g', label='BvP')
    plt.plot(player_bettor.stake_history, 'dodgerblue', label='Player')
    plt.plot(banker_bettor.stake_history, 'r', label='Banker')
#    plt.legend()
    plt.show()

#    len(aShoe.cards)
#    len(discards.cards)


    