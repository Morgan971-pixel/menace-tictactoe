"""
Opponent Strategies for MENACE Training and Testing

This module provides various opponent implementations that can be used
to train MENACE or test its performance against different play styles.

Currently implements:
- Random opponent: Makes random legal moves (primary training opponent)

Future implementations could include:
- Perfect opponent: Always makes optimal moves
- Human opponent: Interactive player interface
- Aggressive opponent: Prioritizes winning over blocking
"""

import random
from .game import EMPTY

def random_opponent_move(board):
    """
    Select a random legal move from available positions.
    
    This is the primary opponent used for MENACE training. Random play
    provides varied game scenarios while being predictably weak, allowing
    MENACE to learn winning strategies effectively.
    
    Args:
        board (Board): Current game state
        
    Returns:
        int or None: Random legal move index (0-8), or None if no moves available
    """
    legal = [i for i,v in enumerate(board.cells) if v == EMPTY]
    return random.choice(legal) if legal else None
