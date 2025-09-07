from menace.game import Board, winner
from menace.train import play_game_once
from menace.menace import MENACE

def human_vs_menace(menace):
    print("Welcome to Tic-Tac-Toe vs MENACE!")
    print("You are O. MENACE is X and moves first.")

    board = Board()
    while True:
        # MENACE move
        move, log = menace.choose_move(board.cells)
        board.make_move(move, 'X')
        print("\nMENACE moved:")
        print(board)

        res = winner(board)
        if res is not None:
            print("Result:", "Draw" if res == 'D' else f"{res} wins")
            break

        # Human move
        legal = board.available_moves()
        print("Your legal moves:", legal)
        while True:
            try:
                mv = int(input("Enter your move index (0-8): "))
                if mv in legal:
                    board.make_move(mv, 'O')
                    break
                print("Illegal move. Try again.")
            except ValueError:
                print("Please type an integer 0-8.")

        print(board)
        res = winner(board)
        if res is not None:
            print("Result:", "Draw" if res == 'D' else f"{res} wins")
            break

if __name__ == "__main__":
    menace = MENACE()
    print("Training MENACE quickly (500 games)...")
    menace, _ = play_game_once(menace), []
    human_vs_menace(menace)
