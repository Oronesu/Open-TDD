import pygame

class Toolbar:
    def __init__(self, window_width, window_height):
        self.width = 224  # Largeur de la barre d'outils
        self.height = window_height
        self.color = (50, 50, 50)  # Correction de l'orthographe de 'coulor' à 'color'
        self.window_width = window_width
        self.rects = []
        self.init_buttons()

    def init_buttons(self):
        self.rects = [
            pygame.Rect(self.window_width - self.width + 10 + (i % 2) * 110, 200 + (i // 2) * 110, 100, 100)
            for i in range(4)
        ]

    def draw(self, fenetre, hp, money, timer, wave):
        # Dessiner la barre d'outils
        pygame.draw.rect(fenetre, self.color, (self.window_width - self.width, 0, self.width, self.height))

        # Dessiner les boutons
        for rect in self.rects:
            pygame.draw.rect(fenetre, (200, 200, 200), rect)

        # Afficher la vie du joueur, l'argent, le timer et la vague
        font = pygame.font.SysFont(None, 36)
        texte_vie = font.render(f'Vie: {hp}', True, (255, 255, 255))
        fenetre.blit(texte_vie, (self.window_width - self.width + 10, 10))
        texte_argent = font.render(f'Argent: {money}', True, (255, 255, 255))
        fenetre.blit(texte_argent, (self.window_width - self.width + 10, 50))
        texte_timer = font.render(f'Timer: {timer}', True, (255, 255, 255))
        fenetre.blit(texte_timer, (self.window_width - self.width + 10, 90))
        texte_vague = font.render(f'Vague: {wave}', True, (255, 255, 255))
        fenetre.blit(texte_vague, (self.window_width - self.width + 10, 130))

    def is_button_clicked(self, pos):
        for rect in self.rects:
            if rect.collidepoint(pos):
                return True
        return False
