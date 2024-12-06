import pygame


class Mob:
    MOB_PROPERTIES = {
        'Soldier': {'health': 50, 'damage': 10, 'reward': 5, 'speed': 5, 'size': (64, 64),},
        'Captain': {'health': 100, 'damage': 25, 'reward': 10, 'speed': 5, 'size': (64, 64),},
        'Sergeant': {'health': 150, 'damage': 35, 'reward': 20, 'speed': 5, 'size': (64, 64),},
        'Tank': {'health': 500, 'damage': 50, 'reward': 40, 'speed': 1, 'size': (64, 64),},
        'Bomber': {'health': 300, 'damage': 40, 'reward': 60, 'speed': 2, 'size': (64, 64),}
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

        # Créer le rect et centrer le mob sur les coordonnées du chemin
        self.rect = pygame.Rect(0, 0, width, height)
        self.rect.center = path[0]
        self.texture=pygame.image.load(f"Textures/{category}.png")
        self.active = True

    def draw(self, surf):
        surf.blit(self.texture, self.rect.topleft)

    def delete(self):
        self.active = False
        self.path = None
        self.rect = None

    def move(self):
        """
        Alan: Fait bouger le mob par une succession de coordonnées jusqu'à la fin du chemin.
        :return: True si le mob a atteint l'arrivée, False sinon (sert pour déduire la vie du joueur
        si le mob arrive au bout du chemin)
        """
        if self.path_index < len(self.path) - 1:                    #Alan: vérifie si le mob est arrivé au bout du chemin
            target = self.path[self.path_index + 1]                 #Alan: le mob prend en cible les prochaines coordonnées qu'il doit atteindre
            dx, dy = (target[0] - self.rect.centerx, target[1]
                                - self.rect.centery)                #Alan: calcule la distance en abscisse et en ordonnée qui sépare le mob du prochain point

            dist = (dx ** 2 + dy ** 2) ** 0.5                       #Alan: calcule la distance globale entre le mob et le prochain point
            move_dist = min(self.speed, dist)                       #Alan: pour éviter qu'il dépasse le point cible et qu'il se bloque

            if dist == 0:
                self.path_index += 1            #Alan: permet au mob de cibler le prochain point de path
                return False
            else:
                self.rect.centerx += move_dist * dx / dist  #Alan: fait bouger le mob en abscisse
                self.rect.centery += move_dist * dy / dist  #Alan: fait bouger le mob en ordonnée
                return False

        else:
            self.delete() #Alan: on détruit l'entité si elle a atteint la fin du chemin
            return True

    def attack(self, health):
        """
        Alan:
        :param health: vie restante du joueur
        :return: le reste de la vie du joueur après l'attaque du mob
        """
        return health - self.damage
