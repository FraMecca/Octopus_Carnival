from collections import namedtuple;

Card = namedtuple('Card', 'seed value')

class Mano:
    cards = list() # lista di cards 
    def __init__(self, carte):
        assert type(carte) is list and type(carte[0]) is Card
        self.cards = carte # lista di Carte

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
        import functools
        def cmp(c1, c2):
            return c1.value < c2.value if c1.seed == c2.seed else c1.seed < c2.seed
        lst = tuple(sorted(self.cards, key=functools.cmp_to_key(cmp)))
        return hash(lst)

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

class Tavolo:
    cards = list() # lista di taggedcards
    def __init__(self, cs):
        assert type(cs) is list
        self.cards = cs

    def __hash__(self):
        return sum([c.__hash__() for c in self.cards])

    def __repr__(self):
        return "Tavolo<%s>" % (self.cards,)

    def getNonValide(self):
        assert type(self.cards[0]) is TaggedCards
        f = [c for c in self.cards if c.tag == 'NonValido']
        return f

    def getValide(self):
        assert type(self.cards[0]) is TaggedCards
        f = [c for c in self.cards if c.tag == 'Valido']
        return f

    def getAll(self):
        return self.cards

    def llen(self):
        return len(flatten(self.getAll()))

    def punteggio(self):
        return len(self.getValide()) - len(self.getNonValide())

# old ocaml work
def flatten(lst):
    return sorted([s for subl in lst for s in subl], key=lambda x: x.value)

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
