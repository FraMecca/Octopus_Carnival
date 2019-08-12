open Core;;
open Out_channel;;

open Cards;;
open Tcards;;
open Table;;

let card_to_string c = String.concat ["{ seed: "; card_type_to_string c.seed;
                                      "; value: "; string_of_int c.value; " }"]
let print_card chan card = Out_channel.output_string chan (card_to_string card);;

let tcards_to_string c = "TCards: <"::
                                  Tcards.card_tag_to_string c.tag::":"::
                                  Tcards.game_strategy_to_string c.strategy::
                                  ">["::
                                  (List.map ~f:(fun c -> card_to_string c) c.cards |> String.concat)::
                                  "]"::[] |> String.concat
let print_tcards chan tcards = Out_channel.output_string chan (tcards_to_string tcards);;

let table_to_string c = "Table: <"::
                        (List.map ~f:(fun c -> tcards_to_string c) c.cards |> String.concat)::
                         ">"::[] |> String.concat ;;
let print_table chan table = Out_channel.output_string chan (table_to_string table);;


let t = play (make [
      Tcards.make [
        Cards.make Pikes 2;
        Cards.make Tiles 2;
        Cards.make Hearts 2;
      ];
      Tcards.make [
        Cards.make Hearts 2;
      ]
    ]) (* table_cards *)
    (Tcards.make [
        Cards.make Pikes 2;
        Cards.make Tiles 2;
        Cards.make Hearts 2;
      ]) (* in_play *)
    (Cards.make Hearts 2) (* to_move *)
(* in  make [
 *     Tcards.make [
 *       Cards.make Pikes 2;
 *       Cards.make Tiles 2;
 *       Cards.make Hearts 2;
 *       Cards.make Hearts 2;
 *     ]
 *   ] ;; *)
    in
    Printf.printf "%a\n" t

let deck = Cards.init
let card, _ = draw deck;;
Printf.printf "%a\n" print_card card

(* Mosse: Aggiunta, spostamento *)
(* 
 Triplette giocabili in mano, doppie usabili, singole usabili
 una volta vista la mano, rimuovi le carte inusabili nel turno;
 considerata una carta giocabile in mano, considera le carte "prossime", bruteforce;
*)

(* TESTS TODO: *)

