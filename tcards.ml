open List;;
open Hashtbl;;

open Cards;;

type card_tag =
  | Invalid
  | Valid

let card_tag_to_string t =
  match t with
  | Invalid -> "Invalid"
  | Valid -> "Valid"

type game_strategy =
  | Tris
  | Straight
  | Single

let game_strategy_to_string t =
  match t with
  | Tris -> "Tris"
  | Straight -> "Straight"
  | Single -> "Single"

type tcards = { cards: card list ; tag: card_tag ; strategy: game_strategy }

let make cards =
  let strategy = if List.length cards = 1 then Single else
    if Cards.is_tris cards then Tris else Straight in
  { cards=cards ; tag=if Cards.is_valid cards then Valid else Invalid; strategy=strategy }

let contains needle haystack = List.mem needle haystack.cards

let (=) a b =
  if List.length a.cards != List.length b.cards || a.tag != b.tag || a.strategy != b.strategy then
    false
  else
    a.cards = b.cards

let length ts = List.length ts.cards
let cmp a b =
  (* TODO: improve *)
  if a.strategy == Tris && List.length a.cards == 4 then -1
  else if b.strategy == Tris && List.length b.cards == 4 then 1
  else if a.strategy != Single && b.strategy == Single then 1
  else if a.strategy == Single && b.strategy != Single then -1
  else if a.tag == Invalid && b.tag == Valid then 1
  else -1 ;;

(* TODO tests *)
assert (make [Cards.make Pikes 2] |>
        cmp (make [Cards.make Pikes 2 ; Cards.make Clovers 2]) == 1);; (* less than *)
assert (make [Cards.make Pikes 2] |>
cmp (make [Cards.make Pikes 2 ; Cards.make Clovers 2 ; Cards.make Tiles 2; Cards.make Hearts 2]) == -1)

let hash ts =
  ts.cards |>
  List.sort (fun a b -> if a.seed == b.seed then Cards.value_cmp a b else Cards.seed_cmp a b) |>
  Hashtbl.hash;;
