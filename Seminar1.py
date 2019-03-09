import chess
import sys
import random
import time
start = time.time()

if __name__ == '__main__':
    file = open(sys.argv[1], "r")
    fen0 = [line for line in file][0]
    move=fen0.split(" ")[-2]
    avmoves=int(fen0.split(" ")[-1])
    positions=fen0.split(" ")[-3]
    startfen=positions+" "+move+" "+" - - 0 0"
    board=chess.Board(startfen)

    print(startfen)

    def first_move(brd, c):
        brd.turn = False
        if c:
            for move in brd.legal_moves:
                brd.turn = True
                if brd.is_check():
                    brd.turn = False
                    break
                brd.turn = False

                brd.push(move)
                first_move(brd,c-1)
                brd.pop()
        else:
            # Set white turn
            brd.turn = True
            if brd.is_checkmate():
                print(brd.fen())
                print([str(m) for m in brd.move_stack])

    first_move(board,4)


end = time.time()
print(end - start)
