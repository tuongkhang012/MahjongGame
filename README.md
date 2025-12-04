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

## Quick Start

``python main.py`` to start the game.

## Requirements

- Python 3.13+
- Pygame
- NumPy
- PyTorch (if using Deep CNN AI)