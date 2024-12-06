import pygame

class Toolbar:
    def __init__(self, window_width, window_height):
        self.width = 224  # Largeur de la barre d'outils
        self.height = window_height
        self.color = (50, 50, 50)
        self.window_width = window_width
        self.rects = []
        self.buttons = ["Sniper", "Lance-flammes", "Mortier", "Minigun", "Upgrade_S", "Upgrade_LF", "Upgrade_Mo", "Upgrade_Mi"]
        self.init_buttons()

    def init_buttons(self):
        self.rects = [
            pygame.Rect(self.window_width - self.width + 10 + (i % 2) * 110, 250 + (i // 2) * 200, 100, 100)
            for i in range(4)
        ] + [pygame.Rect(self.window_width - self.width + 10 + (j % 2) * 110, 351 + (j // 2) * 200, 100, 50)
             for j in range(4)]

    def draw(self, window, hp, money, timer, wave, upg_s, upg_lf, upg_mo, upg_mi, lvl_s, lvl_lf, lvl_mo, lvl_mi):
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
        texte_upg_s = font.render(f'{upg_s} ({lvl_s})', True, (255, 255, 0))
        window.blit(texte_upg_s, (self.window_width - self.width + 15, 365))
        texte_upg_lf = font.render(f'{upg_lf} ({lvl_lf})', True, (255, 255, 0))
        window.blit(texte_upg_lf, (self.window_width - self.width + 125, 365))
        texte_upg_mo = font.render(f'{upg_mo} ({lvl_mo})', True, (255, 255, 0))
        window.blit(texte_upg_mo, (self.window_width - self.width + 15, 565))
        texte_upg_mi = font.render(f'{upg_mi} ({lvl_mi})', True, (255, 255, 0))
        window.blit(texte_upg_mi, (self.window_width - self.width + 125, 565))

    def is_button_clicked(self, pos):
        for i, rect in enumerate(self.rects):
            if rect.collidepoint(pos):
                return self.buttons[i]
        return None
