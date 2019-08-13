def flatten(lst):
    assert type(lst) is list and (type(lst[0]) is set or type(lst[0]) is list)
    return [l for subl in lst for l in subl ]

def find_vicini(gioco, composed_tavolo, mano = None):
    def is_vicino(a, b):
        assert type(a) is tuple and type(b) is tuple
        return (a[0] == b[0] and (a[1] == b[1] - 1 or a[1] == b[1] + 1)) or (a[0] != b[0] and a[1] == b[1])

    assert type(gioco) is list or type(gioco) is set
    results = []
    ricerca = []
    tp = type(composed_tavolo[0])
    tavolo = flatten(composed_tavolo) if tp is list or tp is set else composed_tavolo
    ricerca.extend(tavolo)
    if mano is not None:
        ricerca.extend(mano) 
    for g in gioco:
        results += [t for t in ricerca if is_vicino(t, g)]

    return list(sorted(set(results), key=lambda x: x[1]))

carte_test = [('quadri', 3), ('picche', 1), ('fiori', 1), ('cuori', 1)]
assert set(find_vicini([('quadri', 1)], [carte_test])) == {('fiori', 1), ('cuori', 1), ('picche', 1)}
mano_test = [('quadri', 2),('quadri', 4)]
assert set(find_vicini([('quadri', 1), ('quadri', 3)], [carte_test], mano_test)) == set([('fiori', 1), ('picche', 1), ('cuori', 1), ('quadri', 2), ('quadri', 4)])

def gioca_vicini(carta, tavolo, mano, giocata_attuale, soluzione):
    def prune(carte_giocate, lst, strategia):
        if strategia == 'tris':
            return [l for l in lst if l[0] not in carte_giocate]
        elif strategia == 'scala':
            l = list(sorted(carte_giocate, key=lambda x: x[1]))
            first, last = l[0], l[1]
            return [l for l in lst if l[1] < first or l[1] > last]
        else:
            assert False
        
    giocabili = find_vicini([carta], tavolo)
    if len(giocata_attuale) >= 1:
        l = [c for c in giocata_attuale]
        strategia = 'tris' if l[0][1] == l[0][1] else 'scala'
        giocabili = prune(list(giocata_attuale) + [carta], giocabili, strategia)
    # TODO: fai prune fra gioabili e giocata_attuale
    # ovvero togli vicini che non rispettano la strategia attuale
    # se scala controlli stesso seme e valore minore se carta < giocata_attuale e viceversa
    # se tris controlli no semi doppiioni
    if giocabili == []:
        # piazzamento
        print("DDDDDD: Piazzamento")
        mano.remove(carta)
        giocata_attuale.add(carta)
        return algor(tavolo, mano, giocata_attuale, soluzione)
    else:
        # rimozione
        print("DDDDDD: Rimozione")
        new_carta = giocabili[0]
        len_prima = sum([len(t) for t in tavolo])
        tavolo = list(map(lambda x: x if new_carta not in x else x - set([new_carta]), tavolo))   # remove new_carta from tavolo
        assert sum([len(t) for t in tavolo]) < len_prima or len_prima == 0
        giocata_attuale.add(new_carta)
        return algor(tavolo, mano, giocata_attuale, soluzione)

def print_1(tavolo, mano, giocata_attuale, soluzione):
    print("--------") ;  print("TAVOLO:", tavolo) ; print("MANO:", mano) ; print("ATTUALE:", giocata_attuale)
    print("SOLUZIONE:", soluzione) ; print("--------\n")

def algor(tavolo, mano, giocata_attuale, soluzione):
    print_1(tavolo, mano, giocata_attuale, soluzione)
    for t in tavolo:
        assert type(t) is set
    for m in mano:
        assert type(m) is tuple

    if  giocata_attuale == set():
        for x in mano:
            lanciabili = find_vicini([x], tavolo, mano)
            for carta in lanciabili:
                gioca_vicini(carta, tavolo, mano, giocata_attuale, soluzione)
    else:
        if is_valida(giocata_attuale):
            soluzione, tavolo, mano = aggiorna(tavolo, mano, giocata_attuale, soluzione)
            algor(tavolo, mano, set(), soluzione)
        else:
            rimuovi = non_valide(tavolo)
            tavolo = [t for t in map(lambda x: x if x != rimuovi else None, tavolo) if t is not None] # tavolo - rimuovi
            for r in rimuovi:
                mano.update(r)

            lanciabili = find_vicini(giocata_attuale, tavolo, mano)
            for carta in lanciabili:
                gioca_vicini(carta, tavolo, mano, giocata_attuale, soluzione)

def non_valide(tavolo):
    return [c for c in tavolo if not is_valida(c)]

def aggiorna(tavolo, mano, giocata_attuale, soluzione):
    soluzione.append(giocata_attuale)
    tavolo.append(soluzione[-1])
    print("--------> SOLUZIONE:", soluzione, tavolo, mano)
    return soluzione, tavolo, mano
        
def no_double_seed(carte):
   seeds = set([seed for seed, value in carte])
   return len(seeds) == len(carte)

def is_only_one_seed(carte):
   seeds = set([seed for seed, value in carte])
   return len(seeds) == 1

def no_double_value(carte):
   seeds = set([value for seed, value in carte])
   return len(seeds) == len(carte)

def is_tris(carte):
   values = set([value for seed, value in carte])
   if len(values) == 1:
       return no_double_seed(carte)
   else:
       return False

def split(values, accum=[]):
    if len(values) > 2:
        a = values[0]
        b = values[1]
        if a == b - 1:
            return split(values[1:], accum + [a])
        else:
            return accum + [a], values[1:]
    else:
        return accum + [a], values[1:]

def is_straight(carte):
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
        last = carte[-1][1]
        carte = [v for s, v in carte]
        if last == 13 and carte[0] == 1:
            head, tail = split(carte)
            return _is_straight(head) and _is_straight(tail)
        else:
            return _is_straight(carte)

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

# carte_test = [('quadri', 1), ('picche', 1), ('fiori', 1), ('cuori', 1)]
# print(is_valida(carte_test))

# carte_test = [('picche', 13), ('picche', 12), ('picche', 1)]
# print(is_valida(carte_test))


if __name__ == '__main__':
    tavolo = [{("picche", 8), ("picche", 9), ("picche", 7)}, {("fiori", 9),("fiori", 8), ("fiori", 7)} ,{("cuori", 10), ("cuori", 9),("cuori",  8), ("cuori", 7)}]
    mano = {("cuori", 11),("cuori", 12), ("quadri", 7)}

    algor(tavolo, mano, set(), [])
