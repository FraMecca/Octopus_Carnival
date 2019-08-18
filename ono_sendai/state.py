import sys
sys.path.append('../')
import json

from metro_holografix.cardtypes import *
import symbols as sym

Hand = Tavolo
class Table(Tavolo):

    def is_valid(self):
        return len(self.getNonValide()) == 0

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
        self.cards = cards

    def widget_repr(self):
        yi = [sym.big['hat']]
        seed = self.cards[0][0].lower()
        yi.append(sym.big[seed])
        yi.append(sym.big[self.cards[0][1]])
        for card in self.cards[1:]:
            seed = card[0].lower()
            yi.append(sym.sym[seed][card[1]])
        return yi
             

events = [ # list of tuples table-hand
    (Table([
        TaggedCards([
            Card("Pikes", 2),
            Card("Clovers", 2),
            Card("Tiles", 2),
            Card("Hearts", 2)]),
        TaggedCards([
            Card("Hearts", 1),
            Card("Clovers", 1),
            Card("Pikes", 1),
            Card("Tiles", 1)]),
    ]), Hand([
        Card("Pikes", 12),
        Card("Clovers", 12),
        Card("Tiles", 12),
        Card("Hearts", 12),
        Card("Hearts", 13),
        Card("Clovers", 13),
        Card("Pikes", 13),
        Card("Tiles", 13)
    ]))
]

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

def next():
    return events[-1]

def prev():
    if len(events) >= 2:
        return events.pop()
    else:
        return events[0]

def size():
    return len(events)

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

def update_table(table, hand, src, dst):
    t, h = gioca(table, hand, src, dst)
    events.append((t, h))
    return t, h
