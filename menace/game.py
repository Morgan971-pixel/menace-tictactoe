"""
Tic-Tac-Toe Game Logic

This module provides a clean implementation of tic-tac-toe game mechanics,
separated from AI logic for modularity and testability.

Board Representation:
    Linear list of 9 elements representing a 3x3 grid:
    [0] [1] [2]
    [3] [4] [5]  
    [6] [7] [8]

Design Principles:
- Immutable operations (copy() for safety)
- Clear separation of game rules from AI
- Simple string representation for debugging
- Efficient winner detection using pre-computed lines
"""

EMPTY = ' '

class Board:
    """
    Represents a tic-tac-toe game board.
    
    The board uses a linear representation where positions 0-8 map to:
        0 | 1 | 2
        ----------
        3 | 4 | 5  
        ----------
        6 | 7 | 8
    
    Attributes:
        cells (list): 9-element list containing 'X', 'O', or ' ' (empty)
    
    Examples:
        >>> board = Board()
        >>> board.make_move(4, 'X')  # X takes center
        True
        >>> board.available_moves()
        [0, 1, 2, 3, 5, 6, 7, 8]
        >>> print(board)
        0|1|2
        -----
        3|X|5
        -----
        6|7|8
    """
    
    def __init__(self):
        """Initialize an empty 3x3 tic-tac-toe board."""
        self.cells = [EMPTY] * 9

    def available_moves(self):
        """
        Get list of available move positions.
        
        Returns:
            list: Indices of empty cells (0-8)
        """
        return [i for i, v in enumerate(self.cells) if v == EMPTY]

    def make_move(self, index, symbol):
        """
        Attempt to place a symbol at the given position.
        
        Args:
            index (int): Board position (0-8)  
            symbol (str): 'X' or 'O'
        
        Returns:
            bool: True if move was successful, False if position occupied
        """
        if self.cells[index] == EMPTY:
            self.cells[index] = symbol
            return True
        return False

    def copy(self):
        """
        Create a deep copy of the board.
        
        Returns:
            Board: New Board instance with identical state
            
        Note:
            Used for safe state exploration without modifying original
        """
        new_board = Board()
        new_board.cells = self.cells[:]
        return new_board

    def __str__(self):
        """
        Create a human-readable representation of the board.
        
        Shows actual symbols for occupied positions and position numbers
        for empty positions (helpful for interactive play).
        
        Returns:
            str: Multi-line string representation of board
        """
        rows = []
        for r in range(3):
            row = self.cells[3*r:3*r+3]
            rows.append('|'.join(c if c != EMPTY else str(3*r+i) for i, c in enumerate(row)))
        return '\n'.join(rows)

def winner(board):
    """
    Determine the winner of a tic-tac-toe game.
    
    Checks all possible winning combinations (rows, columns, diagonals)
    to determine if there's a winner or if the game is a draw.
    
    Args:
        board (Board): Current game state
    
    Returns:
        str or None: 
            - 'X' if X has won
            - 'O' if O has won  
            - 'D' if the game is a draw (board full, no winner)
            - None if the game is still in progress
    
    Algorithm:
        1. Check all 8 winning lines (3 rows + 3 columns + 2 diagonals)
        2. Return winner if any line has 3 matching non-empty symbols
        3. Return 'D' for draw if board is full with no winner
        4. Return None if game continues
    
    Winning Lines:
        Rows:      (0,1,2), (3,4,5), (6,7,8)
        Columns:   (0,3,6), (1,4,7), (2,5,8)  
        Diagonals: (0,4,8), (2,4,6)
    """
    lines = [
        (0,1,2),(3,4,5),(6,7,8),  # rows
        (0,3,6),(1,4,7),(2,5,8),  # columns
        (0,4,8),(2,4,6)           # diagonals
    ]
    for a,b,c in lines:
        if board.cells[a] != EMPTY and board.cells[a] == board.cells[b] == board.cells[c]:
            return board.cells[a]
    if EMPTY not in board.cells:
        return 'D'  # draw
    return None
