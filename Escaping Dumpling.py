import pygame
import math
import sys
import random
import pygame.mixer

pygame.init()
pygame.mixer.init()

clock = pygame.time.Clock()
FPS = 60
MINI_GAME_DURATION = 20  # Duration of the mini-game in seconds
mini_game_timer = 0

#sound load
jump_sound = pygame.mixer.Sound("jump01.wav")
coin_sound = pygame.mixer.Sound("coin01.wav")
collision_sound = pygame.mixer.Sound("select.wav")
pygame.mixer.music.load("flowerbed_fields.wav")
pygame.mixer.music.play(-1)  # -1 makes the music loop indefinitely
click_sound = pygame.mixer.Sound("key01.wav")

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

# Fade-out function
def fade_out():
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    fade_surface.fill((0, 0, 0))
    for alpha in range(0, 256, 10):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)

# Fade-in function
def fade_in():
    fade_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    for alpha in range(255, 0, -10):
        fade_surface.set_alpha(alpha)
        screen.blit(fade_surface, (0, 0))
        pygame.display.flip()
        pygame.time.delay(20)

for event in pygame.event.get():
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
    elif event.type == pygame.MOUSEBUTTONDOWN:
        intro = False
        click_sound.play()  # Play the key sound


# 점수
score = 0
score_timer = 0
score_interval = 0.1 * FPS  # Increase score every 0.1 seconds

# 게임 창 생성
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Escaping Dumpling")

