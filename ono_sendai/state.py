import sys
sys.path.append('../')
import json
from copy import deepcopy as copy
from functools import cmp_to_key

from time import sleep

from IPython import embed as fuck

from metro_holografix.cardtypes import *
import symbols as sym

class Table(Tavolo):

    def is_valid(self):
        return len(self.cards) == 0 or (len(self.singles()) == 0 and len(self.getNonValide()) == 0)

    def flatten(self):
        return [c for tc in self.cards for c in tc.cards]

    def split_repr(self, ocards):
        l = len(ocards)
        if l == 13:
            return ocards
        else:
            i = l-1
            while ocards[i].value-1 == ocards[i-1].value:
                i -= 1
            return ocards[i:] + ocards[:i]

    def widget_repr(self):
        for ts in self.cards:
            ocards = list(sorted(ts.cards, key=lambda c: c.value))

            if ts.tipo == 'Scala' and ocards[-1].value == 13 and ocards[0].value == 1:
                ocards = self.split_repr(ocards)

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
    from random import shuffle
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
    def __init__(self, human, ids):
        assert human in ids
        self.humanPlayer = human
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
            if self.cur_player != self.humanPlayer:
                fuck() # debug # TODO: should remove
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

    def advance(self, table, hand):
        self.turn.append((table, hand))
        return table, hand

    def dump(self, fname):
        j = dict()
        j['table'] = [tc.cards for tc in self.table.cards]
        for pl, hand in self.players.items():
            j[pl] = hand.cards
        j['nrounds'] = self.nrounds
        j['deck'] = self.deck
        j['players'] = list(self.players.keys())
        with open(fname, 'w') as f:
            f.write(json.dumps(j))
        return j

    def load(self, fname):
        with open(fname, 'r') as f:
            j = json.loads(f.read())
        self.nrounds = j['nrounds']
        self.deck = [Card(seed, value) for seed, value in j['deck']]
        tcards = []
        for tc in j['table']:
            tcards.append(TaggedCards([Card(seed, value) for seed, value in tc]))
        self.table = Table(tcards)
        self.players = dict()
        for pl in j['players']:
            self.players[pl] = Hand([Card(seed, value) for seed, value in j[pl]])
        

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

def fromHandToEmpty(table, hand, src):
    assert type(src) is int
    to_move = hand.cards[src]
    hcards = hand.cards[:src] + hand.cards[src+1:]
    assert len(hcards) == len(hand.cards) - 1

    assert type(to_move) is Card

    news = [TaggedCards([to_move])] + table.cards
    newTable = Table(news)
    assert len(newTable.flatten()) + len(hcards) == len(hand.cards) + len(table.flatten()), fuck()
    return newTable, Hand(hcards)

def fromHandToTable(table, hand, src, dst):
    assert type(dst) is int
    assert type(src) is int

    in_play = table.cards[dst]
    to_move = hand.cards[src]
    hcards = hand.cards[:src] + hand.cards[src+1:]
    assert len(hcards) == len(hand.cards) - 1

    assert type(to_move) is Card
    assert type(in_play) is TaggedCards or in_play == []

    idx = table.cards.index(in_play)
    news = []
    news = table.cards[:dst] + table.cards[dst+1:] + [TaggedCards(table.cards[dst].cards + [to_move])]
    newTable = Table(news)
    assert len(newTable.flatten()) + len(hcards) == len(hand.cards) + len(table.flatten()), fuck()
    return newTable, Hand(hcards)

def removeFromTcards(t, to_move):
    # tmp = []
    # for j, c in enumerate(t.cards):
    #     if c == to_move:
    #         break
    #     tmp.append(c)
    # tmp.extend(t.cards[j+1:])
    # return tmp
    cards = copy(t.cards)
    cards.remove(to_move)
    return cards

def fromTableToEmpty(table, hand, src, to_move):
    assert type(src) is tuple # TODO: unused src[1], even in other TableToTable
    in_play = []
    tpos, cpos = src
    hcards = hand.cards

    assert type(src[0]) is int
    assert type(to_move) is Card

    news = [TaggedCards([to_move])]

    for i, t in enumerate(table.cards):
        if tpos == i:
            tmp = removeFromTcards(t, to_move)
            if tmp != []:
                news.append(TaggedCards(tmp))
        else:
            news.append(t)
    newTable = Table(news)
    assert len(newTable.flatten()) + len(hcards) == len(hand.cards) + len(table.flatten()), fuck()
    return newTable, Hand(hcards)

def fromTableToTable(table, hand, src, dst, to_move):
    assert type(src) is tuple
    in_play = table.cards[dst]
    tpos, cpos = src
    # to_move = table.cards[tpos].cards[cpos]
    hcards = hand.cards
    assert type(to_move) is Card
    assert type(in_play) is TaggedCards

    news = []
    rimpiazzata = False
    for i, t in enumerate(table.cards):
        if i == dst:
            p = TaggedCards(in_play.cards + [to_move])
            news.append(p)
        elif tpos == i:
            tmp = removeFromTcards(t, to_move)
            if tmp != []:
                news.append(TaggedCards(tmp))
        else:
            news.append(t)
    newTable = Table(news)
    assert len(newTable.flatten()) + len(hcards) == len(hand.cards) + len(table.flatten()), fuck()
    return newTable, Hand(hcards)
