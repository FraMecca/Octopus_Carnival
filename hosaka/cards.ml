open List;;

(* Random.self_init ();;  *)

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

let make seed value =
  { seed=seed; value=value }

let value_cmp a b = if a.value < b.value then -1 else if a.value = b.value then 0 else 1 (* TFW TODO *)
let seed_cmp = fun a b -> if card_type_to_string a.seed > card_type_to_string b.seed then 1 else
    if card_type_to_string a.seed = card_type_to_string b.seed then 0 else -1

let make_set tp =
  let rec range start _end accum = if start < _end then range (start+1) _end accum@[start]  else accum in
  List.map (fun x -> { seed=tp; value=x }) (range 1 14 []);; (* make a set of cards of one seed *)
let init = 
  List.concat [make_set Hearts ; make_set Tiles ; make_set Clovers ; make_set Pikes ;
               make_set Hearts ; make_set Tiles ; make_set Clovers ; make_set Pikes] |>
  List.map (fun e -> Random.bits (), e) |>
  List.sort (fun a b -> if fst a > fst b then 1 else -1)  |>
  List.map snd 

let draw deck = match deck with
    | [] as l -> {seed=Nothing ; value=0}, l
    | hd::tl -> hd, tl

let no_double_seed cards =
  List.sort_uniq seed_cmp cards |> List.length = List.length cards

let is_only_one_seed cards =
  List.sort_uniq seed_cmp cards |> List.length = 1

let no_double_value cards =
  List.sort_uniq value_cmp cards |> List.length = List.length cards

let is_tris cards =
  match (List.sort_uniq value_cmp cards)  with
  | [_] -> no_double_seed cards (* only one value, check for right seeds *)
  | _::_ -> false
  | [] -> assert false

let rec split l fst =
  match l with
  | hd::hd'::tl when hd=hd'-1 -> split (hd'::tl) (fst@[hd])
  | hd::tl -> fst@[hd], tl
  | [] -> assert false


let is_straight _cards =
  let rec _is_straight cards =
    match cards with
    | hd::hd'::tl when hd=hd'-1 -> _is_straight (hd'::tl)
    | [] -> assert false
    | [_] -> true (* list was consumed *)
    | _::_ -> false in

  if (not (no_double_value _cards && is_only_one_seed _cards)) then
    false
  else
    let ocards = List.sort value_cmp _cards  in
    let last = List.rev ocards |> hd in
    let cards  = List.map (fun c -> c.value) ocards (* use only values *) in
    if last.value = 13 && (hd cards) = 1 then (* circolare *)
      let fst, snd = split cards [] in (_is_straight fst) && (_is_straight snd)
    else
      (* let res = _is_straight cards in
       * List.iter (fun c -> Printf.printf "%d:%s - " c.value (card_type_to_string c.seed)) _cards ; Printf.printf "%b\n" res;
       * res *) (* TODO : remove *)
      _is_straight cards

let is_valid _cards =
  let cards = List.sort value_cmp _cards in
  if List.length cards < 3 then
    false
  else
    match cards with
    | a::b::_ when value_cmp a b = 0  -> is_tris cards
    | _ -> is_straight cards;;
