from cardtypes import *
from alg import *

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
assert TaggedCards([Card('picche', 2)]) > TaggedCards([Card('picche',2), Card('fiori', 2), Card('cuori', 2), Card('quadri', 2)])

tavolo_test = Tavolo([TaggedCards([Card('picche', 1), Card('fiori', 1), Card('cuori', 1)])])
mano_test = Mano([Card('picche', 3)])
assert riduci(mano_test, tavolo_test) == []
mano_test = Mano([Card('picche', 1)])
assert set(riduci(mano_test, tavolo_test)) == set([Card('picche', 1)])
mano_test = Mano([Card('picche', 4), Card('picche', 5), Card('picche', 3)  ])
assert set(riduci(mano_test, tavolo_test)) == set([Card('picche', 5), Card('picche', 4), Card('picche', 3)])
