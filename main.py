import pygame
import random
import time

from bird import Bird
from pillar import Pillar

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont('Comic Sans MS', 30)
FONT_BIG = pygame.font.SysFont('Comic Sans MS', 100)
BIRD_PATH = "./assets/frame-11.png"
BG_PATH = "./assets/goodcopybg.png"

BIRD_IMG = pygame.image.load(BIRD_PATH)
BG_IMG = pygame.image.load(BG_PATH)

SCREEN_WIDTH = BG_IMG.get_width() * 2

SCREEN = pygame.display.set_mode([SCREEN_WIDTH, BG_IMG.get_height()])

running = True
startTime = time.time()


def main():
    global running
    bird_start_x = 200
    bird_start_y = 450

    ground_y = 790

    # --------- Pillar values -------
    pillar_start_x = bird_start_x + 700
    pillar_start_y = 0
    pillar_width = 50
    pillar_height = 75
    pillar_velocity_x = 70
    pillar_gap_x = 400
    pillar_gap_y = 150

    winning_score = 10

    # Used to track FPS
    FPSCLOCK = pygame.time.Clock()
    FPS = 60

    # Creates the first pillar and bird objects
    bird = Bird(bird_start_x, bird_start_y, BIRD_IMG)

    first_pillar = Pillar(pillar_start_x, pillar_start_y,
                          pillar_width, pillar_height, pillar_gap_y, ground_y, pillar_velocity_x)

    all_pillars = [first_pillar]

    while running:
        # Game Loop, Runs for each frame

        dt = FPSCLOCK.tick(FPS)

        if not game_over(bird, all_pillars, ground_y, pillar_width):
            # Game continues running

            for event in pygame.event.get():
                event_handler(event, bird, dt)

            all_pillars = generate_pillars(all_pillars, pillar_gap_x,
                                           pillar_start_y, pillar_width, pillar_gap_y, ground_y, pillar_velocity_x)

            score = sum([1 if p.x + p.width < bird.x else 0 for p in all_pillars])

            if score >= winning_score:
                freeze(all_pillars, bird)
                render_win()
            else:
                update_positions(bird, all_pillars, dt)
                render(BG_IMG, all_pillars, bird, pillar_gap_y, ground_y, score)
                pygame.draw.rect(SCREEN, color="red",
                                rect=(bird.x, bird.y, BIRD_IMG.get_width(), BIRD_IMG.get_height()), width=1)


            pygame.display.update()

        else:
            running = False


def game_over(bird, all_pillars, ground_y, pillar_width):
    """Checks whether any losing conditions are met"""

    if bird_collided(bird, all_pillars, pillar_width):
        return True

    if bird.y + BIRD_IMG.get_height() <= ground_y:
        # Bird is above ground, still alive
        return False
    elif bird.y + BIRD_IMG.get_height() > ground_y:
        # Bird has touched ground, game over
        return True


def bird_collided(bird, all_pillars, pillar_width):
    """Checks whether bird has collided with a pipe/pillar"""

    bird_tip = bird.x + BIRD_IMG.get_width()
    bird_bottom = bird.y + BIRD_IMG.get_height() - 10
    bird_top = bird.y + 5

    next_pillar = next(
        pillar for pillar in all_pillars if bird_tip < pillar.x + pillar_width + BIRD_IMG.get_width())

    if bird_tip > next_pillar.x:
        # Within the x coordinate of nearest pillar, collision possible

        if bird_top < next_pillar.height or bird_bottom > next_pillar.y2:
            # Bird within hitbox in y axis
            return True


def generate_pillars(all_pillars, pillar_gap_x, pillar_start_y, pillar_width, pillar_gap_y, ground_y, pillar_velocity_x):
    """Creates the pillars"""

    last_pillar = all_pillars[-1]

    if last_pillar.x < SCREEN_WIDTH:
        pillar_height = random.randint(125, 450)

        new_pillar = Pillar(last_pillar.x + pillar_gap_x, pillar_start_y,
                            pillar_width, pillar_height, pillar_gap_y, ground_y, pillar_velocity_x)

        all_pillars.append(new_pillar)

    return all_pillars


def update_positions(bird, all_pillars, dt):
    """ Updates positions of the bird and pillars"""

    bird.falling(dt)
    bird.update_center_point()

    for pillar in all_pillars:
        pillar.update_position(startTime)


def event_handler(event, bird, dt):
    """ Handles events that occur in the game """

    global running
    if event.type == pygame.QUIT:
        running = False

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            bird.up(dt)

def render_win():
    """Show big white rectangle on win"""
    
    pygame.draw.rect(SCREEN, color="cyan",
                        rect=(0, 0, SCREEN.get_width(), SCREEN.get_height()))
    SCREEN.blit(FONT_BIG.render("Testerna gick igenom!", False, (255, 0, 0)), (40, 40))
    SCREEN.blit(FONT_BIG.render("Företaget är räddat!", False, (255, 0, 0)), (40, 300))
    SCREEN.blit(FONT_BIG.render("Ord 2: stora", False, (255, 0, 0)), (40, 500))

def freeze(all_pillars, bird):
    """Freeze bird and pillars"""
    for pillar in all_pillars:
        pillar.freeze()

    bird.freeze()

def render(BG_IMG, all_pillars, bird, pillar_gap_y, floor_y, score):
    """Draws items onto the SCREEN"""

    SCREEN.blit(BG_IMG, (0, 0))
    SCREEN.blit(BG_IMG,
                (BG_IMG.get_width(), 0))

    for pillar in all_pillars:
        pillar.render(SCREEN)

    bird.render(SCREEN)

    # Score
    pygame.draw.rect(SCREEN, color="white", rect=(10, 10, 70, 70), border_radius=10)
    text = FONT.render(str(score), False, (0, 0, 0))
    SCREEN.blit(text, (20, 20))


if __name__ == "__main__":
    main()
