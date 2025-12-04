# Mahjong Riichi Game

This is a simple implementation of a Mahjong Riichi game.
The game allows players to play Mahjong Riichi with basic rules and functionalities.
For now, the game supports one-player mode against AI opponents.

## Features

- AI uses either random or tile efficiency or Deep CNN to make decisions.
- Basic game follows Mahjong Riichi rules strictly: Tonpuusen, 4 players, Akadora, Open tanyao.
- Graphical User Interface (GUI) using Pygame.
- Tile animations for discarding tiles.
- Player interactions for calling tiles (Chi, Pon, Minkan/Ankan/Chakan, Ron, Tsumo).

## Quick download

`npm run setup` to download all neccessary packages

## Quick Start

- For normal gameplay:

  `python main.py` or `npm start` to start the game.

- Optional argv:

  1. `debug` - to reveal all players hand and draw hitbox
  2. `data=<data_file.json>` - to input predefine data for testing each edge case, some data may not be the same because of latest bots' AI update.

## Requirements

- Python 3.13+
- Pygame
- NumPy
- PyTorch (if using Deep CNN AI)
- Torch (visualize)
- Mahjong
