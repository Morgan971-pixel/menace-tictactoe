# MENACE: Matchbox Educable Noughts And Crosses Engine 🎲❌⭕  

A Python reimplementation of Donald Michie’s **MENACE (1960s)** — a physical matchbox machine that learned Tic-Tac-Toe using beads.

![Learning Curve](examples/learning_curve.png)

---

## ✨ Features
- MENACE agent with reinforcement learning (bead adjustment).
- Symmetry reduction (rotations/reflections).
- Training loop + visualization of win/draw/loss rates.
- Play interactively vs MENACE in the terminal.
- Unit tests included.

---

## 🚀 Getting Started
```bash
git clone https://github.com/Morgan971-pixel/menace-tictactoe.git
cd menace-tictactoe
pip install -e .
```

## Usage

To train MENACE and see the learning curve:
```bash
menace-train
```

To play an interactive game against a trained MENACE in your terminal:
```bash
menace-play
```
