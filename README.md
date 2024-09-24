# Snake Game in Python

This is a classic **Snake Game** implemented using **Python** and **Pygame**. The goal of the game is to control the snake, eat the food, and grow longer while avoiding obstacles and collisions with your own body.

## Features

- **Classic Snake Gameplay**: Control the snake using the arrow keys to eat food and grow longer.
- **Multiple Levels**: As your score increases, the level of difficulty increases by adding more obstacles.
- **Special Food**: Special food items appear randomly, providing various effects such as speeding up or slowing down the snake, adding or removing lives.
- **Score and High Score System**: Tracks and displays the player’s score, with a local high score system to keep track of the top three scores.
- **Lives System**: You start with three lives. If the snake crashes into an obstacle or itself, you lose a life.
- **Boundary Wrapping**: Instead of losing a life when hitting a wall, the snake reappears from the opposite side of the screen.
- **Pause and Restart**: You can pause the game at any time and restart after the game over screen.

## Game Controls

- **Arrow Keys**: Move the snake up, down, left, or right.
- **P Key**: Pause and resume the game.
- **R Key**: Restart the game after it ends.
- **Q Key**: Quit the game after it ends.

## Special Food Effects

- **Yellow (Speed Up)**: Increases the snake's speed.
- **Blue (Slow Down)**: Decreases the snake's speed, but not below a minimum threshold.
- **Cyan (Add Life)**: Grants the player an extra life.
- **Purple (Remove Life)**: Removes one life.

## How to Play

1. Start the game by running the Python script.
2. Use the arrow keys to control the snake and try to eat the red food.
3. Avoid colliding with the blue obstacles or your own body.
4. As you score points, the game increases in difficulty by adding more obstacles and speeding up the snake.
5. Special food items will appear at random intervals, providing various effects.
6. The game ends when you lose all your lives. You can view the high scores and restart the game or quit.

## Installation

1. Clone the repository:
   ```bash
   git clone <your-repository-url>
   cd <your-repository-directory>
2. Install the required dependencies:
   ```bash
   pip install pygame
3. Run the game:
   ```bash
   python snake_game.py
## Files

- **`snake_game.py`**: Main game script.
- **`high_scores.json`**: Stores the high scores locally.
- **`eat.wav`**: Sound effect for when the snake eats food.
- **`game_over.wav`**: Sound effect for game over.
- **`background.mp3`**: Background music that plays during the game.

## Customization

- **Sound Effects**: You can replace the sound effect files (`eat.wav`, `game_over.wav`, and `background.mp3`) with your own to customize the audio experience.
- **Difficulty**: The snake's initial speed and the rate at which it increases with each level can be adjusted in the code.

## Requirements

- Python 3.x
- Pygame
## License

This project is open source and available under the MIT License.

---

Let me know if you need any further adjustments!

