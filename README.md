# CubiXpert

CubiXpert is a **3D Tic-Tac-Toe (4x4x4)** game built with Python and Pygame, featuring a GUI and an AI opponent powered by **Minimax with Alpha-Beta pruning**.

## Features

- 4-layer 3D board rendered in a stylized trapezoid "galaxy" interface
- Human vs AI gameplay
- AI decision-making using Minimax + Alpha-Beta pruning
- Heuristic evaluation based on layer control, edge/corner control, line potential, and mobility
- Win-line visualization and replay flow
- Experimental scripts to compare Minimax vs Alpha-Beta performance

## Project Structure

```text
cubiXpert/
  main.py                       # Entry point
  models/
    cubic_game.py               # Core 3D board logic and win detection
    ai_logic.py                 # AIPlayer (minimax + alpha-beta + heuristic)
  views/gui/
    game_gui.py                 # Pygame interface
    assets/                     # Fonts, sounds, images
  tests/
    test_minimax.py             # Minimax benchmark script
    test_alpha_beta.py          # Alpha-beta benchmark script
    minimax_results.txt         # Sample output log
    alphabeta_results.txt       # Sample output log
  Dockerfile
  docker-compose.yaml
  requirements.txt
```

## Requirements

- Python 3.9+
- `pip`
- Pygame-compatible environment (desktop GUI + audio support)

Install dependency:

```bash
pip install -r requirements.txt
```

## Run Locally

From the project root:

```bash
python main.py
```

### Controls

- Click a cell to place your move
- Close window to exit
- On the end screen, click **Play Again** to restart
- On the end screen, press **Enter** to restart

## AI Details

- AI token: `0` (displayed as `O`)
- Human token: `1` (displayed as `X`)
- Default AI search depth: `2`
- Terminal score for AI win: `+10000`
- Terminal score for human win: `-10000`

The AI uses alpha-beta pruning to reduce branching cost while preserving minimax decision quality.

## Benchmark / Test Scripts

These scripts simulate AI-vs-AI style matches and write result logs into `tests/`.

Run Minimax test:

```bash
python tests/test_minimax.py
```

Run Alpha-Beta test:

```bash
python tests/test_alpha_beta.py
```

Outputs:

- `tests/minimax_results.txt`
- `tests/alphabeta_results.txt`

## Docker

Build and run with Docker Compose:

```bash
docker compose up --build
```

Notes:

- GUI apps in containers require host display forwarding (X server / equivalent).
- `docker-compose.yaml` already includes a `DISPLAY` environment variable for Windows/WSL-style setups.

## Known Notes

- Background music is loaded from `views/gui/assets/sounds/MarwanMoussa-ElBoslaDa3et.mp3`
- If audio initialization fails, the game still runs; the error is printed to console.

## License

This project is licensed under the **GNU General Public License v3.0**. See [LICENSE](LICENSE).
