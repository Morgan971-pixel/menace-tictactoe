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

from typing import Callable

import matplotlib.pyplot as plt
from tqdm import tqdm

from .game import Board, winner
from .menace import MENACE
from .opponent import random_opponent_move

def play_game_once(
    menace: MENACE,
    opponent: Callable[[Board], int | None] = random_opponent_move,
) -> tuple[str, list[tuple[str, int]]]:
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

def train_menace(
    n_games: int = 5000,
    report_every: int = 500,
    opponent: Callable[[Board], int | None] = random_opponent_move,
) -> tuple[MENACE, list[tuple]]:
    """
    Train a MENACE instance against an opponent.

    Per-game results ('X'/'D'/'O') are stored on the returned instance as
    `training_results` so plot_stats can compute rolling averages.

    Returns:
        tuple: (trained MENACE, sampled stats list)
    """
    m = MENACE()
    stats: list[tuple] = []
    results: list[str] = []
    totals = {'X': 0, 'O': 0, 'D': 0}
    bar = tqdm(range(1, n_games + 1), total=n_games, desc="Training")
    for i in bar:
        res, hist = play_game_once(m, opponent)
        totals[res] += 1
        results.append(res)
        m.update(hist, res)
        bar.set_postfix(
            win=f"{totals['X']/i:.3f}",
            draw=f"{totals['D']/i:.3f}",
            loss=f"{totals['O']/i:.3f}",
        )
        if i % report_every == 0 or i == n_games:
            winrate = totals['X'] / i
            drawrate = totals['D'] / i
            losrate = totals['O'] / i
            stats.append((i, totals['X'], totals['D'], totals['O'], winrate, drawrate, losrate))
            print(f"{i} games: win {winrate:.3f}, draw {drawrate:.3f}, loss {losrate:.3f}")
    m.training_results = results
    return m, stats

def play_game_selfplay(menace_x: MENACE, menace_o: MENACE) -> tuple[str, list, list]:
    """
    Play one game with two MENACE instances.

    menace_x plays X and moves first, menace_o plays O.

    Returns:
        tuple: (result, history_x, history_o) where result is 'X', 'O' or 'D'.
    """
    board = Board()
    turn = 'X'
    history_x: list[tuple[str, int]] = []
    history_o: list[tuple[str, int]] = []
    while True:
        if turn == 'X':
            move, log = menace_x.choose_move(board.cells)
            board.make_move(move, 'X')
            history_x.append(log)
        else:
            move, log = menace_o.choose_move(board.cells)
            board.make_move(move, 'O')
            history_o.append(log)
        res = winner(board)
        if res is not None:
            return res, history_x, history_o
        turn = 'O' if turn == 'X' else 'X'

def train_menace_selfplay(
    n_games: int = 5000,
    report_every: int = 500,
) -> tuple[MENACE, MENACE, list[tuple]]:
    """
    Train two MENACE instances against each other through self-play.

    menace_x always plays X and menace_o always plays O. After each game both
    are updated; O's reward uses the result from O's perspective (X and O
    outcomes inverted, draw unchanged).

    Returns:
        tuple: (menace_x, menace_o, sampled stats list)
    """
    menace_x = MENACE()
    menace_o = MENACE()
    stats: list[tuple] = []
    results: list[str] = []
    totals = {'X': 0, 'O': 0, 'D': 0}
    invert = {'X': 'O', 'O': 'X', 'D': 'D'}
    bar = tqdm(range(1, n_games + 1), total=n_games, desc="Self-play")
    for i in bar:
        res, hist_x, hist_o = play_game_selfplay(menace_x, menace_o)
        totals[res] += 1
        results.append(res)
        menace_x.update(hist_x, res)
        menace_o.update(hist_o, invert[res])
        bar.set_postfix(
            x=f"{totals['X']/i:.3f}",
            draw=f"{totals['D']/i:.3f}",
            o=f"{totals['O']/i:.3f}",
        )
        if i % report_every == 0 or i == n_games:
            xrate = totals['X'] / i
            drawrate = totals['D'] / i
            orate = totals['O'] / i
            stats.append((i, totals['X'], totals['D'], totals['O'], xrate, drawrate, orate))
            print(f"{i} games: X {xrate:.3f}, draw {drawrate:.3f}, O {orate:.3f}")
    menace_x.training_results = results
    menace_o.training_results = results
    return menace_x, menace_o, stats

def _rolling_winrate(results: list[str], window: int) -> tuple[list[int], list[float]]:
    """Compute a rolling win rate ('X') over `window` games from raw results."""
    games = []
    rates = []
    wins = 0
    for i, r in enumerate(results, start=1):
        wins += 1 if r == 'X' else 0
        if i > window:
            wins -= 1 if results[i - window - 1] == 'X' else 0
            span = window
        else:
            span = i
        games.append(i)
        rates.append(wins / span)
    return games, rates

def plot_stats(
    stats: list[tuple],
    save_path: str | None = None,
    window: int = 50,
    results: list[str] | None = None,
) -> None:
    """
    Plot the MENACE learning curve.

    When `results` (raw per-game outcomes) is provided, cumulative rates and
    the rolling win rate are both computed at per-game resolution, giving the
    high-fidelity noisy chart that shows actual learning dynamics. Falls back
    to the coarse sampled stats when results is not provided.

    Args:
        stats: Sampled stats from train_menace.
        save_path: If set, the figure is saved here instead of shown.
        window: Window size for the rolling win rate line.
        results: Raw per-game results list ('X'/'D'/'O') from m.training_results.
    """
    color_win  = '#2196F3'
    color_draw = '#FF9800'
    color_loss = '#F44336'

    plt.figure(figsize=(10, 6))

    if results:
        # Per-game cumulative rates (smooth because they are running totals)
        n = len(results)
        games_pg = list(range(1, n + 1))
        wx, dx, lx = 0, 0, 0
        cum_win, cum_draw, cum_loss = [], [], []
        for i, r in enumerate(results, start=1):
            wx += r == 'X'; dx += r == 'D'; lx += r == 'O'
            cum_win.append(wx / i)
            cum_draw.append(dx / i)
            cum_loss.append(lx / i)

        plt.plot(games_pg, cum_win,  label="Win Rate",  color=color_win,  linewidth=2)
        plt.plot(games_pg, cum_draw, label="Draw Rate", color=color_draw, linewidth=2)
        plt.plot(games_pg, cum_loss, label="Loss Rate", color=color_loss, linewidth=2)

        # Rolling win rate — noisy, shows game-by-game variance
        roll_games, roll_rates = _rolling_winrate(results, window)
        plt.plot(
            roll_games, roll_rates,
            label=f"Win Rate (rolling {window})",
            color=color_win, linestyle='--', alpha=0.5, linewidth=1,
        )
    else:
        # Fallback: coarse sampled stats
        games = [s[0] for s in stats]
        plt.plot(games, [s[4] for s in stats], label="Win Rate",  color=color_win,  linewidth=2)
        plt.plot(games, [s[5] for s in stats], label="Draw Rate", color=color_draw, linewidth=2)
        plt.plot(games, [s[6] for s in stats], label="Loss Rate", color=color_loss, linewidth=2)

    plt.xlabel("Games Played")
    plt.ylabel("Rate")
    plt.title("MENACE Learning Curve")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150)
    else:
        plt.show()
