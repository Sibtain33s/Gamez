import pygame
import sys
import random
import time

pygame.init()

# Screen setup
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Menu")
font = pygame.font.SysFont('arial', 32)
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 120, 215)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)

# Menu
menu_items = ["Flappy Bird", "Snake and Ladder", "Space Invaders"]
selected_index = 0

# Pretty Prompts
prompts = {
    10: "🎉 Great Job! You've reached 10 points!",
    20: "🌟 Incredible! 20 points already! You're unstoppable!"
}

def draw_menu():
    screen.fill(BLACK)
    title = font.render("Select a Game", True, WHITE)
    screen.blit(title, (WIDTH//2 - title.get_width()//2, 100))
    for i, item in enumerate(menu_items):
        color = BLUE if i == selected_index else WHITE
        text = font.render(item, True, color)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, 200 + i*50))
    pygame.display.update()

def flappy_bird():
    bird_img = pygame.Surface((34, 24))
    bird_img.fill(YELLOW)
    pipe_surface = pygame.Surface((70, HEIGHT))
    pipe_surface.fill(GREEN)
    bird = bird_img.get_rect(center=(100, HEIGHT // 2))
    gravity = 0.5
    bird_movement = 0
    pipe_list = []
    pipe_heights = [300, 400, 250]
    score = 0
    shown_prompts = set()
    game_active = True
    pygame.time.set_timer(pygame.USEREVENT, 1200)

    def draw_pipes(pipes):
        for pipe in pipes:
            if pipe.bottom >= HEIGHT:
                screen.blit(pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(pipe_surface, False, True)
                screen.blit(flip_pipe, pipe)

    def check_collision(pipes):
        for pipe in pipes:
            if bird.colliderect(pipe):
                return False
        if bird.top <= -100 or bird.bottom >= HEIGHT:
            return False
        return True

    running = True
    while running:
        screen.fill((135, 206, 235))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if game_active:
                        bird_movement = -10
                    else:
                        game_active = True
                        pipe_list.clear()
                        bird.center = (100, HEIGHT // 2)
                        bird_movement = 0
                        score = 0
                        shown_prompts.clear()
            if event.type == pygame.USEREVENT:
                pipe_height = random.choice(pipe_heights)
                bottom = pipe_surface.get_rect(midtop=(WIDTH + 100, pipe_height))
                top = pipe_surface.get_rect(midbottom=(WIDTH + 100, pipe_height - 150))
                pipe_list.extend([bottom, top])

        if game_active:
            bird_movement += gravity
            bird.centery += int(bird_movement)
            pipe_list = [pipe.move(-5, 0) for pipe in pipe_list]
            game_active = check_collision(pipe_list)
            screen.blit(bird_img, bird)
            draw_pipes(pipe_list)
            score_text = font.render(f"Score: {int(score)}", True, WHITE)
            screen.blit(score_text, (20, 20))
            for pipe in pipe_list:
                if pipe.centerx == bird.centerx:
                    score += 0.5

            if int(score) in prompts and int(score) not in shown_prompts:
                prompt_text = font.render(prompts[int(score)], True, RED)
                screen.blit(prompt_text, (WIDTH//2 - prompt_text.get_width()//2, 100))
                shown_prompts.add(int(score))
        else:
            over = font.render("Game Over! Press SPACE", True, RED)
            screen.blit(over, (WIDTH//2 - over.get_width()//2, HEIGHT//2))

        pygame.display.update()
        clock.tick(60)

def snake_and_ladder():
    player_pos = 1
    dice_roll = 0
    board = [i for i in range(1, 101)]
    snakes = {16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78}
    ladders = {1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100}
    dice_font = pygame.font.SysFont('arial', 48)

    def draw_board():
        screen.fill(WHITE)
        size = 60
        for i in range(10):
            for j in range(10):
                num = board[i * 10 + j if i % 2 == 0 else (i + 1) * 10 - 1 - j]
                rect = pygame.Rect(j * size, i * size, size, size)
                pygame.draw.rect(screen, BLACK, rect, 1)
                txt = font.render(str(num), True, BLACK)
                screen.blit(txt, (rect.x + 5, rect.y + 5))

        px = ((player_pos - 1) % 10) * size
        py = ((player_pos - 1) // 10) * size
        if ((player_pos - 1) // 10) % 2 == 1:
            px = WIDTH - size - px
        pygame.draw.circle(screen, RED, (px + size//2, HEIGHT - py - size//2), 20)
        pygame.display.update()

    running = True
    while running:
        draw_board()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_pos < 100:
                    dice_roll = random.randint(1, 6)
                    player_pos += dice_roll
                    player_pos = snakes.get(player_pos, player_pos)
                    player_pos = ladders.get(player_pos, player_pos)
                elif event.key == pygame.K_ESCAPE:
                    return

        pygame.display.set_caption(f"Snake and Ladder - Position: {player_pos}")
        clock.tick(5)


def space_invaders():
    x, y = WIDTH//2, HEIGHT - 60
    bullets = []
    aliens = [pygame.Rect(random.randint(0, WIDTH-40), random.randint(0, 200), 40, 40) for _ in range(5)]
    bullet_speed = -5

    running = True
    while running:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(pygame.Rect(x + 15, y, 5, 10))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: x -= 5
        if keys[pygame.K_RIGHT]: x += 5
        x = max(0, min(x, WIDTH - 40))

        player = pygame.Rect(x, y, 40, 40)
        pygame.draw.rect(screen, BLUE, player)

        for bullet in bullets[:]:
            bullet.y += bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)
            pygame.draw.rect(screen, WHITE, bullet)
            for alien in aliens[:]:
                if bullet.colliderect(alien):
                    bullets.remove(bullet)
                    aliens.remove(alien)
                    break

        for alien in aliens:
            pygame.draw.rect(screen, GREEN, alien)

        if not aliens:
            win = font.render("All aliens defeated! Press ESC", True, GREEN)
            screen.blit(win, (WIDTH//2 - win.get_width()//2, HEIGHT//2))

        pygame.display.update()
        clock.tick(60)

        if pygame.key.get_pressed()[pygame.K_ESCAPE]:
            break

# --- Main Menu Loop ---
running = True
while running:
    draw_menu()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                selected_index = (selected_index - 1) % len(menu_items)
            elif event.key == pygame.K_DOWN:
                selected_index = (selected_index + 1) % len(menu_items)
            elif event.key == pygame.K_RETURN:
                if selected_index == 0:
                    flappy_bird()
                elif selected_index == 1:
                    snake_and_ladder()
                elif selected_index == 2:
                    space_invaders()

pygame.quit()
sys.exit()
