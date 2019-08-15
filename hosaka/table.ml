(* open List;;
 * open Hashtbl;; *)

open Cards;;
open Tcards;;

let sum a b = a + b (* TODO: investigate why list.fold doesn't accept + *)

type table = { cards: tcards list}

let make tcards =
  { cards=(List.sort Tcards.cmp tcards) }

let empty =
  { cards = [] }

let valids table =
  List.filter (fun ts -> ts.tag = Valid) table.cards

let invalids table =
  List.filter (fun ts -> ts.tag = Invalid) table.cards

let score table =
  List.length (valids table) - List.length (invalids table)

let hash table =
  List.map (fun ts ->Tcards.hash ts) table.cards |>
  List.fold_left sum 0

let size table =
  List.map (fun tl -> Tcards.length tl) table.cards |>
  List.fold_left sum 0

let flatten table : card list=
  List.map (fun (ts:tcards) -> ts.cards) table.cards |>
  List.concat |> List.sort Cards.value_cmp

let contains tc table =
  List.mem tc table.cards

let neighbors (tcs:tcards) table : card list=
  let all = flatten table in
  let res = 
  (match tcs.strategy with
  | Tris -> List.filter (fun x -> tcs.cards@[x] |> Cards.is_tris) all
  | Straight -> List.filter (fun x -> tcs.cards@[x] |> Cards.is_straight) all
  | Single -> all |>
              List.filter (fun x -> let cs = tcs.cards@[x] in
                            Cards.is_straight cs || Cards.is_tris cs)
  )|> List.sort_uniq (fun a b -> if a = b then 0 else 1)
  in (
  (* List.iter (fun c -> Printf.printf "%d:%s - " c.value (card_type_to_string c.seed)) tcs.cards; *)
  (* Printf.printf "\n"; *)
  (* List.iter (fun c -> Printf.printf "%d:%s - " c.value (card_type_to_string c.seed)) res ; Printf.printf "\n" ; *)
   res )

let constraints start eend =
  let hand = List.filter (fun ts -> ts.strategy = Single) start.cards in
  let res = List.filter (fun (e:tcards) -> e.strategy = Single && not (List.mem e hand)) eend.cards in
  (List.length res) = 0

let doesnt_improve n scores =
  if List.length scores < n then
    false
  else
    let max = List.fold_left max (-1000) scores in
    let min = List.fold_left min 1000 scores in
    abs (max - min) < (n/7)

let play table in_play to_move : table =
  let rec _play table_cards in_play to_move accum played_already moved_already =
    match table_cards with
    | [] -> accum (* return a new table *)
    | hd::tl -> (* put new combination on the table *)
      if not played_already && eq hd in_play then
        _play tl in_play to_move ((Tcards.make (to_move::in_play.cards))::accum) true moved_already
      else if not moved_already && hd |> Tcards.contains to_move then
        match (Tcards.remove to_move hd) with
        | None -> _play tl in_play to_move accum played_already true
        | Some x -> _play tl in_play to_move (x::accum) played_already true
      else
        _play tl in_play to_move (hd::accum) played_already moved_already
        
  in
  assert (table |> contains in_play) ;
  _play table.cards in_play to_move [] false false |> make

let is_best_outcome table =
  (invalids table |> List.length) = 0

let alg ?maxiter original (dbg: int -> int -> table -> unit) =
  let set = Hashtbl.create 1024 in
  let should_exit = ref false in
  let best = ref original in
  let max_score = ref (score !best) in

  let rec _alg table n scores maxiter =
    let cur_score = score table in
    let uscores = scores[@cur_score] in
    let cur_hash = hash table in
    if !should_exit || Hashtbl.mem set cur_hash then
      ()
    else (
      should_exit := is_best_outcome table;
      Hashtbl.add set cur_hash ();
      dbg n cur_score table ;
      if constraints original table && cur_score > !max_score then
        (max_score := cur_score ; best := table ) ;

      if !should_exit || n > maxiter || doesnt_improve (maxiter/2) uscores then
        ()
      else (
        table.cards |>
        List.map (fun tcs -> neighbors tcs table |> List.map (fun v -> (tcs,v))) |> (* list of cards:neighbors *)
        List.concat |> (* flatten *)
        List.map (fun (card, neigh) -> (play table card neigh)) |>
        List.iter (fun new_table -> _alg new_table (n+1) uscores maxiter)
      )
    )
  in
  let maxiter = match maxiter with None -> 14 | Some x -> x in
  _alg original 0 [] maxiter ; !best, !max_score
