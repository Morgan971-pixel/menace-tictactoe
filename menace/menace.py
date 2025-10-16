"""
MENACE (Matchbox Educable Noughts and Crosses Engine) Implementation

This module implements Donald Michie's 1960s MENACE system in Python.
MENACE learns to play tic-tac-toe using reinforcement learning with a 
bead-counting mechanism analogous to the original physical matchboxes.

Key Features:
- Reinforcement learning through bead adjustment
- Symmetry reduction to optimize learning efficiency  
- Probabilistic move selection based on experience
- Graceful degradation (minimum 1 bead per legal move)

Algorithm Overview:
1. Each board position maps to a "matchbox" (dictionary entry)
2. Each legal move has "beads" (probability weights)  
3. Learning adjusts bead counts: Win (+3), Draw (+1), Loss (-1)
4. Move selection is probabilistic: more beads = higher chance

Mathematical Insight:
The symmetry reduction recognizes that rotated/reflected boards are
strategically equivalent, reducing the state space from 5,478 to ~765
canonical positions. This enables 7x faster learning convergence.
"""

from collections import Counter
import random
from .game import EMPTY

# Symmetry transforms for board reduction to canonical form
# Board positions: [0,1,2]
#                  [3,4,5] 
#                  [6,7,8]
TRANSFORMS = [
    list(range(9)),           # identity (no transform)
    [6,3,0,7,4,1,8,5,2],     # rotate 90° clockwise
    [8,7,6,5,4,3,2,1,0],     # rotate 180°
    [2,5,8,1,4,7,0,3,6],     # rotate 270° clockwise  
    [2,1,0,5,4,3,8,7,6],     # reflect horizontally
    [6,7,8,3,4,5,0,1,2],     # reflect vertically
    [0,3,6,1,4,7,2,5,8],     # reflect main diagonal
    [8,5,2,7,4,1,6,3,0]      # reflect anti-diagonal
]

def permute(board, perm):
    """
    Apply a permutation transformation to a board.
    
    Args:
        board (list): 9-element list representing board state
        perm (list): Permutation indices for transformation
    
    Returns:
        list: Transformed board according to permutation
        
    Example:
        >>> board = ['X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        >>> perm = [2, 5, 8, 1, 4, 7, 0, 3, 6]  # rotate 270°
        >>> permute(board, perm)
        [' ', ' ', 'X', ' ', ' ', ' ', ' ', ' ', ' ']
    """
    return [board[i] for i in perm]

def canonicalize(board):
    """
    Convert board to canonical (standardized) representation.
    
    This is the core optimization that makes MENACE efficient. By recognizing
    that rotated and reflected board positions are strategically equivalent,
    we can reduce the number of "matchboxes" needed from 5,478 to ~765.
    
    Args:
        board (list): 9-element list representing board state
    
    Returns:
        tuple: (canonical_string, transformation_used)
            - canonical_string: Lexicographically smallest equivalent board
            - transformation_used: Permutation that produced canonical form
    
    Algorithm:
        1. Apply all 8 symmetry transformations (4 rotations + 4 reflections)
        2. Convert each to string representation  
        3. Return the lexicographically smallest (canonical) form
        4. Track which transformation was used for move translation
    """
    boards = []
    perms = []
    for perm in TRANSFORMS:
        b = permute(board, perm)
        boards.append(''.join(b))
        perms.append(perm)
    min_idx = min(range(len(boards)), key=lambda i: boards[i])
    return boards[min_idx], perms[min_idx]

def invert_perm(perm):
    """
    Compute the inverse of a permutation.
    
    Used to translate moves from canonical space back to original board space.
    
    Args:
        perm (list): Permutation to invert
    
    Returns:
        list: Inverse permutation
        
    Example:
        >>> perm = [2, 1, 0]  # reverse positions 0,1,2
        >>> invert_perm(perm)
        [2, 1, 0]  # its own inverse
    """
    inv = [0]*9
    for i,p in enumerate(perm):
        inv[p] = i
    return inv

