import pygame


class Mob:
    MOB_PROPERTIES = {
        'Soldier': {'health': 50, 'absorb': 0, 'damage': 10, 'reward' : 5, 'speed': 5, 'size': (20, 20), 'color': (255, 0, 0)},
        'Captain': {'health': 100, 'absorb': 2, 'damage': 25, 'reward' : 10, 'speed': 5, 'size': (25, 25), 'color': (255, 255, 0)},
        'Sergeant': {'health': 150, 'absorb': 3, 'damage': 35, 'reward' : 20, 'speed': 5, 'size': (30, 30), 'color': (0, 255, 0)},
        'Tank': {'health': 500, 'absorb': 7, 'damage': 50, 'reward' : 40, 'speed': 1, 'size': (60, 40), 'color': (128, 128, 128)},
        'Boss': {'health': 300, 'absorb': 5, 'damage': 40, 'reward' : 60, 'speed': 2, 'size': (35, 35), 'color': (238, 130, 238)}
    }

    def __init__(self, path, category):
        self.category = category
        self.path = path
        self.path_index = 0
        properties = self.MOB_PROPERTIES.get(category, {})
        self.health = properties.get('health', 0)
        self.absorb = properties.get('absorb', 0)
        self.damage = properties.get('damage', 0)
        self.reward = properties.get('reward', 0)
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
            dist = (dx ** 2 + dy ** 2) ** 0.5
            move_dist = min(self.speed, dist)  # pour éviter qu'il dépasse le point cible et qu'il se bloque
            if dist <= 5:
                self.path_index += 1
                return False
            else:
                self.rect.x += move_dist * dx / dist
                self.rect.y += move_dist * dy / dist
                return False

        else:
            self.delete()
            return True


#Darren
    def dist_travelled(self):
        '''
        Calcule la distance parcourue sur le chemin
        Appelé par Tours pour trouver le mob le plus avancé sur le chemin
        :return:
        (int) dist_pacourue -> distance parcourue sur le chemin
        '''

        # Si le mob est au début du chemin, la distance est nulle
        if self.path_index == 0:
            return 0
        else:
            # Calculer la distance du point de départ au premier point du chemin
            dx = self.rect.x - self.path[0][0]
            dy = self.rect.y - self.path[0][1]
            dist_parcourue = (dx ** 2 + dy ** 2) ** 0.5  # Distance euclidienne

            # Ajouter les distances entre les points du chemin jusqu'au point atteint
            for i in range(1, self.path_index + 1):
                dx = self.path[i][0] - self.path[i - 1][0]
                dy = self.path[i][1] - self.path[i - 1][1]
                dist_parcourue += (dx ** 2 + dy ** 2) ** 0.5

            # Retourner la distance totale parcourue
            return dist_parcourue

    def attack(self, health):
        return health - self.damage
