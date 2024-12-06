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


def display_menu(window):
    rect = pygame.Rect(WIDTH/2, HEIGHT/2, 100, 50)
    pygame.draw.rect(window, (0, 0, 0), rect)
    font = pygame.font.SysFont(None, 36)
    texte_menu = font.render('Welcome to Open-TDD', True, (255, 255, 255))
    window.blit(texte_menu, (WIDTH/2.5, HEIGHT/3))
    texte_play = font.render('Play', True, (255, 255, 255))
    window.blit(texte_play, (WIDTH/1.9, HEIGHT/1.95))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                return True, True
    return False, True



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




# fonction pour gérer les améliorations des tours
def upgrade_towers(lvl_s, lvl_lf, lvl_mo, lvl_mi, towers):
    base_stats = [[10, 2, 50],
                  [25.0, 1.5, 50.0],
                  [35, 0.8, 50],
                  [40, 10, 50],
                  ]
    for tower in towers:
        if tower.category == 'Sniper':
            level = lvl_s
            i = 0
        elif tower.category == 'Lance-flammes':
            level = lvl_lf
            i = 1
        elif tower.category == 'Mortier':
            level = lvl_mo
            i = 2
        elif tower.category == 'Minigun':
            level = lvl_mi
            i = 3
        for j in range(2):
            base = base_stats[i][[j]]
            for k in range(1, level):
                base *= 1.5
            if j == 0:
                tower.dmg = base
            elif j == 1:
                tower.atk_spd = base
            elif j == 2:
                tower.range = base
    return towers





def handle_events(mobs, toolbar, placing_tower, phantom_tower, towers, money, upg_s, upg_lf, upg_mo, upg_mi, lvl_s, lvl_lf, lvl_mo, lvl_mi):
    tow = ["Sniper", "Lance-flammes", "Mortier", "Minigun"]
    upg = ["Upgrade_S", "Upgrade_LF", "Upgrade_Mo", "Upgrade_Mi"]
    selected_tower = None
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, placing_tower, phantom_tower, money, upg_s, upg_lf, upg_mo, upg_mi, lvl_s, lvl_lf, lvl_mo, lvl_mi

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            selected_tower = False
            selected_upg = False
            if toolbar.is_button_clicked(event.pos) in tow:
                selected_tower = True
            if toolbar.is_button_clicked(event.pos) in upg:
                selected_upg = True

            if selected_tower:
                placing_tower = True
                phantom_tower = Towers.Tower(x, y, toolbar.is_button_clicked(event.pos))
            elif placing_tower:
                new_tower = Towers.Tower(x, y, phantom_tower.category)
                if new_tower.is_within_bounds(WIDTH, GAME_AREA_WIDTH):
                    towers.append(new_tower)
                placing_tower = False
                phantom_tower = None

            if selected_upg:
                if upg.index(toolbar.is_button_clicked(event.pos)) == 0:
                    if money >= upg_s:
                        money -= upg_s
                        upg_s *= 2
                        lvl_s += 1
                elif upg.index(toolbar.is_button_clicked(event.pos)) == 1:
                    if money >= upg_lf:
                        money -= upg_lf
                        upg_lf *= 2
                        lvl_lf += 1
                elif upg.index(toolbar.is_button_clicked(event.pos)) == 2:
                    if money >= upg_mo:
                        money -= upg_mo
                        upg_mo *= 2
                        lvl_mo += 1
                elif upg.index(toolbar.is_button_clicked(event.pos)) == 3:
                    if money >= upg_mi:
                        money -= upg_mi
                        upg_mi *= 2
                        lvl_mi += 1



        elif event.type == pygame.MOUSEMOTION and placing_tower:
            x, y = event.pos
            phantom_tower = Towers.Tower(x, y, phantom_tower.category)

    return True, placing_tower, phantom_tower, money, upg_s, upg_lf, upg_mo, upg_mi, lvl_s, lvl_lf, lvl_mo, lvl_mi


def draw_elements(window, mobs, towers, toolbar, phantom_tower, hp,money, placing_tower, wave, upg_s, upg_lf, upg_mo, upg_mi, lvl_s, lvl_lf, lvl_mo, lvl_mi):
    window.fill(BACKGROUND_COLOR)

    if placing_tower and phantom_tower:
        phantom_tower.draw_phantom(window)

    elapsed_time = pygame.time.get_ticks() // 1000
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer = f'{minutes:02}:{seconds:02}'
    toolbar.draw(window, hp, money, timer, wave, upg_s, upg_lf, upg_mo, upg_mi, lvl_s, lvl_lf, lvl_mo, lvl_mi)

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
    toolbar.draw(window, hp, money, timer, wave, upg_s, upg_lf, upg_mo, upg_mi, lvl_s, lvl_lf, lvl_mo, lvl_mi)


    return hp,money, upg_s, upg_lf, upg_mo, upg_mi

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
    money = 50000
    running = True
    upg_s = 50
    upg_lf = 50
    upg_mo = 50
    upg_mi = 50
    lvl_s = 1
    lvl_lf = 1
    lvl_mo = 1
    lvl_mi = 1
    wave = 1
    next_mob_time = pygame.time.get_ticks()

    mobs=create_wave(wave)

    start = False
    while running:
        if not start:
            start, running = display_menu(window)
        else:
            towers = upgrade_towers(lvl_s, lvl_lf, lvl_mo, lvl_mi, towers) #améliore les tours en fonction de leur niveau

            running, placing_tower, phantom_tower, money, upg_s, upg_lf, upg_mo, upg_mi, lvl_s, lvl_lf, lvl_mo, lvl_mi  = handle_events(mobs, toolbar, placing_tower, phantom_tower, towers, money, upg_s, upg_lf, upg_mo, upg_mi, lvl_s, lvl_lf, lvl_mo, lvl_mi)

            hp, money, upg_s, upg_lf, upg_mo, upg_mi = draw_elements(window, mobs, towers, toolbar, phantom_tower, hp,money, placing_tower, wave, upg_s, upg_lf, upg_mo, upg_mi, lvl_s, lvl_lf, lvl_mo, lvl_mi)

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

