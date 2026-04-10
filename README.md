# Python 2D Survival Game

A lightweight Pygame survival prototype built as a modular engine-free project.

## Overview

This project is a small tile-based survival game prototype written in Python with Pygame. It includes a configurable world, tree breaking, player inventory, simple mob AI, and combat mechanics.

## Features

- Top-down movement with W/A/S/D
- Inventory and hotbar system
- Mouse-driven tree breaking and mob attacks
- Simple sheep mob AI with fleeing behavior
- Loot drops from mob kills
- Config-driven gameplay values in `src/game/logic/core/gameplay_config.py`

## Controls

- W/A/S/D: move player
- Left mouse click: attack mob or break tree
- 1-9: select hotbar slot
- E: toggle inventory
- Inventory UI: drag/drop stacks with the mouse

## Run the game

Install Python 3 and Pygame, then start the game from the project root:

```bash
python3 -m pip install pygame
python3 src/main.py
```

## Project structure

- `src/main.py` — game entry point and main loop
- `src/game/logic/core/` — global config and update loop
- `src/game/logic/entities/` — player, mob and entity logic
- `src/game/logic/systems/` — renderer and inventory system
- `src/game/logic/world/` — world generation and object definitions

## Notes

- This is a work-in-progress prototype.
- The code is structured for modularity and ease of expansion, but may not be fully optimized or bug-free.
- COMMIT HISTORY is tracked in [`COMMITHISTORY.md`](COMMITHISTORY.md) for reference. (Note that the Commit History may be one or two commits behind the latest changes, as I update it manually.)
- Expand the game by adding new mobs, items, and world mechanics.

## Licensing

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.