import pygame
import os



GEN = 0
SCORE = 0

ANIM_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "sprites", "walk1.png")), (85,110)),
              pygame.transform.scale(pygame.image.load(os.path.join("imgs", "sprites", "walk2.png")),(85,110)),
              pygame.transform.scale(pygame.image.load(os.path.join("imgs", "sprites", "walk3.png")),(85,110)),
              pygame.transform.scale(pygame.image.load(os.path.join("imgs", "sprites", "thrust.png")),(85,110)),
              pygame.transform.scale(pygame.image.load(os.path.join("imgs", "sprites", "fall.png")),(85,110))]
              



class Barry:
    IMGS = ANIM_IMGS
    ANIMATION_TIME= 5
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0
        self.img = self.IMGS[0]
        self.thrust = False
        
    def move(self):
        self.tick_count += 1
        if self.vel < -10:
            self.vel = -10
    
       # if self.thrust:
        #    self.vel -= .5
         #   self.height = self.y
        
        #gravity equation, jump; the "+" is there because increasing Y is going down --> this is good
        d = self.vel*self.tick_count + 1.5*self.tick_count**2
        
        if d>= 16:#cap out at 16, to make it move slower, acceleration
            d = 16
        if d<0:#lower cap
            d-=2
        
        self.y = self.y + d #applying grav to char

        #floor and ceiling

        if self.y>=420:#change to barry's height
            self.y = 420
            
        if self.y<=80:
            self.y = 80
            
    def jump(self):
        """
        make the char jump
        :return: None
        """
        self.vel = -10.5
        self.tick_count = 0
        self.height = self.y

    def thrust_on(self):
        self.thrust = True
        self.tick_count = 0
        
    def thrust_off(self):
        self.thrust = False
        self.tick_count = 0
                
    def draw(self, win):
        #IF: character is on the ground
            #DO: running animation DONE
        #IF: thrust is on
            #DO: jetpack sprite
        #ELSE: standard sprite (falling)

        
        self.img_count +=1
        #IF MAN IS ON THE GROUND: y = 440
        if not self.thrust and (self.y >=420):
            if self.img_count < self.ANIMATION_TIME:
                self.img = self.IMGS[0]
            elif self.img_count < self.ANIMATION_TIME*2:
                self.img = self.IMGS[1]
            elif self.img_count < self.ANIMATION_TIME*3:
                self.img = self.IMGS[2]
            elif self.img_count < self.ANIMATION_TIME*4:
                self.img = self.IMGS[1]
            elif self.img_count < self.ANIMATION_TIME*4 +1:
                self.img = self.IMGS[0]
                self.img_count = 0

        else:
            if self.thrust:
                self.img = self.IMGS[3]
            else:
                self.img = self.IMGS[4]
                
            



            
        
        win.blit(self.img, (self.x,self.y))
            
        
    #collision mask
    def get_mask(self):
        return pygame.mask.from_surface(self.img)