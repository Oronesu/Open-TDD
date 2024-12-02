import pygame

TICKS_PER_SECOND = 60

class Tower:
    TOWER_PROPERTIES = {
        'Sniper': {'dmg': 10, 'attack_speed': 2, 'range': 50, 'size': (30, 60), 'color': (255, 0, 0)},
        'Lance-flammes': {'dmg': 25, 'attack_speed': 1.5, 'range': 50, 'size': (35, 70), 'color': (255, 255, 0)},
        'Mortier': {'dmg': 35, 'attack_speed': 0.8, 'range': 50, 'size': (45, 90), 'color': (0, 255, 0)},
        'Minigun': {'dmg': 40, 'attack_speed': 10, 'range': 50, 'size': (40, 80), 'color': (238, 130, 238)}
    }

    def __init__(self, x, y, category):
        self.category = category
        properties = self.TOWER_PROPERTIES.get(category)
        self.dmg = properties['dmg']
        self.atk_spd = properties['attack_speed']
        width, height = properties['size']
        self.rect = pygame.Rect(x, y, width, height)
        self.color = properties['color']
        self.range = properties['range']
        self.attack_cooldown = 0

        # Convertir attack_speed (attaques par seconde) en nombre de ticks entre les attaques
        self.cooldown_time = TICKS_PER_SECOND / self.atk_spd
        self.active = True

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

    def draw_phantom(self, surf):
        phantom_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        phantom_surface.set_alpha(128)
        pygame.draw.rect(phantom_surface, self.color, phantom_surface.get_rect())
        surf.blit(phantom_surface, (self.rect.x, self.rect.y))

    def is_within_bounds(self, width, height):
        return 0 <= self.rect.x <= width - self.rect.width and 0 <= self.rect.y <= height - self.rect.height

    def in_range(self, mobs):
        mobs_in_range = []
        for mob in mobs:
            if mob.rect is not None:
                distance = ((mob.rect.x - self.rect.x) ** 2 + (mob.rect.y - self.rect.y) ** 2)**0.5
                if distance < self.range:
                    mobs_in_range.append(mob)
        return mobs_in_range

    def first_in_range(self, mobs):
        mobs_in_range = self.in_range(mobs)
        if not mobs_in_range:
            return None
        return max(mobs_in_range, key=lambda mob: mob.dist_travelled())

    def attack_mob(self, mob):
        if self.attack_cooldown <= 0:
            mob.health -= self.dmg
            print(mob.health)
            self.attack_cooldown = self.cooldown_time  # Réinitialiser le cooldown d'attaque
            if mob.health <= 0:
                mob.delete()  # Supprimer le mob si sa vie est <= 0

    def update_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
