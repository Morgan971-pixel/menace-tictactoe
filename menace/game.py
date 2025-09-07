EMPTY = ' '

class Board:
    def __init__(self):
        self.cells = [EMPTY] * 9

    def available_moves(self):
        return [i for i, v in enumerate(self.cells) if v == EMPTY]

    def make_move(self, index, symbol):
        if self.cells[index] == EMPTY:
            self.cells[index] = symbol
            return True
        return False

    def copy(self):
        new_board = Board()
        new_board.cells = self.cells[:]
        return new_board

    def __str__(self):
        rows = []
        for r in range(3):
            row = self.cells[3*r:3*r+3]
            rows.append('|'.join(c if c != EMPTY else str(3*r+i) for i, c in enumerate(row)))
        return '\n'.join(rows)

def winner(board):
    lines = [
        (0,1,2),(3,4,5),(6,7,8),
        (0,3,6),(1,4,7),(2,5,8),
        (0,4,8),(2,4,6)
    ]
    for a,b,c in lines:
        if board.cells[a] != EMPTY and board.cells[a] == board.cells[b] == board.cells[c]:
            return board.cells[a]
    if EMPTY not in board.cells:
        return 'D'  # draw
    return None
