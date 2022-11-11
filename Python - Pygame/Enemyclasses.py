
from this import d


class Enemy:
    def __init__(self, rect, icon, behaviorA, behaviorB, behaviorC):
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.icon = icon
        self.behaviorA = behaviorA
        self.behaviorB = behaviorB
        self.behaviorC = behaviorC

    def update(self) :
        self.rect.x += 5
        if self.rect.left > SCREEN_W:
            self.rect.right = 0
    
    def split(self):
        print("the object splits into two here")

    def speed(self):
        print("the enemy speeds up here")


