"""
Interactive Human vs MENACE Gameplay

Command-line interface for playing tic-tac-toe against MENACE. MENACE plays
X and moves first, the human plays O. MENACE can be trained on the fly or
loaded from a saved JSON file.

Usage:
    Run directly: python play_vs_human.py
    Or via entry point: menace-play
"""

import argparse

from menace.game import Board, winner
from menace.train import train_menace
from menace.menace import MENACE

def human_vs_menace(menace: MENACE, learn: bool = True) -> None:
    """
    Run an interactive game between the human (O) and MENACE (X).

    Args:
        menace (MENACE): The MENACE opponent.
        learn (bool): If True, update MENACE beads from the played game.
    """
    print("Welcome to Tic-Tac-Toe vs MENACE!")
    print("You are O. MENACE is X and moves first.")

    board = Board()
    history: list[tuple[str, int]] = []
    while True:
        move, log = menace.choose_move(board.cells)
        board.make_move(move, 'X')
        history.append(log)
        print("\nMENACE moved:")
        print(board)

        res = winner(board)
        if res is not None:
            print("Result:", "Draw" if res == 'D' else f"{res} wins")
            break

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

    if learn:
        menace.update(history, res)

def main() -> None:
    """Parse CLI arguments, prepare MENACE, then play an interactive game."""
    parser = argparse.ArgumentParser(description="Play tic-tac-toe against MENACE.")
    parser.add_argument(
        "--games",
        type=int,
        default=1000,
        help="Training games to run when no saved MENACE is loaded.",
    )
    parser.add_argument("--load", type=str, default=None, help="Path to a saved MENACE JSON to load.")
    parser.add_argument(
        "--no-learn",
        dest="learn",
        action="store_false",
        help="Do not update MENACE beads during the play session.",
    )
    parser.set_defaults(learn=True)
    args = parser.parse_args()

    menace = MENACE()
    if args.load:
        menace.load(args.load)
        print(f"Loaded MENACE from {args.load}")
    else:
        print(f"Training MENACE ({args.games} games)...")
        menace, _ = train_menace(n_games=args.games, report_every=max(1, args.games // 5))

    human_vs_menace(menace, learn=args.learn)

if __name__ == "__main__":
    main()
