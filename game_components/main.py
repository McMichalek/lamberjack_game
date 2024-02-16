import pygame
import random

pygame.init()
pygame.font.init()

screen_width = 300
screen_height = 600
space_size = 50
score = 0

player_x = screen_width / 2 - space_size * 2
player_y = screen_height - space_size * 2

screen = pygame.display.set_mode((screen_width, screen_height))

grass = pygame.Rect(0, screen_height - space_size, screen_width, space_size)
log = pygame.Rect(screen_width / 2 - space_size / 2, 0, space_size, screen_height - space_size)
player = pygame.Rect(player_x, player_y, space_size, space_size)

branches = []
for i in range(screen_height // space_size - 1):
    side = random.choice(['left', 'right', 'none'])
    y = (i * space_size) - space_size / 2
    branches.append((side, y))


def move_branches():
    for i in range(len(branches)):
        side, y = branches[i]
        branches[i] = (side, y + space_size)

    new_branch_side = random.choice(['left', 'right', 'none'])
    if new_branch_side != 'none':
        branches.insert(0, (new_branch_side, space_size / 2))
    else:
        pass

    while branches and branches[-1][1] >= screen_height - space_size:
        branches.pop()


def check_collision():
    player_side = 'left' if player_x < screen_width / 2 else 'right'

    for side, y in branches:
        if side == player_side and y == player_y + space_size / 2:
            return True
    return False


game_active = True
run = True
while run:

    screen.fill((102, 178, 255))

    pygame.draw.rect(screen, (0, 255, 0), grass)
    pygame.draw.rect(screen, (153, 76, 0), log)
    pygame.draw.circle(screen, (255, 0, 0), (player_x + space_size / 2, player_y + space_size / 2), space_size / 2)

    for side, y in branches:
        if side == "left":
            branch = pygame.Rect(screen_width / 2 - space_size / 2 - space_size, y, space_size, 10)
            pygame.draw.rect(screen, (153, 76, 0), branch)
        elif side == "right":
            branch = pygame.Rect(screen_width / 2 + space_size / 2, y, space_size, 10)
            pygame.draw.rect(screen, (153, 76, 0), branch)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN and game_active == True:
            if event.key == pygame.K_a:
                player_x = screen_width / 2 - space_size * 2
                move_branches()
            elif event.key == pygame.K_d:
                player_x = screen_width / 2 + space_size
                move_branches()
            if check_collision():
                game_active = False
            else:
                score += 1

    if not game_active:
        game_font = pygame.font.SysFont('Arial', space_size, bold=True)
        game_over_text = game_font.render('Game Over', True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(screen_width/2, screen_height / 2))
        screen.blit(game_over_text, text_rect)

    score_font = pygame.font.SysFont('Arial', 24, bold=True)
    score_text = score_font.render(f'Score: {score}', True, (255, 255, 255))
    score_rect = score_text.get_rect(topright=(screen_width - 10, 10))
    screen.blit(score_text, score_rect)

    pygame.display.update()

pygame.quit()
