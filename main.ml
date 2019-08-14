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

let printer n score table = 
  Printf.printf "****%d:%d****\n%a\n********\n" n score print_table table;;
let void_printer n score table =  ();;
(* TESTS TODO: *)

(*
assert  ([
    Cards.make Hearts 6;
    Cards.make Hearts 7;
    Cards.make Hearts 8;
    Cards.make Hearts 9;
    Cards.make Hearts 10;]
    |> Cards.is_straight) ;;

assert  ([
    Cards.make Hearts 1;
    Cards.make Hearts 12;
    Cards.make Hearts 2;
    Cards.make Hearts 13;]
    |> Cards.is_straight) ;;
  
let ttable = Table.make [
  Tcards.make [
    Cards.make Clovers 7;
    Cards.make Clovers 8;
    Cards.make Clovers 9;
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
  ]
]
in
let neighs = neighbors 
  (Tcards.make [
    Cards.make Hearts 7;
    Cards.make Hearts 8;
    Cards.make Hearts 9;
    Cards.make Hearts 10;
  ]) ttable in
assert (neighs = [Cards.make Hearts 6]) ;;

let ttable = Table.make [
  Tcards.make [
    Cards.make Hearts 1;
    Cards.make Hearts 2;
    Cards.make Hearts 13;
  ];
  Tcards.make [
    Cards.make Pikes 1;
    Cards.make Pikes 2;
    Cards.make Pikes 3;
  ];
  Tcards.make [
    Cards.make Clovers 2;
    Cards.make Clovers 3;
  ];
  Tcards.make [
    Cards.make Clovers 1;
    Cards.make Tiles 1;
  ];
  Tcards.make [
    Cards.make Hearts 12;
    Cards.make Tiles 12;
  ];
]
in
let neighs = neighbors 
  (Tcards.make [
    Cards.make Hearts 1;
    Cards.make Hearts 2;
    Cards.make Hearts 13;
  ]) ttable in
assert (neighs = [Cards.make Hearts 12]) ;;
*)

let table1 = Table.make [
  Tcards.make [
    Cards.make Clovers 2;
    Cards.make Pikes 2;
    Cards.make Hearts 2;
  ];
  Tcards.make [
    Cards.make Clovers 1;
    Cards.make Tiles 1;
    Cards.make Pikes 1;
    Cards.make Hearts 1;
  ];
  Tcards.make [
    Cards.make Tiles 13;
  ];
  Tcards.make [
    Cards.make Tiles 12;
  ];
  Tcards.make [
    Cards.make Hearts 13;
  ];
  Tcards.make [
    Cards.make Hearts 12;
  ];
  Tcards.make [
    Cards.make Pikes 3;
  ];
  Tcards.make [
    Cards.make Clovers 3;
  ]
] in
let table1x = Table.make [
  Tcards.make [
    Cards.make Clovers 2;
    Cards.make Pikes 2;
    Cards.make Hearts 2;
  ];
  Tcards.make [
    Cards.make Clovers 1;
    Cards.make Tiles 1;
    Cards.make Pikes 1;
    Cards.make Hearts 1;
  ];
  Tcards.make [
    Cards.make Tiles 13;
  ];
  Tcards.make [
    Cards.make Tiles 12;
  ];
  Tcards.make [
    Cards.make Hearts 13;
  ];
  Tcards.make [
    Cards.make Hearts 12;
  ];
  Tcards.make [
    Cards.make Hearts 12;
  ];
  Tcards.make [
    Cards.make Pikes 3;
  ];
  Tcards.make [
    Cards.make Clovers 3;
  ]
] in
let table2 = Table.make [
  Tcards.make [
    Cards.make Clovers 2;
    Cards.make Tiles 2;
    Cards.make Pikes 2;
    Cards.make Hearts 2;
  ];
  Tcards.make [
    Cards.make Clovers 1;
    Cards.make Tiles 1;
    Cards.make Pikes 1;
    Cards.make Hearts 1;
  ];
  Tcards.make [
    Cards.make Pikes 3;
  ]
] in
let table3 = Table.make [
  Tcards.make [
    Cards.make Clovers 7;
    Cards.make Clovers 8;
    Cards.make Clovers 9;
  ];
  Tcards.make [
    Cards.make Hearts 7;
    Cards.make Hearts 8;
    Cards.make Hearts 9;
    Cards.make Hearts 10;
  ];
  Tcards.make [
    Cards.make Pikes 7;
    Cards.make Pikes 8;
    Cards.make Pikes 9;
  ];
  Tcards.make [
    Cards.make Tiles 7;
  ];
  Tcards.make [
    Cards.make Hearts 11;
  ];
  Tcards.make [
    Cards.make Hearts 12;
  ];
] in
let table4 = Table.make [
  Tcards.make [
    Cards.make Clovers 7;
    Cards.make Clovers 8;
    Cards.make Clovers 9;
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
let table5 = Table.make [
  Tcards.make [
    Cards.make Clovers 7;
  ];
  Tcards.make [
    Cards.make Clovers 6;
  ];
  Tcards.make [
    Cards.make Clovers 8;
  ];
] in
let table5x = Table.make [
  Tcards.make [
    Cards.make Clovers 7;
    Cards.make Clovers 8;
    Cards.make Clovers 9;
  ];
  Tcards.make [
    Cards.make Clovers 10;
  ];
  Tcards.make [
    Cards.make Clovers 10;
  ];
] in

assert (alg table1 void_printer |> snd = 4);
assert (alg table2 void_printer |> snd = 3);
assert (alg table3 void_printer |> snd = 4);
assert (alg table4 void_printer |> snd = 4);
assert (alg table5 void_printer |> snd = 1);
assert (alg table5x void_printer |> snd = 0);
assert (alg table1x void_printer |> snd = 2);
assert (alg ~maxiter:21 table1x void_printer |> snd = 3);
assert (alg ~maxiter:14 table1x void_printer |> snd = 2);
let table = table1x in
let res = alg ~maxiter:14 table printer in
Printf.printf "Best result: %d\n%a\n" (res |> snd) print_table (res |> fst)
