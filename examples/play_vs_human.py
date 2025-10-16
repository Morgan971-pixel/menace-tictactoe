"""
Interactive Human vs MENACE Gameplay

This script provides a command-line interface for playing tic-tac-toe 
against a trained MENACE opponent. MENACE plays as X (goes first) while
the human player plays as O.

The script includes:
- Quick MENACE training session (500 games)
- Interactive game loop with move validation
- Clear board display and result reporting

Usage:
    Run directly: python play_vs_human.py
    Or via entry point: menace-play
"""

from menace.game import Board, winner
from menace.train import train_menace
from menace.menace import MENACE

def human_vs_menace(menace):
    """
    Run an interactive tic-tac-toe game between human and MENACE.
    
    Args:
        menace (MENACE): Trained MENACE opponent
    """
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

def main():
    """
    Entry point for interactive MENACE gameplay.
    
    Trains a MENACE instance quickly then starts human vs MENACE game.
    """
    menace = MENACE()
    print("Training MENACE quickly (500 games)...")
    menace, _ = train_menace(n_games=500, report_every=100)
    human_vs_menace(menace)

if __name__ == "__main__":
    main()
