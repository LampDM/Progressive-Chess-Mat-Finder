import chess
import sys
import random
import time
import heapq


import cProfile, pstats, io


def profile(fnc):
    """A decorator that uses cProfile to profile a function"""

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        retval = fnc(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = 'cumulative'
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        print(s.getvalue())
        return retval

    return inner



start = time.time()

#@profile
def profilefun():
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
            return 100 * sum([len(board.attackers(moveside, a)) for a in
                            board.attacks(kingpos)
                            if board.is_attacked_by(moveside, a)])

        def Man_dist(sq1, sq2):
            return abs(chess.square_file(sq1) - chess.square_file(sq2)) + abs(chess.square_rank(sq1) - chess.square_rank(sq2))

        def Manhattan(board,kingpos):
            points = 0

            #For pieces from knight to Queen - no pawns
            for i in range(2,7):
                for p in board.pieces(i, moveside):
                    points += min([Man_dist(p, ksq) for ksq in board.attacks(kingpos)])

            return points * 100

        def BFS_move(brd, c):

            visited = set()
            nextq = [(0, c, id(brd),brd)]
            heapq.heapify(nextq)
            while nextq:

                if (time.time()-start) > 20:
                    break
                current = heapq.heappop(nextq)
                current[3].turn = moveside

                visited.add(current[3].__str__())

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

                    current[3].turn = moveside
                    sc = current[1]

                    current[3].push(move)
                    current[3].turn = moveside

                    # Check if we already saw this board before
                    if current[3].__str__() in visited:
                        current[3].pop()
                        continue

                    # Eliminate premature attacks on the king
                    if sc > 1 and current[3].was_into_check():
                        current[3].pop()
                        continue
                    # Eliminate last moves that don't attack the king
                    if sc == 1 and not current[3].was_into_check():
                        current[3].pop()
                        continue
                    # Keep the king from being captured
                    if current[3].king(enemyside) is None:
                        current[3].pop()
                        continue

                    # Desperate measures
                    rand = 0
                    if (time.time() - start) > 17:
                        rand = random.randint(1,20)
                    r = 1000 + rand

                    # Reward last turn attacks on the king
                    if sc == 1 and current[3].was_into_check():
                        r -= 1000

                    # Apply various heuristics

                    # Coverage of squares around the King
                    r -= KSCoverage(current[3],board.king(enemyside))
                    # Manhattan distance from all non pawn figures to the King
                    r += Manhattan(current[3],board.king(enemyside))

                    ccopy = current[3].copy()
                    current[3].pop()

                    heapq.heappush(nextq, (r,current[1]-1,id(ccopy),ccopy))


        BFS_move(board, avmoves)

    end = time.time()
    #print(end - start)

profilefun()


