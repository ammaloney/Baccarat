# -*- coding: utf-8 -*-
"""
Created on Mon Jan 11 08:47:11 2016

@author: amaloney
"""
# Composite Objects: Betting Strategy
# ==============================================

# A strategy class hierarchy for Betting.
# ::

class BettingStrategy:
    def bet( self ):
        raise NotImplementedError( "No bet method" )
    def record_win( self ):
        pass
    def record_loss( self ):
        pass

class Flat(BettingStrategy):
    def bet( self ):
        return 1

flat_bet= Flat()

flat_bet.bet()

import abc
from abc import abstractmethod
class BettingStrategy2(metaclass=abc.ABCMeta):
    @abstractmethod
    def bet( self ):
        return 1
    def record_win( self ):
        pass
    def record_loss( self ):
        pass

# A strategy class hierarchy for Play.
# ::

class GameStrategy:
    def insurance( self, hand ):
        return False
    def split( self, hand ):
        return False
    def double( self, hand ):
        return False
    def hit( self, hand ):
        return sum(c.hard for c in hand.cards) <= 17

dumb = GameStrategy()

# A simple outline for the Table.
# ::

class Table:
    def __init__( self ):
        self.deck = Deck()
    def place_bet( self, amount ):
        print( "Bet", amount )
    def get_hand( self ):
        try:
            self.hand= Hand2( d.pop(), d.pop(), d.pop() )
            self.hole_card= d.pop()
        except IndexError:
            # Out of cards: need to shuffle.
            # This is not technically correct.
            self.deck= Deck()
            return self.get_hand()
        print( "Deal", self.hand )
        return self.hand
    def can_insure( self, hand ):
        return hand.dealer_card.insure

# A Player definition
# ::

class Player:
    def __init__( self, table, bet_strategy, game_strategy ):
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table= table
    def game( self ):
        self.table.place_bet( self.bet_strategy.bet() )
        self.hand= self.table.get_hand()
        if self.table.can_insure( self.hand ):
            if self.game_strategy.insurance( self.hand ):
                self.table.insure( self.bet_strategy.bet() )
        # etc.

# Typical Use Case
# ::

table = Table()
flat_bet= Flat()
dumb = GameStrategy()
p = Player( table, flat_bet, dumb )
p.game()

# A Player definition using wide-open keyword definitions.
# ::

class Player2( Player ):
    def __init__( self, **kw ):
        """Must provide table, bet_strategy, game_strategy."""
        self.__dict__.update( kw )
    def game( self ):
        self.table.place_bet( self.bet_strategy.bet() )
        self.hand= self.table.get_hand()

# Typical Use Case.
# ::

table = Table()
flat_bet= Flat()
dumb = GameStrategy()
p1 = Player2( table=table, bet_strategy=flat_bet, game_strategy=dumb )
p1.game()

# Bonus Use Case. Set an additional attribute.
# ::

p2 = Player2( table=table, bet_strategy=flat_bet, game_strategy=dumb, log_name="Flat/Dumb" )
p2.game()
print( p2.log_name, p2.hand )

# A Player definition using wide-open keyword definitions.
# ::

class Player3( Player ):
    def __init__( self, table, bet_strategy, game_strategy, **extras ):
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table= table
        self.__dict__.update( extras )

table = Table()
flat_bet= Flat()
dumb = GameStrategy()
p3 = Player3( table, flat_bet, dumb, log_name="Flat/Dumb" )
p3.game()
print( p3.log_name, p3.hand )

# From CH01
class Player4:
    def __init__( self, table, bet_strategy, game_strategy ):
        """Creates a new player associated with a table, and configured with
        proper betting and play strategies

        :param table: an instance of :class:`Table`
        :param bet_strategy: an instance of :class:`BettingStrategy`
        :param  game_strategy: an instance of :class:`GameStrategy`
        """
        self.bet_strategy = bet_strategy
        self.game_strategy = game_strategy
        self.table= table

#From CH 05
# Some additional Callable Examples.
# The BetingStrategy superclass.
# ::

class BettingStrategy:
    def __init__( self ):
       self.win= 0
       self.loss= 0
    def __call__( self ):
        return 1

bet= BettingStrategy()
bet()
bet.win += 1
bet()
bet.loss += 1
bet()

# A stateful betting strategy. Property-based
# ::

class BettingMartingale( BettingStrategy ):
    def __init__( self ):
        self._win= 0
        self._loss= 0
        self.stage= 1
    @property
    def win(self): return self._win
    @win.setter
    def win(self, value):
        self._win = value
        self.stage= 1
    @property
    def loss(self): return self._loss
    @loss.setter
    def loss(self, value):
        self._loss = value
        self.stage *= 2
    def __call__( self ):
       return self.stage

bet= BettingMartingale()
bet()
bet.win += 1
bet()
bet.loss += 1
bet()
