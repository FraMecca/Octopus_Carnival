open Core;;
open Out_channel;;

open Cards;;
open Tcards;;
open Table;;

(* let card_to_string c = String.concat ["{ seed: "; card_type_to_string c.seed;
 *                                       "; value: "; string_of_int c.value; " }"] *)

let card_to_string c = String.concat ["{"; card_type_to_string c.seed;":"; string_of_int c.value; "}"]
let print_card chan card = Out_channel.output_string chan (card_to_string card);;

let tcards_to_string c = "TCards: <"::
                                  Tcards.card_tag_to_string c.tag::":"::
                                  Tcards.game_strategy_to_string c.strategy::
                                  ">["::
                                  (List.map ~f:(fun c -> card_to_string c) c.cards |> String.concat)::
                                  "]"::[] |> String.concat
let print_tcards chan tcards = Out_channel.output_string chan (tcards_to_string tcards);;

let table_to_string c = ""::
                        (List.map ~f:(fun c -> tcards_to_string c) c.cards |> String.concat ~sep:";\n")::
                         ">"::[] |> String.concat ;;
let print_table chan table = Out_channel.output_string chan (table_to_string table);;


let deck = Cards.init
let card, _ = draw deck;;
(* Printf.printf "%a\n" print_card card *)

(* Mosse: Aggiunta, spostamento *)
(* 
 Triplette giocabili in mano, doppie usabili, singole usabili
 una volta vista la mano, rimuovi le carte inusabili nel turno;
 considerata una carta giocabile in mano, considera le carte "prossime", bruteforce;
*)

(* TESTS TODO: *)
let printer table = 
  Printf.printf "********\n%a\n********\n" print_table table;;


(* let rec alg table original_table n (scores:int list) best max_score (dbg: table -> unit) = *)
open Hashtbl;;
let table = Table.make [
  Tcards.make [
    Cards.make Hearts 7;
    Cards.make Hearts 8;
    Cards.make Hearts 9;
  ];
  Tcards.make [
    Cards.make Pikes 7;
    Cards.make Pikes 8;
    Cards.make Pikes 9;
  ];
  Tcards.make [
    Cards.make Hearts 7;
    Cards.make Hearts 8;
    Cards.make Hearts 9;
    Cards.make Hearts 10;
  ];
  Tcards.make [
    Cards.make Hearts 6;
  ];
  Tcards.make [
    Cards.make Hearts 8;
  ]
] in
let new_tables = Table.alg table 0 [] in
(* List.iter ~f:(fun (t,_,_) -> printer t) new_table *)

Table.prova table [] [] (-1000)  printer new_tables []
