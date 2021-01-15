import pygame
import random


# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (255,20,147)
PURPLE = (75,0,130)

#initiate pygame
pygame.init()

# Set the width and height of the screen [width, height]
size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("A level Project")

#Loop until the user clicks the close button.
done = False
    
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
    





#Define the Game class which controls every other class and function
class Game(object):
    def __init__(self):
        #define attributes of the game class
        self.score = 0
        self.game_over = False
        self.level = 0
        # Create a list of all sprite groups
        self.all_sprites_group = pygame.sprite.Group()
        self.outsidewall_group = pygame.sprite.Group()
        self.wall_group = pygame.sprite.Group()
        self.innerwall_group = pygame.sprite.Group()
        self.player_group = pygame.sprite.Group()
        self.bullet_group = pygame.sprite.Group()
        self.enemy_group = pygame.sprite.Group()
        self.coin_group = pygame.sprite.Group()
        self.portal_group = pygame.sprite.Group()
        self.melee_group = pygame.sprite.Group()
        #define each level layout in the Game class constructor 
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
            [1,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,2,2,0,0,0,0,2,2,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,1],
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
            [1,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,2,2,2,2,2,0,0,0,0,2,2,2,2,2,2,2,2,0,0,1],
            [1,0,0,0,0,2,0,0,2,2,2,2,2,2,2,2,0,0,0,0,0,2,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
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
            [1,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,0,0,2,2,0,0,2,2,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,2,0,0,0,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,0,2,0,0,2,2,2,1],
            [1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,2,2,0,0,0,0,0,1],
            [1,0,0,0,0,0,2,0,2,2,2,2,2,2,2,2,0,2,0,0,0,0,0,0,1],
            [1,2,0,0,2,2,2,2,2,2,0,0,0,0,2,2,2,2,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,2,0,0,1],
            [1,2,2,0,0,2,2,2,2,2,0,0,0,0,2,2,2,2,2,2,2,2,0,0,1],
            [1,0,0,0,0,2,0,0,2,2,2,0,0,2,2,2,0,0,0,0,0,2,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,2,0,0,1],
            [1,0,0,0,0,2,2,2,2,2,0,0,0,0,0,0,0,2,2,2,2,2,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,2,2,2,2,0,0,0,2,2,2,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
            [1,0,0,0,0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,0,0,2,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [1,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
        
            ] 
        # Create an array that stores each level           
        self.levels = [self.level1, self.level2, self.level3]
        #run the setup function for the levels
        self.levelsetup()
        #end function

    #define the level setup function to generate each level    
    def levelsetup(self):
        enemies = 0
        #loop to create enemies in random positions in each level but not inside the player or walls
        while enemies != ((2*(self.level+1)) + 1):
            xpos = random.randint(1,23)
            ypos = random.randint(1,23)
            if self.levels[self.level][xpos][ypos] !=1 and self.levels[self.level][xpos][ypos] != 2:
                self.levels[self.level][xpos][ypos] = 4
                enemies = enemies +1
        #level creation by reading through array
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
                    self.player = Player(WHITE, 40, 40,i*40,j*40,100,0,0,0)
                    self.all_sprites_group.add(self.player)
                    self.player_group.add(self.player)
                if char == 4:
                    self.enemy = Enemy(random.randint(0,10),40,40, i*40, j*40, 40)
                    self.all_sprites_group.add(self.enemy)
                    self.enemy_group.add(self.enemy)
        #end procedure


    #define level delete procedure
    def leveldelete(self):
        self.all_sprites_group.empty()
        self.wall_group.empty()
        self.enemy_group.empty()
        self.all_sprites_group.update()

    #endprocess
    def eventprocess(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
        return False            

    #data hiding function to get the score
    def getscore(self):
        return self.score
    #endprocess


    # function to run all the logic of the game
    def runlogic(self):
        if not self.game_over:
            # update sprite movement when game is running
            self.all_sprites_group.update()
            #when the player is deleted then the game should stop
            if len(self.player_group) == 0:
                self.game_over = True
            #endif
            #check if a portal has been touched by the player to change level
            portal_hit = pygame.sprite.groupcollide(self.portal_group, self.player_group, True, True)
            for self.portal in portal_hit:
                #check this is not the last level and if not change the level
                if self.level != (len(self.levels)-1):
                    self.level += 1
                    self.score += (self.player.health*100)+100
                    self.leveldelete()
                    self.levelsetup()
                else:
                    #if the game is over add points to the players score and then stop the game
                    self.score += (self.player.health*100)+100
                    self.game_over = True
                #endif
    #end procedure

    #define function to display everything on the screen
    def display(self, screen):
        # background image.
        screen.fill(BLACK)
        # define game over screen
        if self.game_over:
            screen.fill(BLACK)
            font1 = pygame.font.Font(None, 74)
            font2 = pygame.font.Font(None, 48)
            text = font1.render('GAME OVER', 1, WHITE)
            score = font2.render('SCORE:'+str(self.getscore()), 1, WHITE)
            screen.blit(text, (440,300))
            screen.blit(score, (520,500))
        # define screen when game is running
        if not self.game_over:
            font = pygame.font.Font(None, 24)
            health = font.render('HEALTH:'+str(self.player.gethealth()), 1, WHITE)
            score = font.render('SCORE:'+str(self.getscore()), 1, WHITE)
            money = font.render('MONEY:'+str(self.player.getmoney()), 1, WHITE)
            keys = font.render('KEYS:'+str(self.player.getkeys()), 1, WHITE)
            screen.blit(health, (1050,450))
            screen.blit(score, (1050,500))
            screen.blit(money, (1050,550))
            screen.blit(keys, (1050,600))
            # --- Drawing all sprites
            self.all_sprites_group.draw(screen)
            #endif
        # update the screen with what we've drawn
        pygame.display.flip()
    #end procedure
        
        