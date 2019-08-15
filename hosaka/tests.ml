open Cards;;
open Table;;
open Tcards;;
open Printer;;

let card_tests () =
    let cards = [{seed=Clovers; value=1}; {seed=Hearts; value=1}; {seed=Pikes; value=1}] in
    assert (is_valid cards);

    let cards = [{seed=Tiles; value=1}; {seed=Clovers; value=1}; {seed=Hearts; value=1}; {seed=Pikes; value=1}] in
    assert (is_valid cards);

    let cards = [{seed=Tiles; value=2}; {seed=Clovers; value=1}; {seed=Hearts; value=1}; {seed=Pikes; value=1}] in
    assert (not (is_valid cards));

    let cards = [{seed=Hearts; value=2}; {seed=Hearts; value=2}; {seed=Hearts; value=4}]
    in assert (not (no_double_value cards));

    let cards = [{seed=Hearts; value=2}; {seed=Hearts; value=2}; {seed=Hearts; value=4}]
    in assert (not (no_double_seed cards));

    let cards = [{seed=Pikes; value=2}; {seed=Clovers; value=2}; {seed=Tiles; value=4}; {seed=Hearts; value=4}]
    in assert (no_double_seed cards);

    let cards = [{seed=Hearts; value=4}; {seed=Hearts; value=3}; {seed=Hearts; value=2}; {seed=Hearts; value=1}]
    in assert (is_valid cards);

    let cards = [{seed=Hearts; value=13}; {seed=Hearts; value=12}; {seed=Hearts; value=2}; {seed=Hearts; value=1}]
    in assert (is_valid cards);

    let cards = [{seed=Pikes; value=13}; {seed=Hearts; value=12}; {seed=Hearts; value=2}; {seed=Hearts; value=1}]
    in assert (not (is_valid cards));

    let cards = [{seed=Pikes; value=13}; {seed=Pikes; value=12}; {seed=Pikes; value=1}]
    in assert (is_valid cards);
    let cards = [{seed=Hearts; value=12}; {seed=Pikes; value=12}; {seed=Pikes; value=1}]
    in assert (not (is_valid cards));

    let cards = [{seed=Hearts; value=13}; {seed=Hearts; value=3}; {seed=Hearts; value=2}; {seed=Hearts; value=1}]
    in assert (is_valid cards);


let () =
    assert  ([
        Cards.make Hearts 6;
        Cards.make Hearts 7;
        Cards.make Hearts 8;
        Cards.make Hearts 9;
        Cards.make Hearts 10;]
        |> Cards.is_straight) ;

    assert  ([
        Cards.make Hearts 1;
        Cards.make Hearts 12;
        Cards.make Hearts 2;
        Cards.make Hearts 13;]
        |> Cards.is_straight) ;

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
    assert (neighs = [Cards.make Hearts 6]) ;

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
    assert (neighs = [Cards.make Hearts 12]) ;

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
    (* let table = table1x in
     * let res = alg ~maxiter:14 table printer in
     * Printf.printf "Best result: %d\n%a\n" (res |> snd) print_table (res |> fst) ; *)
    Printf.printf "Tests done.\n" in
 () ;;


card_tests ();;
