# Checker Mate (CAP4621 Project)

This project implements a full Checkers environment along with AI agents that can play against each other. It supports **Minimax**, **Expectimax**, detailed logging, full rule compliance, and optional headless mode.

## Features

- Full checkers rules: legal moves, mandatory captures, multi-jumps, king promotion.
- Two playing modes:
  - **Agent Mode** — AI vs AI simulation.
  - **Human Mode** — play using mouse clicks via Pygame.
- AI Search Algorithms:
  - Minimax with Alpha–Beta Pruning
  - Expectimax
- Adjustable search depth and move delay.
- Logging of moves, board states, and AI decisions.


## Installation

1. Clone or download the project.
```
git clone https://github.com/parkine/checker-mate.git
```

2. Install dependencies:
```
pip install -r requirements.txt
```
Required libraries:
- pygame
- pytest
- Python 3.8+ recommended



## How to Run

### AI vs AI Mode

Runs two AI agents playing against each other.

```
python3 main.py --mode agent
```

### Human vs Human

This opens a Pygame window where you can play checkers manually.

```
python3 main.py --mode human
```


## Optional Arguments

| Argument | Description |
|----------|-------------|
| `--depth N` | Search depth (default 4) |
| `--log-level {INFO,DEBUG,TRACE}` | Controls logging detail (default INFO)|
| `--delay SECONDS` | Delay between AI moves (default 1.0) |
| `--headless` | Run without GUI |
| `--black-search` | minimax or expectimax (default: minimax) |
| `--red-search` | minimax or expectimax (default: minimax) |



## Example Commands

### Expectimax (Red) vs Minimax (Black)

```
python3 main.py --mode agent --red-search expectimax
```

### Run Fully Headless (no window)

```
python3 main.py --mode agent --headless
```


## Project Structure
```
📁 project/
├── main.py                # Entry point
├── agent.py               # AI search (Minimax / Expectimax)
├── game.py                # Game loop
├── checker.py             # Rules + GameState
├── constants.py           # UI + board constants
├── logger.py              # Move logging utilities
├── requirements.txt
├── README.md
│
├── 📁 tests/              # Unit tests
│   ├── test_board.py
│   ├── test_game.py
│   └── ...
│
└── 📁 assets/             # Images and other resources
    └── crown.bmp

```

## Notes

- Agent mode can run headless (without GUI) or with GUI.
- Logging files are stored automatically when running AI vs AI.


## Authors

Group 7
