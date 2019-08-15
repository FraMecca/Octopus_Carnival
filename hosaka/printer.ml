open Cards;;
open Tcards;;
open Table;;

open Core;;
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

let printer n score table = 
  Printf.printf "****%d:%d****\n%a\n********\n" n score print_table table;;
let void_printer _ _ _ = ();;
