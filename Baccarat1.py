# -*- coding: utf-8 -*-
"""
Baccarat1.py 

Created on Sun Aug 23 11:30:55 2015
@author: amaloney
"""

from CasinoCards import Hand, Shoe

#import time

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
    

def getDecision(aShoe, discards):
    """
    Deal a hand of two cards to Player and Banker
    
    If there is no decision after the initial cards are dealt,
    deal one or two more cards according to the rules of the game.
    
    Return the decision (P, B, T, D or p)
    """
    bankerHand = Hand()
    playerHand = Hand()

    if len(aShoe.cards) < 6:
        discards.move_cards(aShoe, len(discards.cards))
        aShoe.shuffle()
        aShoe.cut_cards()
        assert len(discards.cards) == 0
        assert len(aShoe.cards) == 416
        aShoe.burn_top_cards(aShoe, discards)
        
    natural = False
    bankerDraws = False
    playerDraws = False

    aShoe.move_cards(playerHand, 1)
    playerPoints = playerHand.cards[0].value
    aShoe.move_cards(bankerHand, 1)
    bankerPoints = bankerHand.cards[0].value
    aShoe.move_cards(playerHand, 1)

    playerPoints += playerHand.cards[1].value
    if playerPoints > 9:
        playerPoints -= 10

    aShoe.move_cards(bankerHand, 1)
    bankerPoints += bankerHand.cards[1].value
    if bankerPoints > 9:
        bankerPoints -= 10
          
#   Evaluate initial hands
    if playerPoints > 7 :
#        print('Player has a natural, there will be no more cards.')
        natural = True
    if bankerPoints > 7 :
#        print('Banker has a natural, there will be no more cards.')
        natural = True
#   Determine if Player draws a third card
    if not natural:
        if playerPoints > 5:
#            print('Player stands with', playerPoints)
            playerDraws = False
        else:
            playerDraws = True
            aShoe.move_cards(playerHand, 1)
#            print('Player gets the', playerHand.cards[-1], end='')
            playerPoints += playerHand.cards[-1].value
            if playerPoints > 9:
                playerPoints -= 10
#            print(' for a total of ', playerPoints)
            
#   Determine if Banker draws a third card
        if bankerPoints == 7:
            bankerDraws = False
#            print('Banker Stands')
        if not playerDraws:
            if bankerPoints == 6:
                bankerDraws = False
#                print('Banker Stands')
            if bankerPoints < 6:
                bankerDraws = True
        
        if playerDraws:
            playerThirdCardValue = playerHand.cards[-1].value
            if bankerPoints < 3:
                bankerDraws = True
#                print('Banker always draws when holding less than 3')
            if bankerPoints == 3:
                if playerThirdCardValue != 8:
                    bankerDraws = True
#                    print('Banker with 3 draws when player 3rd card != 8')
                else:
                    bankerDraws = False
#                    print('Banker Stands')
            if bankerPoints == 4:
                if 1 < playerThirdCardValue < 8:
                    bankerDraws = True
#                    print('Banker with 4 draws when player 3rd card is 2 - 7')
                else:
                    bankerDraws = False
#                    print('Banker Stands')
            if bankerPoints == 5:
                if 3 < playerThirdCardValue < 8:
                    bankerDraws = True
#                    print('Banker with 5 draws when player 3rd card is 4 - 7')
                else:
                    bankerDraws = False
#                    print('Banker Stands')
            if bankerPoints == 6:
                if 5 < playerThirdCardValue < 8:
                    bankerDraws = True
#                    print('Banker with 6 draws when player 3rd card is 6 or 7')
                else:
                    bankerDraws = False
#                    print('Banker Stands')
    
        if bankerDraws:
            aShoe.move_cards(bankerHand,  1)
#            print('Banker draws the', bankerHand.cards[-1], end='')
            bankerPoints += bankerHand.cards[-1].value
            if bankerPoints > 9:
                bankerPoints -= 10
#            print(' for a total of ', bankerPoints)

    if len(aShoe.cards) < 6:
        print('That was the last hand in this shoe. Will reshuffle the shoe')
    if playerPoints == bankerPoints :
