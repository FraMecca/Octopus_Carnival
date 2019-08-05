open List
open Cards

type ingame_cards = card list
type player = { name: string ; cards: card list }
type table = { deck: card list ; ingame: ingame_cards;  players: player list }

let deck = Cards.init
let card, _ = draw deck;;
Printf.printf "%a\n" print_card card

(* Mosse: Aggiunta, spostamento *)
(* 
 Triplette giocabili in mano, doppie usabili, singole usabili
 una volta vista la mano, rimuovi le carte inusabili nel turno;
 considerata una carta giocabile in mano, considera le carte "prossime", bruteforce;
*)

type status =
  | Valid
  | Invalid
  | Unknown ;;


let no_double_seed cards =
  List.sort_uniq Cards.seed_cmp cards |> List.length = List.length cards

let is_only_one_seed cards =
  List.sort_uniq Cards.seed_cmp cards |> List.length = 1

let no_double_value cards =
  List.sort_uniq Cards.value_cmp cards |> List.length = List.length cards

let is_tris cards =
  match (List.sort_uniq Cards.value_cmp cards)  with
  | [_] -> no_double_seed cards (* only one value, check for right seeds *)
  | _::_ -> false
  | [] -> assert false

let rec split l fst =
  match l with
  | hd::hd'::tl when hd=hd'-1 -> split (hd'::tl) (fst@[hd])
  | hd::tl -> fst@[hd], tl
  | [] -> assert false


let is_straight _cards =
  let rec _is_straight cards =
    match cards with
    | hd::hd'::tl when hd=hd'-1 -> _is_straight (hd'::tl)
    | [] -> assert false
    | [_] -> true (* list was consumed *)
    | _::_ -> false in

  if (not (no_double_value _cards && is_only_one_seed _cards)) then
    false
  else
    let last = List.rev _cards |> hd in
    let cards  = List.map (fun c -> c.value) _cards  (* use only values *) in
    if last.value = 13 && (hd cards) = 1 then (* circolare *)
      let fst, snd = split cards [] in (_is_straight fst) && (_is_straight snd)
    else
      _is_straight cards

let is_valid _cards =
  let cards = List.sort Cards.value_cmp _cards in
  if length cards < 3 then
    false
  else
    match cards with
    | a::b::_ when Cards.value_cmp a b = 0  -> is_tris cards
    | _ -> is_straight cards;;


let rec play cards =
   true 

let start_play ingame cards =
  ingame @ cards |> List.sort Cards.value_cmp |> play
;;
(* TESTS TODO: *)
let cards = [{seed=Clovers; value=1}; {seed=Hearts; value=1}; {seed=Pikes; value=1}] in
assert (is_valid cards);;

let cards = [{seed=Tiles; value=1}; {seed=Clovers; value=1}; {seed=Hearts; value=1}; {seed=Pikes; value=1}] in
assert (is_valid cards);;

let cards = [{seed=Tiles; value=2}; {seed=Clovers; value=1}; {seed=Hearts; value=1}; {seed=Pikes; value=1}] in
assert (not (is_valid cards));;

let cards = [{seed=Hearts; value=2}; {seed=Hearts; value=2}; {seed=Hearts; value=4}]
in assert (not (no_double_value cards));;

let cards = [{seed=Hearts; value=2}; {seed=Hearts; value=2}; {seed=Hearts; value=4}]
in assert (not (no_double_seed cards));;

let cards = [{seed=Pikes; value=2}; {seed=Clovers; value=2}; {seed=Tiles; value=4}; {seed=Hearts; value=4}]
in assert (no_double_seed cards);;

let cards = [{seed=Hearts; value=4}; {seed=Hearts; value=3}; {seed=Hearts; value=2}; {seed=Hearts; value=1}]
in assert (is_valid cards);;

let cards = [{seed=Hearts; value=13}; {seed=Hearts; value=12}; {seed=Hearts; value=2}; {seed=Hearts; value=1}]
in assert (is_valid cards);;

let cards = [{seed=Pikes; value=13}; {seed=Hearts; value=12}; {seed=Hearts; value=2}; {seed=Hearts; value=1}]
in assert (not (is_valid cards));;

let cards = [{seed=Pikes; value=13}; {seed=Pikes; value=12}; {seed=Pikes; value=1}]
in assert (is_valid cards);;
let cards = [{seed=Hearts; value=12}; {seed=Pikes; value=12}; {seed=Pikes; value=1}]
in assert (not (is_valid cards));;

let cards = [{seed=Hearts; value=13}; {seed=Hearts; value=3}; {seed=Hearts; value=2}; {seed=Hearts; value=1}]
in assert (is_valid cards);;


let cards = [{seed=Hearts; value=1}] in
let ingame = [{seed=Hearts; value=13}; {seed=Hearts; value=3}; {seed=Hearts; value=2}]
in assert (start_play ingame cards);;

let cards = [{seed=Tiles; value=12}; {seed=Tiles; value=13}; {seed=Pikes; value=3}; {seed=Clovers; value=3}] in
let ingame = [{seed=Hearts; value=1}; {seed=Hearts; value=13}; {seed=Hearts; value=12};
              {seed=Pikes; value=1}; {seed=Clovers; value=1}; {seed=Tiles; value=1};
              {seed=Hearts; value=2}; {seed=Pikes; value=2}; {seed=Clovers; value=2}]
in assert (start_play ingame cards);; (* Risultato: straight 1-2-12-13 Hearts; straight 1-2-3 Pikes; straight 1-2-3 Clovers; straight 1-13-12 Tiles *)
