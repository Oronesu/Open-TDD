import pygame

class Tour:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

    def draw_phantom(self, surf):
        # Créer une surface temporaire pour le phantome
        phantom_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        # Appliquer la transparence
        phantom_surface.set_alpha(128)  # 128 pour 50% de transparence
        # Dessiner la tour transparente
        pygame.draw.rect(phantom_surface, self.color, phantom_surface.get_rect())
        # Blitter la surface transparente sur l'écran
        surf.blit(phantom_surface, (self.rect.x, self.rect.y))

    def is_within_bounds(self, width, height):
        return 0 <= self.rect.x <= width - self.rect.width and 0 <= self.rect.y <= height - self.rect.height
