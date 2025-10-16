"""
MENACE: Matchbox Educable Noughts And Crosses Engine

A Python implementation of Donald Michie's 1960s MENACE system that learns 
to play tic-tac-toe through reinforcement learning using a bead-counting 
mechanism analogous to physical matchboxes.

This package provides:
- Core MENACE learning algorithm with symmetry reduction
- Game board representation and rule enforcement  
- Training utilities and visualization tools
- Opponent strategies for testing and gameplay
- Interactive examples and demonstrations

Quick Start:
    >>> from menace import MENACE, train_menace
    >>> menace, stats = train_menace(n_games=1000)
    >>> # MENACE is now trained and ready to play

Modules:
    game: Board representation and tic-tac-toe game rules
    menace: Core MENACE learning algorithm implementation
    train: Training orchestration and progress visualization
    opponent: Various opponent strategies for training/testing

Historical Note:
    MENACE was created by Donald Michie in the 1960s using 304 physical 
    matchboxes and colored beads, demonstrating machine learning concepts
    decades before digital computers made such algorithms practical.
"""

# Make MENACE modules easy to import
from .game import Board, winner
from .menace import MENACE
from .opponent import random_opponent_move
from .train import play_game_once, train_menace, plot_stats
