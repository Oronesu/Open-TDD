import pygame

class Mob:
    MOB_PROPERTIES = {
        'Soldier': {'health': 50, 'absorb': 0, 'damage': 10, 'speed': 20, 'size': (20, 20), 'color': (255, 0, 0)},
        'Captain': {'health': 100, 'absorb': 2, 'damage': 25, 'speed': 35, 'size': (25, 25), 'color': (255, 255, 0)},
        'Sergeant': {'health': 150, 'absorb': 3, 'damage': 35, 'speed': 35, 'size': (30, 30), 'color': (0, 255, 0)},
        'Tank': {'health': 500, 'absorb': 7, 'damage': 50, 'speed': 10, 'size': (60, 40), 'color': (128, 128, 128)},
        'Boss': {'health': 300, 'absorb': 5, 'damage': 40, 'speed': 25, 'size': (35, 35), 'color': (238, 130, 238)}
    }

    def __init__(self, path, category):
        self.category = category
        self.path = path
        self.path_index = 0
        properties = self.MOB_PROPERTIES.get(category, {})
        self.health = properties.get('health', 0)
        self.absorb = properties.get('absorb', 0)
        self.damage = properties.get('damage', 0)
        self.speed = properties.get('speed', 0)
        width, height = properties.get('size', (15, 15))
        self.rect = pygame.Rect(path[0][0], path[0][1], width, height)
        self.color = properties.get('color', (0, 0, 0))
        self.active = True

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

    def delete(self):
        self.active = False
        self.path = None
        self.rect = None
        self.color = None

    def move(self):
        if self.path_index < len(self.path) - 1:
            target = self.path[self.path_index + 1]
            dx, dy = target[0] - self.rect.x, target[1] - self.rect.y
            dist = (dx**2 + dy**2)**0.5
            if dist <= 5:
                self.path_index += 1
            else:
                self.rect.x += self.speed * dx / dist
                self.rect.y += self.speed * dy / dist
        else:
            self.delete()
