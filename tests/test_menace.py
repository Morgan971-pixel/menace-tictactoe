from menace.menace import MENACE

def test_menace_initial_box():
    m = MENACE(init_beads=2)
    board = [' '] * 9
    can_str, mapping = m.inspect_box(board)
    # All moves should have 2 beads initially
    assert all(v == 2 for v in mapping.values())
