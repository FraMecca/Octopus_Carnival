open List;;

open Cards;;
open Tcards;;

let sum a b = a + b (* TODO: investigate why list.fold doesn't accept + *)

type table = { cards: tcards list}

let make tcards =
  { cards=tcards }

let valids table =
  List.filter (fun ts -> ts.tag == Valid) table.cards;;

let invalids table =
  List.filter (fun ts -> ts.tag == Invalid) table.cards;;

let score table =
  List.length (valids table) - List.length (invalids table)

let hash table =
  List.map (fun ts ->Tcards.hash ts) table.cards |>
  List.fold_left sum 0;;

let size table =
  List.map (fun tl -> Tcards.length tl) table.cards |>
  List.fold_left sum 0 ;;

let flatten table =
  List.map (fun (ts:tcards) -> ts.cards) table.cards |>
  List.concat ;;

let neighbors tcs table =
  match tcs.strategy with
  | Tris -> List.filter (fun (x:tcards) -> tcs.cards@x.cards |> Cards.is_tris) table.cards
  | Straight -> List.filter (fun (x:tcards) -> tcs.cards@x.cards |> Cards.is_straight) table.cards
  | Single -> List.filter (fun (x:tcards) ->
      tcs.cards@x.cards |> Cards.is_straight || tcs.cards@x.cards |> Cards.is_tris)
      table.cards

let constraints start eend =
  let hand = List.filter (fun ts -> ts.strategy == Single) start.cards in
  let res = List.filter (fun (e:tcards) -> e.strategy == Single && not (List.mem e hand)) eend.cards in
  (List.length res) == 0;; (* investigate why not = nstead of == (TODO) *)

let doesnt_improve scores =
  if List.length scores < 7 then
    false
  else
    let max = List.fold_left max (-1000) scores in
    let min = List.fold_left min 1000 scores in
    abs (max - min) < 2

let play table in_play to_move =
  let rec _play table_cards in_play to_move accum =
    match table_cards with
    (* put new combination on the table *)
    | hd::tl when hd = in_play -> _play tl in_play to_move ((Tcards.make (to_move::in_play.cards))::accum)
    | [] -> accum (* generate a new table *)
    | hd::tl -> if hd |> Tcards.contains to_move then
        let filtered = List.filter (fun x -> x != to_move) hd.cards in
        _play tl in_play to_move ((Tcards.make filtered)::accum)
      else
        _play tl in_play to_move (hd::accum)
  in
  _play table.cards in_play to_move [] |> make
  ;;

