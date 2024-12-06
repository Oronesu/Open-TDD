import pygame

TICKS_PER_SECOND = 60

class Bullet:
    def __init__(self, start_pos, target_pos, dmg, speed):
        self.x, self.y = start_pos
        self.target_x, self.target_y = target_pos
        self.dmg = dmg
        self.speed = speed
        self.rect = pygame.Rect(self.x, self.y, 5, 5)  # Taille du projectile
        self.color = (255, 150, 150)  # Couleur blanche pour le projectile

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = (dx ** 2 + dy ** 2) ** 0.5
        self.move_x = (dx / dist) * self.speed
        self.move_y = (dy / dist) * self.speed

    def move(self):
        self.x += self.move_x
        self.y += self.move_y
        self.rect.topleft = (self.x, self.y)

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
