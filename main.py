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
background_image = pygame.image.load("Textures/Background.png")

PATH = [(0, 128), (640, 128), (640, 448), (448, 448), (448, 320), (256, 320), (256, 448), (128, 448), (128, 640),
        (768, 640), (768, 768)
        ]

TOWERS_PLACEMENT = [(96, 32), (288, 32), (480, 32), (736, 160), (160, 224), (352, 224), (544, 224), (160, 352),
                    (544, 352), (352, 416), (736, 416), (32, 480), (224, 544), (480, 544), (608, 544), (32, 608),
                    (224, 736), (672, 736)]

PLACEMENT_RADIUS = 25
MOB_TYPES = ['Soldier', 'Captain', 'Sergeant', 'Tank', 'Bomber']


#Initialisation de la fenêtre
def init_window():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Open TDD")
    return window


'''---------------------Création des vagues----------------------'''
#Alan

# Alan

def create_wave(wave_number):
    number_of_mobs = 5 * wave_number  # Alan: nombre de mobs dans la vague, dépendant du numéro de vague
    wave_mobs = []
    for _ in range(number_of_mobs):
        mob_type = random.choices(MOB_TYPES, weights=[1, 1, 1, wave_number, wave_number])[0]  # Alan: choix aléatoire du type de mob avec des poids
        wave_mobs.append(Mobs.Mob(PATH, mob_type))  # Alan: ajout du mob à la vague
    return wave_mobs


def update_wave(mobs, wave_mobs, next_mob_time, current_time):
    if wave_mobs and next_mob_time <= current_time:
        mobs.append(wave_mobs.pop(0))                                   # Alan: ajout du mob suivant à la liste des mobs actuels
        next_mob_time = current_time + random.randint(200, 1500)  # Alan: délai jusqu'à l'apparition du prochain mob
    return next_mob_time                                                # Alan: retourne le délai du prochain mob



'''---------------------Vérification de la zone de placement des tours----------------------'''


def is_within_placement_square(x, y):
    """
    Darren:
    Vérifie si la position en x et y du curseur est dans une zone de placement valable
    La zone de placement est marqué par un carré de 25*2 de large autour d'un point donné
    :param x: Abs du curseur
    :param y: Ord du curseur
    :return: Si dans placement: True et les coordonés du centre de la zone (px,py)
    """
    for px, py in TOWERS_PLACEMENT:
        if abs(x - px) <= PLACEMENT_RADIUS and abs(y - py) <= PLACEMENT_RADIUS:
            return True, px, py
    return False, x, y


