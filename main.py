import pygame
import sys
import random

pygame.init()

white = (255, 255, 255)
black = (0, 0, 0)

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Jack Runner")

bg = pygame.image.load("Images/bg.jpeg")
bg = pygame.transform.scale(bg, (800, 600))

rock_image = pygame.image.load("Images/rock.png")

button = pygame.image.load("Images/Button.png")
button = pygame.transform.scale(button, (200, 60))

run_images = [
    pygame.image.load("Images/character.png"),
    pygame.image.load("Images/character1.png"),
    pygame.image.load("Images/character2.png"),
    pygame.image.load("Images/character3.png"),
]

character_width, character_height = run_images[0].get_size()

character_x = 100
character_y = 370
y_velocity = 0
gravity = 0.3
is_jumping = False
ground_char = 510
char_speed = 5
bg_offset = 0
score = 0
current_frame = 0
frame_delay = 8
frame_counter = 0
game_state = "playing"

obstacles = []

class Obstacle:
    def __init__(self, x, y, width, height, passed=False):
        self.rect = pygame.Rect(x, y, width, height)
        self.passed = passed

clock = pygame.time.Clock()

obstacle_timer = 0
obstacle_delay = 120

def create_obstacle():
    x_pos = random.randint(1000, 1200)
    y_pos = random.randint(440, 450)
    width = random.randint(80, 150)
    height = random.randint(60, 120)
    return Obstacle(x_pos, y_pos, width, height)

def reset_game():
    global character_x, character_y, y_velocity, is_jumping, bg_offset, score, current_frame, frame_counter, obstacles, char_speed
    character_x = 100
    character_y = 370
    y_velocity = 0
    is_jumping = False
    bg_offset = 0
    score = 0
    current_frame = 0
    frame_counter = 0
    obstacles.clear()
    char_speed = 5

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if game_state == "game_over" and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if 300 <= mouse_x <= 500 and 250 <= mouse_y <= 310:
                reset_game()
                game_state = "playing"

    if game_state == "playing":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            frame_counter += 1
            if frame_counter >= frame_delay:
                current_frame = (current_frame + 1) % len(run_images)
                frame_counter = 0

        if keys[pygame.K_LEFT]:
            character_x -= char_speed
            bg_offset += char_speed
        if keys[pygame.K_RIGHT]:
            character_x += char_speed
            bg_offset -= char_speed
        else:
            frame_counter = 0

        bg_offset = bg_offset % bg.get_width()

        if not is_jumping and keys[pygame.K_SPACE]:
            y_velocity = -10
            is_jumping = True

        y_velocity += gravity
        character_y += y_velocity

        if character_y >= ground_char - character_height:
            character_y = ground_char - character_height
            y_velocity = 0
            is_jumping = False

        hitbox_width = int(character_width * 0.8)
        hitbox_height = int(character_height * 0.8)
        char_rect = pygame.Rect(character_x + (character_width - hitbox_width) // 2,
                                character_y + (character_height - hitbox_height) // 2,
                                hitbox_width, hitbox_height)

        for obstacle in obstacles[:]:
            obstacle.rect.x -= char_speed
            if obstacle.rect.x + obstacle.rect.width < 0:
                obstacles.remove(obstacle)

            if char_rect.colliderect(obstacle.rect):
                game_state = "game_over"

            if obstacle.rect.x + obstacle.rect.width < character_x and not obstacle.passed:
                score += 1
                obstacle.passed = True

        obstacle_timer += 1
        if obstacle_timer > obstacle_delay:
            obstacles.append(create_obstacle())
            obstacle_timer = 0

        screen.blit(bg, (bg_offset, 0))
        screen.blit(bg, (bg_offset - bg.get_width(), 0))

        for obstacle in obstacles:
            rock_resized = pygame.transform.scale(rock_image, (obstacle.rect.width, obstacle.rect.height))
            screen.blit(rock_resized, obstacle.rect.topleft)

        if score == 5:
            char_speed = 7
        if score == 10:
            char_speed = 9
        if score == 15:
            char_speed = 11
        if score == 20:
            char_speed = 13
        if score == 25:
            char_speed = 15
        if score == 30:
            char_speed = 17
        if score == 40:
            char_speed = 19

        screen.blit(run_images[current_frame], (character_x, character_y))

        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, white)
        screen.blit(score_text, (10, 10))

    elif game_state == "game_over":
        font2 = pygame.font.Font(None, 90)
        game_over_text = font2.render("GAME OVER", True, (255, 0, 0))
        screen.blit(game_over_text, (210, 150))
        screen.blit(button, (300, 250))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
