import chess
import sys

board = chess.Board()

#TODO play with library
print(board.push_san("a3"))

print([i for i in board.legal_moves])

if __name__ == '__main__':
    file = open(sys.argv[1], "r")
    fen0 = [line for line in file][0]
    print(fen0)
    move=fen0.split(" ")[-2]
    avmoves=fen0.split(" ")[-1]
    positions=fen0.split(" ")[-3]
    startfen=positions+" "+move+" "+" - - 0 0"
    board=chess.Board(startfen)
    print(board)


    board.push(chess.Move.from_uci("a2a4"))
    board.push(chess.Move.from_uci("a4a5"))
    board.pop()
    for move in board.legal_moves:
        board.push(chess.Move.from_uci(str(move)))
    print(board.fen())
    print(board)


