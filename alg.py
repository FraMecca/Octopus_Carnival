from collections import namedtuple;
from copy import copy

def flattenByValue(lst):
    return sorted([s for subl in lst for s in subl], key=lambda x: x.value)

def flatten(lst):
    return flattenByValue(lst)

def flattenBySeed(lst):
    return sorted([s for subl in lst for s in subl], key=lambda x: x.seed)

def print_1(tavolo, n):
    print('-------------',n,'-------------')
    for t in tavolo.cards:
        print(t)
    print('-------------',n,'-------------')

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
        self.cards = carte # lista di Carte
        self.tag = 'NonValido' if not is_valida(self.cards) else 'Valido'
        self.tipo = 'Singolo' if len(carte) == 1 else 'Tris' if carte[0].seed != carte[1].seed else 'Scala'

    def __repr__(self):
        return "TaggedCards<%s, %s, %s>" % (self.cards, self.tag, self.tipo)

    def __iter__(self):
        return self.cards.__iter__()

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

def gioca(tavolo, giocata, da_muovere):
    assert type(da_muovere) is Card
    idx = tavolo.cards.index(giocata)
    for current_tag in ['NonValido', 'Valido']:
        for i, t in enumerate(tavolo.cards):
            if t.tag == current_tag and da_muovere in t.cards:
                t = [c for c in t.cards if c != da_muovere]
                if t != []:
                    tavolo.cards[i] = [TaggedCards(t)] # mettilo davanti cosi` che sia il primo
                    # preso in considerazione
                del tavolo.cards[idx]
                tavolo.cards = [TaggedCards(giocata.cards + [da_muovere])] + tavolo.cards
                return tavolo
    assert False

def alg(tavolo, tavolo_iniziale, soluzioni, n):
    # qua si presume di avere gia` tutte le carte della mano stese sul tavolo come gruppo singolo
    # di carte non valide (alla prima iterazione)
    print_1(tavolo, n)
    nonV = tavolo.getNonValide()
    if n >= 20: # maximum depth
        return
    elif len(nonV) == 0:
        return
    else:
        for carte in nonV:
            # carte = nonV[0] # TaggedCards
            assert type(carte) is TaggedCards and carte.tag == 'NonValido'
            vicini = find_vicini(carte, tavolo) # lista di Card
            for v in vicini:
                next_tavolo = gioca(copy(tavolo), carte, v)
                alg(next_tavolo, tavolo_iniziale, soluzioni, n+1)
        
def find_vicini(carte, tavolo):
    assert type(tavolo) is Tavolo and type(carte) is TaggedCards
    all = flatten(tavolo.getAll())
    if carte.tipo == 'Singolo':
        return [a for a in all if is_tris(carte.cards+[a]) or is_straight(carte.cards+[a])]
    elif carte.tipo == 'Tris':
        return [a for a in all if is_tris(carte.cards+[a])]
    elif carte.tipo == 'Scala':
        return [a for a in all if is_straight(carte.cards+[a])]
    else:
        assert False
    
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

    if not no_double_value(carte) and is_only_one_seed(carte):
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
    alg(tavolo, tavolo, [], 0)

