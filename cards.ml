open List;;
open Core;;
open Out_channel;;

Random.self_init ();;

type card_type =
  | Hearts 
  | Tiles 
  | Clovers 
  | Pikes
  | Nothing

let card_type_to_string = function 
  | Hearts -> "Hearts"
  | Tiles -> "Tiles"
  | Clovers -> "Clovers"
  | Pikes-> "Pikes"
  | Nothing-> "Nothing"

type card = { seed: card_type ; value: int }

let card_to_string c = String.concat ["{ seed: "; card_type_to_string c.seed;
                                      "; value: "; string_of_int c.value; " }"]
let print_card chan card = Out_channel.output_string chan (card_to_string card);;
let value_cmp a b = Int.compare a.value b.value
let seed_cmp = fun a b -> if card_type_to_string a.seed > card_type_to_string b.seed then 1 else
    if card_type_to_string a.seed = card_type_to_string b.seed then 0 else -1

let make_set tp =
  List.map ~f:(fun x -> { seed=tp; value=x }) (List.range 1 14);; (* make a set of cards of one seed *)
let init = 
  List.concat [make_set Hearts ; make_set Tiles ; make_set Clovers ; make_set Pikes ;
               make_set Hearts ; make_set Tiles ; make_set Clovers ; make_set Pikes] |>
  List.map ~f:(fun e -> Random.bits (), e) |>
  List.sort ~compare:(fun a b -> if fst a > fst b then 1 else -1)  |>
  List.map ~f:snd 

let draw deck = match deck with
    | [] as l -> {seed=Nothing ; value=0}, l
    | hd::tl -> hd, tl
