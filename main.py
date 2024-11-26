import pygame
import sys
import Mobs
import Towers
import Toolbar
import random

# Initialisation de Pygame
pygame.init()

# Constantes
WIDTH = 1024
HEIGHT = 768
GAME_AREA_WIDTH = WIDTH - 224
FPS = 60
TICK = 30
BACKGROUND_COLOR = (64, 68, 29)
PATH = [
    (0, 100), (50, 100), (100, 100), (150, 100), (200, 100),
    (200, 150), (200, 200), (250, 200), (300, 200), (350, 200),
    (400, 200), (400, 250), (400, 300), (450, 300), (500, 300),
    (550, 300), (550, 350), (550, 400), (600, 400), (650, 400),
    (700, 400), (750, 400), (800, 400)
]


# vague
WAVE = 0
tab_timer = []
change_wave = True


def init_window():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Open TDD")
    return window

def create_wave(wave_nb):
    nb_max_mobs = wave_nb // 2 + 1
    mob_wave = []
    for i in range(nb_max_mobs):
        if mob_wave==[]: mob_wave.append(("Soldier",0.1))
        if wave_nb>10 and random()>=0.7:
            mob_wave.append(("Tank",random.uniform()))
        if wave_nb>7 and random()>0.6:
            mob_wave.append(("Sergant",random.uniform()))
        if wave_nb>5 and random()>0.4:
            mob_wave.append(("Capitain",random.uniform()))
        else:
            mob_wave.append(("Soldier",random.uniform()))

    return mob_wave

def spawn_mobs(mob_wave,current_wave_time,mobs):

    pass


def handle_events(mobs, toolbar, placing_tower, phantom_tower, towers):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, placing_tower, phantom_tower

        keys = pygame.key.get_pressed()
        if mobs and (event.type == pygame.KEYDOWN and keys[pygame.K_DOWN]):
            mobs[0].speed -= 1
        elif mobs and (event.type == pygame.KEYDOWN and keys[pygame.K_UP]):
            mobs[0].speed += 1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if toolbar.is_button_clicked(event.pos):
                placing_tower = True
                phantom_tower = Towers.Tower(x, y, 25, 100, (0, 0, 255))
            elif placing_tower:
                new_tower = Towers.Tower(x, y, 25, 100, (0, 0, 255))
                if new_tower.is_within_bounds(WIDTH, GAME_AREA_WIDTH):
                    towers.append(new_tower)
                placing_tower = False
                phantom_tower = None
        elif event.type == pygame.MOUSEMOTION and placing_tower:
            x, y = event.pos
            phantom_tower = Towers.Tower(x, y, 25, 100, (0, 0, 255))
    '''
    new = False
    
    seconds=time_game()[1]
    if seconds > 0:
        change_wave = True
    if change_wave == True and seconds == 0:  # pour l'instant on va dire qu'on change de vague toutes les minutes
        VAGUE += 1
        change_wave = False
        for t in range(nb_max_mobs + 1):
            tab_timer.append(randint(0, 59))
            new = True
    # tri de la liste:
    if new:
        for i in range(len(tab_timer)):
            for j in range(i, len(tab_timer)):
                tab_timer[i], tab_timer[j] = min(tab_timer[i], tab_timer[j]), max(tab_timer[i], tab_timer[j])
        new = False'''


    return True, placing_tower, phantom_tower


def draw_elements(window, mobs, towers, toolbar, phantom_tower, hp, placing_tower):
    window.fill(BACKGROUND_COLOR)

    if placing_tower and phantom_tower:
        phantom_tower.draw_phantom(window)

    elapsed_time = pygame.time.get_ticks() // 1000
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer = f'{minutes:02}:{seconds:02}'
    toolbar.draw(window, hp=hp, money=500, timer=timer, wave=1)

    for mob in mobs:
        if mob.active:
            reached_end = mob.move()
            if mob.rect.x < GAME_AREA_WIDTH:
                mob.draw(window)
                if reached_end:
                    hp = mob.attack(hp)
            else:
                mob.active = False
    mobs[:] = [mob for mob in mobs if mob.active]

    for tower in towers:
        tower.draw(window)

    toolbar.draw(window, hp=hp, money=500, timer=timer, wave=1)

    return hp


def main():
    window = init_window()
    clock = pygame.time.Clock()
    tick_clock = pygame.time.Clock()
    wave=1
    mobs=spawn_mobs(0,0,0)
    waves = create_wave(WAVE)
    towers = []
    toolbar = Toolbar.Toolbar(WIDTH, HEIGHT)
    placing_tower = False
    phantom_tower = None

    hp = 100
    running = True

    while running:
        running, placing_tower, phantom_tower = handle_events(mobs, toolbar, placing_tower, phantom_tower, towers)
        hp = draw_elements(window, mobs, towers, toolbar, phantom_tower, hp, placing_tower)
        tick_clock.tick(TICK)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
