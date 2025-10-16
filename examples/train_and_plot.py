"""
MENACE Training Demonstration with Visualization

This script demonstrates the complete MENACE training process including
performance visualization. It trains MENACE against a random opponent
and displays the resulting learning curve.

Usage:
    Run directly: python train_and_plot.py
    Or via entry point: menace-train
"""

from menace.train import train_menace, plot_stats

def main():
    """
    Train MENACE and display learning curve visualization.
    
    Trains MENACE for 3000 games against random opponent with progress
    reports every 500 games, then plots the learning statistics.
    """
    # Train MENACE against a random opponent and plot the learning curve
    menace, stats = train_menace(n_games=3000, report_every=500)
    plot_stats(stats)

if __name__ == "__main__":
    main()
