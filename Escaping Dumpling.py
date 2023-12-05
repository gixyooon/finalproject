import pygame
import math
import sys
import random

pygame.init()

clock = pygame.time.Clock()
FPS = 60

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# 게임 창 생성
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Runner")

# 이미지 로드
bg = pygame.image.load("bg.png").convert()
bg_width = bg.get_width()
bg_rect = bg.get_rect()

# 게임 변수 정의
scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

# 캐릭터 설정
character_radius = 25
character_color = (255, 228, 186)
character_rect = pygame.Rect(200 - character_radius, 500 - character_radius, character_radius * 2, character_radius * 2)
character_y_speed = 0
jump_height = -17

# 지면 설정
ground = pygame.Surface((SCREEN_WIDTH, 100))
ground.fill((182, 138, 73))
ground_rect = ground.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))

# 장애물 설정
obstacle_width = 30
obstacle_height = 40
obstacle_color = (220, 220, 220)
obstacle_speed = 5

obstacles = []
obstacle_spawn_count = {}  # 각 y 위치에서의 장애물 생성 횟수를 추적

# UI 설정
ui_radius = 10
ui_heart_color = (255, 0, 0)
ui_highlight_color = (169, 169, 169)  # 짙은 회색
ui_spacing = 4
ui_positions = [(10 + i * (2 * ui_radius + ui_spacing), 10) for i in range(3)]

# 장애물 간격을 확인하는 함수
def check_obstacle_spacing(new_obstacle_rect, existing_obstacles, min_distance, max_distance):
    for existing_obstacle in existing_obstacles:
        if new_obstacle_rect.y == existing_obstacle.y and abs(new_obstacle_rect.x - existing_obstacle.x) < min_distance:
            return False
        elif abs(new_obstacle_rect.x - existing_obstacle.x) < max_distance:
            return False
    return True

# UI 하트를 그리는 함수
def draw_ui_hearts(num_highlighted):
    for i, ui_pos in enumerate(ui_positions):
        if i < num_highlighted:
            pygame.draw.circle(screen, ui_heart_color, ui_pos, ui_radius)
        else:
            pygame.draw.circle(screen, ui_highlight_color, ui_pos, ui_radius)

# 게임 루프
run = True
num_highlighted_ui = 3  # 강조된 UI 하트 개수
collision_occurred = False  # 충돌 여부를 추적하는 플래그

while run:

    clock.tick(FPS)

    # 스크롤링 배경 그리기
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))

    # 캐릭터 그리기
    pygame.draw.circle(screen, character_color, character_rect.center, character_radius)

    # 지면 그리기
    screen.blit(ground, ground_rect.topleft)

    # 장애물 생성
    if random.randint(0, 100) < 2 and not collision_occurred:
        new_obstacle_rect = pygame.Rect(SCREEN_WIDTH, random.choice([445, 470]), obstacle_width, obstacle_height)

        # 장애물 간격 확인
        if new_obstacle_rect.y == 445:
            min_distance = 20
            max_distance = 200
        else:
            min_distance = 90
            max_distance = 200

        # y 위치에서의 생성 횟수 확인
        spawn_count = obstacle_spawn_count.get(new_obstacle_rect.y, 0)
        if spawn_count >= 2:
            # 다른 y 위치 선택
            new_obstacle_rect.y = random.choice([y for y in [445, 470] if y != new_obstacle_rect.y])
            spawn_count = 0  # 새로운 y 위치의 생성 횟수 초기화

        if check_obstacle_spacing(new_obstacle_rect, obstacles, min_distance, max_distance):
            obstacles.append(new_obstacle_rect)
            obstacle_spawn_count[new_obstacle_rect.y] = spawn_count + 1

    # 장애물 이동 및 그리기
    for obstacle_rect in obstacles:
        obstacle_rect.x -= obstacle_speed
        pygame.draw.polygon(screen, obstacle_color, [(obstacle_rect.left, obstacle_rect.bottom),
                                                     (obstacle_rect.centerx, obstacle_rect.top),
                                                     (obstacle_rect.right, obstacle_rect.bottom)])

    # 화면을 벗어난 장애물 제거
    obstacles = [obstacle for obstacle in obstacles if obstacle.right > 0]

    # UI 그리기
    draw_ui_hearts(num_highlighted_ui)

    # 배경 스크롤
    scroll -= 5

    # 스크롤 초기화
    if abs(scroll) > bg_width:
        scroll = 0

    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and character_rect.bottom == ground_rect.top:
        character_y_speed = jump_height

    # 중력 적용
    character_y_speed += 1
    character_rect.y += character_y_speed

    # 캐릭터-지면 충돌
    if character_rect.colliderect(ground_rect):
        character_rect.bottom = ground_rect.top
        character_y_speed = 0

    # 장애물-캐릭터 충돌
    for obstacle_rect in obstacles:
        if character_rect.colliderect(obstacle_rect):
            if num_highlighted_ui > 0:
                num_highlighted_ui -= 1
                collision_occurred = True
                obstacle_rect.x -= 25
                print(f"Heart {num_highlighted_ui + 1} turned gray.")
            break  # 충돌 시 장애물을 왼쪽으로 25 단위 이동하고 루프 종료

    # 충돌 플래그 재설정 여부 확인
    if not any(character_rect.colliderect(obstacle_rect) for obstacle_rect in obstacles):
        collision_occurred = False

    # 화면 업데이트
    pygame.display.update()

pygame.quit()
sys.exit()
