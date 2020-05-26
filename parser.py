### Info
# Prima mutare = White
# King = K Rege
# Queen = Q Regina
# Knight = N Cal
# Bishop = B Nebun
# Rook = R Tura
# Pawn = none Pion
# 0-0 rocada mica ( cu rege)
# 0-0-0 rocada mare ( cu regina )

from pyswip import Prolog

chessTable = []


def generateStep(Piece, player, FromRow, FromColumn, ToRow, ToColumn):
    if Piece == 'Pawn':
        if ToRow < FromRow:
            if ToColumn < FromColumn:
                return -9
            if ToColumn == FromColumn:
                return -8
            if ToColumn > FromColumn:
                return -7
        if ToRow > FromRow:
            if ToColumn < FromColumn:
                return 7
            if ToColumn == FromColumn:
                return 8
            if ToColumn > FromColumn:
                return 9

    if Piece == 'Rook' or Piece == 'Queen':
        if FromRow < ToRow:
            return 8
        if FromRow > ToRow:
            return -8
        if FromColumn < ToColumn:
            return 1
        return -1

    if Piece == 'Knight':
        if FromColumn - ToColumn == 1:
            if FromRow < ToRow:
                return 15
            return -17
        if ToColumn - FromColumn == 1:
            if FromRow < ToRow:
                return 17
            return -15
        if FromRow - ToRow == 1:
            if ToColumn < FromColumn:
                return -10
            return -6
        if ToRow - FromRow == 1:
            if ToColumn < FromColumn:
                return 6
            return 10

    if Piece == 'Bishop' or Piece == 'Queen':
        if ToColumn < FromColumn:
            if ToRow < FromRow:
                return -9
            return 7
        if FromColumn < ToColumn:
            if ToRow < FromRow:
                return -7
            return 9

    if Piece == 'King':
        if ToRow < FromRow:
            if ToColumn < FromColumn:
                return -9
            if ToColumn == FromColumn:
                return -8
            if ToColumn > FromColumn:
                return -7
        if ToRow == FromRow:
            if ToColumn < FromColumn:
                return -1
            if ToColumn > FromColumn:
                return 1
        if ToRow > FromRow:
            if ToColumn < FromColumn:
                return 7
            if ToColumn == FromColumn:
                return 8
            if ToColumn > FromColumn:
                return 9


def algorithm(game):
    game = game.rstrip()
    game = game.split(' ')
    for moveNumber in range(len(game)):
        # White
        if moveNumber % 2 == 0:
            if not moveWhite(game[moveNumber]):
                return False
        # Black
        if moveNumber % 2 == 1:
            if not moveBlack(game[moveNumber]):
                return False
    return True


def generateQuery(move, player):
    commonPieces = ['K', 'Q', 'N', 'B', 'R']
    Piece = "Pawn"
    check = False
    endGame = False
    eat = False
    ToColumn = 0
    ToRow = 0
    FromColumn = 0
    FromRow = 0
    columnMap = {
        'a': 1,
        'b': 2,
        'c': 3,
        'd': 4,
        'e': 5,
        'f': 6,
        'g': 7,
        'h': 8
    }
    pieceMap = {
        'N': "Knight",
        'Q': "Queen",
        'K': "King",
        'R': "Rook",
        'B': "Bishop"
    }

    if move[-1] == '+':
        check = True
        move = move[:-1]

    if move[-1] == '#':
        endGame = True
        move = move[:-1]

    if 'x' in move:
        lists = move.split('x')
        eat = True
        ToColumn = columnMap[lists[1][0]]
        ToRow = 9 - int(lists[1][1])
        if lists[0][0] in pieceMap.keys():
            Piece = pieceMap[lists[0][0]]
        else:
            FromRow = columnMap[lists[0][0]]
            if player == 1:
                FromColumn = ToRow + 1
            else:
                FromColumn = ToRow - 1
        if FromColumn == 0 and FromRow == 0:
            FromColumn, FromRow = getFrom(Piece, player, ToRow, ToColumn)

    else:
        if move[0] in pieceMap.keys():
            Piece = pieceMap[move[0]]
            ToColumn = columnMap[move[1]]
            ToRow = 9 - int(move[2])
        else:
            ToColumn = columnMap[move[0]]
            ToRow = 9 - int(move[1])
            if player == 1:
                for i in range(ToColumn, 8):
                    if chessTable[i - 1][ToRow - 1] == "pawnw":
                        FromRow = ToColumn
                        FromColumn = i
                        break
            if player == 0:
                for i in range(ToColumn, 1, -1):
                    if chessTable[i - 1][ToRow - 1] == "pawnb":
                        FromRow = ToColumn
                        FromColumn = i
                        break
            if FromColumn == ToRow and FromRow == ToColumn:
                FromRow = 0
                FromColumn = 0
        if FromColumn == 0 and FromRow == 0:
            FromColumn, FromRow = getFrom(Piece, player, ToRow, ToColumn)
    return Piece, FromRow, FromColumn, ToRow, ToColumn, eat


