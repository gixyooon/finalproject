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

# ground settings
ground = pygame.Surface((SCREEN_WIDTH, 100))
ground.fill((182, 138, 73))
ground_rect = ground.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

# obstacle settings
obstacle_width = 30
obstacle_height = 30
obstacle_color = (220, 220, 220)
obstacle_speed = 5

obstacles = []
obstacle_spawn_count = {}  # to track obstacle spawn count at each y position

# function to check obstacle spacing
def check_obstacle_spacing(new_obstacle_rect, existing_obstacles, min_distance):
    for existing_obstacle in existing_obstacles:
        if new_obstacle_rect.y == existing_obstacle.y and abs(new_obstacle_rect.x - existing_obstacle.x) < min_distance:
            return False
    return True

# game loop
run = True
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
    if random.randint(0, 100) < 2:
        new_obstacle_rect = pygame.Rect(SCREEN_WIDTH, random.choice([410, 420]), obstacle_width, obstacle_height)

        # check obstacle spacing
        min_distance = 90 if new_obstacle_rect.y == 420 else 20

        # check spawn count at y position
        spawn_count = obstacle_spawn_count.get(new_obstacle_rect.y, 0)
        if spawn_count >= 2:
            # choose a different y position
            new_obstacle_rect.y = random.choice([y for y in [470, 440] if y != new_obstacle_rect.y])
            spawn_count = 0  # reset spawn count for the new y position

        if check_obstacle_spacing(new_obstacle_rect, obstacles, min_distance):
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
        character_y_speed = -15

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
            print("Game Over!")
            run = False

    # update display
    pygame.display.update()

pygame.quit()
sys.exit()
