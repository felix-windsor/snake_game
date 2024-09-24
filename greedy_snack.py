import pygame
import random
import json
import os
import logging
import time

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
initial_speed = 8
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

# Special food types
special_food_types = {
    "speed_up": {"color": YELLOW, "effect": "speed_up"},
    "slow_down": {"color": BLUE, "effect": "slow_down"},
    "add_life": {"color": (0, 255, 255), "effect": "add_life"},
    "remove_life": {"color": (128, 0, 128), "effect": "remove_life"}
}

special_food_spawn_time = random.randint(10, 20)  # Time before spawning special food
special_food_duration = 8  # How long the special food stays on screen


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

def draw_food(food_pos, food_type="normal"):
    if food_type == "normal":
        pygame.draw.rect(window, RED, [food_pos[0], food_pos[1], block_size, block_size])
    else:
        # Draw special food with a unique color
        pygame.draw.rect(window, special_food_types[food_type]["color"], [food_pos[0], food_pos[1], block_size, block_size])

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

    # 初始化蛇的起始位置
    x1 = width // 2
    y1 = height // 2
    x1_change = block_size
    y1_change = 0

    # 初始化蛇身
    snake_list = []
    snake_length = 1

    # 初始化食物的位置
    food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
    food_y = round(random.randrange(0, height - block_size) / block_size) * block_size

    # 初始化时钟
    clock = pygame.time.Clock()

    # 初始化分数和障碍物
    score = 0
    special_food_active = False
    special_food_time = 0
    special_food_pos = None
    special_food_type = None
    obstacles = []  # 用于保存障碍物的位置列表

    # 生成障碍物的函数
    def generate_obstacles(level):
        obstacles.clear()  # 先清空旧的障碍物列表
        while len(obstacles) < level:
            obs_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            obs_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            # 确保障碍物不与蛇和食物重叠
            if [obs_x, obs_y] not in snake_list and [obs_x, obs_y] != [food_x, food_y]:
                obstacles.append([obs_x, obs_y])

    generate_obstacles(level)  # 初始生成障碍物

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
                elif event.key == pygame.K_p:  # 暂停功能
                    pause_game(score, level, lives)

        # 更新蛇的坐标
        x1 += x1_change
        y1 += y1_change

        # 碰撞检测逻辑：蛇如果超出边界，直接从另一侧出现
        if x1 >= width:
            x1 = 0
        elif x1 < 0:
            x1 = width - block_size
        if y1 >= height:
            y1 = 0
        elif y1 < 0:
            y1 = height - block_size

        # 绘制背景
        window.fill(BLACK)

        # 绘制障碍物
        for obs in obstacles:
            pygame.draw.rect(window, (255, 165, 0), [obs[0], obs[1], block_size, block_size])

        # 检查是否撞到障碍物
        if [x1, y1] in obstacles:
            lives -= 1
            if lives == 0:
                update_high_scores(score)
                game_over = True
            else:
                # 重新设置蛇的位置并重置部分状态
                x1 = width // 2
                y1 = height // 2
                snake_list = []
                snake_length = 1
                snake_speed = initial_speed
                generate_obstacles(level)  # 重新生成障碍物

        # 特殊食物生成逻辑
        if not special_food_active and random.randint(1, 100) > 98:
            special_food_type = random.choice(list(special_food_types.keys()))
            special_food_pos = [round(random.randrange(0, width - block_size) / block_size) * block_size,
                                round(random.randrange(0, height - block_size) / block_size) * block_size]
            special_food_time = time.time()
            special_food_active = True

        # 绘制普通食物
        draw_food([food_x, food_y])

        # 绘制特殊食物
        if special_food_active:
            draw_food(special_food_pos, special_food_type)
            # 如果特殊食物的存在时间超过设定时长，则将其移除
            if time.time() - special_food_time > special_food_duration:
                special_food_active = False

        # 更新蛇的身体
        snake_head = [x1, y1]
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]

        # 检查蛇是否撞到自己
        for segment in snake_list[:-1]:
            if segment == snake_head:
                lives -= 1
                if lives == 0:
                    update_high_scores(score)
                    game_over = True

        # 绘制蛇
        draw_snake(snake_list)
        display_score(score, level, lives)

        pygame.display.update()

        # 检查是否吃到普通食物
        if x1 == food_x and y1 == food_y:
            pygame.mixer.Sound.play(eat_sound)
            food_x = round(random.randrange(0, width - block_size) / block_size) * block_size
            food_y = round(random.randrange(0, height - block_size) / block_size) * block_size
            snake_length += 1
            score += 1
            snake_speed += 1

            # 每5分增加一次等级，增加障碍物
            if score % 5 == 0:
                level += 1
                generate_obstacles(level)  # 每增加等级都生成新的障碍物
                snake_speed += 2

        # 检查是否吃到特殊食物
        if special_food_active and x1 == special_food_pos[0] and y1 == special_food_pos[1]:
            pygame.mixer.Sound.play(eat_sound)
            if special_food_type == "speed_up":
                snake_speed += 5  # 提高蛇的速度
            elif special_food_type == "slow_down":
                snake_speed = max(snake_speed - 5, 5)  # 减慢蛇的速度，但不会低于5
            elif special_food_type == "add_life":
                lives += 1  # 增加一条生命
            elif special_food_type == "remove_life":
                lives -= 1  # 减少一条生命
            special_food_active = False  # 吃完特殊食物后移除

        # 控制游戏速度
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
