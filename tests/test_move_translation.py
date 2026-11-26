"""Regression tests: MENACE must map canonical moves back to the real board correctly.

choose_move picks a move in the canonical (rotated/reflected) board and must
translate it back. Before the fix it used the inverse permutation, which is
wrong for the 90 and 270 degree rotations, so MENACE sometimes chose an
occupied square and the move was silently rejected.
"""
from menace.game import Board, winner
from menace.menace import MENACE, TRANSFORMS, canonicalize


def reachable_positions():
    """Every non-terminal position with X (MENACE) to move."""
    seen, out = set(), []

    def walk(cells, turn):
        b = Board()
        b.cells = cells
        if winner(b) is not None:
            return
        if turn == 'X' and tuple(cells) not in seen:
            seen.add(tuple(cells))
            out.append(cells[:])
        for i in range(9):
            if cells[i] == ' ':
                nxt = cells[:]
                nxt[i] = turn
                walk(nxt, 'O' if turn == 'X' else 'X')

    walk([' '] * 9, 'X')
    return out


def test_choose_move_never_picks_an_occupied_square():
    m = MENACE()
    for cells in reachable_positions():
        for _ in range(3):
            move, _ = m.choose_move(cells)
            assert cells[move] == ' ', f"picked occupied square {move} on {''.join(cells)}"


def test_inspect_box_only_maps_to_empty_squares():
    m = MENACE()
    for cells in reachable_positions():
        _, mapping = m.inspect_box(cells)
        assert sorted(mapping) == [i for i, c in enumerate(cells) if c == ' ']


def test_logged_canonical_move_points_at_the_chosen_square():
    m = MENACE()
    for cells in reachable_positions():
        move, (can_str, can_move) = m.choose_move(cells)
        _, perm = canonicalize(cells)
        assert perm[can_move] == move
        assert can_str[can_move] == ' '


def test_every_transform_is_a_permutation():
    for t in TRANSFORMS:
        assert sorted(t) == list(range(9))
