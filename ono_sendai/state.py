import sys
sys.path.append('../')
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
                
             

table = Table([
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
])

# TODO: refactor language
def gioca(tavolo, src, dst):
    giocata = [] if dst == 'Empty' else tavolo.cards[dst]
    da_muovere = tavolo.cards[src[0]].cards[src[1]]
    assert type(dst) is int or dst == 'Empty' or dst == 'Hand'
    assert type(da_muovere) is Card
    assert type(giocata) is TaggedCards or giocata == []
    idx = -1 if dst == 'Empty' else tavolo.cards.index(giocata) 
    news = [TaggedCards([da_muovere])] if giocata == [] else []
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
    return Table(news)

def update_table(table, src, dst):
    return gioca(table, src, dst)