#        print('The hand is a tie.')
        bankerHand.move_cards(discards, len(bankerHand.cards))
        playerHand.move_cards(discards, len(playerHand.cards))
        return 'T'
    if playerPoints > bankerPoints :
        if len(playerHand.cards) == 3 and playerPoints == 8:
#            print('Panda')
            bankerHand.move_cards(discards, len(bankerHand.cards))
            playerHand.move_cards(discards, len(playerHand.cards))
            return 'p'
#        print('Player wins')
        bankerHand.move_cards(discards, len(bankerHand.cards))
        playerHand.move_cards(discards, len(playerHand.cards))
        return 'P'
    if bankerPoints > playerPoints:
        if len(bankerHand.cards) == 3 and bankerPoints == 7:
#            print('Dragon')
            bankerHand.move_cards(discards, len(bankerHand.cards))
            playerHand.move_cards(discards, len(playerHand.cards))
            return 'D'
#        print('Banker wins')
        bankerHand.move_cards(discards, len(bankerHand.cards))
        playerHand.move_cards(discards, len(playerHand.cards))
        return 'B'

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
    stakeHistory = []
    scorecard =[]
    temp = []
    side = 'P'
    nextBet = Bet(2, bankerBet)
    currentBet = nextBet
    
    gameShoe, discards = prepareShoe()
    burn_top_cards(gameShoe, discards)
    file = open('data.out', 'a')
    file.seek(0,2)
    patternPlayer = Player('pattern')
    while len(gameShoe.cards) > 16:
#        Place bet
        if len(temp) > 2:
            nextBet.outcome.name = temp[-2]
                    
        currentBet = nextBet
        print('\nYou bet {}'.format(currentBet))
#        Get decision
        decision = getDecision(gameShoe, discards)
#        settle bets
        if decision != 'T':
            if decision == 'D':
                temp.append('B')
                print('Dragon', end = ' ')
                if currentBet.outcome.name == decision:
                    print('You win {}'.format(
                        currentBet.amount * currentBet.outcome.odds))
                    stake += currentBet.amount * currentBet.outcome.odds
                elif currentBet.outcome.name == 'B':
                    print('Banker bets push')
            elif decision == 'B':
                temp.append('B')
                print('Banker Wins', end = ' ')
                if currentBet.outcome.name == decision:
                    print('You win {}'.format(currentBet.amount))
                    stake += currentBet.amount
                    nextBet.amount += 1
                else:
                    stake -= currentBet.amount
                    nextBet.amount = 2
            elif decision == 'p':
                temp.append('P')
                print('Panda', end = ' ')
                if currentBet.outcome.name == decision:
                    print('You win {}'.format(
                        currentBet.amount * currentBet.outcome.odds))
                    stake += currentBet.amount * currentBet.outcome.odds
                    nextBet.amount += 1
                elif currentBet.outcome.name == 'P':
                    print('Panda - pay Player and Panda bets')
                    stake += currentBet.amount
                    nextBet.amount += 1
                else:
                    stake -= currentBet.amount
                    nextBet.amount = 2
            elif decision == 'P':
                temp.append('P')
                print('Player Wins', end = ' ')
                if currentBet.outcome.name == decision:
                    print('You win {}'.format(currentBet.amount))
                    stake += currentBet.amount
                    nextBet.amount += 1
                else:
                    stake -= currentBet.amount
                    nextBet.amount = 2
        else:
            print('The hand is a tie')

        stakeHistory.append(stake)
        scorecard.append(decision)
        file.write(decision)
    file.write('\n')
    file.close()
    
    print('\n', scorecard)
    print('Total hands:', len(scorecard), 'Banker:', scorecard.count('B'),
          'Player:', scorecard.count('P'), 'Tie:', scorecard.count('T'),
            'Panda:', scorecard.count('p'), 'Dragon:', scorecard.count('D'))
    print(stakeHistory)
    plt.plot(stakeHistory)
    plt.show()

#    len(aShoe.cards)
#    len(discards.cards)


    