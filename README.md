# Ghostly-Potion-Chase

Description:
------------
"Ghostly Potion Chase" is a fast-paced 2D arcade game built with Python and Pygame Zero. 
The player controls a hero who moves horizontally to catch falling magical potions while dodging mischievous ghosts. 
The hero can also attack ghosts to remove them from the playfield.

Features:
---------
- Horizontal-only player movement
- Animated player sprites (idle, walk, attack)
- Animated ghosts patrolling designated areas
- Falling potions collectible
- Player can attack ghosts to remove them
- Win condition: survive until the timer ends
- Lose condition: collision with a ghost
- Menu with options: Start Game, Music On/Off, Sounds On/Off, Exit
- Goal: collect as many potions as possible during the time frame
- Score: Potion +1, Ghost +5

Used Libraries:
------------------
- Pygame Zero (pgzero)
- Rect class from Pygame
- random

Running the Game:
-----------------
1. Make sure all game assets (images and sounds) are in the same folder as game.py
2. Open a terminal/command prompt and navigate to the project folder.
3. Run the game using:
   pgzrun game.py
4. Controls:
   - Left Arrow / Right Arrow: Move player horizontally
   - Space: Attack ghosts
   - Mouse Click: Interact with menu
   - Enter: Return to menu after win/lose
