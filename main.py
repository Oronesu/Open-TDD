import pygame
import sys
import random
import Mobs
import Towers
import Toolbar

# Initialisation de Pygame
pygame.init()

# Constantes
WIDTH = 1024
HEIGHT = 768
GAME_AREA_WIDTH = WIDTH - 224
FPS = 60
TICK = 30
MONEY = 500
BACKGROUND_COLOR = (64, 68, 29)
PATH = [
    (0, 100), (50, 100), (100, 100), (150, 100), (200, 100),
    (200, 150), (200, 200), (250, 200), (300, 200), (350, 200),
    (400, 200), (400, 250), (400, 300), (450, 300), (500, 300),
    (550, 300), (550, 350), (550, 400), (600, 400), (650, 400),
    (700, 400), (750, 400), (800, 400)
]

MOB_TYPES = ['Soldier', 'Captain', 'Sergeant', 'Tank', 'Boss']

def init_window():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Open TDD")
    return window

def create_wave(wave_number):
    number_of_mobs = 5 * wave_number
    wave_mobs = []
    for _ in range(number_of_mobs):
        mob_type = random.choices(MOB_TYPES, weights=[1, 1, 1, wave_number, wave_number])[0]
        wave_mobs.append(Mobs.Mob(PATH, mob_type))
    return wave_mobs

def handle_events(mobs, toolbar, placing_tower, phantom_tower, towers,):
    selected_tower = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, placing_tower, phantom_tower

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            selected_tower = toolbar.is_button_clicked(event.pos)
            if selected_tower:
                placing_tower = True
                phantom_tower = Towers.Tower(x, y, selected_tower)
            elif placing_tower:
                new_tower = Towers.Tower(x, y, phantom_tower.category)
                if new_tower.is_within_bounds(WIDTH, GAME_AREA_WIDTH):
                    towers.append(new_tower)
                placing_tower = False
                phantom_tower = None
        elif event.type == pygame.MOUSEMOTION and placing_tower:
            x, y = event.pos
            phantom_tower = Towers.Tower(x, y, phantom_tower.category)

    return True, placing_tower, phantom_tower


def draw_elements(window, mobs, towers, toolbar, phantom_tower, hp,money, placing_tower, wave):
    window.fill(BACKGROUND_COLOR)

    if placing_tower and phantom_tower:
        phantom_tower.draw_phantom(window)

    elapsed_time = pygame.time.get_ticks() // 1000
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer = f'{minutes:02}:{seconds:02}'
    toolbar.draw(window, hp=hp, money=money, timer=timer, wave=wave)

    for mob in mobs:
        if mob.active:
            reached_end = mob.move()
            if reached_end:
                hp = mob.attack(hp)
            else:
                mob.draw(window)
        else:
            mobs.remove(mob)  # Supprimer les mobs inactifs de la liste

    for tower in towers:
        if not tower.isPlaced:
            if tower.prix <= money:
                money -= tower.prix
                tower.isPlaced = True
        if tower.isPlaced:
            tower.draw(window)
            mobs_in_range = tower.in_range(mobs)
            mob_cible = tower.first_in_range(mobs_in_range)
            if mob_cible:
                money = tower.attack_mob(mob_cible,money)
            tower.update_cooldown()
    toolbar.draw(window, hp=hp, money=money, timer=timer, wave=wave)


    return hp,money

def main():
    window = init_window()
    clock = pygame.time.Clock()
    tick_clock = pygame.time.Clock()

    mobs = []
    towers = []
    toolbar = Toolbar.Toolbar(WIDTH, HEIGHT)
    placing_tower = False
    phantom_tower = None

    hp = 100
    money = 50
    running = True
    wave = 1
    next_mob_time = pygame.time.get_ticks()

    mobs=create_wave(wave)

    while running:
        running, placing_tower, phantom_tower = handle_events(mobs, toolbar, placing_tower, phantom_tower, towers)

        hp, money = draw_elements(window, mobs, towers, toolbar, phantom_tower, hp,money, placing_tower, wave)

        current_time = pygame.time.get_ticks()
        if not any(mob.active for mob in mobs) and next_mob_time <= current_time:
            wave += 1
            money += wave*(5%21)
            mobs=create_wave(wave)
            next_mob_time = current_time + random.randint(1000, 3500)

        tick_clock.tick(TICK)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