def handle_events(toolbar, placing_tower, phantom_tower, towers, money, upgrade_prices, levels):
    """
    Darren:
    Ici on gère  toutes les interactions de l'utilisateur
    ...
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, placing_tower, phantom_tower, money, upgrade_prices, levels

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos

            #Darren
            #-----Fantôme de la tour-----#
            #Darren: Si on selectionne une tour on crée un "fantôme" de la tour pour voir où la tour ira
            selected_tower = toolbar.is_button_clicked(event.pos)
            if selected_tower in ["Sniper", "Flamethrower", "Missile", "Minigun"]:
                placing_tower = True
                phantom_tower = Towers.Tower(x, y, selected_tower, level=1)

            #Alan
            #-----Amélioration des tours-----#
            elif selected_tower in ["Upgrade_Sniper", "Upgrade_Flamethrower", "Upgrade_Missile", "Upgrade_Minigun"]:
                index = ["Upgrade_Sniper", "Upgrade_Flamethrower", "Upgrade_Missile", "Upgrade_Minigun"].index(
                    selected_tower)
                if money >= upgrade_prices[index]:  #Alan:  on vérifie si le joueur possède suffisamment d'argent pour l'amélioration souhaitée
                    money -= upgrade_prices[index]  #Alan: on retire au joueur le montant d'argent correspondant au prix de l'amélioration souhaitée
                    upgrade_prices[index] *= 2      #Alan: on double le prix de la prochaine amélioration
                    levels[index] += 1              #Alan: on incrémente le niveau de toutes les tours de ce type
                    for tower in towers:
                        if tower.category == selected_tower.split('_')[1]:
                            tower.upgrade()

            #Darren
            #-----Placement des tours-----#
            elif placing_tower:
                valid_placement, px, py = is_within_placement_square(x, y)  #Darren: Verif que la tour est dans un emplacement
                if valid_placement:
                    new_tower = Towers.Tower(px, py, phantom_tower.category,
                                level=levels[toolbar.buttons.index(phantom_tower.category)])
                    if new_tower.is_within_bounds(WIDTH, GAME_AREA_WIDTH):  #Darren: Verif que la tour est dans l'espace de jeu
                        towers.append(new_tower)
                    placing_tower = False                                   #Darren: On quitte le mode de placement
                    phantom_tower = None                                    #Darren: On désactive le "fantôme" une fois la tour placée


        #Darren: Tracking de la tour par rapport à la souris
        elif event.type == pygame.MOUSEMOTION and placing_tower:
            x, y = event.pos
            phantom_tower.rect.center = (x, y)

    return True, placing_tower, phantom_tower, money, upgrade_prices, levels


def draw_elements(window, mobs, towers, toolbar, phantom_tower, hp, money, placing_tower, wave, upgrade_prices, levels):
    #On affiche l'image de fond
    window.blit(background_image, (0, 0))
    #Ici on dessine le "fantome de la tour"
    if placing_tower and phantom_tower:
        phantom_tower.draw_phantom(window)

    #Paramètres afin de dessiner la toolbar
    elapsed_time = pygame.time.get_ticks() // 1000
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    timer = f'{minutes:02}:{seconds:02}'

    #Alan
    #On affiche les mobs contenus dans la liste des mobs
    for mob in mobs:
        if mob.active:                  #Alan: pour chaque mob présent sur le plateau de jeu, on vérifie s'il est encore actif
            reached_end = mob.move()    #Alan: si oui, alors on le fait bouger
            if reached_end:             #Alan: puis on regarde s'il a atteint la fin du chemin
                hp = mob.attack(hp)     #Alan: et on retire au joueur de la vie en fonction des dégâts du mob
            else:
                mob.draw(window)        #Alan: sinon, on continue de l'afficher à sa prochaine coordonnée
        else:
            mobs.remove(mob)            #Alan: on supprime le mob s'il n'est plus actif

    #Darren et Alan
    #Ici on affiche les tours contenus dans la liste des tours placés
    for tower in towers:
        if not tower.isPlaced:
            if tower.prix <= money:     #ALan: on vérifie si le joueur possède assez d'argent pour acheter la tour souhaitée
                money -= tower.prix     #Alan: on déduit au joueur le montant d'argent correspondant au prix de la tour
                tower.isPlaced = True
        if tower.isPlaced:
            tower.draw(window)
            money = tower.attack_mob(mobs, money)   #Darren / Alan: on donne au joueur de l'argent si la tour tue un mob
                                                    #Darren / Alan: la mort du mob est déterminée directement dans la fonction
                                                    #Darren / Alan: on donne au joueur la récompense liée au mob s'il meurt, sinon on lui donne 0

    toolbar.draw(window, hp, money, timer, wave, upgrade_prices, levels) #On dessine la toolbar

    return hp, money


import pygame


def display_menu(window):
    bg_image = pygame.image.load("Textures/MainBG.png")
    window.blit(bg_image,(0,0))  # Remplir l'écran avec un fond gris foncé
    # Définir la police
    font = pygame.font.Font(f"Textures/new_monzane.otf", 36)
    texte_menu = font.render('Welcome to Open-TDD', True, (255, 255, 255))
    texte_menu_rect = texte_menu.get_rect(center=(window.get_width() / 2, window.get_height() / 3))
    window.blit(texte_menu, texte_menu_rect.topleft)
    # Définir et dessiner le rectangle du bouton "Play"
    rect = pygame.Rect(window.get_width() / 2 - 50, window.get_height() / 2 - 25, 100, 50)
    pygame.draw.rect(window, (0, 0, 0), rect)
    texte_play = font.render('Play', True, (255, 255, 255))
    texte_play_rect = texte_play.get_rect(center=rect.center)
    window.blit(texte_play, texte_play_rect.topleft)

    pygame.display.flip()  # Mise à jour de l'écran pour afficher les changements

    # Gérer les événements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False, False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):
                return True, True

    return False, True


def init_game():
    """ Fonction pour initialiser les variables de jeu """
    global mobs, towers, toolbar, placing_tower, phantom_tower, hp, money, running, upgrade_prices, levels, wave, next_mob_time, wave_mobs, start
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

'''---------------------Boucle du jeu----------------------'''

def main():
    global mobs, towers, toolbar, placing_tower, phantom_tower, hp, money, running, upgrade_prices, levels, wave, next_mob_time, wave_mobs, start
    window = init_window()
    clock = pygame.time.Clock()
    tick_clock = pygame.time.Clock()

    init_game()

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
                money += (wave % 21) * 5
                wave_mobs = create_wave(wave)

            if hp <= 0:
                init_game()

            tick_clock.tick(TICK)
            pygame.display.flip()
            clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
