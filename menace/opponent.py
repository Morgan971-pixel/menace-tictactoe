import random
from .game import EMPTY

def random_opponent_move(board):
    legal = [i for i,v in enumerate(board.cells) if v == EMPTY]
    return random.choice(legal) if legal else None
