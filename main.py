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

# Clock pour gérer les FPS
clock = pygame.time.Clock()
fps = 60

# Ticks pour gérer la physique du jeu
tick_clock = pygame.time.Clock()
tick = 20

# Couleur de fond (RGB)
couleur_fond = [0, 0, 0]

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
towers = []

# Instancier la barre d'outils
toolbar = Toolbar.Toolbar(largeur, hauteur)

# Etat de placement
placing_tower = None

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if toolbar.is_button_clicked(event.pos):
                placing_tower = True
            elif placing_tower:
                towers.append(Tours.Tour(x, y, 25, 100, (0, 0, 255)))
                placing_tower = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        couleur_fond[0] = (couleur_fond[0] + 1) % 256

    # Remplir la fenêtre avec la couleur de fond
    fenetre.fill(tuple(couleur_fond))  # Utiliser tuple ici

    # Calculer le temps écoulé en secondes et afficher le timer
    temps_ecoule = pygame.time.get_ticks() // 1000
    minutes = temps_ecoule // 60
    secondes = temps_ecoule % 60
    timer = f'{minutes:02}:{secondes:02}'
    toolbar.draw(fenetre, vie=100, argent=500, timer=timer, vague=1)

    # Dessiner les mobs
    for mob in mobs:
        if mob.active:
            mob.draw(fenetre)
            mob.move()
    # Supprimer les mobs inactifs
    mobs = [mob for mob in mobs if mob.active]

    # Dessiner les tours placés
    for tower in towers:
        tower.draw(fenetre)

    tick_clock.tick(tick)

    # Mettre à jour l'affichage
    pygame.display.flip()

    clock.tick(fps)

pygame.quit()
sys.exit()
