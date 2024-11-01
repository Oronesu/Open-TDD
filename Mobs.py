import pygame


class Mob:
    def __init__(self, path, width, height, color):
        self.rect = pygame.Rect(path[0][0], path[0][1], width, height)
        self.color = color
        self.path = path
        self.path_index = 0

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect)

    def move(self):
        if self.path_index < len(self.path)-1:
            target = self.path[self.path_index+1] #On cible la prochain
            dx,dy=target[0]-self.rect.x,target[1]-self.rect.y
            dist=(dx**2+dy**2)**0.5
            if(dist<=5):
                self.path_index+=1
            else:
                self.rect.x+=5*dx/dist
                self.rect.y+=5*dy/dist
        else:
            self.path_index=0