# Move White
def moveWhite(move):
    global chessTable

    if move == 'O-O':
        chessTable = makemove(5, 8, 7, 8)
        chessTable = makemove(8, 8, 6, 8)
        return True
    if move == 'O-O-O':
        chessTable = makemove(5, 8, 3, 8)
        chessTable = makemove(1, 8, 4, 8)
        return True

    player = 1
    Piece = "test"
    Piece, FromColumn, FromRow, ToRow, ToColumn, eat = generateQuery(move, player % 2)

    step = generateStep(Piece, player, FromRow, FromColumn, ToRow, ToColumn)
    string = "problem(Answer, " + str.lower(str(Piece)) + ", " + str(vectorTable(chessTable)) + ", " + str(
        FromColumn) + ", " + str(FromRow) + ", " + str(ToColumn) + ", " + str(ToRow) + ", " + str(step) + ", " + str(
        str.lower(str(eat)[0])) + ")"
    prolog = Prolog()
    prolog.consult("test.pl")
    print(move)
    print(Piece, FromRow, FromColumn, ToRow, ToColumn)
    print(string)

    if bool(list(prolog.query(string))[0]['Answer']) or list(prolog.query(string))[0]['Answer'][0] == '_':
        print('true')
        chessTable = makemove(FromColumn, FromRow, ToRow, ToColumn)
    print()
    print()
    return list(prolog.query(string))[0]['Answer']


# Move Black
def moveBlack(move):
    global chessTable
    if move == 'O-O':
        chessTable = makemove(5, 8, 7, 8)
        chessTable = makemove(8, 8, 6, 8)
        return True
    if move == 'O-O-O':
        chessTable = makemove(5, 8, 3, 8)
        chessTable = makemove(1, 8, 4, 8)
        return True
    player = 2
    Piece, FromColumn, FromRow, ToRow, ToColumn, eat = generateQuery(move, player % 2)
    step = generateStep(Piece, player, FromRow, FromColumn, ToRow, ToColumn)
    string = "problem(Answer, " + str.lower(str(Piece)) + ", " + str(vectorTable(chessTable)) + ", " + str(
        FromColumn) + ", " + str(FromRow) + ", " + str(ToColumn) + ", " + str(ToRow) + ", " + str(step) + ", " + str(
        str.lower(str(eat)[0])) + ")"

    prolog = Prolog()
    prolog.consult("test.pl")
    print(move)
    print(Piece, FromRow, FromColumn, ToRow, ToColumn)
    print(string)
    if bool(list(prolog.query(string))[0]['Answer']) or list(prolog.query(string))[0]['Answer'][0] == '_':
        chessTable = makemove(FromColumn, FromRow, ToRow, ToColumn)
        print('true')
    print()
    print()
    return bool(list(prolog.query(string))[0]['Answer'])


# Citirea fisierului games.txt
def readDocument():
    filepath = "games.txt"
    with open(filepath) as fp:
        line = fp.readlines()

    return line


# Creare lista in lista tabel
def resetTable():
    final = []
    pawns_white = ['pawnw' for i in range(8)]
    pawns_black = ['pawnb' for i in range(8)]
    white_list = ['rookw', 'knightw', 'bishopw', 'queenw', 'kingw', 'bishopw', 'knightw', 'rookw']
    black_list = ['rookb', 'knightb', 'bishopb', 'queenb', 'kingb', 'bishopb', 'knightb', 'rookb']
    empty_list = ['liber' for i in range(8)]

    final.append(black_list)
    final.append(pawns_black)

    for i in range(4):
        final.append(empty_list)
    final.append(pawns_white)
    final.append(white_list)

    return final


# Lista in lista -> vector
def vectorTable(matrix):
    li = []
    for line in matrix:
        for elem in line:
            li.append(elem)

    return li


