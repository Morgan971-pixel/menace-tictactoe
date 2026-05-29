"""
Opponent Strategies for MENACE Training and Testing

This module provides opponent implementations used to train MENACE or test
its performance against different play styles.

Implements:
- Random opponent: makes random legal moves (primary training opponent)
- Minimax opponent: plays optimally as O (also exposed as perfect_opponent_move)
"""

import random
from .game import Board, EMPTY, winner

def random_opponent_move(board: Board) -> int | None:
    """
    Select a random legal move from available positions.

    Args:
        board (Board): Current game state

    Returns:
        int or None: Random legal move index (0-8), or None if none available
    """
    legal = [i for i, v in enumerate(board.cells) if v == EMPTY]
    return random.choice(legal) if legal else None

# Terminal scores from O's perspective: O win is best, X win is worst.
_SCORES = {'O': 1, 'X': -1, 'D': 0}

def _minimax(board: Board, turn: str) -> int:
    """Return the minimax value of board from O's perspective for player `turn`."""
    res = winner(board)
    if res is not None:
        return _SCORES[res]

    legal = board.available_moves()
    if turn == 'O':
        best = -2
        for mv in legal:
            child = board.copy()
            child.make_move(mv, 'O')
            best = max(best, _minimax(child, 'X'))
        return best
    else:
        best = 2
        for mv in legal:
            child = board.copy()
            child.make_move(mv, 'X')
            best = min(best, _minimax(child, 'O'))
        return best

def minimax_opponent_move(board: Board) -> int:
    """
    Return the optimal move index for O using minimax.

    MENACE plays X and the opponent plays O, so this maximises O's outcome
    while minimising X's. Assumes it is O's turn to move.

    Args:
        board (Board): Current game state

    Returns:
        int: Optimal move index (0-8)
    """
    best_move = -1
    best_score = -2
    for mv in board.available_moves():
        child = board.copy()
        child.make_move(mv, 'O')
        score = _minimax(child, 'X')
        if score > best_score:
            best_score = score
            best_move = mv
    return best_move

perfect_opponent_move = minimax_opponent_move
