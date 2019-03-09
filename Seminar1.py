import chess
import sys
import random





if __name__ == '__main__':
    file = open(sys.argv[1], "r")
    fen0 = [line for line in file][0]
    move=fen0.split(" ")[-2]
    avmoves=int(fen0.split(" ")[-1])
    positions=fen0.split(" ")[-3]
    startfen=positions+" "+move+" "+" - - 0 0"
    board=chess.Board(startfen)

    print(startfen)
    # for move in board.legal_moves:
    #     print(move)
    #     board.push(move)
    #     print(board.fen())
    #     board = chess.Board(board.fen().replace("w", "b"))

    #     for move2 in board.legal_moves:
    #         print(move2)
    #         board.push(move2)
    #         print(board.fen())
    #         board.pop()
    #         board = chess.Board(board.fen().replace("w", "b"))
    #
    #     board.pop()
    #     board = chess.Board(board.fen().replace("w", "b"))


    def first_move(brd,c):
        # Set black turn
        brd.turn = False
        if c:
            for move in brd.legal_moves:
                if brd.is_into_check(move) and c!=1:
                    print("Invalid")
                    pass
                brd.push(move)

                first_move(brd,c-1)


                brd.pop()


        else:
            # Set white turn
            brd.turn = True
            if brd.is_checkmate():
                print(brd.fen())



    first_move(board,avmoves)



