import pygame
import os



WIN_WIDTH = 800
WIN_HEIGHT = 600

GEN = 0
SCORE = 0

BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "jjbg.png")), (800,600))


class Background:
    """
    Represnts the moving floor of the game
    """
    global SCORE
    VEL = 8
    WIDTH = BG_IMG.get_width()
    IMG = BG_IMG

    def __init__(self, y):
        """
        Initialize the object
        :param y: int
        :return: None
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self):
        """
        move floor so it looks like its scrolling
        :return: None
        """
        inc = SCORE//3
        
        self.x1 -= (self.VEL + inc)
        self.x2 -= (self.VEL + inc)
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self, win):
        """
        Draw the floor. This is two images that move together.
        :param win: the pygame surface/window
        :return: None
        """
        win.blit(self.IMG, (self.x1, self.y))
        win.blit(self.IMG, (self.x2, self.y))