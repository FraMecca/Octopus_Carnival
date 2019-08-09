from collections import namedtuple;
from copy import deepcopy as copy # FUK

MAX = -1000
best = None
DONE = False
MEM = set()

def flattenByValue(lst):
    return sorted([s for subl in lst for s in subl], key=lambda x: x.value)

def flatten(lst):
    return flattenByValue(lst)

def flattenBySeed(lst):
    return sorted([s for subl in lst for s in subl], key=lambda x: x.seed)

def print_1(tavolo, n):
    st = ('------------- '+str(n)+':'+str(tavolo.punteggio())+' -------------')
    print(st)
    for t in tavolo.cards:
        print(t)
    print(st)

Card = namedtuple('Card', 'seed value')

class Mano:
    cards = list() # lista di cards 
    def __init__(self, carte):
        assert type(carte) is list and type(carte[0]) is Card
        self.cards = carte # lista di Carte
    def cardsByValue(self):
        return sorted(self.cards, key=lambda c: c.value)
    def cardsBySeed(self):
        return sorted(self.cards, key=lambda c: c.seed)

class TaggedCards:
    cards = None
    tag = ''
    tipo = ''
    def __init__(self, carte):
        assert type(carte) is list and type(carte[0]) is Card
        self.cards = list(sorted(carte, key=lambda x: str(x))) # lista di Carte
        self.tag = 'NonValido' if not is_valida(self.cards) else 'Valido'
        self.tipo = 'Singolo' if len(carte) == 1 else 'Tris' if is_tris(carte) else 'Scala'

    def __hash__(self):
                return hash(tuple(self))

    def __repr__(self):
        return "TaggedCards<%s, %s, %s>" % (self.cards, self.tag, self.tipo)

    def __iter__(self):
        return self.cards.__iter__()

    def __eq__(self, other):
        assert type(other) is type(self)
        if len(other.cards) != len(self.cards) or self.tag != other.tag or self.tipo != other.tipo:
            return False
        else:
            return set(self.cards) == set(other.cards)

    def __gt__(self, other):
        if self.tipo == 'Tris' and len(self.cards) == 4:
            return False
        if other.tipo == 'Tris' and len(other.cards) == 4:
            return True
        elif self.tipo != 'Singolo' and other.tipo == 'Singolo':
            return True
        elif self.tipo == 'Singolo' and other.tipo != 'Singolo':
            return False
        elif self.tag == 'NonValido' and other.tag == 'Valido':
            return True
        else:
            return False

    def cardsByValue(self):
        return sorted(self.cards, key=lambda c: c.value)
    def cardsBySeed(self):
        return sorted(self.cards, key=lambda c: c.seed)

        
class Tavolo:
    cards = list() # lista di taggedcards
    def __init__(self, cs):
        assert type(cs) is list
        self.cards = cs

    def __repr__(self):
        return "Tavolo<%s>" % (self.cards,)

    def getNonValide(self):
        assert type(self.cards[0]) is TaggedCards
        f = [c for c in self.cards if c.tag == 'NonValido']
        # return list(flattenByValue(f))
        return f

    def getValide(self):
        assert type(self.cards[0]) is TaggedCards
        f = [c for c in self.cards if c.tag == 'Valido']
        # return list(flattenByValue(f))
        return f

    def getAll(self):
        # return list(flattenByValue(self.cards))
        return self.cards
    def llen(self):
        return len(flatten(self.getAll()))

    def punteggio(self):
        return len(self.getValide()) - len(self.getNonValide())

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
                # tavolo.cards[i] = TaggedCards(t) 
                news.append(TaggedCards(t))
            rimpiazzata = True
            # tavolo.cards[idx] = TaggedCards(giocata.cards + [da_muovere])
            # return tavolo
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
    if DONE or str(tavolo) in MEM:
        print('TTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTTT')
        return
    else:
        DONE = len(tavolo.getNonValide()) == 0 # GLOBAL EXIT
        MEM.add(str(tavolo))
        print(len(MEM))

    print_1(tavolo, n)
    punteggio.append(tavolo.punteggio())
    startL = tavolo.llen()
    if non_migliora(punteggio) or len(tavolo.getNonValide()) == 0 or n > 14:
        if tavolo_rispettato(tavolo_iniziale, tavolo) and tavolo.punteggio() > MAX:
            MAX = tavolo.punteggio()
            best = copy(tavolo)
        return 
    else:
        for carte in tavolo.getAll():
            # carte = nonV[0] # TaggedCards
            assert type(carte) is TaggedCards# and carte.tag == 'NonValido'
            vicini = find_vicini(carte, tavolo) # lista di Card
            for v in vicini:
                next_tavolo = gioca(tavolo, carte, v)
                assert startL == next_tavolo.llen()
                # recur
                alg(next_tavolo, tavolo_iniziale, soluzioni, n+1, copy(punteggio))

