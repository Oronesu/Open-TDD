import pygame


class Mob:
    def __init__(self, path, width, height, color):
        self.rect = pygame.Rect(path[0][0], path[0][1], width, height)
        self.color = color
        self.path = path
        self.path_index = 0

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)





