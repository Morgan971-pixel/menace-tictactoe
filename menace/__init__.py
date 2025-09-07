# Make MENACE modules easy to import
from .game import Board, winner
from .menace import MENACE
from .opponent import random_opponent_move
from .train import play_game_once, train_menace, plot_stats