def find_vicini(carte, tavolo):
    def _find_vicini(carte, all):
        # all = flatten(tavolo.getAll())
        if carte.tipo == 'Singolo':
            return [a for a in all if is_tris(carte.cards+[a]) or is_straight(carte.cards+[a])]
        elif carte.tipo == 'Tris':
            return [a for a in all if is_tris(carte.cards+[a])]
        elif carte.tipo == 'Scala':
            return [a for a in all if is_straight(carte.cards+[a])]
        else:
            assert False

    assert type(tavolo) is Tavolo and type(carte) is TaggedCards
    nonV = flatten(tavolo.getNonValide())
    va = flatten(tavolo.getValide())
    return _find_vicini(carte, nonV) + _find_vicini(carte, va)
    
def no_double_seed(carte):
   seeds = set([c.seed for c in carte])
   return len(seeds) == len(carte)

def is_only_one_seed(carte):
   seeds = set([c.seed for c in carte])
   return len(seeds) == 1

def no_double_value(carte):
   seeds = set([c.value for c in carte])
   return len(seeds) == len(carte)

def is_tris(carte):
   values = set([c.value for c in carte])
   if len(values) == 1:
       return no_double_seed(carte)
   else:
       return False

def split(values, accum=[]):
    a = values[0]
    if len(values) > 2:
        b = values[1]
        if a == b - 1:
            return split(values[1:], accum + [a])
        else:
            return accum + [a], values[1:]
    else:
        return accum + [a], values[1:]

def is_straight(carte):
    assert type(carte) is list and type(carte[0]) is Card
    def _is_straight(carte):
        if len(carte) == 1:
            return True
        elif len(carte) == 0:
            assert False
        else:
            a = carte[0]
            b = carte[1]
            if a == b - 1:
                return _is_straight(carte[1:])
            else:
                return False

    if not (no_double_value(carte) and is_only_one_seed(carte)):
        return False
    else:
        values = [v for s, v in sorted(carte, key=lambda x:x.value)]
        first, last = values[0], values[-1]
        if last == 13 and first == 1:
            head, tail = split(values)
            return _is_straight(head) and _is_straight(tail)
        else:
            return _is_straight(values)

def is_valida(carte):
    carte = list(sorted(carte, key = lambda x : x[1]))
    if len(carte) < 3:
        return False
    else:
        a = carte[0][1]
        b = carte[1][1]
        if a == b:
            return is_tris(carte)
        else:
            return is_straight(carte)

carte_test = [Card('quadri', 1), Card('picche', 1), Card('fiori', 1), Card('cuori', 1)]
print(is_valida(carte_test))

carte_test = [Card('picche', 13), Card('picche', 12), Card('picche', 1)]
print(is_valida(carte_test))

carte_test = [Card('quadri', 1), Card('picche', 1)]
print(is_tris(carte_test))
carte_test = [Card('picche', 13), Card('picche', 1)]
print(is_straight(carte_test))

# find_vicini test
tavolo_test = Tavolo([TaggedCards([Card('picche', 1), Card('fiori', 1), Card('cuori', 1)])])
res =  find_vicini(TaggedCards([Card('quadri', 1)]), tavolo_test)
assert set(res) == {Card('fiori', 1), Card('cuori', 1), Card('picche', 1)}
# mano_test = [('quadri', 2),('quadri', 4)]
tavolo_test = Tavolo([TaggedCards([Card('picche', 1), Card('fiori', 1), Card('cuori', 1)])])
# assert set(find_vicini([('quadri', 1), ('quadri', 3)], [carte_test], mano_test)) == set([('fiori', 1), ('picche', 1), ('cuori', 1), ('quadri', 2), ('quadri', 4)])
tavolo_test = Tavolo([
    TaggedCards([Card(seed='cuori', value=1), Card(seed='fiori', value=1), Card(seed='picche', value=1), Card(seed='quadri', value=1)]),
    TaggedCards([Card(seed='quadri', value=12), Card(seed='cuori', value=12), Card(seed='cuori', value=12), Card(seed='cuori', value=13)])])
res = find_vicini(TaggedCards([Card(seed='quadri', value=13)]), tavolo_test)
assert set(res) == {Card('quadri', 1), Card('quadri', 12), Card('cuori', 13)}

assert TaggedCards([Card('picche', 2)]) < TaggedCards([Card('picche',2), Card('fiori', 2)])
assert TaggedCards([Card('picche', 2)]) < TaggedCards([Card('picche',2), Card('fiori', 2)])
assert TaggedCards([Card('picche', 2)]) > TaggedCards([Card('picche',2), Card('fiori', 2), Card('cuori', 2), Card('quadri', 2)])



if __name__ == '__main__':
    # tavolo = [{("picche", 8), ("picche", 9), ("picche", 7)}, {("fiori", 9),("fiori", 8), ("fiori", 7)} ,{("cuori", 10), ("cuori", 9),("cuori",  8), ("cuori", 7)}]
    # mano = {("cuori", 11),("cuori", 12), ("quadri", 7)}
    tavolo = Tavolo([
        TaggedCards([
            Card("picche", 2),
            Card("fiori", 2),
            Card("cuori", 2)]),
        TaggedCards([
            Card("cuori", 1),
            Card("fiori", 1),
            Card("picche", 1),
            Card("quadri", 1)]),
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
        TaggedCards([
            Card("cuori", 12)])
    ])
        # TaggedCards([
            # Card("quadri", 2)]) # rimuovi
    # ])
    alg(tavolo, tavolo, [], 0, [])
    print('*************************************')
    print(best)
