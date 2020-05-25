problem(Answer, Piece, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step, Eatable) :-
    	verifyData(Answer, ToColumn, ToRow);
    	 Piece == knight ->
            canMoveKnight(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Eatable);
        Piece == pawn ->
            canMovePawn(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step);
        Piece == king ->
            canMoveKing(Answer, [Board|Boards],FromColumn, FromRow, ToColumn, ToRow, Eatable);
        Piece == bishop ->
            canMoveBishop(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step, Eatable);
        Piece == rook ->
            canMoveRook(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step, Eatable);
    	Piece == queen ->
    		canMoveQueen(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step, Eatable)

.

verifyData(Answer, ToColumn, ToRow):-
       (   ToColumn < 1 ; ToRow < 1 ; ToColumn > 8 ; ToRow > 8  )->
    	Answer = false,
    	!
	.


canMoveCastling(Answer, [Board|Boards], Step, FromColumn, FromRow, ToColumn, ToRow, Eatable):-

    (   (   FromRow == 1, ToRow == 1 ) ; (  FromRow == 8, ToRow == 8 )) ->
      End is (ToRow - 1) * 8 + ToColumn - 2,
      Counter is (FromRow - 1) * 8 + FromColumn - 1,
      for_loop(Answer, Counter, End, Step, Eatable, [Board|Boards]);
    Answer = false
   .

moveKing(Answer, [Board|Boards], ToColumn, ToRow, Eatable):-
  	append([Board],Boards,Bs),

    Value is (ToRow - 1) * 8 + ToColumn - 1,

    (   nth0(Value, Bs, X),
		X \== liber, Eatable == f) ->
			Answer = false,
    		!;
    Answer = true
	.

canMoveKing(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Eatable):-
    X is abs(ToRow - FromRow),
    Y is abs(ToColumn - FromColumn),
    (   X @=< 1 , Y @=< 1 )->
            moveKing(Answer, [Board|Boards], ToColumn, ToRow, Eatable)
	.

for_loop(_Answer, Counter, End, _Step, _Eatable, [_Board|_Boards]):- Counter > End.
for_loop(Answer, Counter, End, Step, Eatable, [Board|Boards]):-
    append([Board],Boards,Bs),
    Counter =< End,
   	Index is Counter + Step,
    Index =< End,
	nth0(Index, Bs, X),
    		(   X \== liber, Eatable = f) ->
				Answer = false,
    			!;
    Counter1 is Counter + Step,
   	for_loop(Answer, Counter1, End, Step, Eatable, [Board|Boards]),
    Answer = true,!
	.



moveBishop(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step, Eatable):-
    End is (ToRow - 1) * 8 + ToColumn - 1,
	Counter is (FromRow - 1) * 8 + FromColumn - 1,
    for_loop(Answer, Counter, End, Step, Eatable, [Board|Boards])
    .

canMoveBishop(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step, Eatable):-
    X is abs(FromRow - ToRow),
    Y is abs(FromColumn - ToColumn),
    X == Y ->
        moveBishop(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step, Eatable);
    Answer = false
	.



moveRook(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step, Eatable):-
    End is (ToRow - 1) * 8 + ToColumn - 1,
	Counter is (FromRow - 1) * 8 + FromColumn - 1,
	for_loop(Answer, Counter, End, Step, Eatable, [Board|Boards])
    .



canMoveRook(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step, Eatable):-
    (   (FromRow == ToRow) ; (FromColumn == ToColumn)) ->
       moveRook(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step, Eatable);
    Answer = false
	.



canMoveKnight(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Eatable):-
    append([Board],Boards,Bs),
    X is abs(FromColumn - ToColumn),
    Y is abs(FromRow - ToRow),

    Index is (ToRow - 1) * 8 + ToColumn - 1,
     ((      X == 1, Y == 2 ; X == 2, Y == 1 ) ,   nth0(Index, Bs, Z),
    		(   Z \== liber , Eatable = f)) ->
				Answer = false,
    			!;
    Answer = true
	.



for_loop_pawn(_Answer, Counter, End, _Step, [_Board|_Boards]):- Counter > End.
for_loop_pawn(Answer, Counter, End, Step, [Board|Boards]):-
    append([Board],Boards,Bs),
    Counter =< End,
   	Index is Counter + Step,
    Index =< End,
	nth0(Index, Bs, X),
    		(   X \== liber) ->
				Answer = false,
    			!;
    Counter1 is Counter + Step,
   	for_loop_pawn(Answer, Counter1, End, Step, [Board|Boards]),
    Answer = true,!
	.

movePawn(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step):-
    End is (ToRow - 1) * 8 + ToColumn - 1,
    Counter is (FromRow - 1) * 8 + FromColumn - 1,
    for_loop_pawn(Answer, Counter, End, Step, [Board|Boards])
    .

canMovePawn(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step):-
    X is abs(FromRow - ToRow),
    (   (FromColumn == ToColumn,  X == 1); (FromColumn == ToColumn,  X == 2) ; ( FromColumn < ToColumn, X == 1) ;
    (FromColumn > ToColumn, X == 1)	) ->
        movePawn(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step);
    Answer = false
	.

moveQueen(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step, Eatable):-
    End is (ToRow - 1) * 8 + ToColumn - 1,
    Counter is (FromRow - 1) * 8 + FromColumn - 1,
    for_loop(Answer, Counter, End, Step, Eatable, [Board|Boards])
    .

canMoveQueen(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step, Eatable):-
    X is abs(FromRow - ToRow),
    Y is abs(FromColumn - ToColumn),
    (((FromRow == ToRow) ; (FromColumn == ToColumn)) ;  ( X == Y )) ->
   		moveQueen(Answer, [Board|Boards], FromColumn, FromRow, ToColumn, ToRow, Step, Eatable);
    Answer = false
    .

white_move(Answer, Piece):-
    Piece == queen ->
    	white_queen(Answer)
	.

black_move(Answer, Piece):-
     Piece == queen ->
    	black_queen(Answer)
	.

white_queen(Answer):-
    Answer = whitequeen
	.

black_queen(Answer):-
    Answer = blackqueen
	.