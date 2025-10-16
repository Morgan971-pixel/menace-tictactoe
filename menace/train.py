"""
MENACE Training and Visualization Module

This module orchestrates the training process for MENACE, handling game 
execution, statistics tracking, and learning progress visualization.

The training loop pits MENACE against opponents (typically random) to 
build experience through reinforcement learning. Each game outcome 
adjusts MENACE's internal "bead" counts, gradually improving play quality.

Key Functions:
    play_game_once: Execute single game between MENACE and opponent
    train_menace: Run full training session with progress tracking  
    plot_stats: Visualize learning curves and performance metrics

Training Process:
1. MENACE starts with uniform preferences for all moves
2. Games are played against opponents, recording MENACE's move history
3. After each game, MENACE's preferences are adjusted based on outcome
4. Over many games, winning strategies are reinforced while losing ones fade
5. Progress is tracked and can be visualized to show learning curves

Typical Usage:
    >>> menace, stats = train_menace(n_games=2000, report_every=200)
    >>> plot_stats(stats)  # Show learning curve
"""

import matplotlib.pyplot as plt
from .game import Board, winner
from .menace import MENACE
from .opponent import random_opponent_move

def play_game_once(menace, opponent=random_opponent_move):
    """
    Execute a single tic-tac-toe game between MENACE and an opponent.
    
    MENACE always plays as 'X' (goes first) while the opponent plays as 'O'.
    The game continues until there's a winner or the board is full (draw).
    
    Args:
        menace (MENACE): The MENACE player instance
        opponent (callable): Function that takes a Board and returns a move index
                           Defaults to random_opponent_move
    
    Returns:
        tuple: (game_result, menace_move_history)
            - game_result (str): 'X' (MENACE won), 'O' (opponent won), 'D' (draw)
            - menace_move_history (list): List of (canonical_state, move) tuples
                                        for MENACE's learning update
    
    Game Flow:
        1. MENACE (X) makes first move, logs it for learning
        2. Opponent (O) responds with their move
        3. Repeat until game ends
        4. Return outcome and MENACE's move history for reinforcement learning
    
    Example:
        >>> menace = MENACE()
        >>> result, history = play_game_once(menace)
        >>> print(f"Game result: {result}")
        >>> menace.update(history, result)  # Learn from this game
    """
    board = Board()
    turn = 'X'
    history = []
    while True:
        if turn == 'X':
            move, log = menace.choose_move(board.cells)
            board.make_move(move, 'X')
            history.append(log)
        else:
            move = opponent(board)
            if move is None:
                break
            board.make_move(move, 'O')
        res = winner(board)
        if res is not None:
            return res, history
        turn = 'O' if turn == 'X' else 'X'

def train_menace(n_games=5000, report_every=500):
    m = MENACE()
    stats = []
    totals = {'X':0,'O':0,'D':0}
    for i in range(1, n_games+1):
        res, hist = play_game_once(m)
        totals[res] += 1
        m.update(hist, res)
        if i % report_every == 0 or i == n_games:
            winrate = totals['X']/i
            drawrate = totals['D']/i
            losrate = totals['O']/i
            stats.append((i, totals['X'], totals['D'], totals['O'], winrate, drawrate, losrate))
            print(f"{i} games: win {winrate:.3f}, draw {drawrate:.3f}, loss {losrate:.3f}")
    return m, stats

def plot_stats(stats):
    games = [s[0] for s in stats]
    wins = [s[4] for s in stats]
    draws = [s[5] for s in stats]
    losses = [s[6] for s in stats]

    plt.figure(figsize=(8,5))
    plt.plot(games, wins, label="Win Rate")
    plt.plot(games, draws, label="Draw Rate")
    plt.plot(games, losses, label="Loss Rate")
    plt.xlabel("Games Played")
    plt.ylabel("Rate")
    plt.title("MENACE Learning Curve")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
