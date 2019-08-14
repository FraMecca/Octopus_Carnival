open List;;
open Hashtbl;;

open Cards;;

type card_tag =
  | Invalid
  | Valid

let card_tag_to_string t =
  match t with
  | Invalid -> "Invalid"
  | Valid -> "Valid"

type game_strategy =
  | Tris
  | Straight
  | Single

let game_strategy_to_string t =
  match t with
  | Tris -> "Tris"
  | Straight -> "Straight"
  | Single -> "Single"

type tcards = { cards: card list ; tag: card_tag ; strategy: game_strategy }

let make cards =
  let strategy = if List.length cards = 1 then Single else
    if Cards.is_tris cards then Tris else Straight in
  { cards=cards |> List.sort value_cmp ; tag=if Cards.is_valid cards then Valid else Invalid; strategy=strategy }

let contains needle haystack = List.mem needle haystack.cards

let eq a b =
  if List.length a.cards <> List.length b.cards || a.tag != b.tag || a.strategy != b.strategy then
    false
  else
    a.cards = b.cards

let length ts = List.length ts.cards

let cmp (a:tcards) (b:tcards) =
  let tup = (a.strategy, length a, b.strategy, length b, a.tag, b.tag) in
  match tup with
  | Straight, al, Straight, bl, _, _ -> if al < bl then 1 else -1
  | Tris, 4, _, _, _, _ -> -1
  | _,  _, Tris, 4, _, _ -> 1
  | Tris, 3, _, _, _, _ -> -1
  | _,  _, Tris, 3, _, _ -> 1
  | Straight, 3, _, _, _, _ -> -1
  | _,  _, Straight, 3, _, _ -> 1
  | Straight, al, _, _, _, _ when al > 3 -> -1
  | _, _, Straight, bl, _, _ when bl > 3 -> 1
  | Single, _, Single, _, _, _ -> -1 (* avoid ordering by card value here *)
  | (Straight|Tris), _, Single, _, _, _ -> 1
  | Single, _, (Straight|Tris), _, _, _ -> -1
  | _, _, _, _, Invalid, Valid -> 1
  | _, _, _, _, Valid, Invalid -> -1
  | _ -> -1 (* doesn't matter if -1 or 1, just don't discriminate otherwise can't try all possible combinations *);;


let hash ts =
  ts.cards |>
  List.sort (fun a b -> if a.seed == b.seed then Cards.value_cmp a b else Cards.seed_cmp a b) |>
  Hashtbl.hash;;

let remove card tcards =
  assert (List.mem card tcards.cards);
  match (List.filter (fun x -> x <> card) tcards.cards) with
  | [] -> None 
  | (hd::tl) as lst -> Some (make lst) ;;

let r = remove (Cards.make Hearts 7) (make [Cards.make Hearts 7; Cards.make Clovers 7; Cards.make Pikes 7;]) in
match r with
| None -> assert false
| Some x -> if x <> (make [Cards.make Clovers 7; Cards.make Pikes 7]) then assert false
