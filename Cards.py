"""This module contains classes used to create card based casino games
and uses code from:

Think Python, 2nd Edition
by Allen Downey
http://thinkpython2.com

Copyright 2015 Allen Downey

License: http://creativecommons.org/licenses/by/4.0/

Added the ability to cut the deck.

"""

##from __future__ import print_function, division

import random


class Card(object):
    """Represents a standard playing card.
    
    Attributes:
      suit: integer 0-3
      rank: integer 1-13
      game_value: integer -- defaults to rank
      Subclasses should override game_value as needed
    """

    suit_names = ["Clubs", "Diamonds", "Hearts", "Spades"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7", 
              "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit=0, rank=2):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        """Returns a human-readable string representation."""
        return '%s of %s' % (Card.rank_names[self.rank],
                             Card.suit_names[self.suit])

    def __lt__(self, other):
        """Compares this card to other, first by suit, then rank.

        returns: boolean
        """
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 < t2


class Deck(object):
    """Represents a deck of cards.

    Attributes:
      cards: list of Card objects.
    """
    
    def __init__(self):
        """Initializes the Deck with 52 cards.
        """
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
#                game_value = rank
                card = Card(suit, rank)
                self.cards.append(card)

    def __str__(self):
        """Returns a string representation of the deck.
        """
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

    def add_card(self, card):
        """Adds a card to the deck.

        card: Card
        """
        self.cards.append(card)

    def remove_card(self, card):
        """Removes a card from the deck or raises exception if it is not there.
        
        card: Card
        """
        self.cards.remove(card)

    def pop_card(self, i=-1):
        """Removes and returns a card from the deck.

        i: index of the card to pop; by default, pops the last card.
        """
        return self.cards.pop(i)

    def shuffle(self):
        """Shuffles the cards in this deck."""
        random.shuffle(self.cards)

    def sort(self):
        """Sorts the cards in ascending order."""
        self.cards.sort()

    def move_cards(self, hand, num):
        """Moves the given number of cards from the deck into the Hand.

        hand: destination Hand object
        num: integer number of cards to move
        """
        for i in range(num):
            hand.add_card(self.pop_card())

    def cut_cards(self, cut_point = 0):
        """ Cut the deck by moving cut_point number of cards from the
        top of the deck to the bottom of the deck. Because of the way
        move_cards works, the cut out section needs to be reversed before
        being added to the bottom of the deck.

        By default, the cut_point is a random number between 1/3 and 2/3
        of the number of cards in the deck.
        """
        if cut_point == 0:
            lower_bound = int(len(self.cards) * .33)
            upper_bound = int(len(self.cards) * .66)
            cut_point = random.randint(lower_bound, upper_bound)
##        print("Cut cards at ", cut_point)
        temp = Hand()
        self.move_cards(temp, cut_point)
        temp.cards.reverse()
        while (len(temp.cards) > 0):
            self.cards.insert(0, temp.pop_card())

class Hand(Deck):
    """Represents a hand of playing cards."""
    
    def __init__(self, label=''):
        self.cards = []
        self.label = label

class Shoe(Deck):
    """A shoe holds (usually) 8 decks of playing cards """

    def __init__(self, decks = 8):
        """ Initialize the shoe with decks number of decks """
        self.cards = []
        for n in range(decks):
            aDeck = Deck()
            aDeck.move_cards(self, 52)

def find_defining_class(obj, method_name):
    """Finds and returns the class object that will provide 
    the definition of method_name (as a string) if it is
    invoked on obj.

    obj: any python object
    method_name: string method name
    """
    for ty in type(obj).mro():
        if method_name in ty.__dict__:
            return ty
    return None


if __name__ == '__main__':
    deck = Deck()
    deck.shuffle()
    deck.cut_cards()

    hand = Hand()
#    print(find_defining_class(hand, 'shuffle'))

    deck.move_cards(hand, 5)
    hand.sort()
    print(hand)
