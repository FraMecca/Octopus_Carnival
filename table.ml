open List;;

open Cards;;
open Tcards;;

let sum a b = a + b (* TODO: investigate why list.fold doesn't accept + *)

type table = { cards: tcards list}

let make tcards =
  { cards=tcards }

let empty =
  { cards = [] }

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

let flatten table : card list=
  List.map (fun (ts:tcards) -> ts.cards) table.cards |>
  List.concat ;;

let contains tc table =
  List.mem tc table.cards

let neighbors tcs table : card list=
  let all = flatten table in
  match tcs.strategy with
  | Tris -> List.filter (fun x -> tcs.cards@[x] |> Cards.is_tris) all
  | Straight -> List.filter (fun x -> tcs.cards@[x] |> Cards.is_straight) all
  | Single -> all |>
              List.filter (fun x -> let cs = tcs.cards@[x] in
                            Cards.is_straight cs || Cards.is_tris cs)
      

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
        match (Tcards.remove to_move hd) with
        | None -> _play tl in_play to_move accum
        | Some x -> _play tl in_play to_move (x::accum)
      else
        _play tl in_play to_move (hd::accum)
  in
  assert (table |> contains in_play) ;
  _play table.cards in_play to_move [] |> make
  ;;

let update best max_score original newt score =
  if score > max_score && (constraints original newt) then
    score, newt
  else
    max_score, best

let is_best_outcome table =
  (invalids table |> List.length) == 0

(* let rec alg table original_table n (scores:int list) best max_score (dbg: table -> unit) =
 *   dbg table ;
 *   let ascore = score table in 
 *   (\* if Hashset.has (hash table) then () *\)
 *   (\* else ( *\)
 *     (\* Hashset.add (hash table) ; *\)
 *     let mmax, bbest = update best max_score original_table table ascore in
 *     if is_best_outcome table || n > 14 || doesnt_improve (scores@[ascore]) then
 *       ()
 *     else
 *       table.cards |>
 *       List.map (fun tcs -> neighbors tcs table |> List.map (fun v -> (tcs,v))) |> (\* lista di carta:vicini *\)
 *       List.concat |> (\* flatten *\)
 *       List.map (fun (card, neigh) -> play table card neigh) |> (\* list of new_tables *\)
 *       List.iter (fun new_table -> alg new_table original_table (n+1) (scores@[ascore]) bbest mmax dbg)
 *   (\* ) *\) *)

let alg table n (scores:int list) : (table * int * int list) list =
  table.cards |>
  List.map (fun tcs -> neighbors tcs table |> List.map (fun v -> (tcs,v))) |> (* lista di carta:vicini *)
  List.concat |> (* flatten *)
  List.map (fun (card, neigh) -> (play table card neigh), (n+1), (scores@[score table]) )

let condizioni table n scores set =
  if List.mem (hash table) set || doesnt_improve scores ||
     is_best_outcome table || n > 14 then
    true
  else false
  
let rec prova original_table set best max_score (dbg: table -> unit) (accum: (table*int*int list) list)
    (sols: (table*int*int list) list) =
  match accum with
  | [] -> sols
  | (table, n, scores)::tl -> dbg table ;
    if condizioni table n scores set then
      prova original_table ((hash table)::set) best max_score dbg tl ([table, n, scores]@sols)
    else
      prova original_table ((hash table)::set) best max_score dbg ((alg table n scores)@tl) sols
