"""
MENACE Training Demonstration with Visualization

Trains MENACE against a random opponent, optionally saves the trained
instance, and plots the learning curve.

Usage:
    Run directly: python train_and_plot.py
    Or via entry point: menace-train
"""

import argparse

from menace.train import train_menace, plot_stats

def main() -> None:
    """Parse CLI arguments, train MENACE, and optionally save and plot."""
    parser = argparse.ArgumentParser(description="Train MENACE and plot its learning curve.")
    parser.add_argument("--games", type=int, default=5000, help="Number of training games.")
    parser.add_argument("--report-every", type=int, default=500, help="Report interval in games.")
    parser.add_argument("--save", type=str, default=None, help="Path to save the trained MENACE as JSON.")
    parser.add_argument(
        "--no-plot",
        dest="plot",
        action="store_false",
        help="Skip showing the plot (plotting is on by default).",
    )
    parser.set_defaults(plot=True)
    args = parser.parse_args()

    menace, stats = train_menace(n_games=args.games, report_every=args.report_every)

    if args.save:
        menace.save(args.save)
        print(f"Saved trained MENACE to {args.save}")

    if args.plot:
        plot_stats(stats, results=menace.training_results)

if __name__ == "__main__":
    main()
