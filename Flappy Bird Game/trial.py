import random
import pygame
import sys
from pygame.locals import *

# Game Constants
FPS = 51
WIDTH, HEIGHT = 200, 400
GROUNDY = HEIGHT * 0.8

# Initialize Pygame
pygame.init()
FPSCLOCK = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird by Mr. NIRVAAN')

# Load Assets
GAME_SPRITES = {}
PLAYER = 'Gallery/Flappy Bird BIRD.png'
BACKGROUND = 'Gallery/Flappy Bird BACKGROUND.jpg'
PIPE = 'Gallery/Flappy Bird PIPE.png'
MESSAGE = 'Gallery/Flappy Bird MESSAGE.png'
BASE = 'Gallery/Flappy Bird BASE.png'

GAME_SPRITES['message'] = pygame.image.load(MESSAGE).convert_alpha()
GAME_SPRITES['base'] = pygame.image.load(BASE).convert_alpha()
GAME_SPRITES['pipe'] = (
    pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
    pygame.image.load(PIPE).convert_alpha()
)
GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()

# High Score
high_score = 0


def welcome_screen():
    """Display the welcome screen with high score."""
    global high_score

    playerx = WIDTH // 5
    messagex = (WIDTH - GAME_SPRITES['message'].get_width()) // 2
    messagey = int(HEIGHT * 0.13)

    while True:
        screen.blit(GAME_SPRITES['background'], (0, -30))
        screen.blit(GAME_SPRITES['player'], (playerx, 150))
        screen.blit(GAME_SPRITES['message'], (messagex, messagey))
        screen.blit(GAME_SPRITES['base'], (0, GROUNDY))

        # Display High Score
        font = pygame.font.Font(None, 32)
        label_surface = font.render("High Score:", True, (255, 255, 255))  # White text
        score_surface = font.render(str(high_score), True, (0, 0, 0))  # Black text

        screen.blit(label_surface, (WIDTH // 2 - 49, 15))
        screen.blit(score_surface, (WIDTH // 2 + 75, 17))
        pygame.display.update()
        FPSCLOCK.tick(FPS)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key in [K_ESCAPE, K_q]):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and event.key in [K_SPACE, K_UP] or event.type == MOUSEBUTTONDOWN:
                return


def display_score(screen, score):
    """Render and display only the score on the screen (not high score)."""
    font = pygame.font.Font(None, 40)
    label_surface = font.render("Score:", True, (255, 255, 255))  # White text
    score_surface = font.render(str(score), True, (0, 0, 0))  # Black text

    screen.blit(label_surface, (WIDTH // 2 - 50, 15))
    screen.blit(score_surface, (WIDTH // 2 + 40, 17))


def main_game():
    """Main game loop."""
    global high_score  

    score = 0
    playerx = WIDTH // 5
    playery = HEIGHT // 2

    newpipe1 = get_random_pipe()
    newpipe2 = get_random_pipe()

    upper_pipes = [{'x': WIDTH + 200, 'y': newpipe1[0]['y']},
                   {'x': WIDTH + 200 + (WIDTH // 2), 'y': newpipe2[0]['y']}]

    lower_pipes = [{'x': WIDTH + 200, 'y': newpipe1[1]['y']},
                   {'x': WIDTH + 200 + (WIDTH // 2), 'y': newpipe2[1]['y']}]

    pipeVelX = -1.6
    playerVelY = -2
    playerAccY = 0.157
    playerFlapAccV = -3
    playerFlapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key in [K_ESCAPE, K_q]):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key in [K_SPACE, K_UP] or event.type == MOUSEBUTTONDOWN:
                if playery > 0:
                    playerVelY = playerFlapAccV
                    playerFlapped = True

        if is_collide(playerx, playery, upper_pipes, lower_pipes):
            pygame.time.wait(400)
            if score > high_score:
                high_score = score  
            return

        playerMidPos = playerx + GAME_SPRITES['player'].get_width() // 2
        for pipe in upper_pipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width() // 2
            if playerMidPos > pipeMidPos and not pipe.get('passed', False):
                score += 1
                print(f"Your score is {score}")
                pipe['passed'] = True

        if playerVelY < 10 and not playerFlapped:
            playerVelY += playerAccY
        if playerFlapped:
            playerFlapped = False

        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY, GROUNDY - playery - playerHeight)

        for upperPipe, lowerPipe in zip(upper_pipes, lower_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if upper_pipes[-1]['x'] < WIDTH // 2:
            newpipe = get_random_pipe()
            upper_pipes.append(newpipe[0])
            lower_pipes.append(newpipe[1])

        if len(upper_pipes) > 0 and upper_pipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        screen.blit(GAME_SPRITES['background'], (0, -80))
        for upperPipe, lowerPipe in zip(upper_pipes, lower_pipes):
            screen.blit(GAME_SPRITES['pipe'][0], (upperPipe['x'], upperPipe['y']))
            screen.blit(GAME_SPRITES['pipe'][1], (lowerPipe['x'], lowerPipe['y']))

        screen.blit(GAME_SPRITES['base'], (0, GROUNDY))
        screen.blit(GAME_SPRITES['player'], (playerx, playery))

        display_score(screen, score)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def is_collide(playerx, playery, upper_pipes, lower_pipes):
    """Check for collisions with pipes or ground."""
    playerHeight = GAME_SPRITES['player'].get_height()
    playerWidth = GAME_SPRITES['player'].get_width()

    hitbox_shrink_x = playerWidth // 4  
    hitbox_shrink_y = playerHeight // 6  

    player_hitbox = pygame.Rect(
        playerx + hitbox_shrink_x,
        playery + hitbox_shrink_y,
        playerWidth - 2 * hitbox_shrink_x,
        playerHeight - 2 * hitbox_shrink_y
    )

    if playery + playerHeight >= GROUNDY:
        return True

    for pipe in upper_pipes + lower_pipes:
        pipe_rect = pygame.Rect(
            pipe['x'], pipe['y'],
            GAME_SPRITES['pipe'][0].get_width(),
            GAME_SPRITES['pipe'][0].get_height()
        )

        if player_hitbox.colliderect(pipe_rect):
            return True

    return False


def get_random_pipe():
    """Generate a new set of pipes."""
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = HEIGHT // 3
    y2 = offset + random.randrange(0, int(HEIGHT - GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipeX = WIDTH + 10
    y1 = pipeHeight - y2 + offset

    return [{'x': pipeX, 'y': -y1}, {'x': pipeX, 'y': y2}]


if __name__ == "__main__":
    while True:
        welcome_screen()
        main_game()
