# -*- coding: utf-8 -*-
"""
Contains the function getDecision for baccarat.

Created on Sun Dec 13 18:01:26 2015


@author: amaloney
"""
from CasinoCards import Hand

def getDecision(aShoe, discards):
    """
    Deal a hand of two cards to Player and Banker
    
    If there is no decision after the initial cards are dealt,
    deal one or two more cards according to the rules of the game.
    
    Return the decision (P, B, T, D or p) where:
    'T' = Tie bets win (9:1), Player and Banker bets push, all side bets lose
    'B' = Banker bets win, all other bets lose
    'D' = Dragon 7 bets win (40:1), bets on Banker push, all other bets lose
    'P' = Player bets win, all other bets lose
    'p' = Panda 8 (25:1) and Player bets win, all other bets lose
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

#   Deal 2 cards to Player and Banker
    aShoe.move_cards(playerHand, 1)
    aShoe.move_cards(bankerHand, 1)
    aShoe.move_cards(playerHand, 1)
    aShoe.move_cards(bankerHand, 1)

    playerPoints =  playerHand.cards[0].value + playerHand.cards[1].value
    playerPoints = playerPoints % 10

    bankerPoints = bankerHand.cards[0].value + bankerHand.cards[1].value
    bankerPoints = bankerPoints % 10
#    print('player: {} -- banker:{}'.format(playerPoints, bankerPoints))
          
#   Evaluate initial hands
    if playerPoints > 7 :
#        print('Player has a natural {}, there will be no more cards.'
#                .format(playerPoints))
        natural = True
    if bankerPoints > 7 :
#        print('Banker has a natural {}, there will be no more cards.'
#                .format(bankerPoints))
        natural = True
#   Determine if Player draws a third card
    if natural is not True:
        if playerPoints > 5:
#            print('Player stands with', playerPoints)
            playerDraws = False
        else:
            playerDraws = True
            aShoe.move_cards(playerHand, 1)
#            print('Player with', playerPoints, 
#                  'draws the', playerHand.cards[-1], end='')
            playerPoints += playerHand.cards[-1].value
            playerPoints = playerPoints % 10
#            print(' for a total of ', playerPoints)
            
#   Determine if Banker draws a third card
        if bankerPoints == 7:
            bankerDraws = False
#            print('Banker Stands with', bankerPoints)
        if playerDraws is not True:
            if bankerPoints == 6:
                bankerDraws = False
#                print('Banker Stands with', bankerPoints)
            if bankerPoints < 6:
                bankerDraws = True

        if playerDraws:
            playerThirdCardValue = playerHand.cards[-1].value
#            print('Banker has', bankerPoints)
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
#                    print('Banker with 6 draws when player 3rd card is 6 - 7')
                else:
                    bankerDraws = False
#                    print('Banker Stands')
    
        if bankerDraws:
            aShoe.move_cards(bankerHand,  1)
#            print('Banker draws the', bankerHand.cards[-1], end='')
            bankerPoints += bankerHand.cards[-1].value
            bankerPoints = bankerPoints % 10
#            print(' for a total of ', bankerPoints)

    if playerPoints == bankerPoints :
#        print('The hand is a tie.')
        bankerHand.move_cards(discards, len(bankerHand.cards))
        playerHand.move_cards(discards, len(playerHand.cards))
#        input('press enter to continue')
        return 'T'
    if playerPoints > bankerPoints :
        if len(playerHand.cards) == 3 and playerPoints == 8:
#            print('Panda')
            bankerHand.move_cards(discards, len(bankerHand.cards))
            playerHand.move_cards(discards, len(playerHand.cards))
#            input('press enter to continue')
            return 'p'
#        print('Player wins')
        bankerHand.move_cards(discards, len(bankerHand.cards))
        playerHand.move_cards(discards, len(playerHand.cards))
#        input('press enter to continue')
        return 'P'
    if bankerPoints > playerPoints:
        if len(bankerHand.cards) == 3 and bankerPoints == 7:
#            print('Dragon')
            bankerHand.move_cards(discards, len(bankerHand.cards))
            playerHand.move_cards(discards, len(playerHand.cards))
#            input('press enter to continue')
            return 'D'
#        print('Banker wins')
        bankerHand.move_cards(discards, len(bankerHand.cards))
        playerHand.move_cards(discards, len(playerHand.cards))
#        input('press enter to continue')
        return 'B'
    