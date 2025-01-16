import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Bird settings
BIRD_WIDTH = 40
BIRD_HEIGHT = 40
BIRD_X = 50
BIRD_Y = 300
BIRD_GRAVITY = 0.6
BIRD_JUMP = -8   # Adjusted jump height

# Pipe settings
PIPE_WIDTH = 70
PIPE_HEIGHT = 400
PIPE_GAP = 150
PIPE_SPEED = 3

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_image = pygame.image.load("Flappy/flappy_bird.png")
bird_image = pygame.transform.scale(bird_image, (BIRD_WIDTH, BIRD_HEIGHT))
background_image = pygame.image.load("Flappy/background.jpg")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Function to create pipes
def create_pipe():
    height = random.randint(150, 450)
    top_pipe = pygame.Rect(SCREEN_WIDTH, 0, PIPE_WIDTH, height)
    bottom_pipe = pygame.Rect(SCREEN_WIDTH, height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - height - PIPE_GAP)
    return top_pipe, bottom_pipe

# Main game loop
def main():
    global score, high_score
    clock = pygame.time.Clock()
    bird_y = BIRD_Y
    bird_velocity = 0
    pipes = []
    score = 0
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_velocity = BIRD_JUMP

        # Bird movement
        bird_velocity += BIRD_GRAVITY
        bird_y += bird_velocity

        # Pipe movement
        if len(pipes) == 0 or pipes[-1][0].x < SCREEN_WIDTH - 200:
            pipes.append(create_pipe())

        for pipe in pipes:
            pipe[0].x -= PIPE_SPEED
            pipe[1].x -= PIPE_SPEED

        # Remove off-screen pipes
        if pipes[0][0].x < -PIPE_WIDTH:
            pipes.pop(0)
            score += 1

        # Check for collisions
        bird_rect = pygame.Rect(BIRD_X, bird_y, BIRD_WIDTH, BIRD_HEIGHT)
        for pipe in pipes:
            if bird_rect.colliderect(pipe[0]) or bird_rect.colliderect(pipe[1]):
                running = False

        if bird_y > SCREEN_HEIGHT or bird_y < 0:
            running = False

        # Draw everything
        screen.blit(background_image, (0, 0))
        screen.blit(bird_image, (BIRD_X, bird_y))
        for pipe in pipes:
            pygame.draw.rect(screen, GREEN, pipe[0])
            pygame.draw.rect(screen, GREEN, pipe[1])

        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {score}", True, BLACK)
        screen.blit(text, (10, 10))

        pygame.display.flip()
        clock.tick(30)

    if score > high_score:
       high_score = score

    end_screen(score, high_score)

def start_screen():
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Flappy Bird", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    font = pygame.font.Font(None, 36)
    text = font.render("Press SPACE to start", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height()))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def end_screen(score, high_score):
    screen.fill(WHITE)
    font = pygame.font.Font(None, 74)
    text = font.render("Game Over", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    font = pygame.font.Font(None, 36)
    text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height()))
    text = font.render(f"High Score: {high_score}", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height() * 2))

    # Draw buttons
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + text.get_height() * 3, 200, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + text.get_height() * 4 + 10, 200, 50)
    pygame.draw.rect(screen, GREEN, restart_button)
    pygame.draw.rect(screen, RED, quit_button)
    text = font.render("Restart", True, WHITE)
    screen.blit(text, (restart_button.x + (restart_button.width - text.get_width()) // 2, restart_button.y + (restart_button.height - text.get_height()) // 2))
    text = font.render("Quit", True, WHITE)
    screen.blit(text, (quit_button.x + (quit_button.width - text.get_width()) // 2, quit_button.y + (quit_button.height - text.get_height()) // 2))

    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if restart_button.collidepoint(mouse_pos):
                    waiting = False
                    main()  # Restart the game
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    exit()

if __name__ == "__main__":
    high_score = 0
    start_screen()
    while True:
        main()
        end_screen(score, high_score)
        start_screen()
