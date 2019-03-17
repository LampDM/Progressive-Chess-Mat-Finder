import chess
import sys
import random
import time
from collections import deque
start = time.time()
if __name__ == '__main__':
    file = open(sys.argv[1], "r")
    fen0 = [line for line in file][0]
    avmoves=int(fen0.split(" ")[-1])
    startfen=fen0.split(" ")[-3]+" "+fen0.split(" ")[-2]+" "+" - - 0 0"
    board=chess.Board(startfen)

    #print(startfen)

    def rate(move,current):
        score=1000 + random.randint(1,10)
        avmovs=current[1]
        board=current[0]

        # If move is a capture reward it
        if board.is_capture(move):
            score-=50
        # If move is irreversible reward it
        if board.is_irreversible(move):
            score -= 20

        # Reward Manhattan distance to the King
            ms = move.uci()[:2]
            # Name of file
            kf = chess.square_file(board.king(True))
            mf = int([a for a in range(len(chess.FILE_NAMES)) if chess.FILE_NAMES[a] == ms[0]][0])

            # Number of rank
            kr = chess.square_rank(board.king(True))
            mr = int(ms[1])-1
            md = abs(kf-mf)+abs(kr-mr)
            score+= md * 100

        return score

    def BFS_move(brd, c):
        nextq = deque([(brd, c, 0)])
        while nextq:
            #print(len(nextq))
            nextq = deque(sorted(list(nextq), key=lambda x: x[2]))
            current = nextq.popleft()
            current[0].turn = False
            if current[1] == 0:
                current[0].turn = True
                if current[0].is_checkmate():
                    #print(current[0].fen())
                    sstr=""
                    moveslist=[str(m) for m in current[0].move_stack]
                    for move in moveslist:
                        sstr+=move[:2]+"-"+move[2:]+";"
                    print(sstr[:-1])
                    break
                current[0].turn = False
                continue

            for move in current[0].legal_moves:
                r = rate(move, current)
                current[0].turn = False
                sc = current[1]
                ccopy = current[0].copy()
                ccopy.push(move)
                ccopy.turn = False

                # Eliminate premature attacks on the king - Chess
                if sc > 1 and ccopy.was_into_check():
                    continue
                # Eliminate last moves that don't attack the king - Chess
                if sc == 1 and not ccopy.was_into_check():
                    continue
                # Reward last turn attacks on the king
                if sc == 1 and ccopy.was_into_check():
                    r -= 1000
                # Keep the king from being captured
                if ccopy.king(True) is None:
                    continue
                nextq.append((ccopy, current[1]-1, r))

    BFS_move(board, avmoves)


end = time.time()
#print(end - start)
