import chess
import sys
import random
import time
from collections import deque
start = time.time()
if __name__ == '__main__':
    file = open(sys.argv[1], "r")
    fen0 = [line for line in file][0]
    fen0s = fen0.split(" ")
    avmoves=int(fen0.split(" ")[-1])
    startfen=fen0s[-3]+" "+fen0s[-2]+" "+" - - 0 0"
    board=chess.Board(startfen)

    # Check who plays black or white
    color=fen0s[1]
    moveside = False
    if color == "w":
        moveside = True
    enemyside = not moveside

    #print(startfen)

    def KSCoverage(board, kingpos):
        points = 0
        ksquares = [ a for a in board.attacks(kingpos)]
        for a in ksquares:
            if board.is_attacked_by(moveside,a):
                points -= 100 * len(board.attackers(moveside,a))
        return points

    def rate(move,current):
        score=1000 #+ random.randint(1,10)
        avmovs=current[1]
        board=current[0]

        # If move is a capture reward it
        #if board.is_capture(move):
        #    score -= 50
        # If move is irreversible reward it
        #if board.is_irreversible(move):
            #score -= 20

        # Reward Manhattan distance to the King
        ms = move.uci()[:2]
        # Name of file
        kf = chess.square_file(board.king(enemyside))
        mf = int([a for a in range(len(chess.FILE_NAMES)) if chess.FILE_NAMES[a] == ms[0]][0])

        # Number of rank
        kr = chess.square_rank(board.king(enemyside))
        mr = int(ms[1])-1
        md = abs(kf-mf)+abs(kr-mr)
        score+= md * 100

        return score

    def BFS_move(brd, c):

        nextq = deque([(brd, c, 0)])
        while nextq:
            if (float(time.time()) - float(start)) > 20:
                #print("Took to long " + str((float(time.time()) - float(start))))
                #break
                pass

            #print(len(nextq))
            nextq = deque(sorted(list(nextq), key=lambda x: x[2]))
            current = nextq.popleft()
            current[0].turn = moveside
            if current[1] == 0:
                current[0].turn = enemyside
                if current[0].is_checkmate():
                    #print(current[0].fen())
                    sstr=""
                    moveslist=[str(m) for m in current[0].move_stack]
                    for move in moveslist:
                        sstr+=move[:2]+"-"+move[2:]+";"
                    print(sstr[:-1])
                    break
                current[0].turn = moveside
                continue

            for move in current[0].legal_moves:
                r = rate(move, current)
                current[0].turn = moveside
                sc = current[1]
                ccopy = current[0].copy()
                ccopy.push(move)
                ccopy.turn = moveside

                # Eliminate premature attacks on the king
                if sc > 1 and ccopy.was_into_check():
                    continue
                # Eliminate last moves that don't attack the king
                if sc == 1 and not ccopy.was_into_check():
                    continue
                # Reward last turn attacks on the king
                if sc == 1 and ccopy.was_into_check():
                    r -= 1000
                # Keep the king from being captured
                if ccopy.king(enemyside) is None:
                    continue

                # Apply after move heuristics to score

                # Coverage of squares around the King
                r += KSCoverage(ccopy, board.king(enemyside))

                nextq.append((ccopy, current[1]-1, r))

    BFS_move(board, avmoves)


end = time.time()
#(end - start)
