import pygame
import Bullet

TICKS_PER_SECOND = 60

class Tower:
    TOWER_PROPERTIES = {
        'Sniper': {'dmg': 25, 'attack_speed': 2, 'prix' : 50, 'range': 200, 'isPlaced': False, 'size': (45, 45), 'color': (255, 0, 0)},
        'Lance-flammes': {'dmg': 20, 'attack_speed': 5,  'prix' : 50, 'range': 100, 'isPlaced': False, 'size': (45, 45), 'color': (255, 255, 0)},
        'Mortier': {'dmg': 200, 'attack_speed': 0.1, 'prix' : 50, 'range': 500, 'isPlaced': False, 'size': (45, 45), 'color': (0, 255, 0)},
        'Minigun': {'dmg': 20, 'attack_speed': 10, 'prix' : 50, 'range': 100, 'isPlaced': False, 'size': (45, 45), 'color': (238, 130, 238)}
    }

    def __init__(self, x, y, category):
        self.category = category
        properties = self.TOWER_PROPERTIES.get(category)
        self.dmg = properties['dmg']
        self.atk_spd = properties['attack_speed']
        self.prix = properties['prix']
        width, height = properties['size']
        self.rect = pygame.Rect(x, y, width, height)
        self.color = properties['color']
        self.range = properties['range']
        self.isPlaced = properties['isPlaced']
        self.attack_cooldown = 0

        # Convertir attack_speed (attaques par seconde) en nombre de ticks entre les attaques
        self.cooldown_time = TICKS_PER_SECOND / self.atk_spd
        self.active = True
        self.bullets = []

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)
        for bullet in self.bullets:
            bullet.draw(surf)

    def draw_phantom(self, surf):
        phantom_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        phantom_surface.set_alpha(128)
        pygame.draw.rect(phantom_surface, self.color, phantom_surface.get_rect())
        surf.blit(phantom_surface, (self.rect.x, self.rect.y))

        # Dessiner le cercle de portée en jaune
        center = (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2)
        pygame.draw.circle(surf, (255, 255, 0), center, self.range, 1)

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

    def attack_mob(self, mob, money):
        if self.attack_cooldown <= 0:
            mob.health -= self.dmg
            print(mob.health)
            self.attack_cooldown = self.cooldown_time  # Réinitialiser le cooldown d'attaque
            if mob.health <= 0:
                money += mob.reward
                mob.delete()  # Supprimer le mob si sa vie est <= 0
            else:
                # Créer un projectile vers le mob
                start_pos = (self.rect.centerx, self.rect.centery)
                target_pos = (mob.rect.centerx, mob.rect.centery)
                bullet = Bullet.Bullet(start_pos, target_pos, self.dmg, 40)
                self.bullets.append(bullet)

        return money


    def update_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def update_bullets(self, mobs):
        for bullet in self.bullets:
            bullet.move()
            for mob in mobs:
                if mob.rect is not None and bullet.rect.colliderect(mob.rect):
                    mob.health -= bullet.dmg
                    self.bullets.remove(bullet)
                    if mob.health <= 0:
                        mob.delete()
                    break
