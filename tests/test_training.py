from menace.train import train_menace

def test_training_runs():
    menace, stats = train_menace(n_games=100, report_every=50)
    assert len(stats) > 0
    # MENACE should have some matchboxes after training
    assert len(menace.matchboxes) > 0
