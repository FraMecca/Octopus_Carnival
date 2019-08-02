open Core
       
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
let print_card chan card = output_string chan (card_to_string card);;

(*
let deck =
  let ordered_deck =
    let make_set tp =
      List.map ~f:(fun x->{seed=tp; value=x}) (List.range 1 14) in (* make a set of cards of one seed *)
    List.concat [make_set Hearts ; make_set Tiles ; make_set Clovers ; make_set Pikes] in
  let nd = List.map ~f:(fun e -> Random.bits (), e) ordered_deck in
  let sorted = List.sort ~compare:compare nd in List.map ~f:snd sorted;;
*)
let make_set tp =
  List.map ~f:(fun x->{seed=tp; value=x}) (List.range 1 14);;(* make a set of cards of one seed *)
let deck = 
  List.concat [make_set Hearts ; make_set Tiles ; make_set Clovers ; make_set Pikes] |>
  List.map ~f:(fun e -> Random.bits (), e) |> List.sort ~compare:compare  |> List.map ~f:snd 

let draw deck = match deck with
    | [] -> {seed=Nothing ; value=0}, []
    | hd::tl -> hd, tl

let deck = deck
let card, _ = draw deck;;

Printf.printf "%a" print_card card
