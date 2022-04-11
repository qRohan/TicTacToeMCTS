from MCTS import MCTS
from TicTacToe import GameBoard


if __name__ == "__main__":
    board = GameBoard()
    # board = GameBoard([[0,0,0],[0,1,0],[2,0,0]])
    # board = GameBoard([[1,0,0],[1,1,2],[2,2,0]])
    print(board)
    # mcts = MCTS(board, 2, 4000)
    # mcts.run_mcts()

    while True:

        move = tuple(map(int, input().split(",")))
        move = (move[0], move[1])
        board = board.play(move)
        print(board)
        if board.winner is not None:
            if board.winner:
                print("Player Wins")
            else:
                print("DRAW")
            break

        mcts = MCTS(board, 1, 2000)
        move_comp = mcts.run_mcts()
        board = board.play(move_comp)
        print(board)
        if board.winner is not None:
            if board.winner:
                print("Computer Wins")
            else:
                print("DRAW")
            break
