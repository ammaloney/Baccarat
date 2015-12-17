# -*- coding: utf-8 -*-
"""
Baccarat1.py 

Created on Sun Aug 23 11:30:55 2015
@author: amaloney
"""

from CasinoCards import Shoe

from getDecision import getDecision

scorecard = []

def prepareShoe():
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
        

if __name__ == '__main__':
    
    from Player import Bet, Player
    from baccarat import Outcome
    import matplotlib.pyplot as plt
    
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
    player_bettor = Player('player_bettor')
    
    while len(gameShoe.cards) > 16:
        

#        Place bet
        banker_bettor.place_bet(2, 'B')
        player_bettor.place_bet(2, 'P')

        currentBet = nextBet
#        print('\nYou bet {}'.format(currentBet))
        
#        Get decision
        decision = getDecision(gameShoe, discards)
        
#        settle bets
        if decision != 'T':
            if decision == 'D':
                temp.append('B')
#                print('Dragon', end = ' ')
                if currentBet.outcome.name == decision:
#                    print('You win {}'.format(
#                        currentBet.amount * currentBet.outcome.odds))
                    stake += currentBet.amount * currentBet.outcome.odds
#                elif currentBet.outcome.name == 'B':
#                    print('Banker bets push')
            elif decision == 'B':
                temp.append('B')
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
            pass
#            print('The hand is a tie')

        stakeHistory.append(stake)
        walkHistory.append(walk)
        scorecard.append(decision)
        file.write(decision)
    file.write('\n')
    file.close()
    
    print('\n', scorecard)
    print('Total hands:', len(scorecard), 'Banker:', scorecard.count('B'),
          'Player:', scorecard.count('P'), 'Tie:', scorecard.count('T'),
            'Panda:', scorecard.count('p'), 'Dragon:', scorecard.count('D'))
    print(stakeHistory)
    plt.plot(stakeHistory, label='Stake')
    plt.plot(walkHistory, 'g', label='BvP')
#    plt.legend()
    plt.show()

#    len(aShoe.cards)
#    len(discards.cards)


    