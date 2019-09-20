import pygame
import neat
import time
import os
import random
import pickle


from barry import Barry
from zapper import Zapper
from background import Background



pygame.font.init()

WIN_WIDTH = 800
WIN_HEIGHT = 600

GEN = 0
SCORE = 0

ANIM_IMGS = [pygame.transform.scale(pygame.image.load(os.path.join("imgs", "sprites", "walk1.png")), (85,110)),
              pygame.transform.scale(pygame.image.load(os.path.join("imgs", "sprites", "walk2.png")),(85,110)),
              pygame.transform.scale(pygame.image.load(os.path.join("imgs", "sprites", "walk3.png")),(85,110)),
              pygame.transform.scale(pygame.image.load(os.path.join("imgs", "sprites", "thrust.png")),(85,110)),
              pygame.transform.scale(pygame.image.load(os.path.join("imgs", "sprites", "fall.png")),(85,110))]
              
ZAP_IMGS = [pygame.image.load(os.path.join("imgs", "zappers","vertical1.png")),
            pygame.image.load(os.path.join("imgs","zappers", "horizontal1.png")),
            pygame.image.load(os.path.join("imgs", "zappers","vertical2.png")),
            pygame.image.load(os.path.join("imgs", "zappers","horizontal2.png")),
            pygame.image.load(os.path.join("imgs", "zappers","right-left2.png")),
            pygame.image.load(os.path.join("imgs", "zappers","right-left3.png"))]


BG_IMG = pygame.transform.scale(pygame.image.load(os.path.join("imgs", "jjbg.png")), (800,600))



STAT_FONT = pygame.font.SysFont("comicsans", 50)



def draw_window(win, barrys, zappers, score, gen, bg):
    global SCORE
    bg.draw(win)#for bg scroll
    for zapper in zappers:
        zapper.draw(win)

    

    text = STAT_FONT.render("Score: " + str(SCORE), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    text = STAT_FONT.render("Gen: " + str(gen), 1, (255,255,255))
    win.blit(text, (10,10))
    
    for barry in barrys:
        barry.draw(win)#animation loop

    pygame.display.update()



  
def main(genomes, config):#eval
    global GEN
    global SCORE
    
    GEN+=1
    nets = []
    ge = []
    barrys = []
    

    for _, g in genomes:#list index same
        net = neat.nn.FeedForwardNetwork.create(g,config)
        nets.append(net)
        barrys.append(Barry(230,420))
        g.fitness = 0
        ge.append(g)

    bg= Background(0)

    zappers = [Zapper(800, height = 400, img_no = 0)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    
    

    score = 0
    SCORE = score


    
    run = True
    while run:
    
        clock.tick(45)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        
        zapper_ind = 0
        if len(barrys) > 0:
            if len(zappers) > 1 and barrys[0].x > zappers[0].x + zappers[0].img.get_width():#if zaps were passed
                zapper_ind = 1
        else:
            run = False
            break
        
        for x, barry in enumerate(barrys):
            barry.move()
            ge[x].fitness += 0.1

    
            
#ZAP INDEX indicates the zapper that the current chars are on. [0 or 1] because max 2 zaps on screen at any time

            
            #distance from char to floor and ceiling
            top_dist_barry = abs(barry.y - 80)
            bot_dist_barry = abs(barry.y - 420)
            
            #distance from floor/ceiling to top and bottom of zappers
            top_dist_zap = abs(zappers[zapper_ind].top - 80)
            bot_dist_zap = abs(zappers[zapper_ind].bottom - 420)

            #distance from char to top and bottom of zappers
            bz_top = abs(barry.y - zappers[zapper_ind].top)
            bz_bot = abs(barry.y - zappers[zapper_ind].bottom)


            

            
            output = nets[barrys.index(barry)].activate((barry.y, bz_top, bz_bot))
                            #distance from ceiling to top zap point
                            #distance from floor to bottom zap point
                            #char height
                            #zap top/bottom height
            
            if output[0] > 0.5:
                if top_dist_zap>bot_dist_zap:
                    barry.jump()#movement options
                
                

            
            

            
            
                                          
                    
                                           

        add_zapper = False

        bg.move()
        rem = []
        for zapper in zappers:#signal for generating new zappers
            for x, barry in enumerate(barrys):
                if zapper.collide(barry):
                    ge[x].fitness -=1
                    barrys.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                if not zapper.passed and zapper.x < barry.x:
                    zapper.passed = True
                    add_zapper = True
                
            if zapper.x + zapper.img.get_width() < 0:
                rem.append(zapper)
            
            zapper.move() 
        if add_zapper:
            zappers.append(Zapper(800, height = random.randrange(0,400), img_no = random.randrange(0, 5)))
            for g in ge:
                g.fitness += 5
            SCORE +=1
        for r in rem:#removing the zappers
            zappers.remove(r)
            
        draw_window(win, barrys, zappers, SCORE, GEN, bg)
        # break if score gets large enough
        if score > 50:
            pickle.dump(nets[0],open("best.pickle", "wb"))
            break

               
        
def run(config_path):
    #running through config txt file, modified
    config  = neat.config.Config(neat.DefaultGenome,
                                 neat.DefaultReproduction,
                                 neat.DefaultSpeciesSet,
                                 neat.DefaultStagnation,
                                 config_path)

    #popluation
    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main,50)#run main thru 50 gens - fitness

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
