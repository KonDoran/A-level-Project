import pygame
import random
import os
import sys

current_path = os.path.dirname(__file__)#where this file is located
image_path = os.path.join(current_path, 'images')
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (255,20,147)
PURPLE = (75,0,130)
ORANGE = (255,69,0)
BACKGROUND_IMAGE = pygame.image.load(os.path.join(image_path, 'background.png'))
pygame.init()

# Set the width and height of the screen [width, height]
size = (1200, 1000)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tile Movement Game")

#Loop until the user clicks the close button.
done = False
    
    # Used to manage how fast the screen updates
clock = pygame.time.Clock()







class Game(object):
    def __init__(self):
        self.score = 0
        self.game_over = False
        self.level = 0
        # Create a list of all sprites
        self.all_sprites_group = pygame.sprite.Group()
        self.outsidewall_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.innerwall_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.key_group = pygame.sprite.Group()
        self.portal_group = pygame.sprite.Group()
        self.door_group = pygame.sprite.Group()
        self.sword_group = pygame.sprite.Group()
        self.levelcomplete = [False, False, False, False, False]
        self.level1 = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
            [1,0,0,0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,0,0,0,6],
            [1,0,0,0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,6],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        
            ]

        self.level2 = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
            [1,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,0,2,0,0,2,2,2,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,2,0,0,2,2,2,1],
            [1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,0,2,2,2,2,2,2,2,2,0,2,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,2,2,0,0,0,0,2,2,2,2,0,0,0,0,0,0,1],
            [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
            [6,0,0,0,0,2,2,2,2,2,0,0,0,0,2,2,2,2,2,2,2,2,0,0,6],
            [6,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,6],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
            [1,2,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,2,2,2,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
            [1,0,0,0,0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        
            ]

        self.level3 = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
            [1,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,0,2,0,0,2,2,2,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,2,0,0,2,2,2,1],
            [1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,0,2,2,2,2,2,2,2,2,0,2,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,2,2,0,0,0,0,2,2,2,2,0,0,0,0,0,0,1],
            [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
            [6,0,0,0,0,2,2,2,2,2,0,0,0,0,2,2,2,2,2,2,2,2,0,0,6],
            [6,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,6],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
            [1,2,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,2,2,2,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
            [1,0,0,0,0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        
            ]

        self.level4 = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
            [1,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,0,2,0,0,2,2,2,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,2,0,0,2,2,2,1],
            [1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,0,2,2,2,2,2,2,2,2,0,2,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,2,2,0,0,0,0,2,2,2,2,0,0,0,0,0,0,1],
            [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
            [6,0,0,0,0,2,2,2,2,2,0,0,0,0,2,2,2,2,2,2,2,2,0,0,6],
            [6,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,6],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
            [1,2,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,2,2,2,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
            [1,0,0,0,0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        
            ]

        self.level5 = [
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
            [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
            [1,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,0,2,0,0,2,2,2,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,2,0,0,2,2,2,1],
            [1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,0,2,2,2,2,2,2,2,2,0,2,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,2,2,0,0,0,0,2,2,2,2,0,0,0,0,0,0,1],
            [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
            [6,0,0,0,0,2,2,2,2,2,0,0,0,0,2,2,2,2,2,2,2,2,0,0,6],
            [6,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,6],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
            [1,2,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,2,2,2,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
            [1,0,0,0,0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        
            ]
                        
        self.levels = [self.level1, self.level2, self.level3,self.level4, self.level5]
        self.levelsetup()
        self.player = Player(WHITE, 40, 40,40,500,100,0,0,0)
        self.all_sprites_group.add(self.player)
        self.player_group.add(self.player)

        
    def levelsetup(self):
    
        if (self.level + 1) % 5 == 0:
            enemies = 0
            while enemies != ((2*(self.level+1)) + 1):
                xpos = random.randint(1,23)
                ypos = random.randint(1,23)
                if self.levels[self.level][xpos][ypos] !=1 and self.levels[self.level][xpos][ypos] != 2:
                    self.levels[self.level][xpos][ypos] = random.randint(3,5)
                    enemies = enemies +1
        else:
            enemies = 0
            while enemies != ((2*(self.level+1)) + 1):
                xpos = random.randint(1,23)
                ypos = random.randint(1,23)
                if self.levels[self.level][xpos][ypos] !=1 and self.levels[self.level][xpos][ypos] != 2:
                    self.levels[self.level][xpos][ypos] = random.randint(3,4)
                    enemies = enemies +1
                

        for j in range(len(self.levels[self.level])):
            for i in range(len(self.levels[self.level][j])):
                #print(i,j)
                char = self.levels[self.level][j][i]
                if char == 1:
                    self.outsidewall = Wall(RED,40,40,i*40, j*40, i, j)
                    self.all_sprites_group.add(self.outsidewall)
                    self.wall_group.add(self.outsidewall)
                    self.outsidewall_group.add(self.outsidewall)
                if char == 2:
                    self.innerwall = InnerWall(RED,40,40,i*40, j*40, i, j)
                    self.all_sprites_group.add(self.innerwall)
                    self.wall_group.add(self.innerwall)
                    self.innerwall_group.add(self.innerwall)
                if char == 3:
                    if self.levelcomplete[self.level] == False:
                        self.enemy = BowEnemy(random.randint(0,10),40,40, i*40, j*40, 40)
                        self.all_sprites_group.add(self.enemy)
                        self.enemy_group.add(self.enemy)
                if char == 4:
                    if self.levelcomplete[self.level] == False:
                        self.enemy = MeleeEnemy(random.randint(0,10),40,40, i*40, j*40, 40)
                        self.all_sprites_group.add(self.enemy)
                        self.enemy_group.add(self.enemy)
                if char == 5:
                    if self.levelcomplete[self.level] == False:
                        self.boss = BossEnemy(random.randint(0,10),80,80, i*40, j*40, 40)
                        self.all_sprites_group.add(self.boss)
                        self.enemy_group.add(self.boss)
                if char == 6:
                    if self.levelcomplete[self.level] == False:
                        self.door = Door(PURPLE,40,40,i*40, j*40, i, j)
                        self.all_sprites_group.add(self.door)
                        self.wall_group.add(self.door)
                        self.door_group.add(self.door)

    def leveldelete(self):
        self.all_sprites_group.empty()
        self.wall_group.empty()
        self.enemy_group.empty()
        self.all_sprites_group.add(self.player)
        self.all_sprites_group.update()

    #endprocess
    def eventprocess(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False            


    def getscore(self):
        return self.score
    #endprocess

    def runlogic(self):
        if not self.game_over:
            #print(self.levelcomplete)
            # Move all the sprites
            self.all_sprites_group.update()
            if len(self.player_group) == 0:
                self.game_over = True
            
            if self.player.rect.x > 1000:
                if self.level != (len(self.levels)-1):
                    self.levelcomplete[self.level] = True
                    self.level += 1
                    self.player.gamekeys = 0
                    self.player.rect.x = 40
                    self.leveldelete()
                    self.levelsetup()
                else:
                    self.score += (self.player.health*100)+100
                    self.game_over = True
                    
            elif self.player.rect.x < 0:
                self.levelcomplete[self.level] = True
                print(self.levelcomplete)
                self.level -= 1
                self.leveldelete()
                self.player.rect.x = 960
                self.levelsetup()
                


    def display(self, screen):
        # background image.
        screen.fill(BLACK)
        #screen.blit(BACKGROUND_IMAGE,(0,0))
        if self.game_over:
            screen.fill(BLACK)
            font1 = pygame.font.Font(None, 74)
            font2 = pygame.font.Font(None, 48)
            text = font1.render('GAME OVER', 1, WHITE)
            score = font2.render('SCORE:'+str(self.getscore()), 1, WHITE)
            screen.blit(text, (440,300))
            screen.blit(score, (520,500))
        if not self.game_over:
            font = pygame.font.Font(None, 24)
            score = font.render('SCORE:'+str(self.getscore()), 1, WHITE)
            money = font.render('MONEY:'+str(self.player.getmoney()), 1, WHITE)
            keys = font.render('KEYS:'+str(self.player.getkeys()), 1, WHITE)
            screen.blit(score, (1050,500))
            screen.blit(money, (1050,550))
            screen.blit(keys, (1050,600))
            # --- Drawing code should go here
            self.all_sprites_group.draw(screen)
            #endif
        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
    #end procedure
        
        
        
        
        
        
        
        
# Create a Player Class
class Player(pygame.sprite.Sprite):
    #define the constructor for the player
    speed_x = 0
    speed_y = 0
    def __init__(self,color , width, height, x, y, health, score, money, gamekeys):
        #call sprite constructor
        super().__init__()
        #create a sprite
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        #set the position of the sprite
        self.rect = self.image.get_rect()
        self.current_health = 100
        self.maximum_health = health
        self.health_bar_length = 180
        self.health_ratio = self.maximum_health/ self.health_bar_length
        self.score = score
        self.money = money
        self.gamekeys = gamekeys
        self.rect.x = x
        self.rect.y = y
        self.directionx = 0
        self.directiony = 5
        self.previoustime = pygame.time.get_ticks()
        
    #end procedure
    def gethealth(self, amount):
        if self.current_health < self.maximum_health:
            self.current_health += amount
        if self.current_health >= self.maximum_health:
            self.current_health = self.maximum_health
    #endprocedure

    def sethealth(self, newhealth):
        self.health = newhealth
    #endfunction

    def getdamage(self,amount):
        if self.current_health > 0:
            self.current_health -= amount
        if self.current_health <=0:
            self.current_health = 0


    def basic_health(self):
        pygame.draw.rect(screen, (255,0,0), (50,50, self.current_health/self.health_ratio,25))
        print("hi")

    def getscore(self):
        return self.score
    #endprocedure

    def setscore(self, score):
        self.score = score
    #endfunction

    def getkeys(self):
        return self.gamekeys
    #endprocedure

    def setkeys(self, keys):
        self.gamekeys = keys
    #endfunction

    def getmoney(self):
        return self.money
    #endprocedure

    def setmoney(self, money):
        self.money = money
    #endfunction

    def changespeed(self, x, y):
        self.speed_x += x
        self.speed_y += y


    def update(self):
        self.basic_health()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.changespeed(-4,0)
            self.directionx = -6
            self.directiony = 0
        if keys[pygame.K_d]:
            self.changespeed(4,0)
            self.directionx = 6
            self.directiony = 0      
        if keys[pygame.K_w]:
            self.changespeed(0,-4)
            self.directionx = 0
            self.directiony = -6
        if keys[pygame.K_s]:
            self.changespeed(0,4)
            self.directionx = 0
            self.directiony = 6
        if keys[pygame.K_SPACE]:
            self.currenttime = pygame.time.get_ticks()
            if self.currenttime - self.previoustime > 500:
                bullet = Bullet(RED, self.directionx, self.directiony)
                game.bullet_group.add(bullet)
                game.all_sprites_group.add(bullet)
                self.previoustime = self.currenttime
        if keys[pygame.K_e]:
            if len(game.sword_group) == 0:
                sword = Sword(GREEN)
                game.sword_group.add(sword)
                game.all_sprites_group.add(sword)
                


        #end if





        self.move(self.speed_x,self.speed_y)
        self.speed_x = 0
        self.speed_y = 0
        player_hit_group = pygame.sprite.groupcollide(game.player_group, game.enemy_group, False, False)
        for self in player_hit_group:
            self.getdamage(2)
            if self.current_health < 1:
                game.score += 100
                self.kill()
    #end procedure

    def move(self, speedx, speedy):
        #move along x
        self.rect.x += self.speed_x

        wallcollision = pygame.sprite.spritecollide(self,game.wall_group, False)
        for wall in wallcollision:
            if self.speed_x > 0:
                self.rect.right = wall.rect.left
            else:
                self.rect.left = wall.rect.right    
        #move the player up and down the screen
        self.rect.y += self.speed_y
        #check for collision
        wallcollision = pygame.sprite.spritecollide(self, game.wall_group, False) 
        for wall in wallcollision:
            #if there is a collision while moving up then set the speed to 0
            if self.speed_y > 0: 
                #i
                self.rect.bottom = wall.rect.top
            else:
                self.rect.top = wall.rect.bottom
    #end procedure    
#end class

class Bullet(pygame.sprite.Sprite):
    def __init__(self, color, speedx, speedy):
        #Call the sprite constructor
        super().__init__()
        self.image = pygame.Surface([6,4])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.speedx = speedx
        self.speedy = speedy
        self.rect.y = game.player.rect.y + 10
        self.rect.x = game.player.rect.x  + 10

    def update(self):
        self.rect.y += self.speedy
        if pygame.sprite.groupcollide(game.bullet_group, game.wall_group, True, False) == True:
            self.remove()
        self.rect.x += self.speedx
        if pygame.sprite.groupcollide(game.bullet_group, game.wall_group, True, False) == True:
            self.remove()
        

class Sword(pygame.sprite.Sprite):
    def __init__(self, color):
        #call sprite constructor
        super().__init__()
        self.image = pygame.Surface([20,5])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.y = game.player.rect.y + 18
        self.rect.x = game.player.rect.x  + 40

    def update(self):
        self.rect.y = game.player.rect.y + 18
        self.rect.x = game.player.rect.x  + 40
        keys = pygame.key.get_pressed()
        if not keys[pygame.K_e]:
            self.kill()

    def attack(self):
        enemy_hit_group = pygame.sprite.spritecollide(self, game.enemy_group, False)



class Key(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        self.image = pygame.Surface([10,10])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def update(self):
        key_hit_group = pygame.sprite.groupcollide(game.key_group, game.player_group, False, False)
        for self in key_hit_group:
            game.player.gamekeys += 1
            game.score += 50
            self.kill()
            





#class Portal(pygame.sprite.Sprite):
    #def __init__(self,color,x,y):
        #super().__init__()
        #self.image = pygame.Surface([40,40])
        #self.image.fill(color)
        #self.rect = self.image.get_rect()
        #self.rect.y = y
        #self.rect.x = x
    #end procedure    
    #def update(self):
        #pass

class Wall(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, posx, posy):
        #call sprite constructor
        super().__init__()
        #create a sprite
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        #set the position of the sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.positionx = posx
        self.positiony = posy
    #end procedure
    def update(self):
        pass
    #end procedure

    def getpos(self):
        return [self.positionx, self.positiony]

class InnerWall(Wall):

        #wallhits = durability
    pass
    #endprocedure
    def update(self):
        pass
        
class Door(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, posx, posy):
        super().__init__()
        self.image = pygame.Surface([width,height])
        self.image.fill(color)
        #set the position of the sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.positionx = posx
        self.positiony = posy
    #end procedure

    def update(self):
        if  game.player.gamekeys >= ((2*(game.level+1)) + 1):
            self.kill()




class MeleeEnemy(pygame.sprite.Sprite):
    def __init__(self, direction, width, height, x, y, health):
        #call sprite constructor
        super().__init__()
        #create a sprite
        self.image = pygame.Surface([width,height])
        self.image.fill(YELLOW)
        #set the position of the sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health
        self.direction = direction
        self.move = 5
        
    #end procedure
    def update(self):
        
        self.MOVE()
        enemybullet_hit_group = pygame.sprite.groupcollide(game.enemy_group, game.bullet_group, False, True)
        for self in enemybullet_hit_group:
            self.health -= 20
            #print(self.health)
            if self.health < 1:
                game.score += 100
                gamekey = Key(PINK, self.rect.x + 2, self.rect.y + 9)
                game.all_sprites_group.add(gamekey)
                game.key_group.add(gamekey)
                self.kill()
        enemysword_hit_group = pygame.sprite.groupcollide(game.enemy_group, game.sword_group, False, False)
        for self in enemysword_hit_group:
            self.health -= 4

            if self.health < 1:
                game.score += 100
                gamekey = Key(PINK, self.rect.x + 2, self.rect.y + 9)
                game.all_sprites_group.add(gamekey)
                game.key_group.add(gamekey)
                self.kill()
                
    #end procedure


    def MOVE(self):
        if self.direction % 2 == 0:
            self.rect.x += self.move
            wallcollision = pygame.sprite.groupcollide(game.enemy_group,game.wall_group, False,False)
            for wall in wallcollision:
                if self.move > 0:
                    self.rect.right = wall.rect.left
                    self.move = self.move * -1
                else:
                    self.rect.left = wall.rect.right    
                    self.move = self.move * -1
    
    
    
        #move the player up and down the screen
        else:
            self.rect.y += self.move
            #check for collision
            wallcollision = pygame.sprite.groupcollide(game.enemy_group, game.wall_group, False, False) 
            for wall in wallcollision:
                #if there is a collision while moving up then set the speed to 0
                if self.move > 0: 
                    self.rect.bottom = wall.rect.top
                    self.move = self.move * -1
                else:
                    self.rect.top = wall.rect.bottom
                    self.move = self.move * -1


    def gethealth(self):
        return self.health
    #endprocedure

    def sethealth(self, newhealth):
        self.health = newhealth
    #endfunction


class BowEnemy(pygame.sprite.Sprite):
    def __init__(self, direction, width, height, x, y, health):
        #call sprite constructor
        super().__init__()
        #create a sprite
        self.image = pygame.Surface([width,height])
        self.image.fill(ORANGE)
        #set the position of the sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health
        self.direction = direction
        
    #end procedure
    def update(self):
        
        enemybullet_hit_group = pygame.sprite.groupcollide(game.enemy_group, game.bullet_group, False, True)
        for self in enemybullet_hit_group:
            self.health -= 20
            #print(self.health)
                
            if self.health < 1:
                game.score += 100
                gamekey = Key(PINK, self.rect.x + 2, self.rect.y + 9)
                game.all_sprites_group.add(gamekey)
                game.key_group.add(gamekey)
                self.kill()     
        enemysword_hit_group = pygame.sprite.groupcollide(game.enemy_group, game.sword_group, False, False)
        for self in enemysword_hit_group:
            self.health -= 4   

            if self.health < 1:
                game.score += 100
                gamekey = Key(PINK, self.rect.x + 2, self.rect.y + 9)
                game.all_sprites_group.add(gamekey)
                game.key_group.add(gamekey)
                self.kill()     
    #end procedure
    def gethealth(self):
        return self.health
    #endprocedure

    def sethealth(self, newhealth):
        self.health = newhealth
    #endfunction

class BossEnemy(pygame.sprite.Sprite):
    def __init__(self, direction, width, height, x, y, health):
        #call sprite constructor
        super().__init__()
        #create a sprite
        self.image = pygame.Surface([width,height])
        self.image.fill(YELLOW)
        #set the position of the sprite
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.health = health
        self.direction = direction

class HealthBar(pygame.sprite.Sprite):
     def __init__(self, width, height, x, y):
        self.image = pygame.Surface([width,height])
        self.image.fill(GREEN)
        #set the position of the sprite
        
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


game = Game()
# -------- Main Program Loop -----------
while not done:
        # --- Main event loop
    done = game.eventprocess()
    
        # --- Game logic should go here
    game.runlogic()

        #draw the screen
    game.display(screen)
        
        # --- Limit to 60 frames per second
    clock.tick(60)
    
    # Close the window and quit.
pygame.quit()

