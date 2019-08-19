(* Mosse: Aggiunta, spostamento *)
(* 
 Triplette giocabili in mano, doppie usabili, singole usabili
 una volta vista la mano, rimuovi le carte inusabili nel turno;
 considerata una carta giocabile in mano, considera le carte "prossime", bruteforce;
*)
open Printer;;
open Yojson.Basic.Util;;

let read_json () =
  let json = Yojson.Basic.from_channel stdin in let open Yojson.Basic.Util in
  let make_card l =
    let hd = List.hd l |> to_string in
    let tl = List.tl l |> List.hd |> to_int in
    Cards.make (Cards.string_to_card_type hd) tl in

  let hand = json |> member "hand" |> to_list |>
             List.map (fun c -> [ c |> to_list |> make_card ] |> Tcards.make) in (* List of tcards `singles *)
  let table = json |> member "table" |> to_list |>
              List.map (fun l -> to_list l |> List.map (fun cl -> cl |> to_list |> make_card) |> Tcards.make)
              |> Table.make
  in
  (hand, table)

let to_json (table:Table.table) =
  let cards_to_json (cards:Cards.card list) =
    `List (List.map (fun (c:Cards.card) -> `List [`String (c.seed |> Cards.card_type_to_string); `Int c.value]) cards) in
  let tcards_to_json (tc:Tcards.tcards) =
    cards_to_json tc.cards in
  `List (List.map (fun tcl -> tcards_to_json tcl) table.cards);;

let open Yojson.Basic.Util in
let hand, table = read_json () in
let tn = Table.make (table.cards@hand) in
let res, _ = Table.alg ~maxiter:14 tn void_printer in
(* Printf.printf "%a\n" print_table res;; *)
to_json res |> Yojson.Basic.to_channel stdout
