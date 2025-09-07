from menace.train import train_menace, plot_stats

def main():
    # Train MENACE against a random opponent and plot the learning curve
    menace, stats = train_menace(n_games=3000, report_every=500)
    plot_stats(stats)

if __name__ == "__main__":
    main()
