# Poker Equity Calculator

A Python tool for calculating hand equity in Texas Hold'em using Monte Carlo simulation, given known hole cards, board state, and number of opponents.

## Features
- Monte Carlo simulation of remaining board runouts
- Support for preflop, flop, turn, and river equity calculations
- Multi-way pot support (2+ players)
- Range vs. range or specific hand vs. specific hand comparisons
- Allows for unknown player hole cards (1 card known or neither cards known)
- Hand strength breakdown (win % / tie %) 

## Project Structure
```
poker_equity_calculator/
├── src/
│   ├── __init__.py
│   ├── deck.py         # create deck, remove known cards, parse cards, hands, board
│   ├── evaluator.py    # evaluate 5 card hand, find best hand of 7
│   └── simulator.py    # simulate random games and track wins/ties for each player
├── main.py     
└── README.md
```

## Installation
```bash
git clone https://github.com/<your-username>/poker_equity_calculator.git
cd poker_equity_calculator
```

### Requirements
- Python 3.x
- No external libraries required

## Usage
```bash
python main.py --players 2 --hands Kh3s Ad --board Ah2s7s
```

### Options
| Flag | Description | Default |
|---|---|---|
| `--players` | Number of player 2-6 (required) | — |
| `--hands` | Known hole cards per player seperated by space (required) | — |
| `--board` | Known board cards (flop, turn, river) | ' ' |
| `--sims` | Number of simulations | 10000 |

## Sample Output
```
========================================
RESULTS
========================================
Player 1 (Kh 3s):
  Win %: 5.55%
  Tie %: 0.07%
----------------------------------------
Player 2 (Ad):
  Win %: 94.38%
  Tie %: 0.07%
----------------------------------------
```

## How It Works
1. **Input parsing** — hole cards and board cards are parsed into a standard internal representation.
2. **Simulation** — for each trial, remaining deck cards are shuffled and dealt for unknown player hole cards and remaining board cards.
3. **Hand evaluation** — each player's best 5-card hand is scored and compared.
4. **Equity aggregation** — win/tie/loss counts are tallied across all simulations and converted to percentages.

Accuracy scales with the number of simulations; default is set to balance speed and precision (~10k trials gives roughly ±0.5–1%  margin of error).

## Author
Anthony Schneider