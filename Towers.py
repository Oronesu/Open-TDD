import pygame
import Bullet

TICKS_PER_SECOND = 60

class Tower:
    TOWER_PROPERTIES = {
        'Sniper': {'dmg': 25, 'attack_speed': 2, 'prix': 50, 'range': 200, 'isPlaced': False, 'size': (64, 64)},
        'Flamethrower': {'dmg': 20, 'attack_speed': 5, 'prix': 50, 'range': 100, 'isPlaced': False, 'size': (64, 64)},
        'Missile': {'dmg': 200, 'attack_speed': 0.1, 'prix': 50, 'range': 500, 'isPlaced': False, 'size': (64, 64)},
        'Minigun': {'dmg': 20, 'attack_speed': 10, 'prix': 50, 'range': 100, 'isPlaced': False, 'size': (64, 64)}
    }

    def __init__(self, x, y, category):
        self.category = category
        properties = self.TOWER_PROPERTIES.get(category)
        self.dmg = properties['dmg']
        self.atk_spd = properties['attack_speed']
        self.prix = properties['prix']
        width, height = properties['size']
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
        self.range = properties['range']
        self.isPlaced = properties['isPlaced']
        self.attack_cooldown = 0
        self.texture = pygame.image.load(f'Textures/{category}.png')
        self.texture_top = pygame.image.load(f'Textures/{category}_top.png')
        self.cooldown_time = TICKS_PER_SECOND / self.atk_spd
        self.active = True
        self.bullets = []
        self.target = None

    def draw(self, surf):
        surf.blit(self.texture, self.rect.topleft)
        surf.blit(self.texture_top, self.rect.topleft)
        for bullet in self.bullets:
            bullet.draw(surf)

    def draw_phantom(self, surf):
        phantom_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        phantom_surface.set_alpha(128)
        phantom_surface.blit(self.texture, (0, 0))
        phantom_surface.blit(self.texture_top, (0, 0))
        surf.blit(phantom_surface, self.rect.topleft)
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


    def attack_mob(self, mobs, money):
        self.update_bullets(mobs)
        mobs_in_range= self.in_range(mobs)
        if mobs_in_range:
            self.target=mobs_in_range[0]

        if self.attack_cooldown <= 0 and self.target:
            self.target.health -= self.dmg
            print(self.target.health)
            self.attack_cooldown = self.cooldown_time
            if self.target.health <= 0:
                money += self.target.reward
                self.target.delete()
                self.target = None
            else:
                start_pos = (self.rect.centerx, self.rect.centery)
                target_pos = (self.target.rect.centerx, self.target.rect.centery)
                bullet = Bullet.Bullet(start_pos, target_pos, self.dmg, 30)
                self.bullets.append(bullet)
        self.update_cooldown()
        return money

    def update_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1

    def update_bullets(self, mobs):
        for bullet in self.bullets:
            bullet.move()
            for mob in mobs:
                if mob.rect is not None and bullet.rect.colliderect(mob.rect):
                    self.bullets.remove(bullet)
                    break
