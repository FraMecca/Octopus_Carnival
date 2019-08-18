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
        return len(self.singles()) == 0 and len(self.getNonValide()) == 0

    def widget_repr(self):
        for ts in self.cards:
            yi = [sym.big['hat']]
            seed = ts.cards[0][0].lower()
            yi.append(sym.big[seed])
            yi.append(sym.big[ts.cards[0][1]])
            for card in ts.cards[1:]:
                seed = card[0].lower()
                yi.append(sym.sym[seed][card[1]])
            yield yi
                

class Hand:
    def __init__(self, cards):
        def sortc(a, b):
            return -1 if (a[1],a[0]) < (b[1],b[0]) else 1
        self.cards = list(sorted(cards, key=cmp_to_key(sortc)))

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
    odeck = [m for seed in ['Pikes', 'Hearts', 'Clovers', 'Tiles']  for m in make_set(seed)]
    shuffle(odeck)
    return odeck

class WrongMoveException(Exception):
    pass

class State:
    def __init__(self, ids):
        self.deck = make_deck()
        self.players = dict()
        self.table = Table([])
        self.round = None
        self.ids = ids
        self.cur_player = ids[0]
        for i in ids:
            cards = [self.deck.pop() for i in range(11)]
            self.players[i] = Hand(cards)

    def draw(self):
        hand = self.players[self.cur_player] 
        nhand = Hand(hand.cards + [self.deck.pop()])
        self.players[self.cur_player] = nhand
        self.round = None

    def next_turn(self):
        assert self.round is None
        next_player = self.ids[(self.ids.index(self.cur_player) + 1) % len(self.ids)]
        self.cur_player = next_player
        self.round = [(copy(self.table), copy(self.players[self.cur_player]))]

    def done(self):
        assert self.round is not None
        original = self.table
        table, hand = self.last()
        if not table.is_valid() or len(set(original.cards) - set(table.cards)) != 0:
            raise WrongMoveException()
        else:
            self.table, self.players[self.cur_player] = table, hand
            self.round = None
        
    def last(self):
        return self.round[-1]

    def backtrack(self):
        if len(self.round) >= 2:
            return self.round.pop()
        else:
            return self.round[0]

    def size(self):
        return len(self.round)

    def advance(self, src, dst):
        table, hand = self.last()
        t, h = gioca(table, hand, src, dst)
        self.round.append((t, h))
        return t, h

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

