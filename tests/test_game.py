from menace.game import Board, winner

def test_initial_board_empty():
    b = Board()
    assert b.available_moves() == list(range(9))

def test_winner_detection_rows():
    b = Board()
    b.cells = ['X','X','X',' ',' ',' ',' ',' ',' ']
    assert winner(b) == 'X'

def test_draw():
    b = Board()
    b.cells = ['X','O','X','X','O','O','O','X','X']
    assert winner(b) == 'D'
