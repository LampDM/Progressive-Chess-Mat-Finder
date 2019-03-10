import chess
import sys
import random
import time
from collections import deque
import operator
start = time.time()

if __name__ == '__main__':
    file = open(sys.argv[1], "r")
    fen0 = [line for line in file][0]
    avmoves=int(fen0.split(" ")[-1])
    startfen=fen0.split(" ")[-3]+" "+fen0.split(" ")[-2]+" "+" - - 0 0"
    board=chess.Board(startfen)

    print(startfen)


    def DFS_move(brd, c):
        brd.turn = False
        if c:
            for move in brd.legal_moves:
                brd.turn = True
                if brd.is_check():
                    brd.turn = False
                    break
                brd.turn = False

                brd.push(move)
                DFS_move(brd,c-1)
                brd.pop()
        else:
            # Set white turn
            brd.turn = True
            if brd.is_checkmate():
                print(brd.fen())
                print([str(m) for m in brd.move_stack])


    def rate(move,current):
        score=1000+random.randint(1,10)
        avmovs=current[1]
        board=current[0]
        if board.is_capture(move):
            score-=500
        if board.is_irreversible(move):
            score -= 20

        return score


    def BFS_move(brd, c):
        nextq = deque([(brd, c)])
        while nextq:
            current = nextq.popleft()
            current[0].turn = False
            if current[1] == 0:
                current[0].turn = True
                if current[0].is_checkmate():
                    print(current[0].fen())
                    print([str(m) for m in current[0].move_stack])
                current[0].turn = False
                continue

            n_legal_moves = [(move, rate(move, current)) for move in current[0].legal_moves]
            n_legal_moves.sort(key = operator.itemgetter(1))

            for move,r in n_legal_moves:
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

                nextq.append((ccopy, current[1]-1))



    BFS_move(board, avmoves)
    #DFS_move(board,avmoves)
end = time.time()
print(end - start)
