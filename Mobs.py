import pygame

class Mob:
    def __init__(self, path, category):
        self.category = category
        self.path = path
        self.path_index = 0
        if self.category == 'Soldier':
            self.health = 50
            self.absorb = 0
            self.damage = 10
            self.speed = 20
            self.rect = pygame.Rect(path[0][0], path[0][1], 15, 15)
            self.color = (255, 0, 0)
        if self.category == 'Captain':
            self.health = 100
            self.absorb = 0, 2
            self.damage = 25
            self.speed = 35
            self.rect = pygame.Rect(path[0][0], path[0][1], 15, 15)
            self.color = (255, 255, 0)
        if self.category == 'Sergeant':
            self.health = 150
            self.absorb = 0, 3
            self.damage = 35
            self.speed = 35
            self.rect = pygame.Rect(path[0][0], path[0][1], 15, 15)
            self.color = (255, 0, 0)
        if self.category == 'Tank':
            self.health = 500
            self.absorb = 0, 7
            self.damage = 50
            self.speed = 10
            self.rect = pygame.Rect(path[0][0], path[0][1], 15, 15)
            self.color = (128, 128, 128)
        if self.category == 'Boss':
            self.health = 300
            self.absorb = 0, 5
            self.damage = 40
            self.speed = 25
            self.rect = pygame.Rect(path[0][0], path[0][1], 15, 15)
            self.color = (238, 130, 238)


    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

    def delete(self):
        self.active = False



    def move(self):
        if self.path_index < len(self.path)-1:
            target = self.path[self.path_index+1] #On cible la prochain
            dx,dy=target[0]-self.rect.x,target[1]-self.rect.y
            dist=(dx**2+dy**2)**0.5
            if(dist<=5):
                self.path_index+=1
            else:
                self.rect.x+=50*dx/dist
                self.rect.y+=50*dy/dist
        else:
            self.active=False
            self.delete()



