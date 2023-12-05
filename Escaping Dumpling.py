import pygame
import math
import sys
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Runner")

# load image
bg = pygame.image.load("bg.png").convert()
bg_width = bg.get_width()
bg_rect = bg.get_rect()

# define game variables
scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

# character settings
character_radius = 25
character_color = (255, 228, 186)
character_rect = pygame.Rect(200 - character_radius, 500 - character_radius, character_radius * 2, character_radius * 2)
character_y_speed = 0
jump_height = -17

# ground settings
ground = pygame.Surface((SCREEN_WIDTH, 100))
ground.fill((182, 138, 73))
ground_rect = ground.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

# obstacle settings
obstacle_width = 30
obstacle_height = 40
obstacle_color = (220, 220, 220)
obstacle_speed = 5

obstacles = []
obstacle_spawn_count = {}  # to track obstacle spawn count at each y position

# UI settings
ui_radius = 10
ui_heart_color = (255, 0, 0)
ui_highlight_color = (169, 169, 169)  # Dark gray
ui_spacing = 4
ui_positions = [(10 + i * (2 * ui_radius + ui_spacing), 10) for i in range(3)]

# function to check obstacle spacing
def check_obstacle_spacing(new_obstacle_rect, existing_obstacles, min_distance, max_distance):
    for existing_obstacle in existing_obstacles:
        if new_obstacle_rect.y == existing_obstacle.y and abs(new_obstacle_rect.x - existing_obstacle.x) < min_distance:
            return False
        elif abs(new_obstacle_rect.x - existing_obstacle.x) < max_distance:
            return False
    return True

# function to draw UI hearts
def draw_ui_hearts(num_highlighted):
    for i, ui_pos in enumerate(ui_positions):
        if i < num_highlighted:
            pygame.draw.circle(screen, ui_heart_color, ui_pos, ui_radius)
        else:
            pygame.draw.circle(screen, ui_highlight_color, ui_pos, ui_radius)

# game loop
run = True
num_highlighted_ui = 3  # Number of highlighted UI hearts
collision_occurred = False  # Flag to track if collision occurred

while run:

    clock.tick(FPS)

    # draw scrolling background
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))

    # draw character
    pygame.draw.circle(screen, character_color, character_rect.center, character_radius)

    # draw ground
    screen.blit(ground, ground_rect.topleft)

    # spawn obstacle
    if random.randint(0, 100) < 2 and not collision_occurred:
        new_obstacle_rect = pygame.Rect(SCREEN_WIDTH, random.choice([445, 470]), obstacle_width, obstacle_height)

        # check obstacle spacing
        if new_obstacle_rect.y == 445:
            min_distance = 20
            max_distance = 200
        else:
            min_distance = 90
            max_distance = 200

        # check spawn count at y position
        spawn_count = obstacle_spawn_count.get(new_obstacle_rect.y, 0)
        if spawn_count >= 2:
            # choose a different y position
            new_obstacle_rect.y = random.choice([y for y in [445, 470] if y != new_obstacle_rect.y])
            spawn_count = 0  # reset spawn count for the new y position

        if check_obstacle_spacing(new_obstacle_rect, obstacles, min_distance, max_distance):
            obstacles.append(new_obstacle_rect)
            obstacle_spawn_count[new_obstacle_rect.y] = spawn_count + 1

    # move and draw obstacles
    for obstacle_rect in obstacles:
        obstacle_rect.x -= obstacle_speed
        pygame.draw.polygon(screen, obstacle_color, [(obstacle_rect.left, obstacle_rect.bottom),
                                                     (obstacle_rect.centerx, obstacle_rect.top),
                                                     (obstacle_rect.right, obstacle_rect.bottom)])

    # remove off-screen obstacles
    obstacles = [obstacle for obstacle in obstacles if obstacle.right > 0]

    # draw UI
    draw_ui_hearts(num_highlighted_ui)

    # scroll background
    scroll -= 5

    # reset scroll
    if abs(scroll) > bg_width:
        scroll = 0

    # event handler
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and character_rect.bottom == ground_rect.top:
        character_y_speed = jump_height

    # apply gravity
    character_y_speed += 1
    character_rect.y += character_y_speed

    # character-ground collision
    if character_rect.colliderect(ground_rect):
        character_rect.bottom = ground_rect.top
        character_y_speed = 0

    # obstacle-character collision
    for obstacle_rect in obstacles:
        if character_rect.colliderect(obstacle_rect):
            if num_highlighted_ui > 0:
                num_highlighted_ui -= 1
                collision_occurred = True
                obstacle_rect.x -= 25
                print(f"Heart {num_highlighted_ui + 1} turned gray.")
            break  # Move the obstacle to the left by 25 units upon collision and exit the loop

    # Check if collision flag should be reset
    if not any(character_rect.colliderect(obstacle_rect) for obstacle_rect in obstacles):
        collision_occurred = False

    # update display
    pygame.display.update()

pygame.quit()
sys.exit()
