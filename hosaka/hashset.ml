open Hashtbl;;

(* This is a mess but I need sets for memoization.
 * This is my best effort as of now *)
(* let null = ()
 * 
 * let s = Hashtbl.create 1024
 * 
 * let add key =
 *   Hashtbl.add s key null;
 *   false
 * 
 * let has key =
 *   Hashtbl.mem s key *)
