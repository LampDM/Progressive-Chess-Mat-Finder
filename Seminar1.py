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

    def islastTurnCheck(move,current):
        current[0].push(move)
        current[0].turn = True
        rez= current[0].is_check()
        current[0].turn = False
        return rez and current[1] == 1

    def rate(move,current):
        score=1000 + random.randint(1,10)
        avmovs=current[1]
        board=current[0]
        if board.is_capture(move):
            score-=500
        if board.is_irreversible(move):
            score -= 20
        #if islastTurnCheck(move, current):
        #    score -= 1000
        #    print("last turn check")


        return score


    def BFS_move(brd, c):
        nextq = deque([(brd, c, 0)])
        while nextq:
            print(len(nextq))
            nextq = deque(sorted(list(nextq), key=lambda x: x[2]))
            current = nextq.popleft()
            current[0].turn = False
            if current[1] == 0:
                current[0].turn = True
                if current[0].is_checkmate():
                    print(current[0].fen())
                    print([str(m) for m in current[0].move_stack])
                    break
                current[0].turn = False
                continue

            n_legal_moves = [(move, rate(move, current)) for move in current[0].legal_moves]

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
                # Reward last turn attacks on the king
                if sc == 1 and ccopy.was_into_check():
                    r -= 1000
                nextq.append((ccopy, current[1]-1, r))


    def isCheckMate(node):
        node[0].turn = True
        return node[0].is_checkmate() and node[1] == 0

    def newRate(move,current):
        score = random.randint(1, 3)
        return score

    BFS_move(board, avmoves)

    # def Astar(brd,c):
    #     brd.turn=False
    #     openList = deque([(brd.copy(),c,0)])
    #
    #     while openList:
    #
    #         openList = deque(sorted(list(openList), key=lambda x: x[2]))
    #         cnode = openList.popleft()
    #         print(len(openList))
    #         if len(openList)>55000:
    #             print(openList)
    #             break
    #         print(cnode[1])
    #         if cnode[1] == 0:
    #             if isCheckMate(cnode):
    #                 print("check mate found")
    #                 print(cnode)
    #             continue
    #
    #         cnode[0].turn=False
    #         for move in cnode[0].legal_moves:
    #             ccopy=cnode[0].copy()
    #             premovepts_h = newRate(move,ccopy)
    #             ccopy.push(move)
    #             ccopy.turn = False
    #             # Expert heuristics function here
    #             #f = premovepts_h + cnode[2]+1
    #             f = 0
    #
    #             openList.append((ccopy, cnode[1]-1, f))


    #DFS_move(board,avmoves)
    #Astar(board,avmoves)

end = time.time()
print(end - start)
