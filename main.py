import pygame
import sys
import Mobs
import Tours
import Toolbar

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
largeur = 1024  # Largeur augmentée pour un écran plus grand
hauteur = 768   # Hauteur augmentée pour maintenir le ratio 4:3

# Créer la fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Ma Fenêtre Pygame")

# Définir la largeur de la zone de jeu (en dehors de la toolbar)
largeur_zone_jeu = largeur - 224  # Par exemple, la toolbar prend les derniers 100 pixels

# Clock pour gérer les FPS
clock = pygame.time.Clock()
fps = 60

# Ticks pour gérer la physique du jeu
tick_clock = pygame.time.Clock()
tick = 20

# Couleur de fond (RGB)
couleur_fond = [64, 68, 29]

# Chemin
path = [
    (0, 100), (50, 100), (100, 100), (150, 100), (200, 100),
    (200, 150), (200, 200), (250, 200), (300, 200), (350, 200),
    (400, 200), (400, 250), (400, 300), (450, 300), (500, 300),
    (550, 300), (550, 350), (550, 400), (600, 400), (650, 400),
    (700, 400), (750, 400), (800, 400)
]

# Créer les objets
mobs = [Mobs.Mob(path, 'Tank')]
#mobs = mobs + [Mobs.Mob(path, 'Captain')]
#mobs = mobs + [Mobs.Mob(path, 'Sergeant')]
#mobs = mobs + [Mobs.Mob(path, 'Tank')]
#mobs = mobs + [Mobs.Mob(path, 'Boss')]
towers = []

# Instancier la barre d'outils
toolbar = Toolbar.Toolbar(largeur, hauteur)

# Etat de placement et tour fantôme
placing_tower = False
phantom_tower = None

hp = 100
dmg = False

# Boucle principale
running = True
while running:
    # Gérer les événements
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if mobs != []:
            if keys[pygame.K_DOWN]:
                mobs[0].speed = mobs[0].speed - 1
            if keys[pygame.K_UP]:
                mobs[0].speed = mobs[0].speed +  1
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if toolbar.is_button_clicked(event.pos):
                placing_tower = True
                phantom_tower = Tours.Tour(x, y, 25, 100, (0, 0, 255))  # Initialiser la tour fantôme
            elif placing_tower:
                new_tower = Tours.Tour(x, y, 25, 100, (0, 0, 255))
                if new_tower.is_within_bounds(largeur, largeur_zone_jeu):
                    towers.append(new_tower)
                placing_tower = False
                phantom_tower = None  # Réinitialiser la tour fantôme

        elif event.type == pygame.MOUSEMOTION and placing_tower:
            x, y = event.pos
            phantom_tower = Tours.Tour(x, y, 25, 100, (0, 0, 255))


    # Remplir la fenêtre avec la couleur de fond
    fenetre.fill(tuple(couleur_fond))

    # Dessiner le phantôme de la tour si on est en mode placement et que phantom_tower est défini
    if placing_tower and phantom_tower:
        phantom_tower.draw_phantom(fenetre)

    # Calculer le temps écoulé en secondes et afficher le timer
    temps_ecoule = pygame.time.get_ticks() // 1000
    minutes = temps_ecoule // 60
    secondes = temps_ecoule % 60
    timer = f'{minutes:02}:{secondes:02}'
    toolbar.draw(fenetre, vie=hp, argent=500, timer=timer, vague=1)

    # Dessiner les mobs


                
    for mob in mobs:
      if mob.active:
        reached_end=mob.move()
        if mob.rect.x < largeur_zone_jeu:
          mob.draw(fenetre)
          if reached_end:
            hp = mob.attack(hp)
            reached_end = False
        else:
          mob.active = False #désactiver les bos en dehors de la zone de jeu

    # Supprimer les mobs inactifs
    mobs = [mob for mob in mobs if mob.active]

    # Dessiner les tours placées
    for tower in towers:
        tower.draw(fenetre)

    # Dessiner la toolbar par-dessus tout
    toolbar.draw(fenetre, vie=100, argent=500, timer=timer, vague=1)

    tick_clock.tick(tick)

    # Mettre à jour l'affichage
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
sys.exit()
