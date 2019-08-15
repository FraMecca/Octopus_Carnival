from copy import deepcopy as copy # FUK
from cardtypes import *

DO_TESTS = False
DO_PRINT = True
MAX = -1000
best = None
DONE = False
MEM = set()

def print_1(tavolo, n):
    if not DO_PRINT:
        return                  
    global MEM, MAX
    st = ('------------- '+str(n)+':'+str(tavolo.punteggio())+':'+str(MAX)+' -------------'+'='+str(len(MEM)))
    print(st)
    for t in tavolo.cards:
        print(t)
    print(st)

def gioca(tavolo, giocata, da_muovere):
    assert type(da_muovere) is Card
    idx = tavolo.cards.index(giocata)
    news = [TaggedCards(giocata.cards + [da_muovere])]
    rimpiazzata = False
    for i, t in enumerate(tavolo.cards):
        if i == idx:
            continue # skip the one containing giocata
        if not rimpiazzata and da_muovere in t.cards:
            t = [c for c in t.cards if c != da_muovere]
            if t != []:
                news.append(TaggedCards(t))
            rimpiazzata = True
        else:
            news.append(t)
    return Tavolo(news)

def non_migliora(punteggio):
    assert type(punteggio) is list
    if len(punteggio) <= 7:
        return False
    p = punteggio[-7:]
    ma = max(p)
    mi = min(p)
    return abs(ma-mi) < 2

def tavolo_rispettato(start, end):
    start_mano = set([c for c in start.cards if c.tipo == 'Singolo'])
    for e in end.cards:
        if e.tipo == 'Singolo' and e not in start_mano:
            return False
    return True
    
def alg(tavolo, tavolo_iniziale, soluzioni, n, punteggio):
    # qua si presume di avere gia` tutte le carte della mano stese sul tavolo come gruppo singolo
    # di carte non valide (alla prima iterazione)
    global MAX, DONE, best, MEM
    if DONE or tavolo.__hash__() in MEM:
        return
    else:
        DONE = len(tavolo.getNonValide()) == 0 # GLOBAL EXIT
        MEM.add(tavolo.__hash__())

    print_1(tavolo, n)
    punteggio.append(tavolo.punteggio())
    startL = tavolo.llen()
    if tavolo_rispettato(tavolo_iniziale, tavolo) and tavolo.punteggio() > MAX:
        MAX = tavolo.punteggio()
        best = copy(tavolo)

    if len(tavolo.getNonValide()) == 0 or n > 14 or non_migliora(punteggio):
        return
    else:
        for carte in tavolo.getAll():
            assert type(carte) is TaggedCards# and carte.tag == 'NonValido'
            vicini = find_vicini(carte, tavolo) # lista di Card
            for v in vicini:
                next_tavolo = gioca(tavolo, carte, v)
                assert startL == next_tavolo.llen()
                alg(next_tavolo, tavolo_iniziale, soluzioni, n+1, copy(punteggio))

def find_vicini(carte, tavolo):
    def _find_vicini(carte, all):
        if carte.tipo == 'Singolo':
            return [a for a in all if is_tris(carte.cards+[a]) or is_straight(carte.cards+[a])]
        elif carte.tipo == 'Tris':
            return [a for a in all if is_tris(carte.cards+[a])]
        elif carte.tipo == 'Scala':
            return [a for a in all if is_straight(carte.cards+[a])]
        else:
            assert False

    assert type(tavolo) is Tavolo and type(carte) is TaggedCards
    return _find_vicini(carte, flatten(tavolo.getAll()))


if DO_TESTS:
    import test

def riduci(mano, tavolo):
    assert type(mano) is Mano and type(tavolo) is Tavolo
    tagged_mano = [TaggedCards([c]) for c in mano.cards]
    tavolo_e_mano = Tavolo(tavolo.cards+tagged_mano)
    return [c.cards[0] for c in tagged_mano if find_vicini(c, tavolo_e_mano) != []]
        
if __name__ == '__main__':
    tavolo1 = Tavolo([
        TaggedCards([
            Card("picche", 2),
            Card("fiori", 2),
            Card("cuori", 2)]),
        TaggedCards([
            Card("cuori", 1),
            Card("fiori", 1),
            Card("picche", 1),
            Card("quadri", 1)]),
        # mano
        TaggedCards([
            Card("quadri", 13)]),
        TaggedCards([
            Card("quadri", 12)]),
        TaggedCards([
            Card("cuori", 13)]),
        TaggedCards([
            Card("cuori", 12)]),
        TaggedCards([
            Card("fiori", 3)]),
        TaggedCards([
            Card("picche", 3)]),
        # TaggedCards([
            # Card("cuori", 12)])
    ])
    tavolo2 = Tavolo([
        TaggedCards([
            Card("picche", 2),
            Card("fiori", 2),
            Card("quadri", 2),
            Card("cuori", 2)]),
        TaggedCards([
            Card("cuori", 1),
            Card("fiori", 1),
            Card("picche", 1),
            Card("quadri", 1)]),
        # mano
        TaggedCards([
            Card("picche", 3)]),
    ])
    tavolo3 = Tavolo([
        TaggedCards([
            Card("fiori", 7),
            Card("fiori", 8),
            Card("fiori", 9)]),
        TaggedCards([
            Card("picche", 7),
            Card("picche", 8),
            Card("picche", 9)]),
        TaggedCards([
            Card("cuori", 7),
            Card("cuori", 8),
            Card("cuori", 9),
            Card("cuori", 10)]),
        # mano
        TaggedCards([
            Card("cuori", 11)]),
        TaggedCards([
            Card("cuori", 12)]),
        TaggedCards([
            Card("quadri", 7)])
    ])
    tavolo4 = Tavolo([
        TaggedCards([
            Card("fiori", 7),
            Card("fiori", 8),
            Card("fiori", 9)]),
        TaggedCards([
            Card("picche", 7),
            Card("picche", 8),
            Card("picche", 9)]),
        TaggedCards([
            Card("cuori", 7),
            Card("cuori", 8),
            Card("cuori", 9),
            Card("cuori", 10)]),
        # mano
        TaggedCards([
            Card("cuori", 6)]),
        TaggedCards([
            Card("cuori", 8)])
    ])
    tavolo5 = Tavolo([
        # mano
        TaggedCards([
            Card("cuori", 7)]),
        TaggedCards([
            Card("cuori", 6)]),
        TaggedCards([
            Card("cuori", 8)])
    ])

    tavolo = tavolo1
    alg(tavolo, tavolo, [], 0, [])
    # print('****BEST:')
    # print_1(best, MAX)