# Intro Screen
def intro_screen():
    intro = True
    click_blink_timer = 0
    show_click_text = True

    # Load intro background
    intro_bg = pygame.image.load("ffbg.png").convert()
    intro_bg = pygame.transform.scale(intro_bg, (600, 600))
    intro_bg_width = intro_bg.get_width()

    # Starting position of the intro background
    intro_bg_scroll = 0
    
    # Load dumpling images
    dumpling_images = [
        pygame.transform.scale(pygame.image.load("dumpling3.png").convert_alpha(), (220, 220)),
        pygame.transform.scale(pygame.image.load("dumpling4.png").convert_alpha(), (220, 220))
    ]
    dumpling_rect = dumpling_images[0].get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
    dumpling_timer = pygame.time.get_ticks()
    dumpling_interval = 500  # 0.5초

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                intro = False

        # Draw the scrolling intro background
        for i in range(0, 3):  # Draw 3 copies for continuous scrolling
            screen.blit(intro_bg, (i * intro_bg_width + intro_bg_scroll, 0))

        # Update the intro background scroll
        intro_bg_scroll -= 2
        if abs(intro_bg_scroll) > intro_bg_width:
            intro_bg_scroll = 0

        # Draw "Escaping Dumpling" text at the center
        font = pygame.font.Font("PowerPixel.ttf", 60)
        text = font.render("Escaping Dumpling", True, (0, 0, 0))
        text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80 ))
        screen.blit(text, text_rect)
    

        # Check if it's time to switch dumpling images
        current_time = pygame.time.get_ticks()
        if current_time - dumpling_timer >= dumpling_interval:
            dumpling_timer = current_time
            # Switch between the two dumpling images
            dumpling_images.reverse()

        # Draw dumpling image
        screen.blit(dumpling_images[0], dumpling_rect.topleft)

        # Draw "Click to Start" button
        small_font = pygame.font.Font("PowerPixel.ttf", 25)
        button_text = small_font.render("Click to Start", True, (170, 25, 25))  # (R, G, B) for #aa1919
        button_rect = button_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 220))
        screen.blit(button_text, button_rect)

        # Draw instructions for the main game
        font = pygame.font.Font("PowerPixel.ttf", 15)
        instructions_text1 = font.render("Space Bar | Jumping in Main Game", True, (170, 100, 25))
        screen.blit(instructions_text1, (SCREEN_WIDTH // 2 - instructions_text1.get_width() // 2, SCREEN_HEIGHT - 165))
        instructions_text2 = font.render("Up & Down Key | Moving in Mini Game", True, (170, 100, 25))
        screen.blit(instructions_text2, (SCREEN_WIDTH // 2 - instructions_text2.get_width() // 2, SCREEN_HEIGHT - 145))


        # Blink the "Click to Start" button
        click_blink_timer += 1
        if click_blink_timer >= FPS:
            show_click_text = not show_click_text
            click_blink_timer = 0

        if show_click_text:
            screen.blit(button_text, button_rect)

        pygame.display.update()
        clock.tick(FPS)

# Call the intro screen function
intro_screen()

# 이미지 로드
bg = pygame.image.load("fbg.png").convert()
bg = pygame.transform.scale(bg, (600, 600))
bg_width = bg.get_width()
bg_rect = bg.get_rect()
obstacle_image = pygame.image.load("forkframe.png").convert_alpha()
obstacle_image = pygame.transform.scale(obstacle_image, (45, 45))
mini_game_heart_image = pygame.image.load("heartitem.png").convert_alpha()
mini_game_heart_image = pygame.transform.scale(mini_game_heart_image, (45, 45))
item_image = pygame.image.load("wing.png").convert_alpha()
item_image = pygame.transform.scale(item_image, (50, 50))
ground_image = pygame.image.load("ground.png").convert_alpha()
ground_image = pygame.transform.scale(ground_image, (SCREEN_WIDTH, 100))

# 게임 변수 정의
scroll = 0
tiles = math.ceil(SCREEN_WIDTH / bg_width) + 1

# Load character sprites
character_sprite1 = pygame.image.load("dumpling1.png").convert_alpha()
character_sprite1 = pygame.transform.scale(character_sprite1, (50, 50))

character_sprite2 = pygame.image.load("dumpling2.png").convert_alpha()
character_sprite2 = pygame.transform.scale(character_sprite2, (50, 50))

# Initialize current character sprite
current_character_sprite = character_sprite1
character_animation_timer = 0
character_animation_interval = 0.1 * FPS  # Switch sprite every 0.1 seconds
character_y_speed = 0
jump_height = -17

# 지면 설정
ground = pygame.Surface((SCREEN_WIDTH, 100))
ground.fill((182, 138, 73))
ground_rect = ground.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
screen.blit(ground_image, ground_rect.topleft)


# 장애물 설정
obstacle_width = 50
obstacle_height = 50
obstacle_color = (220, 20, 20)
obstacle_speed = 5

obstacles = []
obstacle_spawn_count = {}  # 각 y 위치에서의 장애물 생성 횟수를 추적

# UI 설정
num_highlighted_ui = 3

# Font for displaying UI hearts count
font = pygame.font.Font("PowerPixel.ttf", 36)

# 장애물 간격을 확인하는 함수
def check_obstacle_spacing(new_obstacle_rect, existing_obstacles, min_distance, max_distance):
    for existing_obstacle in existing_obstacles:
        if new_obstacle_rect.y == existing_obstacle.y and abs(new_obstacle_rect.x - existing_obstacle.x) < min_distance:
            return False
        elif abs(new_obstacle_rect.x - existing_obstacle.x) < max_distance:
            return False
    return True

# 게임 오버 화면 그리기
def draw_game_over():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)  # 불투명도 설정 (0: 완전 투명, 255: 완전 불투명)
    overlay.fill((0, 0, 0))  # 검정색 배경
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font("PowerPixel.ttf", 74)
    game_over_text = font.render("Game Over", True, (255, 255, 255))
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

# Mini-Game Variables
mini_game_bg = pygame.image.load("ffbg.png").convert()
mini_game_bg = pygame.transform.scale(mini_game_bg, (600, 600))
mini_game_bg_width = mini_game_bg.get_width()
mini_game_bg_rect = mini_game_bg.get_rect()

mini_game_obstacle_image = pygame.image.load("skick.png").convert_alpha()
mini_game_obstacle_image = pygame.transform.scale(mini_game_obstacle_image, (120, 350))
mini_game_obstacle_rect = mini_game_obstacle_image.get_rect()

mini_game_item_rect = pygame.Rect(0, 0, 0, 0)
mini_game_character_y_speed = 0
mini_game_obstacle_speed = 5
mini_game_item_rect = pygame.Rect(0, 0, 0, 0)  # Add this line to initialize the variable

def countdown_timer():
    font = pygame.font.Font("PowerPixel.ttf", 100)
    for i in range(3, 0, -1):
        timer_text = font.render(str(i), True, (255, 255, 255))
        screen.blit(timer_text, (SCREEN_WIDTH // 2 - timer_text.get_width() // 2, SCREEN_HEIGHT // 2 - timer_text.get_height() // 2))
        pygame.display.update()
        pygame.time.delay(1000)




# Mini-Game Loop

def run_mini_game():
    global ui_highlight_color
    global num_highlighted_ui
    global mini_game_timer
    global mini_game_obstacles
    global mini_game_obstacle_speed

    mini_game_scroll = 0
    mini_game_tiles = math.ceil(SCREEN_WIDTH / mini_game_bg_width) + 1

    mini_game_obstacle_width = 50
    mini_game_obstacle_speed = 5
    mini_game_obstacle_spacing = 100
    mini_game_obstacles = []
    
    character_rect.topleft = (200, 0)
    
    
    # Load character sprites
    character_sprite1 = pygame.image.load("dumpling1.png").convert_alpha()
    character_sprite1 = pygame.transform.scale(character_sprite1, (50, 50))

    character_sprite2 = pygame.image.load("dumpling2.png").convert_alpha()
    character_sprite2 = pygame.transform.scale(character_sprite2, (50, 50))

    # Initialize current character sprite
    current_character_sprite = character_sprite1
    character_animation_timer = 0
    character_animation_interval = 0.2 * FPS  # Switch sprite every 0.5 seconds
    character_y_speed = 0

    character_animation_timer += 1
    if character_animation_timer >= character_animation_interval:
        character_animation_timer = 0
        # Switch between the two sprites
        if current_character_sprite == character_sprite1:
            current_character_sprite = character_sprite2
        else:
            current_character_sprite = character_sprite1

    mini_game_item_radius = 25
    mini_game_item_rect = pygame.Rect(SCREEN_WIDTH, random.randint(50, SCREEN_HEIGHT - 50), mini_game_item_radius * 2, mini_game_item_radius * 2)
    
    mini_game_run = True
    item_spawn_timer = 0
    item_spawn_interval = random.randint(5, 10) * FPS  # 5 to 10 seconds

    while mini_game_run and mini_game_timer < MINI_GAME_DURATION * FPS:
        clock.tick(FPS)
        mini_game_timer += 1

        # 스크롤링 배경 그리기
        for i in range(0, mini_game_tiles):
            screen.blit(mini_game_bg, (i * mini_game_bg_width + mini_game_scroll, 0))

        # Display the number of UI hearts in the top left corner
        font = pygame.font.Font("PowerPixel.ttf", 20)
        ui_text = font.render(f'Hearts: {num_highlighted_ui}', True, (0, 0, 0))
        screen.blit(ui_text, (20, 20))
        
        # 시간 감소
        remaining_time = max(0, int((MINI_GAME_DURATION * FPS - mini_game_timer) / FPS))
        time_text = font.render(f'Time: {remaining_time}s', True, (0, 0, 0))
        screen.blit(time_text, (SCREEN_WIDTH - 20 - score_text.get_width(), 20))

        # 장애물 생성
        if random.randint(0, 100) < 5:
            new_obstacle_rect = pygame.Rect(SCREEN_WIDTH, random.randint(-300, 550), mini_game_obstacle_width, random.randint(150, 400))

            # 장애물 간격 확인
            if not mini_game_obstacles or new_obstacle_rect.x - mini_game_obstacles[-1].x > mini_game_obstacle_spacing:
                mini_game_obstacles.append(new_obstacle_rect)

        # 아이템 생성 및 이동
        item_spawn_timer += 1
        if item_spawn_timer >= item_spawn_interval:
            new_item_x = SCREEN_WIDTH
            while any(
                obstacle_rect.x <= new_item_x <= obstacle_rect.x + 65
                for obstacle_rect in mini_game_obstacles
            ):
                new_item_x = random.randint(SCREEN_WIDTH, SCREEN_WIDTH + 200)
            mini_game_item_rect = pygame.Rect(
                new_item_x,
                random.randint(50, SCREEN_HEIGHT - 50),
                mini_game_item_radius * 2,
                mini_game_item_radius * 2,
            )
            item_spawn_timer = 0

        if mini_game_item_rect is not None:
            mini_game_item_rect.x -= mini_game_obstacle_speed
            screen.blit(mini_game_heart_image, mini_game_item_rect.topleft)

        # 장애물 이동 및 그리기
        for obstacle_rect in mini_game_obstacles:
            obstacle_rect.x -= mini_game_obstacle_speed
            # pygame.draw.rect(screen, obstacle_color, obstacle_rect)  # Remove this line
            screen.blit(mini_game_obstacle_image, obstacle_rect.topleft)  # Add this line


        # 캐릭터 그리기
        screen.blit(current_character_sprite, character_rect.topleft)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            character_y_speed = -10
        elif keys[pygame.K_DOWN]:
            character_y_speed = 10
        else:
            character_y_speed = 0

        # 중력 적용
        character_y_speed += 5
        character_rect.y += character_y_speed
        
        # 화면 업데이트
        pygame.display.update()

        # 배경 스크롤
        mini_game_scroll -= 5

        # 스크롤 초기화
        if abs(mini_game_scroll) > mini_game_bg_width:
            mini_game_scroll = 0

        # 장애물 충돌 검사
        for obstacle_rect in mini_game_obstacles:
            if character_rect.colliderect(obstacle_rect):
                print("Collision with obstacle in mini-game! Game Over!")
                collision_sound.play()
                mini_game_run = False
                break
            
        # 위, 아래 벽 충돌 검사
        if character_rect.top <= -10 or character_rect.bottom >= SCREEN_HEIGHT + 10:
            print("Character hit the top or bottom wall in mini-game! Game Over!")
            collision_sound.play()
            mini_game_run = False

        # 아이템-캐릭터 충돌
        if  character_rect.colliderect(mini_game_item_rect):
            print("Character collected the item!")
            coin_sound.play()
            mini_game_item_rect.x = SCREEN_WIDTH  # Reset the item position
            num_highlighted_ui += 1
            print(num_highlighted_ui)
            
    # Reset variables for the next mini-game
    mini_game_obstacles = []
    mini_game_timer = 0

    return







# Original Game Loop
run = True

score = 0
score_timer = 0
score_interval = 0.25 * FPS  # Increase score every 0.25 seconds

speed_increase_interval = 100  # 100의 배수마다 속도 증가
speed_increase_amount = 0.1 # 속도 증가량

collision_occurred = False  # 충돌 여부를 추적하는 플래그
game_over = False  # 게임 오버 여부 플래그

collision_occurred = False  # 충돌 여부를 추적하는 플래그
game_over = False  # 게임 오버 여부 플래그

item_width = 30
item_height = 30
item_color = (255, 255, 255)
item_speed = -10
item_spawn_timer = 0
item_spawn_interval = 10 * FPS  # 20초

# 캐릭터 이미지 로드
character_sprite = pygame.image.load("dumpling1.png").convert_alpha()
character_sprite = pygame.transform.scale(character_sprite, (50, 50))
character_rect = character_sprite.get_rect(center=(200, 500))
character_y_speed = 0

# Index to keep track of the state of hearts
original_game_heart_index = num_highlighted_ui - 1

# Let's Get Hearts! 텍스트를 나타내고 페이드인
def show_lets_get_hearts_text():
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    font = pygame.font.Font("PowerPixel.ttf", 40)
    text = font.render("Let's Get Hearts!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

    pygame.display.update()
    pygame.time.delay(1500)  # 3초 동안 화면 정지
    fade_in()  # 페이드인
    
def show_speed_up_text():
    font = pygame.font.Font("PowerPixel.ttf", 40)
    text = font.render("Speed Up!", True, (255, 255, 255))
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)
    

mini_game_triggered = False
mini_game_timer = 0  # Add this line to reset the timer
mini_game_obstacles = []  # Add this line to clear the obstacles



# Fade in from black at the beginning
fade_in()

while run:

    clock.tick(FPS)

    # 스크롤링 배경 그리기
    for i in range(0, tiles):
        screen.blit(bg, (i * bg_width + scroll, 0))

    # 게임 오버 시 화면 그리기
    if game_over:
        draw_game_over()
        
        font = pygame.font.Font("PowerPixel.ttf", 36)
        score_text = font.render(f'Score: {score}', True, (255, 255, 255))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))

        pygame.display.update()

        # 재시작을 위한 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Reset the game state here if needed
                pass

    # 게임 오버가 아니면 게임 진행
    elif not game_over:
        
        # Update the character sprite based on a timer
        character_animation_timer += 1
        if character_animation_timer >= character_animation_interval:
            character_animation_timer = 0
            # Switch between the two sprites
            if current_character_sprite == character_sprite1:
                current_character_sprite = character_sprite2
            else:
                current_character_sprite = character_sprite1

        # ... (Your existing code)

        # Draw the current character sprite
        screen.blit(current_character_sprite, character_rect.topleft)

        # 지면 그리기
        screen.blit(ground_image, ground_rect.topleft)


        # 장애물 생성
        if random.randint(0, 100) < 2 and not collision_occurred:
            new_obstacle_rect = pygame.Rect(SCREEN_WIDTH, random.choice([445, 470]), obstacle_width, obstacle_height)

            # 장애물 간격 확인
            if new_obstacle_rect.y == 445:
                min_distance = 90
                max_distance = 150
            else:
                min_distance = 90
                max_distance = 150

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
            screen.blit(obstacle_image, obstacle_rect.topleft)

        # 아이템 생성 및 이동
        item_spawn_timer += 1
        if item_spawn_timer >= item_spawn_interval:
            item_rect = pygame.Rect(
                SCREEN_WIDTH, 
                random.randint(300, 500),  # y 좌표를 300에서 500 사이로 설정
                item_width, 
                item_height
            )
            item_spawn_timer = 0

        if 'item_rect' in locals():
            item_rect.x += item_speed
            item_rect.y += item_speed/5
            screen.blit(item_image, item_rect.topleft)

            # 아이템이 화면을 벗어나면 다시 생성
            if item_rect.right < 0:
                del item_rect
            if 'item_rect' in locals():  # del로 인해 item_rect가 삭제된 경우를 확인
                if item_rect.y > 500:
                    item_rect.y -= 2
                if item_rect.y < 300:
                    item_rect.y += 2

        # 화면을 벗어난 장애물 제거
        obstacles = [obstacle for obstacle in obstacles if obstacle.right > 0]
        
        # Display the number of UI hearts in the top left corner
        ui_text = font.render(f'Hearts: {num_highlighted_ui}', True, (0, 0, 0))
        screen.blit(ui_text, (20, 20))

        # 배경 스크롤
        scroll -= 5

        # 스크롤 초기화
        if abs(scroll) > bg_width:
            scroll = 0

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and character_rect.bottom == ground_rect.top:
                    character_y_speed = jump_height
                    jump_sound.play()  # Play the jump sound

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

        # obstacle-character collision
        for obstacle_rect in obstacles:
            if character_rect.colliderect(obstacle_rect):
                if not collision_occurred:  # 충돌이 처음 감지된 경우에만 처리
                    collision_occurred = True
                    if num_highlighted_ui > 1:
                        num_highlighted_ui -= 1
                        print(f"Heart {num_highlighted_ui + 1} turned gray.") 
                        collision_sound.play()
                    else:
                        print("All hearts turned gray. Game Over!")
                        collision_sound.play()
                        game_over = True
                break 

        # 아이템-캐릭터 충돌
        if 'item_rect' in locals() and character_rect.colliderect(item_rect):
            coin_sound.play()
            print("Character collected the item!")
            del item_rect  # 아이템 제거
            mini_game_triggered = True  # 미니 게임 시작 플래그 설정

        # 충돌 플래그 재설정 여부 확인
        if not any(character_rect.colliderect(obstacle_rect) for obstacle_rect in obstacles):
            collision_occurred = False
            # If there are hearts to change, change the color of the next red heart to gray
            if original_game_heart_index >= 0 and num_highlighted_ui > 1:
                ui_highlight_color = (169, 169, 169)
                original_game_heart_index -= 1
                
        # 미니 게임 시작
        if mini_game_triggered:
            fade_out()  # Fade out before entering the mini-game
            show_lets_get_hearts_text()  # Let's Get Hearts! 텍스트 표시
            run_mini_game()
            fade_in()  # Fade in when returning from the mini-game
            mini_game_triggered = False  # 미니 게임이 종료되면 플래그 재설정
            
        # 점수 갱신
        score_timer += 1
        if score_timer >= score_interval:
            score += 1
            score_timer = 0
            
        # 점수가 100의 배수일 때 속도 증가
        if score % speed_increase_interval == 0 and score > 0:
            obstacle_speed += speed_increase_amount
            item_speed += speed_increase_amount
            mini_game_obstacle_speed += speed_increase_amount
            show_speed_up_text()
            

            
    
    #점수 표시
    font = pygame.font.Font("PowerPixel.ttf", 20)
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (SCREEN_WIDTH - 20 - score_text.get_width(), 20))

    # 화면 업데이트
    pygame.display.update()
    

pygame.quit()
sys.exit()
pygame.quit()
sys.exit()
