# -*- coding: utf-8 -*-
"""
Baccarat1.py 

Created on Sun Aug 23 11:30:55 2015
@author: amaloney
"""

from CasinoCards import Hand, Shoe

#class BaccaratCard(Card):
#    def __init__(self, suit=0, rank=2, value=2):
#        self.suit = suit
#        self.rank = rank
#        if rank > 9:
#            self.value = 0
#            print('init in BaccaratCard')
#        else:
#            self.value = rank
#    def __str__(self):
#        """Returns a human-readable string representation."""
#        return 'In Baccarat, the %s of %s, has a value of %d' % (
#                Card.rank_names[self.rank],
#                Card.suit_names[self.suit], 
#                self.value)
#
#class BaccaratDeck(Deck):
#    """Represents a deck of Baccarat cards.
#
#    Attributes:
#      cards: list of Card objects.
#    """
#    
#    def __init__(self):
#        """Initializes the Deck with 52 cards.
#        """
#        self.cards = []
#        for suit in range(4):
#            for rank in range(1, 14):
#                if rank > 9:
#                    value = 0
#                else:
#                    value = rank
#                card = BaccaratCard(suit, rank, value)
#                self.cards.append(card)
#
#class BaccaratShoe(Shoe):
#    """A shoe holds (usually) 8 decks of playing cards """
#
#    def __init__(self, decks = 8):
#        """ Initialize the shoe with decks number of decks """
#        self.cards = []
#        for n in range(decks):
#            aDeck = BaccaratDeck()
#            aDeck.move_cards(self, 52)

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

def prepareShoe(aShoe, discards):
    aShoe = Shoe()
    discards = Shoe()
    aShoe.shuffle()
    aShoe.cut_cards()
    discards.cards = []
    return aShoe, discards
    

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
#    if len(aShoe.cards) == 416:
#        handsThisShoe = 0    
#    print('Card for Player')
    aShoe.move_cards(playerHand, 1)
    playerPoints = playerHand.cards[0].value
#    if playerHand.cards[0].rank > 9:
#        playerPoints = 0
#    else:
#        playerPoints = playerHand.cards[0].rank

#    print('Card for Banker')
    aShoe.move_cards(bankerHand, 1)
    bankerPoints = bankerHand.cards[0].value
#    if bankerHand.cards[0].rank > 9:
#        bankerPoints = 0
#    else:
#        bankerPoints = bankerHand.cards[0].rank

    aShoe.move_cards(playerHand, 1)
#    if playerHand.cards[1].rank < 10:
    playerPoints += playerHand.cards[1].value
    if playerPoints > 9:
        playerPoints -= 10

    aShoe.move_cards(bankerHand, 1)
#    if bankerHand.cards[1].rank < 10:
    bankerPoints += bankerHand.cards[1].value
    if bankerPoints > 9:
        bankerPoints -= 10

    print('Player has the', playerHand.cards[0], 'and the', 
          playerHand.cards[1], 'for a total of', playerPoints )
    print('Banker has the', bankerHand.cards[0], 'and the', 
          bankerHand.cards[1], 'for a total of', bankerPoints )

    if playerPoints > 7 :
        print('Player has a natural, there will be no more cards.')
        natural = True
    if bankerPoints > 7 :
        print('Banker has a natural, there will be no more cards.')
        natural = True
    if not natural:
        if playerPoints > 5:
            print('Player stands with', playerPoints)
            playerStands = True
        else:
            playerStands = False
            aShoe.move_cards(playerHand, 1)
            print('Player gets the', playerHand.cards[-1], end='')
            if playerHand.cards[-1].value < 9 :
                playerPoints += playerHand.cards[-1].value
                if playerPoints > 9 :
                    playerPoints -= 10
            print(' for a total of ', playerPoints)
        
        if bankerPoints == 7:
            bankerStands = True
            print('Banker Stands')
        if playerStands and (bankerPoints > 5 and bankerPoints < 7):
            bankerStands = True
            print('Banker Stands')
        if playerStands and bankerPoints < 6:
            bankerStands = False
    
        if not playerStands:
#            if playerHand.cards[-1].value > 9:
#                playerThirdCardValue = 0
#            else:
            playerThirdCardValue = playerHand.cards[-1].value
    
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
            aShoe.move_cards(bankerHand,  1)
            print('Banker draws the', bankerHand.cards[-1], end='')
#            if bankerHand.cards[-1].value < 10:
            bankerPoints += bankerHand.cards[-1].value
            if bankerPoints > 9:
                bankerPoints -= 10
            print(' for a total of ', bankerPoints)

    if len(aShoe.cards) < 6:
        print('That was the last hand in this shoe. Will reshuffle the shoe')
#    handsThisShoe += 1
#    print('Hands so far ', handsThisShoe)
    if playerPoints == bankerPoints :
        print('The hand is a tie.')
        bankerHand.move_cards(discards, len(bankerHand.cards))
        playerHand.move_cards(discards, len(playerHand.cards))
        return 'T'
    if playerPoints > bankerPoints :
        if len(playerHand.cards) == 3 and playerPoints == 8:
            print('Panda')
            bankerHand.move_cards(discards, len(bankerHand.cards))
            playerHand.move_cards(discards, len(playerHand.cards))
            return 'p'
        print('Player wins')
        bankerHand.move_cards(discards, len(bankerHand.cards))
        playerHand.move_cards(discards, len(playerHand.cards))
        return 'P'
    if bankerPoints > playerPoints:
        if len(bankerHand.cards) == 3 and bankerPoints == 7:
            print('Dragon')
            bankerHand.move_cards(discards, len(bankerHand.cards))
            playerHand.move_cards(discards, len(playerHand.cards))
            return 'D'
        print('Banker wins')
        bankerHand.move_cards(discards, len(bankerHand.cards))
        playerHand.move_cards(discards, len(playerHand.cards))
        return 'B'

# Usage:
aShoe, discards = prepareShoe(aShoe, discards)
getDecision(aShoe, discards)
len(aShoe.cards)
len(discards.cards)


    