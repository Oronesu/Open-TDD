import pygame

class Toolbar:
    def __init__(self, window_width, window_height):
        self.width = 224
        self.height = window_height
        self.color = (50,50,50)
        self.window_width = window_width
        self.rects = []
        self.buttons = ["Sniper", "Flamethrower", "Missile", "Minigun", "Upgrade_Sniper", "Upgrade_Flamethrower", "Upgrade_Missile", "Upgrade_Minigun"]
        self.icons = {}
        self.init_buttons()
        # Charger une police monospace
        self.font = pygame.font.Font(f"Textures/new_monzane.otf", 20)

    def init_buttons(self):
        # Long tableau pour mettre les emplacements pour les boutons (Fait avec l'aide d'IA pour les calculs de positions ma faute j'assume)
        self.rects = [
            pygame.Rect(self.window_width - self.width + 10 + (i % 2) * 110, 250 + (i // 2) * 200, 100, 100)
            for i in range(4)
        ] + [pygame.Rect(self.window_width - self.width + 10 + (j % 2) * 110, 351 + (j // 2) * 200, 100, 50)
             for j in range(4)]

        # Charger les icônes des tours
        for button in self.buttons[:4]:  # Charger les icônes seulement pour les tours, pas pour les upgrades
            category = button
            self.icons[button] = pygame.transform.scale(pygame.image.load(f'Textures/Ico-{category}.png'), (74, 74))

    def draw(self, window, hp, money, timer, wave, upgrade_prices, levels):
        pygame.draw.rect(window, self.color, (self.window_width - self.width, 0, self.width, self.height))  # Darren: dessine la barre d'outils
        for i, rect in enumerate(self.rects):
            pygame.draw.rect(window, (100, 100, 100), rect)  # Darren: dessine chaque bouton de la barre d'outils

            if self.buttons[i] in self.icons:
                # Dessiner l'icône sur le bouton
                icon = self.icons[self.buttons[i]]
                icon_rect = icon.get_rect(center=rect.center)
                window.blit(icon, icon_rect.topleft)

        texte_vie = self.font.render(f'Vie: {hp}', True, (255, 255, 255))
        window.blit(texte_vie, (self.window_width - self.width + 10, 10))  # Darren: affiche les points de vie
        texte_argent = self.font.render(f'Argent: {money}', True, (255, 255, 255))
        window.blit(texte_argent, (self.window_width - self.width + 10, 50))  # Darren: affiche l'argent
        texte_timer = self.font.render(f'Timer: {timer}', True, (255, 255, 255))
        window.blit(texte_timer, (self.window_width - self.width + 10, 90))  # Darren: affiche le timer
        texte_vague = self.font.render(f'Vague: {wave}', True, (255, 255, 255))
        window.blit(texte_vague, (self.window_width - self.width + 10, 130))  # Darren: affiche la vague actuelle

        # Darren
        for i, price in enumerate(upgrade_prices):
            text = self.font.render(f'{price} ({levels[i]})', True, (255, 255, 0))
            window.blit(text, (self.window_width - self.width + 15 + (i % 2) * 110, 365 + (i // 2) * 200))  # Darren: affiche le prix et le niveau des améliorations

    # Darren: Ici on gère juste si le bouton est cliqué
    def is_button_clicked(self, pos):
        for i, rect in enumerate(self.rects):
            if rect.collidepoint(pos):
                return self.buttons[i]
        return None