def getFrom(Piece, player, ToRow, ToColumn):
    playerColor = {
        1: 'w',
        0: 'b'
    }
    FromRow = 0
    FromColumn = 0
    copy = vectorTable(chessTable)

    if Piece == 'King':
        position = (ToRow - 1) * 8 + ToColumn - 1
        if -1 < position - 9 < 64:
            if copy[position - 9] == 'king' + playerColor[player]:
                return findValue(position - 9)
        if -1 < position - 7 < 64:
            if copy[position - 7] == 'king' + playerColor[player]:
                return findValue(position - 7)
        if -1 < position + 9 < 64:
            if copy[position + 9] == 'king' + playerColor[player]:
                return findValue(position + 9)
        if -1 < position + 7 < 64:
            if copy[position + 7] == 'king' + playerColor[player]:
                return findValue(position + 7)
        if -1 < position - 8 < 64:
            if copy[position - 8] == 'king' + playerColor[player]:
                return findValue(position - 8)
        if -1 < position + 8 < 64:
            if copy[position + 8] == 'king' + playerColor[player]:
                return findValue(position + 8)
        if -1 < position - 1 < 64:
            if copy[position - 1] == 'king' + playerColor[player]:
                return findValue(position - 1)
        if -1 < position + 1 < 64:
            if copy[position + 1] == 'king' + playerColor[player]:
                return findValue(position + 1)

    if Piece == 'Bishop':
        position = (ToRow - 1) * 8 + ToColumn - 1
        k = -9
        while -1 < position - k < 64:
            if copy[position - k] == 'bishop' + playerColor[player]:
                return findValue(position - k)
            k -= 9
        k = -7
        while -1 < position - k < 64:
            if copy[position - k] == 'bishop' + playerColor[player]:
                return findValue(position - k)
            k -= 7
        k = 7
        while -1 < position - k < 64:
            if copy[position - k] == 'bishop' + playerColor[player]:
                return findValue(position - k)
            k += 7
        k = 9
        while -1 < position - k < 64:
            if copy[position - k] == 'bishop' + playerColor[player]:
                return findValue(position - k)
            k += 9

    if Piece == 'Knight':
        position = (ToRow - 1) * 8 + ToColumn - 1
        if -1 < position - 15 < 64:
            if copy[position - 15] == 'knight' + playerColor[player]:
                return findValue(position - 15)
        if -1 < position - 17 < 64:
            if copy[position - 17] == 'knight' + playerColor[player]:
                return findValue(position - 17)
        if -1 < position + 15 < 64:
            if copy[position + 15] == 'knight' + playerColor[player]:
                return findValue(position + 15)
        if -1 < position + 17 < 64:
            if copy[position + 17] == 'knight' + playerColor[player]:
                return findValue(position + 17)
        if -1 < position - 6 < 64:
            if copy[position - 6] == 'knight' + playerColor[player]:
                return findValue(position - 6)
        if -1 < position + 6 < 64:
            if copy[position + 6] == 'knight' + playerColor[player]:
                return findValue(position + 6)
        if -1 < position + 10 < 64:
            if copy[position + 10] == 'knight' + playerColor[player]:
                return findValue(position + 10)
        if -1 < position - 10 < 64:
            if copy[position - 10] == 'knight' + playerColor[player]:
                return findValue(position - 10)

    if Piece == 'Queen':
        for lin in range(1, 9):
            for col in range(1, 9):
                if copy[(lin - 1) * 8 + col - 1] == 'queen' + playerColor[player]:
                    return lin, col

    if Piece == 'Rook':
        position = (ToRow - 1) * 8 + ToColumn - 1
        k = -8
        while -1 < position + k < 64:
            if copy[position + k] == 'rook' + playerColor[player]:
                return findValue(position + k)
            k = k - 8

        k = ToColumn - 1
        while k >= 0:
            if chessTable[ToRow - 1][k] == 'rook' + playerColor[player]:
                return ToRow, k + 1
            k = k - 1

        k = 8
        while -1 < position + k < 64:
            if copy[position + k] == 'rook' + playerColor[player]:
                return findValue(position + k)
            k = k + 8

        k = ToColumn + 1
        while k <= 7:
            if chessTable[ToRow - 1][k] == 'rook' + playerColor[player]:
                return ToRow, k + 1
            k = k + 1

    if Piece == 'Pawn':
        position = (ToRow - 1) * 8 + ToColumn - 1
        k = -8
        while -1 < position + k < 64:
            if copy[position + k] == 'pawn' + playerColor[player]:
                return findValue(position + k)
            k = k - 8

        k = 8
        while -1 < position + k < 64:
            if copy[position + k] == 'pawn' + playerColor[player]:
                return findValue(position + k)
            k = k + 8

    return FromRow, FromColumn


def makemove(FromRow, FromColumn, ToRow, ToColumn):
    copy = []
    second = []
    value = 'test'
    i = 0
    j = 0
    for linie in chessTable:
        if i == FromColumn - 1:
            li = []
            for elem in linie:
                if j == FromRow - 1:
                    value = elem
                    li.append('liber')
                else:
                    li.append(elem)
                j += 1
            copy.append(li)

        else:
            copy.append(linie)
        i += 1
    i = 0
    j = 0
    for linie in copy:
        if i == ToRow - 1:
            li = []
            for elem in linie:
                if j == ToColumn - 1:
                    li.append(value)
                else:
                    li.append(elem)
                j += 1
            second.append(li)

        else:
            second.append(linie)
        i += 1

    return second


def findValue(value):
    for lin in range(1, 9):
        for col in range(1, 9):
            if value == (lin - 1) * 8 + col - 1:
                return lin, col


if __name__ == '__main__':
    listOfMoves = readDocument()
    for game in listOfMoves:
        chessTable = resetTable()
        if algorithm(game):
            print("Valid game")

