import sys
sys.path.append('../')
import json
from copy import deepcopy as copy
from functools import cmp_to_key

from IPython import embed as fuck

from metro_holografix.cardtypes import *
import symbols as sym

class Table(Tavolo):

    def is_valid(self):
        return len(self.cards) == 0 or (len(self.singles()) == 0 and len(self.getNonValide()) == 0)

    def flatten(self):
        return [c for tc in self.cards for c in tc.cards]

    def widget_repr(self):
        for ts in self.cards:
            ocards = list(sorted(ts.cards, key=lambda c: c.value))
            yi = [sym.big['hat']]
            seed = ocards[0][0].lower()
            yi.append(sym.big[seed])
            yi.append(sym.big[ocards[0][1]])
            for card in ocards[1:]:
                seed = card[0].lower()
                yi.append(sym.sym[seed][card[1]])
            yield yi

    def equality(self, other):
        b = set(other.flatten())
        a = set(self.flatten())
        gt = a - b
        lt = b - a
        if gt == lt and lt == set():
            return True
        else:
            return False

class Hand:
    def __init__(self, cards):
        def sortc(a, b):
            return -1 if (a[1],a[0]) < (b[1],b[0]) else 1
        self.cards = list(sorted(cards, key=cmp_to_key(sortc)))

    def __repr__(self):
        return 'Hand<'+ str(self.cards) + '>'

    def widget_repr(self):
        yi = [sym.big['hat']]
        seed = self.cards[0][0].lower()
        yi.append(sym.big[seed])
        yi.append(sym.big[self.cards[0][1]])
        for card in self.cards[1:]:
            seed = card[0].lower()
            yi.append(sym.sym[seed][card[1]])
        return yi

def make_deck():
    from random import shuffle # TODO: mersenne
    def make_set(seed):
        for i in range(1, 14):
            yield Card(seed, i)
    odeck = [m for seed in ['Pikes', 'Hearts', 'Clovers', 'Tiles']  for m in make_set(seed)] * 2
    shuffle(odeck)
    assert len(odeck) == 104 
    return odeck

class WrongMoveException(Exception):
    pass

class State:
    def __init__(self, ids):
        self.deck = make_deck()
        self.winner = None
        self.hasEnded = False
        self.players = dict()
        self.table = Table([])
        self.turn = None
        self.ids = ids
        self.cur_player = ids[0]
        self.nrounds = 0
        for i in ids:
            cards = [self.deck.pop() for i in range(11)]
            self.players[i] = Hand(cards)

    def draw(self):
        hand = self.players[self.cur_player] 
        nhand = Hand(hand.cards + [self.deck.pop()])
        self.players[self.cur_player] = nhand
        assert len(self.players[self.cur_player].cards) == len(hand.cards) + 1
        self.turn = None

    def next_turn(self):
        assert self.turn is None
        next_player = self.ids[(self.ids.index(self.cur_player) + 1) % len(self.ids)]
        self.cur_player = next_player
        self.turn = [(copy(self.table), copy(self.players[self.cur_player]))]
        self.nrounds = self.nrounds + 1 if self.cur_player == self.ids[0] else self.nrounds

    def done(self):
        assert self.turn is not None
        original = self.table
        table, hand = self.last()

        if original.equality(table):
            raise WrongMoveException()
        elif not table.is_valid() or len(set(original.flatten()) - set(table.flatten())) != 0:
            if self.cur_player != 'you':
                fuck() # debug
            raise WrongMoveException()
        else:
            self.table, self.players[self.cur_player] = table, hand
            self.turn = None
            if len(hand.cards) == 0:
                # won
                self.hasEnded = True
                self.winner = self.cur_player
        
    def last(self):
        return self.turn[-1]

    def backtrack(self):
        if len(self.turn) >= 2:
            return self.turn.pop()
        else:
            return self.turn[0]

    def size(self):
        return len(self.turn)

    def move_and_advance(self, src, dst):
        table, hand = self.last()
        t, h = gioca(table, hand, src, dst)
        self.turn.append((t, h))
        return t, h

    def advance(self, table, hand):
        self.turn.append((table, hand))
        return table, hand

def fromJson(j):
    hcards = [Card(seed, value) for seed, value in j['hand']]
    tcards = []
    for tc in j['table']:
        tcards.append(TaggedCards([Card(seed, value) for seed, value in tc]))
    return Table(tcards), Hand(hcards)

def toJson(table, hand):
    j = dict()
    j['hand'] = hand.cards
    j['table'] = []
    for tc in table.cards:
        j['table'].append(tc.cards)
    return json.dumps(j)

# TODO: refactor language
def gioca(tavolo, hand, src, dst):
    giocata = [] if dst == 'Empty' else tavolo.cards[dst]
    da_muovere = hand.cards[src[1]] if src[0] == 'Hand' else tavolo.cards[src[0]].cards[src[1]]
    hcards = hand.cards[:src[1]] + hand.cards[src[1]+1:] if src[0] == 'Hand' else hand.cards
    assert src[0] != 'Hand' or len(hcards) == len(hand.cards) - 1

    assert type(dst) is int or dst == 'Empty'
    assert type(src[0]) is int or src[0] == 'Hand'
    assert type(da_muovere) is Card
    assert type(giocata) is TaggedCards or giocata == []

    idx = -1 if dst == 'Empty' else tavolo.cards.index(giocata) 
    news = [TaggedCards([da_muovere])] if type(giocata) is list else []
    rimpiazzata = False
    for i, t in enumerate(tavolo.cards):
        if i == idx:
            p = TaggedCards(giocata.cards + [da_muovere])
            news.append(p)
        elif not rimpiazzata and da_muovere in t.cards:
            t = [c for c in t.cards if c != da_muovere]
            if t != []:
                news.append(TaggedCards(t))
            rimpiazzata = True
        else:
            news.append(t)
    return Table(news), Hand(hcards)
