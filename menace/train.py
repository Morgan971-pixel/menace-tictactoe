import matplotlib.pyplot as plt
from .game import Board, winner
from .menace import MENACE
from .opponent import random_opponent_move

def play_game_once(menace, opponent=random_opponent_move):
    board = Board()
    turn = 'X'
    history = []
    while True:
        if turn == 'X':
            move, log = menace.choose_move(board.cells)
            board.make_move(move, 'X')
            history.append(log)
        else:
            move = opponent(board)
            if move is None:
                break
            board.make_move(move, 'O')
        res = winner(board)
        if res is not None:
            return res, history
        turn = 'O' if turn == 'X' else 'X'

def train_menace(n_games=5000, report_every=500):
    m = MENACE()
    stats = []
    totals = {'X':0,'O':0,'D':0}
    for i in range(1, n_games+1):
        res, hist = play_game_once(m)
        totals[res] += 1
        m.update(hist, res)
        if i % report_every == 0 or i == n_games:
            winrate = totals['X']/i
            drawrate = totals['D']/i
            losrate = totals['O']/i
            stats.append((i, totals['X'], totals['D'], totals['O'], winrate, drawrate, losrate))
            print(f"{i} games: win {winrate:.3f}, draw {drawrate:.3f}, loss {losrate:.3f}")
    return m, stats

def plot_stats(stats):
    games = [s[0] for s in stats]
    wins = [s[4] for s in stats]
    draws = [s[5] for s in stats]
    losses = [s[6] for s in stats]

    plt.figure(figsize=(8,5))
    plt.plot(games, wins, label="Win Rate")
    plt.plot(games, draws, label="Draw Rate")
    plt.plot(games, losses, label="Loss Rate")
    plt.xlabel("Games Played")
    plt.ylabel("Rate")
    plt.title("MENACE Learning Curve")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()
