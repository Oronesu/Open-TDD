import pygame

class Toolbar:
    def __init__(self, window_width, window_height):
        self.width = 224  # Largeur de la barre d'outils
        self.height = window_height
        self.color = (50, 50, 50)
        self.window_width = window_width
        self.rects = []
        self.buttons = ["Sniper", "Lance-flammes", "Mortier", "Minigun"]
        self.init_buttons()

    def init_buttons(self):
        self.rects = [
            pygame.Rect(self.window_width - self.width + 10 + (i % 2) * 110, 200 + (i // 2) * 110, 100, 100)
            for i in range(4)
        ]

    def draw(self, window, hp, money, timer, wave):
        # Dessiner la barre d'outils
        pygame.draw.rect(window, self.color, (self.window_width - self.width, 0, self.width, self.height))

        # Dessiner les boutons
        for rect in self.rects:
            pygame.draw.rect(window, (200, 200, 200), rect)

        # Afficher la vie du joueur, l'argent, le timer et la vague
        font = pygame.font.SysFont(None, 36)
        texte_vie = font.render(f'Vie: {hp}', True, (255, 255, 255))
        window.blit(texte_vie, (self.window_width - self.width + 10, 10))
        texte_argent = font.render(f'Argent: {money}', True, (255, 255, 255))
        window.blit(texte_argent, (self.window_width - self.width + 10, 50))
        texte_timer = font.render(f'Timer: {timer}', True, (255, 255, 255))
        window.blit(texte_timer, (self.window_width - self.width + 10, 90))
        texte_vague = font.render(f'Vague: {wave}', True, (255, 255, 255))
        window.blit(texte_vague, (self.window_width - self.width + 10, 130))

    def is_button_clicked(self, pos):
        for i, rect in enumerate(self.rects):
            if rect.collidepoint(pos):
                return self.buttons[i]
        return None
