# -*- coding: utf-8 -*-
"""
Baccarat.py 

Created on Sun Aug 23 11:30:55 2015
@author: amaloney
"""

from Cards import Hand, Shoe


class Dealer():
    """ This class represents the main game logic.
    
    I know how to generate a decision which will be one of five results:
        1 - Player hand wins
        2 - Banker hand wins
        3 - there is a Tie hand
        4 - Banker wins with a three card total of 7 known as a Dragon
        5 - Player wins with a three card total of 8 known as a Panda
        
    I use a Shoe to get cards from 
    I use 2 instances of Cards.Hand:
        1 each for the Player hand and the Banker hand
    """
    
def __init__(self):
    self.aShoe = Shoe()
    self.discards = Shoe()
    self.bankerHand = Hand()
    self.playerHand = Hand()
    self.handsThisShoe = 0

def prepareShoe(self):
    self.aShoe.shuffle()
    self.aShoe.cut_cards()
    self.discards.cards = []

def getDecision(self, aShoe, discards):
    """
    Deal a hand of two cards to Player and Banker
    
    If there is no decision after the initial cards are dealt,
    deal one or two more cards according to the rules of the game.
    
    Return the decision (P, B, T, D or p)
    """
    if len(self.aShoe.cards) < 6:
        self.discards.move_cards(self.aShoe, len(self.discards.cards))
        self.aShoe.shuffle()
        self.aShoe.cut_cards()
        assert len(self.discards.cards) == 0
        assert len(self.aShoe.cards) == 416
    
    natural = False
    bankerStands = False
    playerStands = False
    if len(self.aShoe.cards) == 416:
        self.handsThisShoe = 0    
#    print('Card for Player')
    self.aShoe.move_cards(self.playerHand, 1)
    if self.playerHand.cards[0].rank > 9:
        playerPoints = 0
    else:
        playerPoints = self.playerHand.cards[0].rank

#    print('Card for Banker')
    self.aShoe.move_cards(self.bankerHand, 1)
    if self.bankerHand.cards[0].rank > 9:
        bankerPoints = 0
    else:
        bankerPoints = self.bankerHand.cards[0].rank

    self.aShoe.move_cards(self.playerHand, 1)
    if self.playerHand.cards[1].rank < 10:
        playerPoints += self.playerHand.cards[1].rank
    if playerPoints > 9:
        playerPoints -= 10

    self.aShoe.move_cards(self.bankerHand, 1)
    if self.bankerHand.cards[1].rank < 10:
        bankerPoints += self.bankerHand.cards[1].rank
    if bankerPoints > 9:
        bankerPoints -= 10

    print('Player has the ', self.playerHand.cards[0], ' and the ', 
          self.playerHand.cards[1], ' for a total of ', playerPoints )
    print('Banker has the ', self.bankerHand.cards[0], ' and the ', 
          self.bankerHand.cards[1], ' for a total of ', bankerPoints )

    if playerPoints > 7 :
        print('Player has a natural, there will be no more cards.')
        natural = True
    if bankerPoints > 7 :
        print('Banker has a natural, there will be no more cards.')
        natural = True
    if not natural:
        if playerPoints > 5:
            print('Player stands with ', playerPoints)
            playerStands = True
        else:
            playerStands = False
            self.aShoe.move_cards(self.playerHand, 1)
            print('Player gets the ', self.playerHand.cards[-1])
            if self.playerHand.cards[-1].rank < 9 :
                playerPoints += self.playerHand.cards[-1].rank
                if playerPoints > 9 :
                    playerPoints -= 10
            print('for a total  of ', playerPoints)
        
        if bankerPoints == 7:
            bankerStands = True
            print('Banker Stands')
        if playerStands and bankerPoints > 5:
            bankerStands = True
            print('Banker Stands')
        if playerStands and bankerPoints < 6:
            bankerStands = False
    
        if not playerStands:
            if self.playerHand.cards[-1].rank > 9:
                playerThirdCardValue = 0
            else:
                playerThirdCardValue = self.playerHand.cards[-1].rank
    
        if not playerStands and bankerPoints == 3:
            if playerThirdCardValue != 8:
                bankerStands = False
                print('Banker with 3 draws when player 3rd card != 8')
            else:
                bankerStands = True
                print('Banker Stands')
        if not playerStands and bankerPoints == 4:
            if playerThirdCardValue > 1 and playerThirdCardValue < 8:
                bankerStands = False
                print('Banker with 4 draws when player 3rd card is 2 - 7')
            else:
                bankerStands = True
                print('Banker Stands')
        if not playerStands and bankerPoints == 5:
            if playerThirdCardValue > 3 and playerThirdCardValue < 8:
                bankerStands = False
                print('Banker with 5 draws when player 3rd card is 4 - 7')
            else:
                bankerStands = True
                print('Banker Stands')
        if not playerStands and bankerPoints == 6:
            if playerThirdCardValue > 5 and playerThirdCardValue < 8:
                bankerStands = False
                print('Banker with 6 draws when player 3rd card is 6 or 7')
            else:
                bankerStands = True
                print('Banker Stands')
    
        if not bankerStands:
            self.aShoe.move_cards(self.bankerHand,  1)
            print('Banker draws the ', self.bankerHand.cards[-1])
            if self.bankerHand.cards[-1].rank < 10:
                bankerPoints += self.bankerHand.cards[-1].rank
                if bankerPoints > 9:
                    bankerPoints -= 10
            print('for a total of ', bankerPoints)

    if len(self.aShoe.cards) < 6:
        print('That was the last hand in this shoe. Will reshuffle the shoe')
    self.handsThisShoe += 1
    print('Hands so far ', self.handsThisShoe)
    if playerPoints == bankerPoints :
        print('The hand is a tie.')
        self.bankerHand.move_cards(self.discards, len(self.bankerHand.cards))
        self.playerHand.move_cards(self.discards, len(self.playerHand.cards))
        return 'T'
    if playerPoints > bankerPoints :
        if len(self.playerHand.cards) == 3 and playerPoints == 8:
            print('Panda')
            self.bankerHand.move_cards(self.discards, len(self.bankerHand.cards))
            self.playerHand.move_cards(self.discards, len(self.playerHand.cards))
            return 'p'
        print('Player wins')
        self.bankerHand.move_cards(self.discards, len(self.bankerHand.cards))
        self.playerHand.move_cards(self.discards, len(self.playerHand.cards))
        return 'P'
    if bankerPoints > playerPoints:
        if len(self.bankerHand.cards) == 3 and bankerPoints == 7:
            print('Dragon')
            self.bankerHand.move_cards(self.discards, len(self.bankerHand.cards))
            self.playerHand.move_cards(self.discards, len(self.playerHand.cards))
            return 'D'
        print('Banker wins')
        self.bankerHand.move_cards(self.discards, len(self.bankerHand.cards))
        self.playerHand.move_cards(self.discards, len(self.playerHand.cards))
        return 'B'
 
if __name__ == "__main__":
    mae = Dealer()
    print(mae)
    mae.aShoe.shuffle()
    
    
    
    