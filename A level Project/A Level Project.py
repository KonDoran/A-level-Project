import pygame
import random
import os



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


class Player(pygame.sprite.Sprite):
    #define the constructor for the player
    speed_x = 0
    speed_y = 0
    def __init__(self,color , width, height, x, y, health, score, money, gamekeys):
        #call sprite constructor
        super().__init__()
        #create a sprite
        self.image = pygame.image.load(os.path.join(image_path, 'player.png'))
        #set the position of the sprite
        self.rect = self.image.get_rect()
        self.health = health
        self.score = score
        self.money = money
        self.gamekeys = gamekeys
        self.rect.x = x
        self.rect.y = y
        self.directionx = 0
        self.directiony = 5
        
    #end procedure
    def gethealth(self):
        return self.health
    #endprocedure

    def sethealth(self, newhealth):
        self.health = newhealth
    #endfunction

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
            if len(game.bullet_group) == 0:
                #print("held down")
                bullet = Bullet(RED, self.directionx, self.directiony)
                game.bullet_group.add(bullet)
                game.all_sprites_group.add(bullet)
                
        #end if
        self.move(self.speed_x,self.speed_y)
        self.speed_x = 0
        self.speed_y = 0
        player_hit_group = pygame.sprite.groupcollide(game.player_group, game.enemy_group, False, False)
        for self in player_hit_group:
            self.health -= 2
            if self.health < 1:
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
        self.image = pygame.image.load(os.path.join(image_path, 'fireball.png'))
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
        
class Key(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(image_path, 'silverkey.png'))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

    def update(self):
        key_hit_group = pygame.sprite.groupcollide(game.key_group, game.player_group, True, False)
        for self in key_hit_group:
            game.player.gamekeys += 1
            game.score += 50
            if  game.player.gamekeys == ((2*(game.level+1)) + 1):
                game.portal = Portal(PURPLE, 23*40, 23*40)
                game.all_sprites_group.add(game.portal)
                game.portal_group.add(game.portal)





class Portal(pygame.sprite.Sprite):
    def __init__(self,color,x,y):
        super().__init__()
        self.image = pygame.image.load(os.path.join(image_path, 'portal2.png'))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
    #end procedure    
    def update(self):
        pass

class Wall(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, posx, posy):
        #call sprite constructor
        super().__init__()
        #create a sprite
        self.image = pygame.image.load(os.path.join(image_path, 'wall.png'))
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
        

class Enemy(pygame.sprite.Sprite):
    def __init__(self, direction, width, height, x, y, health):
        #call sprite constructor
        super().__init__()
        #create a sprite
        self.image = pygame.image.load(os.path.join(image_path, 'enemy.png'))
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
        enemy_hit_group = pygame.sprite.pygame.sprite.groupcollide(game.enemy_group, game.bullet_group, False, True)
        for self in enemy_hit_group:
            self.health -= 20
            #print(self.health)
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
       
        