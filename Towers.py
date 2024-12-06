import pygame
import Bullet

TICKS_PER_SECOND = 60

class Tower:
    TOWER_PROPERTIES = {
        'Sniper': {'dmg': 25, 'attack_speed': 2, 'prix': 50, 'range': 200, 'size': (64, 64)},
        'Flamethrower': {'dmg': 20, 'attack_speed': 5, 'prix': 50, 'range': 100, 'size': (64, 64)},
        'Missile': {'dmg': 200, 'attack_speed': 0.1, 'prix': 50, 'range': 500, 'size': (64, 64)},
        'Minigun': {'dmg': 20, 'attack_speed': 10, 'prix': 50, 'range': 100, 'size': (64, 64)}
    }

    def __init__(self, x, y, category, level=1):
        self.category = category
        properties = self.TOWER_PROPERTIES.get(category)

        # Attributs améliorables
        self.level = level
        self.dmg = properties['dmg'] * (1.5 ** (level - 1))                 # Alan: les dégâts augmente avec le niveau
        self.atk_spd = properties['attack_speed'] * (1.5 ** (level - 1))    # Alan: la vitesse d'attaque augmente avec le niveau
        self.range = properties['range'] * (1.5 ** (level - 1))             # Alan: la portée augmente avec le niveau
        self.prix = properties['prix']

        # Attributs pour affichage
        width, height = properties['size']
        self.rect = pygame.Rect(x - width // 2, y - height // 2, width, height)  # Darren: position et taille de la tour
        self.isPlaced = False
        self.texture = pygame.image.load(f'Textures/{category}.png')            # Darren: texture de la base de la tourelle
        self.texture_top = pygame.image.load(f'Textures/{category}_top.png')    # Darren: texture du "haut" de la tourelle
        self.active = True

        # Attributs pour attaque
        self.attack_cooldown = 0
        self.cooldown_time = TICKS_PER_SECOND / self.atk_spd  # Darren: temps de rechargement entre deux attaques
        self.bullets = []
        self.target = None

    """Partie affichage"""

    def draw(self, surf):
        surf.blit(self.texture, self.rect.topleft)
        surf.blit(self.texture_top, self.rect.topleft)
        for bullet in self.bullets:
            bullet.draw(surf)  # Darren: dessine les balles tirées par la tour

    def draw_phantom(self, surf):
        phantom_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        phantom_surface.set_alpha(128)                                  # Darren: rend l'image semi-transparente
        phantom_surface.blit(self.texture, (0, 0))
        phantom_surface.blit(self.texture_top, (0, 0))
        surf.blit(phantom_surface, self.rect.topleft)                   # Darren: dessine l'ombre de la tour
        center = (self.rect.x + self.rect.width // 2, self.rect.y + self.rect.height // 2)
        pygame.draw.circle(surf, (255, 255, 0), center, self.range, 1)  # Darren: dessine le cercle de portée de la tour

    def is_within_bounds(self, width, height):
        return 0 <= self.rect.x <= width - self.rect.width and 0 <= self.rect.y <= height - self.rect.height  # Darren: vérifie si la tour est dans les limites


    """Partie attaques"""

    def in_range(self, mobs):
        mobs_in_range = []
        for mob in mobs:
            if mob.rect is not None:
                distance = ((mob.rect.x - self.rect.x) ** 2 + (mob.rect.y - self.rect.y) ** 2) ** 0.5
                if distance < self.range:               # Darren: vérifie si le mob est dans la portée de la tour
                    mobs_in_range.append(mob)
        return mobs_in_range

    def attack_mob(self, mobs, money):
        self.update_bullets(mobs)
        mobs_in_range = self.in_range(mobs)
        if mobs_in_range:
            self.target = mobs_in_range[0]              # Darren: sélectionne le premier mob dans la portée comme cible

        if self.attack_cooldown <= 0 and self.target:
            self.target.health -= self.dmg              # Darren: inflige des dégâts à la cible
            self.attack_cooldown = self.cooldown_time   # Darren: réinitialise le temps de rechargement
            if self.target.health <= 0:
                money += self.target.reward             # Darren: ajoute la récompense pour avoir éliminé la cible
                self.target.delete()                    # Darren: supprime la cible si la cible est éliminée
                self.target = None
            else:
                start_pos = (self.rect.centerx, self.rect.centery)
                target_pos = (self.target.rect.centerx, self.target.rect.centery)
                bullet = Bullet.Bullet(start_pos, target_pos, self.dmg, 30)  # Darren: crée une nouvelle balle tirée
                self.bullets.append(bullet)
        self.update_cooldown()
        return money  # Darren: retourne le montant d'argent mis à jour

    def update_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1  # Darren: réduit le temps de rechargement

    def update_bullets(self, mobs):
        for bullet in self.bullets:
            bullet.move()  # Darren: déplace la balle
            for mob in mobs:
                if mob.rect is not None and bullet.rect.colliderect(mob.rect):
                    self.bullets.remove(bullet)  # Darren: supprime la balle si elle touche un mob
                    break

    """Partie upgrades"""
    #Alan:
    #Gestion des améliorations
    def upgrade(self):
        self.level += 1
        self.dmg *= 1.5
        self.atk_spd *= 1.5
        self.range *= 1.5
        self.cooldown_time = TICKS_PER_SECOND / self.atk_spd
