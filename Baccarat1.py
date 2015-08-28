# -*- coding: utf-8 -*-
"""
Baccarat1.py 

Created on Sun Aug 23 11:30:55 2015
@author: amaloney
"""

from CasinoCards import Hand, Shoe

scorecard = []

def prepareShoe(aShoe, discards):
    aShoe = Shoe()
    discards = Shoe()
    aShoe.shuffle()
    aShoe.cut_cards()
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
        
    natural = False
    bankerStands = False
    playerStands = False

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

#    print('Player has the', playerHand.cards[0], 'and the', 
#          playerHand.cards[1], 'for a total of', playerPoints )
#    print('Banker has the', bankerHand.cards[0], 'and the', 
#          bankerHand.cards[1], 'for a total of', bankerPoints )

    if playerPoints > 7 :
#        print('Player has a natural, there will be no more cards.')
        natural = True
    if bankerPoints > 7 :
#        print('Banker has a natural, there will be no more cards.')
        natural = True
    if not natural:
        if playerPoints > 5:
#            print('Player stands with', playerPoints)
            playerStands = True
        else:
            playerStands = False
            aShoe.move_cards(playerHand, 1)
#            print('Player gets the', playerHand.cards[-1], end='')
            playerPoints += playerHand.cards[-1].value
            if playerPoints > 9:
                playerPoints -= 10
#            print(' for a total of ', playerPoints)
        
        if bankerPoints == 7:
            bankerStands = True
#            print('Banker Stands')
        if playerStands and (bankerPoints > 5 and bankerPoints < 7):
            bankerStands = True
#            print('Banker Stands')
        if playerStands and bankerPoints < 6:
            bankerStands = False
    
        if not playerStands:
            playerThirdCardValue = playerHand.cards[-1].value
    
        if not playerStands and bankerPoints == 3:
            if playerThirdCardValue != 8:
                bankerStands = False
#                print('Banker with 3 draws when player 3rd card != 8')
            else:
                bankerStands = True
#                print('Banker Stands')
        if not playerStands and bankerPoints == 4:
            if playerThirdCardValue > 1 and playerThirdCardValue < 8:
                bankerStands = False
#                print('Banker with 4 draws when player 3rd card is 2 - 7')
            else:
                bankerStands = True
#                print('Banker Stands')
        if not playerStands and bankerPoints == 5:
            if playerThirdCardValue > 3 and playerThirdCardValue < 8:
                bankerStands = False
#                print('Banker with 5 draws when player 3rd card is 4 - 7')
            else:
                bankerStands = True
#                print('Banker Stands')
        if not playerStands and bankerPoints == 6:
            if playerThirdCardValue > 5 and playerThirdCardValue < 8:
                bankerStands = False
#                print('Banker with 6 draws when player 3rd card is 6 or 7')
            else:
                bankerStands = True
#                print('Banker Stands')
    
        if not bankerStands:
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
            print('Panda')
            bankerHand.move_cards(discards, len(bankerHand.cards))
            playerHand.move_cards(discards, len(playerHand.cards))
            return 'p'
#        print('Player wins')
        bankerHand.move_cards(discards, len(bankerHand.cards))
        playerHand.move_cards(discards, len(playerHand.cards))
        return 'P'
    if bankerPoints > playerPoints:
        if len(bankerHand.cards) == 3 and bankerPoints == 7:
            print('Dragon')
            bankerHand.move_cards(discards, len(bankerHand.cards))
            playerHand.move_cards(discards, len(playerHand.cards))
            return 'D'
#        print('Banker wins')
        bankerHand.move_cards(discards, len(bankerHand.cards))
        playerHand.move_cards(discards, len(playerHand.cards))
        return 'B'

if __name__ == '__main__':
    scorecard =[]
    aShoe = Shoe()
    discards = Shoe()
    aShoe, discards = prepareShoe(aShoe, discards)
    burn_top_cards(aShoe, discards)
    while len(aShoe.cards) > 16:
        scorecard.append(getDecision(aShoe, discards))
    print(scorecard)
    print(len(scorecard))
#    len(aShoe.cards)
#    len(discards.cards)


    