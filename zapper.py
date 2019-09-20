import random
import pygame
import os



GEN = 0
SCORE = 0



              
ZAP_IMGS = [pygame.image.load(os.path.join("imgs", "zappers","vertical1.png")),
            pygame.image.load(os.path.join("imgs","zappers", "horizontal1.png")),
            pygame.image.load(os.path.join("imgs", "zappers","vertical2.png")),
            pygame.image.load(os.path.join("imgs", "zappers","horizontal2.png")),
            pygame.image.load(os.path.join("imgs", "zappers","right-left2.png")),
            pygame.image.load(os.path.join("imgs", "zappers","right-left3.png"))]



class Zapper:
    global SCORE
    GAP = 200
    VEL = 8

    def __init__(self, x, height = 0, img_no = random.randint(0,7)):#always at end of screen, need to vary the Y
        self.x = x
        self.height = height

        self.top = 0
        self.bottom = 0

        self.img = ZAP_IMGS[img_no]

        self.passed = False
        self.set_height()

    def move(self):
        inc = SCORE//3 #accelerate every 5 zappers
        self.x -= (self.VEL + inc)

    def draw(self, win):
        win.blit(self.img, (self.x, self.height))

    def collide(self, barry):#no box collisions, visually accurate 
        barry_mask = barry.get_mask()
        mask = pygame.mask.from_surface(self.img)
        offset = (self.x - barry.x, 0 - round(barry.y - self.height))


        point = barry_mask.overlap(mask, offset)
        if point:
            return True
        return False
    def set_height(self):
        """
        set the height of the zapper, from the top of the screen
        :return: None
        """
        if self.height == 0:
            self.height = random.randrange(80,375)
        self.top = self.height
        self.bottom = self.height + self.img.get_height()
