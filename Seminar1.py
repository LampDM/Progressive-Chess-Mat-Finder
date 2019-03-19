import chess
import sys
import random
import time
import heapq

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
        ksquares = [a for a in board.attacks(kingpos)]
        for a in ksquares:
            if board.is_attacked_by(moveside,a):
                points -= 100 * len(board.attackers(moveside,a))
        return points

    def rate(move,current):
        score=1000 #+ random.randint(1,10)
        avmovs=current[1]
        board=current[3]

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

        #nextq = deque([(brd, c, 0)])
        nextq = [(0, c, id(brd),brd)]
        heapq.heapify(nextq)
        while nextq:
            #if (float(time.time()) - float(start)) > 20:
                #print("Took to long 20+")
                #break
                #pass

            #nextq = deque(sorted(list(nextq), key=lambda x: x[2]))

            current = heapq.heappop(nextq)
            current[3].turn = moveside

            # Check if the given position is a checkmate
            if current[1] == 0:
                current[3].turn = enemyside
                if current[3].is_checkmate():
                    #print(current[3].fen())
                    sstr=""
                    moveslist=[str(m) for m in current[3].move_stack]
                    for move in moveslist:
                        sstr+=move[:2]+"-"+move[2:]+";"
                    print(sstr[:-1])
                    break
                current[3].turn = moveside
                continue

            # The main loop
            for move in current[3].legal_moves:
                r = rate(move, current)
                current[3].turn = moveside
                sc = current[1]

                current[3].push(move)
                current[3].turn = moveside

                # Eliminate premature attacks on the king
                if sc > 1 and current[3].was_into_check():
                    current[3].pop()
                    continue
                # Eliminate last moves that don't attack the king
                if sc == 1 and not current[3].was_into_check():
                    current[3].pop()
                    continue
                # Reward last turn attacks on the king
                if sc == 1 and current[3].was_into_check():
                    r -= 1000
                # Keep the king from being captured
                if current[3].king(enemyside) is None:
                    current[3].pop()
                    continue

                # Apply after move heuristics to score

                # Coverage of squares around the King

                r += KSCoverage(current[3], board.king(enemyside))

                ccopy = current[3].copy()
                current[3].pop()
                heapq.heappush(nextq, (r,current[1]-1,id(ccopy),ccopy))
                #nextq.append((ccopy, current[1]-1, r))


    BFS_move(board, avmoves)


end = time.time()
#print(end - start)
