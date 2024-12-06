import pygame
import sys
import random
import Mobs
import Towers
import Toolbar

'''---------------------Constantes----------------------'''
# Initialisation de Pygame
pygame.init()

# Constantes
WIDTH = 1024
HEIGHT = 768
GAME_AREA_WIDTH = WIDTH - 224
FPS = 60
TICK = 30

# Charger l'image de fond
background_image = pygame.image.load("Background.png")

PATH = [(0, 128), (640, 128), (640, 448), (448, 448), (448, 320), (256, 320), (256, 448), (128, 448), (128, 640),
        (768, 640), (768, 768)
        ]

TOWERS_PLACEMENT = [(96, 32), (288, 32), (480, 32), (736, 160), (160, 224), (352, 224), (544, 224), (160, 352),
                    (544, 352), (352, 416), (736, 416), (32, 480), (224, 544), (480, 544), (608, 544), (32, 608),
                    (224, 736), (672, 736)]

PLACEMENT_RADIUS = 25
MOB_TYPES = ['Soldier', 'Captain', 'Sergeant', 'Tank', 'Bomber']


def init_window():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Open TDD")
    return window


'''---------------------Création des vagues----------------------'''


def create_wave(wave_number):
    number_of_mobs = 5 * wave_number
    wave_mobs = []
    for _ in range(number_of_mobs):
        mob_type = random.choices(MOB_TYPES, weights=[1, 1, 1, wave_number, wave_number])[0]
        wave_mobs.append(Mobs.Mob(PATH, mob_type))
    return wave_mobs


def update_wave(mobs, wave_mobs, next_mob_time, current_time):
    if wave_mobs and next_mob_time <= current_time:
        mobs.append(wave_mobs.pop(0))
        next_mob_time = current_time + random.randint(200, 1500)
    return next_mob_time


'''---------------------Vérification de la zone de placement des tours----------------------'''


def is_within_placement_square(x, y):
    '''
    Vérifie si la position en x et y du curseur est dans une zone de placement valable
    La zone de placement est marqué par un carré de 25*2 de large autour d'un point donné
    :param x: Abs du curseur
    :param y: Ord du curseur
    :return: Si dans placement: True et les coordonés du centre de la zone (px,py)
    '''
    for px, py in TOWERS_PLACEMENT:
        if abs(x - px) <= PLACEMENT_RADIUS and abs(y - py) <= PLACEMENT_RADIUS:
            return True, px, py
    return False, x, y


def handle_events(toolbar, placing_tower, phantom_tower, towers, money, upgrade_prices, levels):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, placing_tower, phantom_tower, money, upgrade_prices, levels

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            selected_tower = toolbar.is_button_clicked(event.pos)

            if selected_tower in ["Sniper", "Flamethrower", "Missile", "Minigun"]:
                placing_tower = True
                phantom_tower = Towers.Tower(x, y, selected_tower, level=1)

            elif selected_tower in ["Upgrade_Sniper", "Upgrade_Flamethrower", "Upgrade_Missile", "Upgrade_Minigun"]:
                index = ["Upgrade_Sniper", "Upgrade_Flamethrower", "Upgrade_Missile", "Upgrade_Minigun"].index(
                    selected_tower)
                if money >= upgrade_prices[index]:
                    money -= upgrade_prices[index]
                    upgrade_prices[index] *= 2
                    levels[index] += 1
                    for tower in towers:
                        if tower.category == selected_tower.split('_')[1]:
                            tower.upgrade()

            elif placing_tower:
                valid_placement, px, py = is_within_placement_square(x, y)
                if valid_placement:
                    new_tower = Towers.Tower(px, py, phantom_tower.category,
                                level=levels[toolbar.buttons.index(phantom_tower.category)])

                    if new_tower.is_within_bounds(WIDTH, GAME_AREA_WIDTH):
                        towers.append(new_tower)
                    placing_tower = False
                    phantom_tower = None

        elif event.type == pygame.MOUSEMOTION and placing_tower:
            x, y = event.pos
            phantom_tower.rect.center = (x, y)

    return True, placing_tower, phantom_tower, money, upgrade_prices, levels


def draw_elements(window, mobs, towers, toolbar, phantom_tower, hp, money, placing_tower, wave, upgrade_prices, levels):
    window.blit(background_image, (0, 0))

    if placing_tower and phantom_tower:
        phantom_tower.draw_phantom(window)

    elapsed_time = pygame.time.get_ticks() // 1000
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer = f'{minutes:02}:{seconds:02}'
    toolbar.draw(window, hp, money, timer, wave, upgrade_prices, levels)

    for mob in mobs:
        if mob.active:
            reached_end = mob.move()
            if reached_end:
                hp = mob.attack(hp)
            else:
                mob.draw(window)
        else:
            mobs.remove(mob)

    for tower in towers:
        if not tower.isPlaced:
            if tower.prix <= money:
                money -= tower.prix
                tower.isPlaced = True
        if tower.isPlaced:
            tower.draw(window)
            money = tower.attack_mob(mobs, money)

    toolbar.draw(window, hp, money, timer, wave, upgrade_prices, levels)

    return hp, money


def display_menu(window):
    window.fill((50, 50, 50))  # Remplir l'écran avec un fond gris foncé
    rect = pygame.Rect(WIDTH / 2 - 50, HEIGHT / 2 - 25, 100, 50)
    pygame.draw.rect(window, (0, 0, 0), rect)
    font = pygame.font.SysFont(None, 36)
    texte_menu = font.render('Welcome to Open-TDD', True, (255, 255, 255))
    window.blit(texte_menu, (WIDTH / 2.5, HEIGHT / 3))
    texte_play = font.render('Play', True, (255, 255, 255))
    window.blit(texte_play, (WIDTH / 2.9, HEIGHT / 1.95))

    pygame.display.flip()  # Mise à jour de l'écran pour afficher les changements

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                return True, True

    return False, True


'''---------------------Boucle du jeu----------------------'''


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
    money = 20000
    running = True
    upgrade_prices = [50, 50, 50, 50]
    levels = [1, 1, 1, 1]
    wave = 1

    next_mob_time = pygame.time.get_ticks()
    wave_mobs = create_wave(wave)

    start = False
    while running:
        if not start:
            start, running = display_menu(window)
        else:
            running, placing_tower, phantom_tower, money, upgrade_prices, levels = (
                handle_events(toolbar, placing_tower, phantom_tower, towers, money, upgrade_prices, levels))
            hp, money = draw_elements(window, mobs, towers, toolbar, phantom_tower, hp, money, placing_tower, wave,
                                      upgrade_prices, levels)

            current_time = pygame.time.get_ticks()
            next_mob_time = update_wave(mobs, wave_mobs, next_mob_time, current_time)

            if not any(mob.active for mob in mobs) and next_mob_time <= current_time:
                wave += 1
                money += wave * (5 % 21)
                wave_mobs = create_wave(wave)

            tick_clock.tick(TICK)
            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
