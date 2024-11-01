import pygame
import sys
import Mobs
import Tours

# Initialisation de Pygame
pygame.init()

# Définir les dimensions de la fenêtre
largeur = 800
hauteur = 600

# Créer la fenêtre
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Ma Fenêtre Pygame")

#Clock pour gérer les FPS
clock = pygame.time.Clock()
fps = 60

#Ticks pour gérer la physique du jeu
tick_clock = pygame.time.Clock()
tick=20

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
mob1 = Mobs.Mob(path, 20, 20, (255, 0, 0))
world_trade_center = Tours.Tour(10, 250, 25, 100, (0, 0, 255))

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys=pygame.key.get_pressed()
    if keys[pygame.K_DOWN]:
        couleur_fond[0] = (couleur_fond[0] + 1) % 256

    # Remplir la fenêtre avec la couleur de fond
    fenetre.fill(tuple(couleur_fond))  # Utiliser tuple ici

    # Dessiner les objets
    mob1.draw(fenetre)
    world_trade_center.draw(fenetre)

    tick_clock.tick(tick)
    #mob1.move()

    # Mettre à jour l'affichage
    pygame.display.flip()

    clock.tick(fps)

pygame.quit()
sys.exit()


