from collections import Counter
import random
from .game import EMPTY

# Symmetry transforms for board reduction
TRANSFORMS = [
    list(range(9)),
    [6,3,0,7,4,1,8,5,2],  # rot90
    [8,7,6,5,4,3,2,1,0],  # rot180
    [2,5,8,1,4,7,0,3,6],  # rot270
    [2,1,0,5,4,3,8,7,6],  # reflect horiz
    [6,7,8,3,4,5,0,1,2],  # reflect vert
    [0,3,6,1,4,7,2,5,8],  # reflect diag1
    [8,5,2,7,4,1,6,3,0]   # reflect diag2
]

def permute(board, perm):
    return [board[i] for i in perm]

def canonicalize(board):
    boards = []
    perms = []
    for perm in TRANSFORMS:
        b = permute(board, perm)
        boards.append(''.join(b))
        perms.append(perm)
    min_idx = min(range(len(boards)), key=lambda i: boards[i])
    return boards[min_idx], perms[min_idx]

def invert_perm(perm):
    inv = [0]*9
    for i,p in enumerate(perm):
        inv[p] = i
    return inv

class MENACE:
    def __init__(self, init_beads=4, reward_win=3, reward_draw=1, reward_loss=-1):
        self.matchboxes = dict()
        self.init_beads = init_beads
        self.reward_win = reward_win
        self.reward_draw = reward_draw
        self.reward_loss = reward_loss
        random.seed(1)

    def _ensure_box(self, board):
        can_str, perm = canonicalize(board)
        if can_str not in self.matchboxes:
            b = list(can_str)
            moves = [i for i,v in enumerate(b) if v == EMPTY]
            beads = Counter({m: self.init_beads for m in moves})
            self.matchboxes[can_str] = beads
        return can_str, perm, self.matchboxes[can_str]

    def choose_move(self, board):
        can_str, perm, beads = self._ensure_box(board)
        choices = []
        for move, count in beads.items():
            choices += [move] * max(1, count)
        chosen_can_move = random.choice(choices)
        inv_perm = invert_perm(perm)
        chosen_orig = inv_perm[chosen_can_move]
        return chosen_orig, (can_str, chosen_can_move)

    def update(self, history, result):
        if result == 'X':
            delta = self.reward_win
        elif result == 'D':
            delta = self.reward_draw
        else:
            delta = self.reward_loss

        for can_str, move in history:
            if can_str not in self.matchboxes:
                continue
            self.matchboxes[can_str][move] += delta
            if self.matchboxes[can_str][move] < 1:
                self.matchboxes[can_str][move] = 1

    def inspect_box(self, board):
        can_str, perm, beads = self._ensure_box(board)
        inv_perm = invert_perm(perm)
        mapping = {inv_perm[m]: beads[m] for m in beads}
        return can_str, mapping
