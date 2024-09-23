import pygame  
import random
import json
import os
import logging

# Set up logging
logging.basicConfig(filename='snake_game.log', level=logging.DEBUG)

# Initialize Pygame
pygame.init()

# Set up the game window
width = 800
height = 600
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Snake and food properties
block_size = 20
initial_speed = 15
snake_speed = initial_speed
level = 1  # Add levels
lives = 3  # Add lives

# Font for display
font = pygame.font.SysFont(None, 30)
large_font = pygame.font.SysFont(None, 50)

# High scores file
high_scores_file = "high_scores.json"

# Sound effects (you can replace with your own sound files)
pygame.mixer.init()
eat_sound = pygame.mixer.Sound('eat.wav')
game_over_sound = pygame.mixer.Sound('game_over.wav')
background_music = 'background.mp3'  # Example for background music

# Load background music
pygame.mixer.music.load(background_music)
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)  # Loop the background music

# Load and save high scores
def load_high_scores():
    try:
        if os.path.exists(high_scores_file):
            with open(high_scores_file, "r") as f:
                return json.load(f)
        return [0, 0, 0]
    except Exception as e:
        logging.error(f"Error loading high scores: {e}")
        return [0, 0, 0]

def save_high_scores(scores):
    try:
        with open(high_scores_file, "w") as f:
            json.dump(scores, f)
    except Exception as e:
        logging.error(f"Error saving high scores: {e}")

# Load high scores
high_scores = load_high_scores()

def draw_snake(snake_list):
    for block in snake_list:
        pygame.draw.rect(window, GREEN, [block[0], block[1], block_size, block_size])

def draw_food(food_pos):
    pygame.draw.rect(window, RED, [food_pos[0], food_pos[1], block_size, block_size])

def display_score(score, level, lives):
    score_text = font.render(f"Score: {score}  Level: {level}  Lives: {lives}", True, WHITE)
    window.blit(score_text, [10, 10])

def display_high_scores():
    high_score_text = font.render("Top Scores:", True, WHITE)
    window.blit(high_score_text, [width - 200, 10])
    for i, score in enumerate(high_scores):
        score_text = font.render(f"{i+1}. {score}", True, WHITE)
        window.blit(score_text, [width - 200, 40 + i * 30])

def update_high_scores(score):
    global high_scores
    high_scores.append(score)
    high_scores.sort(reverse=True)
    high_scores = high_scores[:3]
    save_high_scores(high_scores)
    logging.info(f"Updated high scores: {high_scores}")

def draw_text_center(text, font, color, y_offset=0):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (width // 2, height // 2 + y_offset)
    window.blit(text_surface, text_rect)

def game_over_screen(score):
    pygame.mixer.Sound.play(game_over_sound)
    window.fill(BLACK)
    draw_text_center("Game Over!", large_font, RED, -100)
    draw_text_center(f"Final Score: {score}", font, WHITE, -50)
    draw_text_center("Press R to Restart", font, WHITE, 50)
    draw_text_center("Press Q to Quit", font, WHITE, 100)
    display_high_scores()
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_r:
                    return True

def start_screen():
    blink = True
    start_text_color = (255, 255, 0)
    clock = pygame.time.Clock()
    waiting = True
    while waiting:
        for i in range(height):
            color = (min(i // 3, 255), min(i // 2, 255), 100)
            pygame.draw.line(window, color, (0, i), (width, i))
        draw_text_center("Snake Game", large_font, GREEN, -150)
        draw_text_center("Use arrow keys to control the snake", font, WHITE, -50)
        draw_text_center("Eat food to grow longer and increase score", font, WHITE, 0)
        if blink:
            draw_text_center("Press any key to start", font, start_text_color, 100)
        pygame.display.update()
        blink = not blink
        clock.tick(3)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                else:
                    return True

def pause_game(score, level, lives):
    paused = True
    draw_text_center(f"Paused: Score: {score}  Level: {level}  Lives: {lives}", large_font, WHITE, 0)
    pygame.display.update()
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False

def game_loop():
    global snake_speed, level, lives
    game_over = False
    x1 = width // 2
    y1 = height // 2
    x1_change = block_size
    y1_change = 0
    snake_list = []
    snake_length = 1
    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
    clock = pygame.time.Clock()
    score = 0
    obstacles = []  # List to hold obstacles

    # Function to generate obstacles
    def generate_obstacles(level):
        for _ in range(level):
            obs_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            obs_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            obstacles.append([obs_x, obs_y])

    generate_obstacles(level)  # Generate initial obstacles

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -block_size
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = block_size
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -block_size
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = block_size
                    x1_change = 0
                elif event.key == pygame.K_p:
                    pause_game(score, level, lives)

        # Check for boundaries
        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0 or [x1, y1] in obstacles:
            lives -= 1
            if lives == 0:
                update_high_scores(score)
                game_over = True
            else:
                x1 = width // 2
                y1 = height // 2
                snake_list = []
                snake_length = 1
                snake_speed = initial_speed

        x1 += x1_change
        y1 += y1_change
        window.fill(BLACK)

        # Draw obstacles
        for obs in obstacles:
            pygame.draw.rect(window, BLUE, [obs[0], obs[1], block_size, block_size])

        while [food_x, food_y] in snake_list or [food_x, food_y] in obstacles:
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

        draw_food([food_x, food_y])
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # Check for self-collision
        for segment in snake_list[:-1]:
            if segment == snake_head:
                lives -= 1
                if lives == 0:
                    update_high_scores(score)
                    game_over = True

        draw_snake(snake_list)
        display_score(score, level, lives)
        pygame.display.update()

        if x1 == food_x and y1 == food_y:
            pygame.mixer.Sound.play(eat_sound)
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            snake_length += 1
            score += 1
            snake_speed += 1

            if score % 5 == 0:  # Every 5 points increase level and difficulty
                level += 1
                generate_obstacles(level)
                snake_speed += 2

        clock.tick(snake_speed)

    return game_over_screen(score)

# Start the game
def main():
    logging.info("Game started")
    if not start_screen():
        return

    while True:
        global snake_speed, level, lives
        snake_speed = initial_speed
        level = 1
        lives = 3
        result = game_loop()
        if result is False:
            break
        elif result is True:
            continue

    logging.info("Game ended")
    pygame.quit()

if __name__ == "__main__":
    main()

