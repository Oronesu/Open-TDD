import pygame
class Tour:
    def __init__(self,x,y,width,height,color):
        self.rect=pygame.Rect(x,y,width,height)
        self.color=color

    def draw(self,surf):
        pygame.draw.rect(surf,self.color,self.rect)