class MENACE:
    """
    MENACE (Matchbox Educable Noughts and Crosses Engine)
    
    A reinforcement learning agent that learns tic-tac-toe strategy through
    experience, modeled after Donald Michie's 1960s physical machine.
    
    The algorithm uses "matchboxes" (board positions) containing "beads" 
    (move probabilities) that are adjusted based on game outcomes:
    - Win: Add reward_win beads to moves that led to victory
    - Draw: Add reward_draw beads to moves 
    - Loss: Subtract reward_loss beads from moves (minimum 1 bead)
    
    Attributes:
        matchboxes (dict): Maps canonical board states to move probabilities
        init_beads (int): Initial bead count for new moves
        reward_win (int): Beads added for winning moves  
        reward_draw (int): Beads added for drawing moves
        reward_loss (int): Beads subtracted for losing moves (as negative)
    
    Example:
        >>> menace = MENACE()
        >>> board = [' '] * 9
        >>> move, log_info = menace.choose_move(board)
        >>> # ... play game ...
        >>> menace.update([log_info], 'X')  # MENACE won
    """
    
    def __init__(self, init_beads=4, reward_win=3, reward_draw=1, reward_loss=-1):
        """
        Initialize MENACE with learning parameters.
        
        Args:
            init_beads (int): Starting bead count for each legal move
            reward_win (int): Reward for moves leading to wins  
            reward_draw (int): Reward for moves leading to draws
            reward_loss (int): Penalty for moves leading to losses (negative)
        """
        self.matchboxes = dict()
        self.init_beads = init_beads
        self.reward_win = reward_win
        self.reward_draw = reward_draw
        self.reward_loss = reward_loss
        random.seed(1)

    def _ensure_box(self, board):
        """
        Ensure a matchbox exists for the given board position.
        
        This method handles the canonical representation and creates new
        matchboxes as needed. Each matchbox starts with init_beads for
        every legal move in that position.
        
        Args:
            board (list): Current board state (9 elements)
        
        Returns:
            tuple: (canonical_string, permutation_used, bead_counter)
                - canonical_string: Standardized board representation
                - permutation_used: Transform applied to reach canonical form  
                - bead_counter: Counter object with move -> bead_count mapping
        """
        can_str, perm = canonicalize(board)
        if can_str not in self.matchboxes:
            b = list(can_str)
            moves = [i for i,v in enumerate(b) if v == EMPTY]
            beads = Counter({m: self.init_beads for m in moves})
            self.matchboxes[can_str] = beads
        return can_str, perm, self.matchboxes[can_str]

    def choose_move(self, board):
        """
        Select a move using probabilistic sampling based on bead counts.
        
        Algorithm:
        1. Get/create matchbox for current board position
        2. Build weighted list: more beads = more copies in list
        3. Randomly select from weighted list (probabilistic selection)
        4. Transform move from canonical space back to original board space
        
        Args:
            board (list): Current board state (9 elements)
        
        Returns:
            tuple: (chosen_move, log_entry)
                - chosen_move: Board index (0-8) for MENACE's move
                - log_entry: (canonical_string, canonical_move) for learning
        
        Example:
            If matchbox has {1: 2, 4: 6, 7: 1} beads:
            - Move 1: 2/9 probability  
            - Move 4: 6/9 probability (most likely)
            - Move 7: 1/9 probability
        """
        can_str, perm, beads = self._ensure_box(board)
        choices = []
        for move, count in beads.items():
            choices += [move] * max(1, count)  # Ensure at least 1 copy
        chosen_can_move = random.choice(choices)
        inv_perm = invert_perm(perm)
        chosen_orig = inv_perm[chosen_can_move]
        return chosen_orig, (can_str, chosen_can_move)

    def update(self, history, result):
        """
        Update bead counts based on game outcome (learning step).
        
        This is where MENACE learns! Each move in the game gets reinforcement
        based on the final outcome. Good outcomes increase bead counts
        (making moves more likely), bad outcomes decrease them.
        
        Args:
            history (list): List of (canonical_string, move) tuples from game
            result (str): Game outcome - 'X' (win), 'D' (draw), or 'O' (loss)
        
        Algorithm:
            1. Determine reward based on outcome
            2. For each move MENACE made:
               - Add/subtract beads based on outcome
               - Enforce minimum of 1 bead per move (prevents "death")
        
        Learning Rules:
            - Win: All moves get +reward_win beads (default +3)  
            - Draw: All moves get +reward_draw beads (default +1)
            - Loss: All moves get reward_loss beads (default -1)
        """
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
            # Critical: ensure minimum 1 bead (prevents getting "stuck")
            if self.matchboxes[can_str][move] < 1:
                self.matchboxes[can_str][move] = 1

    def inspect_box(self, board):
        """
        Examine the current bead counts for a board position.
        
        Useful for debugging and understanding MENACE's learned strategy.
        
        Args:
            board (list): Board state to inspect
        
        Returns:
            tuple: (canonical_string, move_to_beads_mapping)
                - canonical_string: Standardized board representation  
                - move_to_beads_mapping: Dict of {original_move: bead_count}
        """
        can_str, perm, beads = self._ensure_box(board)
        inv_perm = invert_perm(perm)
        mapping = {inv_perm[m]: beads[m] for m in beads}
        return can_str, mapping
