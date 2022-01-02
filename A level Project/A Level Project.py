import pygame
import random
import os
import sys
import numpy as np
import math
from collections import deque
vec = pygame.math.Vector2


#use os to find the path of this file:
current_path = os.path.dirname(__file__)
#use os to find the folder called 'images' in the same folder as this file
image_path = os.path.join(current_path, 'images')
# Define colours as tuples
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PINK = (204,102,153)
PURPLE = (75,0,130)
BROWN = (150, 75, 0)
ORANGE = (230,165,0)
BLUE = (30,144,255)
PERFECTBLUE = (0,0,255)
LIGHTBLUE = (173, 216, 240)
GREY = (180,180,180)
#use os to find the menu background image in the images folder
BACKGROUND_IMAGE = pygame.image.load(os.path.join(image_path, 'Menu background.png'))
#Define constants for grid class for pathfinding:s
#Define the size of each tile (size of walls/ player)
TILESIZE = 40
#Specify how many tiles form the width of the grid and the height of the grid.
GRIDWIDTH = 25
GRIDHEIGHT = 25
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
#Define the highscore file as highscore.txt
HS_FILE = "highscore.txt"
PLAYERSHEET = "BlueKnightSpriteSheet.png"
TILESSHEET = "tilessheet.png"
#Use os to find the highscore file
hs_path = os.path.join(current_path, 'highscore')
#Use os to find the folder called icons to use when showing the start and end points in the pathfinding algorithm
icon_dir = os.path.join(current_path, 'icons')
#Initiate pygame module
pygame.init()

# Set the width and height of the screen [width, height]
size = (1200, 1000)
screen_width = 1200
screen_height = 1000
screen = pygame.display.set_mode(size)
#Set the window name to DUNGEON ESCAPE
pygame.display.set_caption("Dungeon Escape")
#Define the clock used for what refresh rate the game runs at.
clock = pygame.time.Clock()
#Create a function used to format text used in buttons
def text_objects(text,font):
    #Render the text input as white and return the position of the surface.
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()
#end procedure

#Create a button function that interacts with the mouse. When hovered over by the mouse change colour and define the x position, y position and width and height of the Button.
#Also specify what the button does when it is pressed and what text is in the button
def button_1(message,xpos,ypos,width,height,inactivecolor,activecolor,action1=None):
    #Find the position of the mouse
    mouse = pygame.mouse.get_pos()
    #Check if the mouse is being clicked
    click = pygame.mouse.get_pressed()
    #Check if the mouse's position is the same as the button's position
    if xpos+width >mouse[0] > xpos and ypos+height > mouse[1] > ypos:
        #Draw the button with its inactive colour
        pygame.draw.rect(screen, inactivecolor,(xpos,ypos,width,height),5)
        #Check if the mouse is clicked:
        if click[0] == 1 and action1 !=None:
            #Check what the action of the button does.
            if action1 == "1":
                #If the button has action 1 then it will start the gameloop when pressed.
                gameloop()
            elif action1 == "Q":
                    #if the button has the action Q then exit the window
                    pygame.quit()
    else:
        #When the button is not hovered over by the mouse then draw the button with it's active colour
        pygame.draw.rect(screen, activecolor,(xpos,ypos,width,height),5)
    #Draw the text of the buutton in the middle of the button  
    smallText = pygame.font.Font("freesansbold.ttf",30)
    textSurf, textRect = text_objects(message, smallText)
    textRect.center = ( (xpos+(width/2)), (ypos+(height/2)) )
    screen.blit(textSurf, textRect)
#end function




#Create a function for the Main Menu of the game.
#Display the buttons for Starting the game and Quiting.
def game_intro():
    intro = True
    #Use while loop so that the Menu refreshes 60 times per second
    while intro:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
              intro = False # Flag that we are done so we exit this loop and quit the game
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE: 
                         intro=False
                         
    #Drawing the menu screen
        screen.fill(BLACK)
        #Draw the Background image for the background
        screen.blit(BACKGROUND_IMAGE, [0,0])
        #Set the font and text for the title and center it.
        font = pygame.font.Font('freesansbold.ttf', 84)
        text = font.render(str("DUNGEON ESCAPE"), 1, WHITE)
        text_rect = text.get_rect(center=(screen_width//2, screen_height//6))
        screen.blit(text, text_rect)
        #Draw the buttons for starting the game and quiting
        button_1("START GAME",475,420,250,60,WHITE,GREY,"1")
        button_1("QUIT",475,490,250,60,WHITE,GREY,"Q")
        #Display the image in the window
        pygame.display.flip()
        #Refresh at 60Hz
        clock.tick(60)
#end procedure





#Create a game loop function that is called after the Menu
def gameloop():
    #Create a function that draws the icons used in the shortest path and center them
    def draw_icons():
        start_center = (game.menemy.goal.x * TILESIZE + TILESIZE / 2, game.menemy.goal.y * TILESIZE + TILESIZE / 2)
        screen.blit(home_img, home_img.get_rect(center=start_center))
        goal_center = (game.menemy.start.x * TILESIZE + TILESIZE / 2, game.menemy.start.y * TILESIZE + TILESIZE / 2)
        screen.blit(cross_img, cross_img.get_rect(center=goal_center))









    #Loop until the user clicks the close button.
    done = False
        
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()



    #Create A Game class that holds all the Sprite groups and level information
    #Use a game object to establish a game loop that is used to setup the game
    class Game(object):
        def __init__(self):
            #Define all the atributes of the Game class
            #Set the Score of the game to 0
            self.score = 0
            #define spritesheets in game class as attributes
            Game.wallspritesheet = SpriteSheet(os.path.join(image_path, TILESSHEET))
            Game.playerspritesheet = SpriteSheet(os.path.join(image_path, PLAYERSHEET))
            Game.invertedplayerspritesheet = SpriteSheet(os.path.join(image_path,"BlueKnightSpriteSheetflipped.png"))
            Game.cratespritesheet = SpriteSheet(os.path.join(image_path, "crate.png"))
            Game.doorspritesheet = SpriteSheet(os.path.join(image_path, "doorsheet.png"))
            Game.floorspritesheet = SpriteSheet(os.path.join(image_path, "floor.png"))
            Game.benemyspritesheet = SpriteSheet(os.path.join(image_path, "bow enemy.png"))
            Game.menemyspritesheet = SpriteSheet(os.path.join(image_path, "menemy.png"))
            Game.bossspritesheet = SpriteSheet(os.path.join(image_path, "boss enemy.png"))
            Game.keyspritesheet = SpriteSheet(os.path.join(image_path, "silverkey.png"))
            Game.bulletspritesheet = SpriteSheet(os.path.join(image_path, "fireball.png"))
            Game.enemybulletspritesheet = SpriteSheet(os.path.join(image_path, "enemyfireball.png"))
            #Use an attribute to tell whether the game has finished
            self.game_over = False
            #Set the game level to 0
            self.level = 0
            # Create a different sprite groups to be used for collisions and updates
            self.all_sprites_group = pygame.sprite.Group()
            self.outsidewall_group = pygame.sprite.Group()
            self.wall_group = pygame.sprite.Group()
            self.innerwall_group = pygame.sprite.Group()
            self.player_group = pygame.sprite.Group()
            self.bullet_group = pygame.sprite.Group()
            self.enemy_group = pygame.sprite.Group()
            self.menemy_group = pygame.sprite.Group()
            self.key_group = pygame.sprite.Group()
            self.portal_group = pygame.sprite.Group()
            self.door_group = pygame.sprite.Group()
            self.sword_group = pygame.sprite.Group()
            self.spike_group = pygame.sprite.Group()
            self.chest_group = pygame.sprite.Group()
            self.boss_group = pygame.sprite.Group()
            self.enemybullet_group = pygame.sprite.Group()
            self.ground_group = pygame.sprite.Group()
            #Call the load data method to be used to find and store high scores
            self.load_data()
            #Create a list of which chests have been unlocked
            self.chestunlocked = [False, False, False, False, False]
            #Set a timer for how long to display text
            self.previoustexttime = pygame.time.get_ticks()
            #Create a list of all the levels that have been completed
            self.levelcomplete = [False, False, False, False, False]
            #Create a 2D array of each level with each digit representing a tile of 40 by 40 pixels
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
                [1,0,0,0,0,0,0,0,7,0,0,0,0,0,0,7,0,0,0,0,0,0,0,0,6],
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
                [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
                [1,0,0,0,0,2,2,2,2,2,0,0,0,0,2,2,2,2,2,2,2,2,0,0,1],
                [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
                [1,2,0,2,2,2,0,0,0,0,0,0,0,0,0,0,0,2,2,2,2,2,0,0,1],
                [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1],
                [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,2,2,0,0,0,2,2,2,1],
                [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,1],
                [1,0,0,0,0,2,0,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,0,0,1],
                [1,0,0,0,0,2,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            
                ]

            self.level3 = [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,2,2,2,2,0,0,0,0,0,0,7,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,2,2,2,7,7,2,2,2,1],
                [1,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,1],
                [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,6],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,1],
                [1,2,2,2,2,0,0,0,2,2,2,2,2,2,2,2,2,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,2,2,2,2,0,0,0,0,0,0,0,7,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,2,7,7,2,2,2,2,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            
                ]

            self.level4 = [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,2,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,2,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,2,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,2,0,0,0,0,2,0,0,0,0,0,2,2,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,2,0,0,0,0,0,2,2,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,2,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,2,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,2,2,2,2,2,2,0,0,0,0,2,2,2,2,2,2,2,2,2,2,2,2,2,1],
                [6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,6],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
                [1,2,2,2,2,2,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
                [1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,2,2,2,7,7,7,7,7,1],
                [1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
                [1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
                [1,0,0,0,0,0,2,0,0,0,0,0,0,0,0,0,0,0,2,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            
                ]

            self.level5 = [
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,7,7,7,7,7,7,7,7,7,7,7,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,6],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,7,7,7,7,7,7,7,7,7,7,7,7,7,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
            
                ]
            #Create a list of all the levels                
            self.levels = [self.level1, self.level2, self.level3,self.level4, self.level5]
            #Initiate the level setup for the first level
            self.levelsetup()
            #Create an object of the player class and add him to Sprite groups
            self.player = Player(WHITE, 40, 40,40,500,100,0,0,0)
            self.all_sprites_group.add(self.player)
            self.player_group.add(self.player)
        #end method    

        #Create a method to read the highscore file and set the highscore in the game
        def load_data(self):
            #load high score file
            f = open(os.path.join(hs_path, HS_FILE), "r")
            try:
                #If file has data in it then set the highscore
                self.highscore = int(f.readline())
                #print(self.highscore)
            except:
                #Else if this doesn't work then set the highscore to 0
                self.highscore = 0
                #print(self.highscore)
            #load spritesheet
        
        #end method

        #Create a method that creates all the objects according to the 2D array in the game class.
        def levelsetup(self):
            #Set the count to 0
            self.count = 0
            self.bosscount = 0
            #Spawn the boss enemy when the level is 5
            if (self.level + 1) % 5 == 0:
                self.levels[self.level][10][10] = 5

            else:
                #When the level is not level 5 then create enemies according to what level the player is on.
                enemies = 0
                while enemies != ((2*(self.level+1)) + 1):
                    #Find two random numbers between 1 and 23
                    xpos = random.randint(1,23)
                    ypos = random.randint(1,23)
                    #Check if the numbers correspond to coordinates of walls or other sprites
                    if self.levels[self.level][xpos][ypos] !=1 and self.levels[self.level][xpos][ypos] != 2 and self.levels[self.level][xpos][ypos] != 7:
                        #set the coordinates to a random number to spawn either a Melee enemy or Bow enemy
                        self.levels[self.level][xpos][ypos] = random.randint(3,4)
                        enemies = enemies +1

            #Search through the 2D array and create objects that corespond to each coordinate that forms the grid.
            for j in range(len(self.levels[self.level])):
                for i in range(len(self.levels[self.level][j])):
                    #print(i,j)
                    #Check what each character is in every index then create objects according to each character
                    char = self.levels[self.level][j][i]
                    if char == 1:
                        #Create outside wall object and add it to corresponding Sprite groups and add the coordinates to the wall list
                        self.outsidewall = Wall(RED,40,40,i*40, j*40, i, j)
                        self.all_sprites_group.add(self.outsidewall)
                        self.wall_group.add(self.outsidewall)
                        self.outsidewall_group.add(self.outsidewall)
                        #g.walls.append(vec((self.outsidewall.rect.x/40), (self.outsidewall.rect.y/40)))
                    if char == 2:
                        #Create inner object and add it to corresponding Sprite groups and add the coordinates to the wall list
                        self.innerwall = InnerWall(RED,40,40,i*40, j*40, i, j)
                        self.all_sprites_group.add(self.innerwall)
                        self.wall_group.add(self.innerwall)
                        self.innerwall_group.add(self.innerwall)
                        #g.walls.append(vec((self.innerwall.rect.x/40), (self.innerwall.rect.y/40)))
                    if char == 3:
                        #Create Bow enemy object and add it to corresponding Sprite groups
                        if self.levelcomplete[self.level] == False:
                            self.benemy = BowEnemy(random.randint(0,10),40,40, i*40, j*40, 40)
                            self.all_sprites_group.add(self.benemy)
                            self.enemy_group.add(self.benemy)
                    if char == 4:
                        #Create Melee enemy object and add it to corresponding Sprite groups
                        if self.levelcomplete[self.level] == False:
                            self.menemy = MeleeEnemy(random.randint(0,10),40,40, i*40, j*40, 40)
                            self.all_sprites_group.add(self.menemy)
                            self.enemy_group.add(self.menemy)
                            self.menemy_group.add(self.menemy)
                    if char == 5:
                        #Create Boss object and add it to corresponding Sprite groups
                        if self.levelcomplete[self.level] == False:
                            self.boss = BossEnemy(random.randint(0,10),160,160, i*40, j*40, 1000)
                            self.all_sprites_group.add(self.boss)
                            self.boss_group.add(self.boss)
                    if char == 6:
                        #Create Door object and add it to corresponding Sprite groups
                        if self.levelcomplete[self.level] == False:
                            self.door = Door(PURPLE,40,40,i*40, j*40, i, j)
                            self.all_sprites_group.add(self.door)
                            self.wall_group.add(self.door)
                            self.door_group.add(self.door)
                    if char == 7:
                        #Create Spike object and add it to corresponding Sprite groups
                        self.spike = Spikes(GREY, 40,40,i*40, j*40, i, j)
                        #self.all_sprites_group.add(self.spike)
                        self.spike_group.add(self.spike)
                    
                    self.ground = Ground(i*40,j*40)
                    self.ground_group.add(self.ground)
        #end method

        #Method to delete each level when the player completes it
        def leveldelete(self):
            #Remove all sprites and readd the player
            self.all_sprites_group.empty()
            self.wall_group.empty()
            self.spike_group.empty()
            self.enemy_group.empty()
            self.bullet_group.empty()
            self.menemy_group.empty()
            self.key_group.empty()
            self.portal_group.empty()
            self.door_group.empty()
            self.sword_group.empty()
            self.chest_group.empty() 
            self.boss_group.empty()
            self.enemybullet_group.empty()
            self.ground_group.empty()
            self.all_sprites_group.add(self.player)
            self.all_sprites_group.update()

        #endprocess
        #Method used to check for event if they quit
        def eventprocess(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
            return False            

        #Method to get score of the game
        def getscore(self):
            return self.score
        #endprocess

        #Method that processes all interactions not within other classes
        def runlogic(self):
            if not self.game_over:
                #When the game is running and all the enemies and boss are dead create a chest
                if len(self.enemy_group) == 0:
                    if len(self.boss_group) == 0:
                        self.levelcomplete[self.level] = True
                if self.levelcomplete[self.level] == True:
                    if len(self.chest_group) == 0:
                        #Use count to only create one chest per level
                        if self.count == 0:
                            self.count+=1
                            print(self.count)
                            #create chest object and add it to sprite groups
                            self.chest = Chest(BROWN, 40, 40, 460,440, self.level)
                            self.all_sprites_group.add(self.chest)
                            self.chest_group.add(self.chest)
                #print(self.levelcomplete)
                # Move all the sprites
                self.sword_group.update()
                self.spike_group.update()
                self.all_sprites_group.update()
                #Check if the player has died
                if len(self.player_group) == 0:
                    #If true, then end the game
                    self.game_over = True
                #print(len(game.enemy_group))
                #Change the level when the player goes past the boundaries(goes through the doors)
                if self.player.rect.x > 1000:
                    #Check if this is the last level and if not set to true and increase the level
                    if self.level != (len(self.levels)-1):
                        self.levelcomplete[self.level] = True
                        self.chestunlocked[self.level] = False
                        self.level += 1
                        #Reset the room keys needed to proceed to next levels
                        self.player.gamekeys = 0
                        self.player.rect.x = 40
                        #Run level delete then create the next level
                        self.leveldelete()
                        self.levelsetup()
                        
                    else:
                        #If the final level then end the game
                        self.game_over = True
                #Check if the player goes back a level        
                elif self.player.rect.x < 0:
                    #set the level back one and then setup the new level    
                    self.chestunlocked[self.level] = False
                    self.level -= 1
                    self.leveldelete()
                    self.player.rect.x = 960
                    self.levelsetup()
        #end method

        #Create a method to display all sprites and text
        def display(self, screen):
            # background image.
            screen.fill(BLACK)
            #screen.blit(BACKGROUND_IMAGE, (0,0))
            if self.game_over:
                #If the game is over then create a game over screen
                #First set the screen black
                screen.fill(BLACK)
                screen.blit(BACKGROUND_IMAGE, (0,0))
                #Then draw text of Game over, score and Highscore
                font1 = pygame.font.Font(None, 74)
                font2 = pygame.font.Font(None, 48)
                font = pygame.font.Font(None, 48)
                text = font1.render('GAME OVER', 1, WHITE)
                score = font2.render('SCORE:'+str(self.getscore()), 1, WHITE)
                self.hs = font.render('HIGHSCORE:'+str(self.highscore),1, WHITE)
                self.text_rect = self.hs.get_rect(center=((screen_width)/2, 700))
                text_rect2 = text.get_rect(center=((screen_width)/2, 300))
                #Check if the score is greater than the old highscore and set the highscore as the score
                if self.score > self.highscore:
                    self.highscore = self.score
                    #Open the highscore file
                    f = open(os.path.join(hs_path, HS_FILE), "w")
                    #Change the file to have new high score
                    f.write(str(self.score))
                screen.blit(self.hs, self.text_rect)
                screen.blit(text, text_rect2)
                screen.blit(score, (520,500))
            if not self.game_over:
                #When the game is running Display text on the right handside of the screen with the score and keys of the player
                font = pygame.font.Font(None, 24)
                score = font.render('SCORE:'+str(self.getscore()), 1, WHITE)
                keys = font.render('KEYS:'+str(self.player.getkeys()), 1, WHITE)
                #move = font.render('TO MOVE')
                #attack1 = font.render('TO SWING SWORD')
                #attack2 = font.render('TO SHOOT FIREBALL')
                #Draw the player function for the health bar of the player
                self.player.advanced_health()
                #Draw the text of the player's health over the health bar
                health = font.render(str(self.player.current_health), 1, WHITE)
                screen.blit(score, (1050,500))
                screen.blit(keys, (1050,550))
                screen.blit(health, (1081, 51))

                # --- Drawing code for sprites
                self.sword_group.draw(screen)
                self.ground_group.draw(screen)
                self.spike_group.draw(screen)
                self.all_sprites_group.draw(screen)
                self.boss_group.draw(screen)
                #Check which chest has been unlocked and display text until player moves to next level
                if self.chestunlocked[self.level] == True:
                    if self.level == 0:
                        font3 = pygame.font.Font(None, 48)
                        msg = font3.render('FIREBALL UNLOCKED', 1, BLUE)
                        text_rect = msg.get_rect(center=((screen_width-200)/2, screen_height/6))
                        screen.blit(msg, text_rect)
                    if self.level == 1:
                        font3 = pygame.font.Font(None, 48)
                        msg = font3.render('SWORD RADIUS INCREASED', 1, BLUE)
                        text_rect = msg.get_rect(center=((screen_width-200)/2, screen_height/6))
                        screen.blit(msg, text_rect)
                    if self.level == 2:
                        font3 = pygame.font.Font(None, 48)
                        msg = font3.render('HEALTH INCREASED', 1, BLUE)
                        text_rect = msg.get_rect(center=((screen_width-200)/2, screen_height/6))
                        screen.blit(msg, text_rect)
                    if self.level == 3:
                        font3 = pygame.font.Font(None, 48)
                        msg = font3.render('MULTISHOT UNLOCKED', 1, BLUE)
                        text_rect = msg.get_rect(center=((screen_width-200)/2, screen_height/6))
                        screen.blit(msg, text_rect)
                    if self.level == 4:
                        font3 = pygame.font.Font(None, 48)
                        msg = font3.render('BOSS COMPLETE', 1, BLUE)
                        text_rect = msg.get_rect(center=((screen_width-200)/2, screen_height/6))
                        screen.blit(msg, text_rect)

                #if self.secondchest == True
                #self.enemy_group.update()
                #Check if the level is multiple of 5. If true then display the boss health bar.
                if (self.level + 1) % 5 == 0:
                    self.boss.advanced_health()
                #current = self.player.start + self.player.path[vec2int(self.player.start)]
                #while current != self.player.goal:
                    #x = current.x * TILESIZE + TILESIZE / 2
                    #y = current.y * TILESIZE + TILESIZE / 2
                    #img = arrows[vec2int(self.player.path[(current.x, current.y)])]
                    #r = img.get_rect(center=(x, y))
                    #screen.blit(img, r)
                    # find next in path
                    #current = current + self.player.path[vec2int(current)]
                #draw_icons()
                #self.player.basic_health()
                
                #endif
            # --- Go ahead and update the screen with what we've drawn.
            pygame.display.flip()
        #end procedure
            



    class SpriteSheet(object):
        #Utility class required to pass and load spritesheets
        def __init__(self, filename):
            self.spritesheet = pygame.image.load(filename).convert_alpha()

        def get_image(self, x, y, width, height,newwidth, newheight):
            #grab image inside spritesheet
            image = pygame.Surface([width,height])
            image.blit(self.spritesheet, (0,0), (x, y, width, height))
            image = pygame.transform.scale(image, (newwidth,newheight))
            return image
            
            
            
            
            
            
    # Create a Player Class
    class Player(pygame.sprite.Sprite):
        #define constants for speed of player
        speed_x = 0
        speed_y = 0
        #Method for when the player object is initially created.
        def __init__(self,color , width, height, x, y, health, score, money, gamekeys):
            #call sprite constructor
            super().__init__()
            #create a sprite
            self.walkimagearray = [Game.playerspritesheet.get_image(82,1200,80,100,40,40),Game.playerspritesheet.get_image(103,907,80,100,40,40),Game.playerspritesheet.get_image(291,908,87,97,40,40), Game.playerspritesheet.get_image(388,908,88,98,40,40), Game.playerspritesheet.get_image(485,908,90,99,40,40),Game.playerspritesheet.get_image(590,908,82,99,40,40), Game.playerspritesheet.get_image(688,908,81,99,40,40),Game.playerspritesheet.get_image(786,908,80,98,40,40),Game.invertedplayerspritesheet.get_image(1917,908,80,99,40,40),Game.invertedplayerspritesheet.get_image(1820,908,80,99,40,40),Game.invertedplayerspritesheet.get_image(1723,908,86,97,40,40),]
            self.attackarray = []
            self.image = self.walkimagearray[0]
            self.image.set_colorkey(GREEN)
            self.numberarray = 0
            #self.image.fill(color)
            #set the position of the sprite
            self.rect = self.image.get_rect()
            #Set the current and maximum health of the player to be used for health bar
            self.current_health = 50
            self.maximum_health = health
            self.health_bar_length = 180
            self.target_health = 100
            self.health_change_speed = 2
            self.health_bar_color = GREEN
            self.health_ratio = self.maximum_health/ self.health_bar_length
            #Player score is tallied and added to game score
            self.score = score
            #Money attribute currently not used but can be used in a future update
            self.money = money
            #keys used to check to open doors to go to next level
            self.gamekeys = gamekeys
            self.rect.x = x
            self.rect.y = y
            #Set original direction for player
            self.directionx = 0
            self.directiony = 5
            #Set player attribute that are unlocked after opening chests
            self.canshoot = False
            self.multishot  = False
            self.swordradius = 50
            self.bulletcount = 3
            #Set timers to be used for attacks
            self.previoushealthtime = pygame.time.get_ticks()
            self.previousbullettime = pygame.time.get_ticks()
            self.previousdamagetime = pygame.time.get_ticks()
            self.previousattacktime = pygame.time.get_ticks()
            self.previousbulletaddtime = pygame.time.get_ticks()
            
        #end procedure

        #Method to increase health of player 
        def gethealth(self, amount):
            if self.target_health < self.maximum_health:
                self.target_health += amount
            if self.target_health >= self.maximum_health:
                self.target_health = self.maximum_health
        #endprocedure

        #Method to remove health of palyer
        def getdamage(self,amount):
            if self.target_health > 0:
                self.target_health -= amount
            if self.target_health <=0:
                self.target_health = 0
        #end method

        #Method used to create helath bar
        def advanced_health(self):
            transition_width = 0
            transition_color = RED
            
            #When health is added set the transition bar to green and increase health bar at set speed
            if self.current_health < self.target_health:
                self.current_health += self.health_change_speed
                transition_width = int((self.target_health - self.current_health)/ self.health_ratio)
                transition_color = GREEN
            #When health is removed set the transition bar to yellow and decrease the health bar at a set speed
            if self.current_health > self.target_health:
                self.current_health -= self.health_change_speed
                transition_width = int((self.target_health - self.current_health)/ self.health_ratio)
                transition_color = YELLOW

            #Change the health bar colour depending on the amount of health
            if self.current_health >= 70:
                self.health_bar_color = GREEN
            if self.current_health >= 50 and self.current_health < 70:
                self.health_bar_color = ORANGE
            if self.current_health < 30 and self.current_health >=0:
                self.health_bar_color = RED
            #set the health bar size equal to the current health divided by max health
            health_bar_width = int(self.current_health/ self.health_ratio)
            health_bar = pygame.Rect(1005,45, health_bar_width, 25)
            #transition bar is set to the right of the health bar
            transition_bar = pygame.Rect(health_bar.right, 45, transition_width, 25)
            #Draw all 3 bars over each other
            pygame.draw.rect(screen, self.health_bar_color, health_bar)
            pygame.draw.rect(screen,transition_color, transition_bar)
            pygame.draw.rect(screen, WHITE, (1005, 45, self.health_bar_length, 25), 4)
        #end method

        #Get player score
        def getscore(self):
            return self.score
        #endprocedure

        #get player's node position vector on grid
        def getpos(self):
            return vec(self.rect.x/40, self.rect.y/40)
        #endfunction

        #set player score
        def setscore(self, score):
            self.score = score
        #endfunction
        #get player's key number
        def getkeys(self):
            return self.gamekeys
        #endprocedure

        #set player's key number
        def setkeys(self, keys):
            self.gamekeys = keys
        #endfunction

        #get player's money 
        def getmoney(self):
            return self.money
        #endprocedure

        #set player's money
        def setmoney(self, money):
            self.money = money
        #endfunction

        #Change the player's speed by the values entered
        def changespeed(self, x, y):
            self.speed_x += x
            self.speed_y += y

        #Update method for player to control movement and damage taken
        def update(self):
            if self.speed_x ==0 and self.speed_y == 0:
                self.image = Game.playerspritesheet.get_image(82,1200,80,100,40,40)
                self.image.set_colorkey(GREEN)
            #Check for what keys are pressed
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                #Move the player to the left and change the direction
                self.changespeed(-2,0)
                self.directionx = -6
                self.directiony = 0
                self.numberarray += 0.2
                self.image = self.walkimagearray[int(self.numberarray)]
                self.image.set_colorkey(GREEN)
                if self.numberarray > 7:
                    self.numberarray = 0
            if keys[pygame.K_d]:
                #move the player to the right and change the direction
                self.changespeed(2,0)
                self.directionx = 6
                self.directiony = 0      
            if keys[pygame.K_w]:
                #move the player up and change the direction
                self.changespeed(0,-2)
                self.directionx = 0
                self.directiony = -6
            if keys[pygame.K_s]:
                #move the player down and change the direction
                self.changespeed(0,2)
                self.directionx = 0
                self.directiony = 6
            if keys[pygame.K_e]:
                #When the E key is pressed and bullet shooting is unlocked then create a fireball that travel in the direction set by the player from the previous key pressed
                if self.canshoot == True:
                    #Check if multishot is unlocked
                    if self.multishot == False:
                        if self.bulletcount > 0:
                            #Create a bullet once per second
                            self.currentbullettime = pygame.time.get_ticks()
                            if self.currentbullettime - self.previousbullettime > 1000:
                                bullet = Bullet(RED, self.directionx, self.directiony)
                                game.bullet_group.add(bullet)
                                game.all_sprites_group.add(bullet)
                                #remove 1 from the bullet count
                                self.bulletcount -= 1
                                self.previousbullettime = self.currentbullettime
                    else:
                        #If multishot is active then produce a bullet every 100 milliseconds only if bulletcount is greater than zero
                        if self.bulletcount > 0:
                            self.currentbullettime = pygame.time.get_ticks()
                            if self.currentbullettime - self.previousbullettime > 100:
                                #remove 1 from bullet count so bullets can only be produced in maximum of 3 per second
                                self.bulletcount -=1
                                bullet = Bullet(RED, self.directionx, self.directiony)
                                game.bullet_group.add(bullet)
                                game.all_sprites_group.add(bullet)
                                self.previousbullettime = self.currentbullettime
            if keys[pygame.K_SPACE]:
                #Check if Space has been pressed and if the sword hasn't already been created
                if len(game.sword_group) == 0:
                    #create a sword with a set radius that lasts for 1 second and add the sword to its sprite groups
                    self.currentattacktime = pygame.time.get_ticks()
                    if self.currentattacktime - self.previousattacktime > 1000:
                        sword = Sword(BLACK, self.swordradius)
                        game.sword_group.add(sword)
                        #game.all_sprites_group.add(sword)
                        self.previousattacktime = self.currentattacktime
            #Check if the timer is greater than one to add bullets to the bulletcount
            self.currentbulletaddtime = pygame.time.get_ticks()
            if self.currentbulletaddtime - self.previousbulletaddtime > 1000:
                if self.multishot == False:
                    self.bulletcount += 1
                else:
                    self.bulletcount +=3
                self.previousbulletaddtime = self.currentbulletaddtime

            #Bulletcount is limited to 3
            if self.bulletcount > 3:
                self.bulletcount = 3
            #Refresh the health bar so an increase in the maximum health resets the health bar ratio
            self.health_ratio = self.maximum_health/ self.health_bar_length
            self.currenthealthtime = pygame.time.get_ticks()
            #Check if 10 seconds have passed to add 10 health to the palyer
            if self.currenthealthtime -self.previoushealthtime > 10000:
                self.gethealth(10)
                self.previoushealthtime = self.currenthealthtime
            #Check if the player's health is 0 and kill the player to end the game.
            if self.current_health < 1:
                game.score += 100
                self.kill()
            #use the move function by the speed specified according to the key press
            self.move(self.speed_x,self.speed_y)
            #Reset the speeds to prevent the player accelerating
            self.speed_x = 0
            self.speed_y = 0 
        #end procedure


        #Method that takes input speeds and moves players position according to speed.
        def move(self, speedx, speedy):
            #move left or right
            self.rect.x += self.speed_x
            #Check if the player collides with the wall
            wallcollision = pygame.sprite.spritecollide(self,game.wall_group, False)
            for wall in wallcollision:
                if self.speed_x > 0:
                    #stop the player moving into the wall
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
                    #stop the player moving into the wall
                    self.rect.bottom = wall.rect.top
                else:
                    self.rect.top = wall.rect.bottom
        #end procedure    
    #end class

    #Class for Player bullets
    class Bullet(pygame.sprite.Sprite):
        #Method to initiate bullet objects
        def __init__(self, color, speedx, speedy):
            #Call the sprite constructor
            super().__init__()
            #Bullet created in the center of the player object
            self.image = Game.bulletspritesheet.get_image(0,0,22,24,12,12)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.speedx = speedx
            self.speedy = speedy
            self.rect.y = game.player.rect.y + 10
            self.rect.x = game.player.rect.x  + 10

        #Update method that moves the player by the speed which is defined by the direction that the player last moved in.
        def update(self):
            self.rect.y += self.speedy
            #Check if it collides with a wall and kills the sprite
            if pygame.sprite.groupcollide(game.bullet_group, game.wall_group, True, False) == True:
                self.kill()
            self.rect.x += self.speedx
            #Check if it collides with a wall and kills the sprite
            if pygame.sprite.groupcollide(game.bullet_group, game.wall_group, True, False) == True:
                self.kill()
                #Check if it travel past the boundaries and kills the sprite
            if self.rect.x > 1000:
                self.kill()
            if self.rect.x < 0:
                self.kill()

    class Ground(pygame.sprite.Sprite):
        def __init__(self, x, y):
            super().__init__()
            self.id = random.randint(1,2)
            if self.id == 1:
                self.image = Game.floorspritesheet.get_image(960,160,32,32,40,40)
            else:
                self.image = pygame.transform.rotate(Game.floorspritesheet.get_image(992,160,32,32,40,40), 90*random.randint(0,3))
            #self.image.fill(color)
            #set the position of the sprite
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
        #end procedure
        #No updates needed for wall class
        def update(self):
            pass
        #end procedure
    
    #Enemy Bullet Class shot from Bow enemy
    class EnemyBullet(pygame.sprite.Sprite):
        def __init__(self, color, speedx, speedy, x, y):
            super().__init__()
            self.image = Game.enemybulletspritesheet.get_image(0,0,22,24,12,12)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.speedx = speedx
            self.speedy = speedy
            self.rect.y = y
            self.rect.x = x

        #Update method that moves the bullet according to the speed set by the bow enemy
        def update(self):
            #move the bullet up and down
            self.rect.y += self.speedy
            #check for wall collision and kill the bullet
            if pygame.sprite.groupcollide(game.enemybullet_group, game.wall_group, True, False) == True:
                self.kill()

            #move the bullet left or right    
            self.rect.x += self.speedx
            #check for wall collision and kill the bullet
            if pygame.sprite.groupcollide(game.enemybullet_group, game.wall_group, True, False) == True:
                self.kill()
            #Check if it travel past the boundaries and kills the sprite
            if self.rect.x > 1000:
                self.kill()
            if self.rect.x < 0:
                self.kill()

            #Check if it collides with the player and inflict 10 damage on the player
            player_hit_group = pygame.sprite.groupcollide(game.player_group, game.enemybullet_group, False, True)
            for game.player in player_hit_group:
                game.player.getdamage(10)
            #Check for collision with player bullet and kill the bullet and then kill itself and add points to game score
            enemybullet_hit_group = pygame.sprite.groupcollide(game.enemybullet_group, game.bullet_group, False, True)
            for self in enemybullet_hit_group:
                self.kill()
                game.score +=20
            #Check for collision with player's sword and kill itself when colliding and add points to game score
            enemysword_hit_group = pygame.sprite.groupcollide(game.enemybullet_group, game.sword_group, False, False)
            for self in enemysword_hit_group:
                self.kill()
                game.score +=20
                

    #Sword Class that is used with the player
    class Sword(pygame.sprite.Sprite):
        def __init__(self, color, radius):
            #call sprite constructor
            super().__init__()
            self.image = pygame.Surface((radius, radius))
            #self.image.fill(BLACK)
            #Create a circle to form the radius that the sword covers
            pygame.draw.circle(self.image, (color), (int(radius/2), int(radius/2)), int(radius/2))
            self.rect = self.image.get_rect() 
            self.rect.center = (0, 0)
            self.previousattacktime = pygame.time.get_ticks()
            self.radius = radius

        #Update function to set the sword to always be centered on the player depending on the size of the radius
        def update(self):
            if self.radius == 50:
                self.rect.y = game.player.rect.y -5
                self.rect.x = game.player.rect.x  -5
            else:
                self.rect.y = game.player.rect.y -15
                self.rect.x = game.player.rect.x  -15
            #Set the sword to remove itself after 750 milliseconds after Space is pressed
            self.currentattacktime = pygame.time.get_ticks()
            if self.currentattacktime - self.previousattacktime > 750:
                self.kill()
                self.previousattacktime = self.currentattacktime

            


    #Key class that is created after every enemy is killed
    class Key(pygame.sprite.Sprite):
        def __init__(self,color,x,y):
            #Initiate sprite constructor
            super().__init__()
            self.image = Game.keyspritesheet.get_image(0,0,38,22,25,15)
            self.image.set_colorkey(BLACK)
            self.rect = self.image.get_rect()
            self.rect.y = y
            self.rect.x = x

        #Update function check for collision and increase game score
        def update(self):
            #Check for collision with player and add one to key attribute in player
            key_hit_group = pygame.sprite.groupcollide(game.key_group, game.player_group, False, False)
            for self in key_hit_group:
                #increase score and then remove itself.
                game.player.gamekeys += 1
                game.score += 50
                self.kill()
                


    #Wall class to create boundaries
    class Wall(pygame.sprite.Sprite):
        def __init__(self, color, width, height, x, y, posx, posy):
            #call sprite constructor
            super().__init__()
            #create a sprite
            self.image = Game.wallspritesheet.get_image(479,576,32,32,40,40)
            #self.image.fill(color)
            #set the position of the sprite
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.positionx = posx
            self.positiony = posy
        #end procedure
        #No updates needed for wall class
        def update(self):
            pass
        #end procedure

        #Method to find the vector position of the wall in the grid
        def getpos(self):
            return [self.positionx/40, self.positiony/40]

    #Innerwall Class inherits the wall class
    class InnerWall(Wall):
        def __init__(self, color, width, height, x, y, posx, posy):
            super().__init__(color, width, height, x, y, posx, posy)
            self.image = Game.cratespritesheet.get_image(0,0,32,32,40,40)
        
        
        #endprocedure

        #Update function for the inner wall could be used in the future to make them destructible
        def update(self):
            pass

    #Door class is used to prevent the player from proceeding to next level without completing the level.        
    class Door(pygame.sprite.Sprite):
        def __init__(self, color, width, height, x, y, posx, posy):
            super().__init__()
            #use sprite constructor
            self.angle = 0
            self.positionx = posx
            self.positiony = posy
            if self.positionx == 0:
                self.angle = 90
            elif self.positionx == 24:
                self.angle = -90
            self.image = pygame.transform.rotate(Game.doorspritesheet.get_image(64,96,16,16,40,40), self.angle)
            self.image.set_colorkey(ORANGE)
            #self.image.fill(color)
            #set the position of the sprite
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            
            
            
        #end procedure

        #Update function checks what the level is and checks if the level is over before removing the door object
        def update(self):
            if (game.level + 1) % 5 != 0:
                #Check if the level is a multiple of 5 and if not then check all keys have been collected and the chest unlocked
                if  game.player.gamekeys >= ((2*(game.level+1)) + 1):
                    if game.chestunlocked[game.level] == True:
                        self.kill()
                        
            else:
                #If the level is a multiple of 5 and the boss has been defeated then open the doors.
                if len(game.boss_group) == 0:
                    if game.chestunlocked[game.level] == True:
                        self.kill()

    #Spike class which covers a full tile and inflicts damage to the player when active
    class Spikes(pygame.sprite.Sprite):
        def __init__(self, color, width, height, x, y, posx, posy):
            super().__init__()
            #Use sprite constructor
            self.image = pygame.image.load(os.path.join(image_path, "spike down.png"))
            #self.image.fill(color)
            self.rect = self.image.get_rect()
            #set the coordinates
            self.rect.x = x
            self.rect.y = y
            #Set timers to change every 4 seconds between active and inactive states
            self.previousattacktime = pygame.time.get_ticks()
            self.color = color
            self.previousdamagetime = pygame.time.get_ticks()

        #end procedure

        #Update function
        def update(self):
            #Check if the time is greater than 4 seconds before changing state
            self.currentattacktime = pygame.time.get_ticks()
            if self.currentattacktime - self.previousattacktime > 4000:
                if self.color == GREY:
                    self.color = LIGHTBLUE
                    self.image = pygame.image.load(os.path.join(image_path, "spike up.png"))
                    #reset the timer
                    self.previousattacktime = self.currentattacktime
                else:
                #If they are already active after 4 seconds then switch back to inactive
                    self.color = GREY
                    self.image = pygame.image.load(os.path.join(image_path, "spike down.png"))
                    #reset the timer
                    self.previousattacktime = self.currentattacktime
            #If the spikes are active then check for player collision
            if self.color == LIGHTBLUE:
                player_hit_group = pygame.sprite.spritecollide(self, game.player_group, False, False)
                for game.player in player_hit_group:
                    #If player collision is true then inflict 5 damage every 4 seconds (this limits the spike to only attack the player once when activated)
                    self.currentdamagetime = pygame.time.get_ticks()
                    if self.currentdamagetime - self.previousdamagetime > 4000:
                        game.player.getdamage(5)
                        #reset attack timer
                        self.previousdamagetime = self.currentdamagetime


    #Chest class used to unlock player's abilities at the end of each level
    class Chest(pygame.sprite.Sprite):
        def __init__(self,color, width, height, x, y, level):
            super().__init__()
            self.image = Game.wallspritesheet.get_image(224,0,32,32,40,40)
            self.image.set_colorkey(GREEN)
            #set the position of the sprite
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.level = level

        #Update function used to check for player collision
        def update(self):
            #Check what the level is so when the chest collides with the player then unlock an ability for each level.
            chest_hit_group = pygame.sprite.groupcollide(game.chest_group, game.player_group, False, False)
            for game.chest in chest_hit_group:
                if self.level == 0:
                    game.player.canshoot = True
                    
                if self.level == 1:
                    game.player.swordradius = 70
                    
                if self.level == 2:
                    game.player.maximum_health = 200
                    
                if self.level == 3:
                    game.player.multishot = True
                #When the player collides then remove the chest and set the chest unlocked to true for that level.
                game.chestunlocked[game.level] = True
                self.kill()

    #Melee Enemy class 
    class MeleeEnemy(pygame.sprite.Sprite):
        def __init__(self, direction, width, height, x, y, health):
            #call sprite constructor
            super().__init__()
            #create a sprite
            self.image = Game.menemyspritesheet.get_image(19,21,43,55,40,40)
            self.image.set_colorkey(GREEN)
            #set the position of the sprite
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.health = health
            self.direction = direction
            self.speed_x = 0
            self.speed_y = 0
            #self.goal = vec(13,3)
            #self.start = vec(self.rect.x, self.rect.y)
            #Set timers to attack the player and set the movement speed to 3 pixels per frame
            #self.previouspathtime = pygame.time.get_ticks()
            self.movex = 1
            self.movey = 1
            self.previousdamagetime = pygame.time.get_ticks()
            self.previousattacktime = pygame.time.get_ticks()
        #end procedure

        #Method to add the speed to the object to move up, down and side to side
        def changespeed(self,x,y):
            self.speed_x += x
            self.speed_y += y


        #update function handles collisions and changes behaviour depending on the range of the enemy
        def update(self):

            #Check if the player is 300 pixels away from the enemy
            if self.is_close() == True:
                #if this is true then use the movetoplayer method to make the enemy move towards the player.
                self.movetoplayer(game.player)
            #If False then use the move method instead which makes the enmey bounce off walls.
            if self.is_close() == False:
                self.MOVE()
                wallcollision = pygame.sprite.spritecollide(self, game.wall_group, False)
                if wallcollision:
                    #if there is a collision then reflect the speeds
                    self.movex = self.movex * -1
                    self.movey = self.movey * -1

            #if the enemy collides with a bullet then subtract 20 health from the enemy.
            enemybullet_hit_group = pygame.sprite.groupcollide(game.enemy_group, game.bullet_group, False, True)
            for self in enemybullet_hit_group:
                self.health -= 20
                #print(self.health)
                #Check if the health is greater than zero. Else it will create an instance of a key and increase the game score by 100 before removing itself.
                if self.health < 1:
                    game.score += 100
                    gamekey = Key(PINK, self.rect.x + 2, self.rect.y + 9)
                    game.all_sprites_group.add(gamekey)
                    game.key_group.add(gamekey)
                    self.kill()
            #check for a collision with the sword and only allow the sword to inflict 20 damage per second on the enemy.
            enemysword_hit_group = pygame.sprite.groupcollide(game.enemy_group, game.sword_group, False, False)
            for self in enemysword_hit_group:
                self.currentdamagetime = pygame.time.get_ticks()
                if self.currentdamagetime - self.previousdamagetime > 1000:
                    self.health -= 20
                    self.previousdamagetime = self.currentdamagetime
                
                #Check if the health is greater than zero. Else it will create an instance of a key and increase the game score by 100 before removing itself.
                if self.health < 1:
                    game.score += 100
                    gamekey = Key(PINK, self.rect.x + 2, self.rect.y + 9)
                    game.all_sprites_group.add(gamekey)
                    game.key_group.add(gamekey)
                    self.kill()
                #endif
            #next

            #Check for collision with player.
            player_hit_group = pygame.sprite.groupcollide(game.player_group, game.menemy_group, False, False)
            for game.player in player_hit_group:
                #if the player collides with the enemy then subtract 10 health from the player every 2 seconds 
                self.currentattacktime = pygame.time.get_ticks()
                if self.currentattacktime - self.previousattacktime > 2000:
                    game.player.getdamage(10)
                    self.previousattacktime = self.currentattacktime
                 
            #self.currentpathtime = pygame.time.get_ticks()
            #if self.currentpathtime - self.previouspathtime > 500:                  
                #self.g = SquareGrid(GRIDWIDTH, GRIDHEIGHT)
                #self.goal = vec((game.player.rect.x/40),(game.player.rect.y/40))
                #self.start = vec(self.rect.x, self.rect.y)
                #print(self.start)
                #self.path = breadth_first_search(g,self.goal, self.start)
                #self.previouspathtime = self.currentpathtime
                #pass

                
                
        #Method to find vector position of the enemy on the grid
        def getpos(self):
            return vec(self.rect.x/40, self.rect.y/40)

        #Method used to control how the enemy moves when the player is not in range
        def MOVE(self):
            #Using a random number between 1 and 10 and check if it divisible by 2. this provides a 50 50 chance of the enemy bouncing up and down or side to side.
            if self.direction % 2 == 0:
                self.movey = 0
                self.rect.x += self.movex
                #If divisible by 2 then move to the right by 3 pixels.
            else:
                self.movex = 0
                self.rect.y += self.movey

        #Method to change how the enemy moves when the player is within range of the enemy
        def movetoplayer(self, Player):
            #Compare the player's position to the enemy's position and change the speed of the enemy to move it closer to the player.
            if Player.rect.x > self.rect.x:
                self.speed_x = 1
            if Player.rect.x < self.rect.x:
                self.speed_x = -1
            if Player.rect.y > self.rect.y:
                self.speed_y = 1
            if Player.rect.y < self.rect.y:
                self.speed_y = -1
            if Player.rect.x == self.rect.x:
                self.speed_x = 0
            if Player.rect.y == self.rect.y:
                self.speed_y = 0

             # Move along x axis
            self.rect.x += self.speed_x

            # Did enemy hit a wall
            block_hit_list = pygame.sprite.spritecollide(self, game.wall_group, False)  # false so it doesn't remove the wall, true would
            for wall in block_hit_list:
                # If moving right, place enemy to the left side of wall

                if self.speed_x > 0:
                    self.rect.right = wall.rect.left
                    
                else:
                    #  if  moving left, do the opposite.
                    self.rect.left = wall.rect.right
                    


            # Move along y axis
            self.rect.y += self.speed_y

            # Did enemy hit a wall
            block_hit_list = pygame.sprite.spritecollide(self, game.wall_group, False)
            for wall in block_hit_list:
                # Do same as above but on the y axis
                if self.speed_y > 0:
                    self.rect.bottom = wall.rect.top

                else:
                    self.rect.top = wall.rect.bottom


        #Method using trigonometry to check the distance between the player and the enemy and outputs whether the player is within 300 pixels or not.
        def is_close(self):
            lengthx = self.rect.x - game.player.rect.x
            lengthy = self.rect.y - game.player.rect.y
            distance = math.sqrt((lengthx ** 2) + (lengthy ** 2))
            if distance < 300:
                return True
            else:
                return False

        #method used to get the enemy's health
        def gethealth(self):
            return self.health
        #endprocedure

        #method to set the enemies health
        def sethealth(self, newhealth):
            self.health = newhealth
        #endfunction

    #Bow enemy class
    class BowEnemy(pygame.sprite.Sprite):
        def __init__(self, direction, width, height, x, y, health):
            #call sprite constructor
            super().__init__()
            #create a sprite
            self.image = Game.benemyspritesheet.get_image(19,21,43,55,40,40)
            self.image.set_colorkey(PERFECTBLUE)
            #set the position of the sprite
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            self.health = health
            self.direction = direction
            self.previousdamagetime = pygame.time.get_ticks()
            self.previousattacktime = pygame.time.get_ticks()
            #self.angle = 180
        #end procedure

        #Update function used to check if the player is in range and calculate the speeds for the bullet fired
        def update(self):
            
            if self.is_close() == True:
                #If player in range then calculate y distance and x distance as well as distance
                xdiff = (game.player.rect.x) - (self.rect.x)
                ydiff = (game.player.rect.y) - (self.rect.y)
                self.angle = math.atan2(ydiff,xdiff)
                xspeed = 3 * math.cos(self.angle)
                yspeed = 3 * math.sin(self.angle)
                #Every 1 second an enemy bullet object is created travelling in the direction using the xspeed and yspeed.
                self.currentattacktime = pygame.time.get_ticks()
                if self.currentattacktime - self.previousattacktime > 2000:
                    game.ebullet = EnemyBullet(RED, xspeed, yspeed, self.rect.x+20, self.rect.y+20)
                    game.all_sprites_group.add(game.ebullet)
                    game.enemybullet_group.add(game.ebullet)
                    #reset the timer
                    self.previousattacktime = self.currentattacktime
            
            #Create a line for testing purposes to be used to check for line of sight. If line of sight is true then the enemy can shoot.
            line = pygame.draw.line(screen, RED, (game.player.rect.x,game.player.rect.y), (self.rect.x,self.rect.y))
            

            
            #if the enemy collides with a bullet then subtract 20 health from the enemy.
            enemybullet_hit_group = pygame.sprite.groupcollide(game.enemy_group, game.bullet_group, False, True)
            for self in enemybullet_hit_group:
                self.health -= 20
                #print(self.health)
                
                #Check if the health is greater than zero. Else it will create an instance of a key and increase the game score by 100 before removing itself.
                if self.health < 1:
                    game.score += 100
                    gamekey = Key(PINK, self.rect.x + 2, self.rect.y + 9)
                    game.all_sprites_group.add(gamekey)
                    game.key_group.add(gamekey)
                    self.kill()     

            #check for a collision with the sword and only allow the sword to inflict 20 damage per second on the enemy.
            enemysword_hit_group = pygame.sprite.groupcollide(game.enemy_group, game.sword_group, False, False)
            for self in enemysword_hit_group:
                self.currentdamagetime = pygame.time.get_ticks()
                if self.currentdamagetime - self.previousdamagetime > 1000:
                    self.health -= 20
                    self.previousdamagetime = self.currentdamagetime

                #Check if the health is greater than zero. Else it will create an instance of a key and increase the game score by 100 before removing itself.
                if self.health < 1:
                    game.score += 100
                    gamekey = Key(PINK, self.rect.x + 2, self.rect.y + 9)
                    game.all_sprites_group.add(gamekey)
                    game.key_group.add(gamekey)
                    self.kill()

        
        #def line(self):
        #    pygame.draw.line(screen, RED, (game.player.rect.x,game.player.rect.y), (self.rect.x,self.rect.y))

        #end procedure

        #Get enemy's health
        def gethealth(self):
            return self.health
        #endprocedure

        #Set enemy's health
        def sethealth(self, newhealth):
            self.health = newhealth
        #endfunction

        #Method using trigonometry to check the distance between the player and the enemy and outputs whether the player is within 400 pixels or not.
        def is_close(self):
            #Calculate x distance and y distance to player
            lengthx = self.rect.x - game.player.rect.x
            lengthy = self.rect.y - game.player.rect.y
            #find total distance/ hypotenouse
            distance = math.sqrt((lengthx ** 2) + (lengthy ** 2))
            #If distance is less than 400 then return True
            if distance < 400:
                return True
            else:
                return False


    #Boss Enemy Class
    class BossEnemy(pygame.sprite.Sprite):
        def __init__(self, direction, width, height, x, y, health):
            #call sprite constructor
            super().__init__()
            #create a sprite
            self.image = Game.bossspritesheet.get_image(23,21,36,53,width,height)
            self.image.set_colorkey(PERFECTBLUE)
            #set the position of the sprite
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.y = y
            #Define attributes for health to be used in boss health bar
            self.current_health = 999
            self.maximum_health = health
            self.health_bar_length = 200
            self.target_health = 1000
            self.health_change_speed = 2
            self.health_bar_color = GREEN
            self.health_ratio = self.maximum_health/ self.health_bar_length
            self.direction = direction
            #Set timers to be used for attacks.
            self.previoushealthtime = pygame.time.get_ticks()
            self.previousdamagetime = pygame.time.get_ticks()
            self.previousattacktime = pygame.time.get_ticks()


        #method used to increase the health of the boss by an amount 
        def gethealth(self, amount):
            if self.target_health < self.maximum_health:
                self.target_health += amount
            if self.target_health >= self.maximum_health:
                self.target_health = self.maximum_health
        #endprocedure

        #Method used to remove health from the boss
        def getdamage(self,amount):
            if self.target_health > 0:
                self.target_health -= amount
            if self.target_health <=0:
                self.target_health = 0

        #Method used to create helath bar
        def advanced_health(self):
            transition_width = 0
            transition_color = RED
            
            #When health is added set the transition bar to green and increase health bar at set speed
            if self.current_health < self.target_health:
                self.current_health += self.health_change_speed
                transition_width = int((self.target_health - self.current_health)/ self.health_ratio)
                transition_color = GREEN
            #When health is removed set the transition bar to yellow and decrease the health bar at a set speed
            if self.current_health > self.target_health:
                self.current_health -= self.health_change_speed
                transition_width = int((self.target_health - self.current_health)/ self.health_ratio)
                transition_color = YELLOW

            #Change the health bar colour depending on the amount of health
            if self.current_health >= 700:
                self.health_bar_color = GREEN
            if self.current_health >= 500 and self.current_health < 700:
                self.health_bar_color = ORANGE
            if self.current_health < 300 and self.current_health >=0:
                self.health_bar_color = RED
            #set the health bar size equal to the current health divided by max health
            health_bar_width = int(self.current_health/ self.health_ratio)
            health_bar = pygame.Rect(self.rect.x-20,self.rect.y-40, health_bar_width, 25)
            #transition bar is set to the right of the health bar
            transition_bar = pygame.Rect(health_bar.right, self.rect.y-40, transition_width, 25)
            if self.current_health > 0:
                #Draw all 3 bars over each other
                pygame.draw.rect(screen, self.health_bar_color, health_bar)
                pygame.draw.rect(screen,transition_color, transition_bar)
                pygame.draw.rect(screen, WHITE, (self.rect.x-20, self.rect.y-40, self.health_bar_length, 25), 4)


        #Update function to change behaviour of Boss depending on its health.
        def update(self):

            #Every 10 seconds the boss regains health
            self.health_ratio = self.maximum_health/ self.health_bar_length
            self.currenthealthtime = pygame.time.get_ticks()
            if self.currenthealthtime - self.previoushealthtime > 10000:
                self.gethealth(10)
                #reset the timer
                self.previoushealthtime = self.currenthealthtime

            #Check if the health is zero then add to the game score and kill the boss
            if self.current_health < 1:
                game.score += 1000
                self.kill()

            #When the health of the boss is greater than 60% then just move towards the player
            if self.current_health >= 700:
                #move towards the player no matter the range
                self.movetoplayer(game.player)
            #When the health is lower than 60% but above 30% then move around and shoot at the player
            if self.current_health < 700 and self.current_health >= 400:
                #move towards the player and shoot projectiles
                #Calculate y distance and x distance as well as distance
                self.movetoplayer(game.player)
                xdiff = (game.player.rect.x) - (self.rect.x+80)
                ydiff = (game.player.rect.y) - (self.rect.y+80)
                self.angle = math.atan2(ydiff,xdiff)
                xspeed = 3 * math.cos(self.angle)
                yspeed = 3 * math.sin(self.angle)
                #Every 1 second an enemy bullet object is created travelling in the direction using the xspeed and yspeed.
                self.currentattacktime = pygame.time.get_ticks()
                if self.currentattacktime - self.previousattacktime > 1500:
                    game.ebullet = EnemyBullet(RED, xspeed, yspeed, self.rect.x+80, self.rect.y+80)
                    game.all_sprites_group.add(game.ebullet)
                    game.enemybullet_group.add(game.ebullet)
                    self.previousattacktime = self.currentattacktime
            if self.current_health < 400:
                #If the boss is less than 30% then shoot 8 bullets travelling up, down, left, right and all diagonal directions
                #shoot projectiles in all directions and spawn in enemies
                self.movetoplayer(game.player)
                self.currentattacktime = pygame.time.get_ticks()
                #Repeat this every second
                if self.currentattacktime - self.previousattacktime > 3500:
                    if len(game.enemybullet_group) == 0:
                        game.ebullet = EnemyBullet(RED, 3, 0, self.rect.x+80, self.rect.y+80)
                        game.all_sprites_group.add(game.ebullet)
                        game.enemybullet_group.add(game.ebullet)
                        game.ebullet = EnemyBullet(RED, 3, 3, self.rect.x+80, self.rect.y+80)
                        game.all_sprites_group.add(game.ebullet)
                        game.enemybullet_group.add(game.ebullet)
                        game.ebullet = EnemyBullet(RED, 3, -3, self.rect.x+80, self.rect.y+80)
                        game.all_sprites_group.add(game.ebullet)
                        game.enemybullet_group.add(game.ebullet)
                        game.ebullet = EnemyBullet(RED, -3, 0, self.rect.x+80, self.rect.y+80)
                        game.all_sprites_group.add(game.ebullet)
                        game.enemybullet_group.add(game.ebullet)
                        game.ebullet = EnemyBullet(RED, -3, 3, self.rect.x+80, self.rect.y+80)
                        game.all_sprites_group.add(game.ebullet)
                        game.enemybullet_group.add(game.ebullet)
                        game.ebullet = EnemyBullet(RED, -3, -3, self.rect.x+80, self.rect.y+80)
                        game.all_sprites_group.add(game.ebullet)
                        game.enemybullet_group.add(game.ebullet)
                        game.ebullet = EnemyBullet(RED, 0, 3, self.rect.x+80, self.rect.y+80)
                        game.all_sprites_group.add(game.ebullet)
                        game.enemybullet_group.add(game.ebullet)
                        game.ebullet = EnemyBullet(RED, 0, -3, self.rect.x+80, self.rect.y+80)
                        game.all_sprites_group.add(game.ebullet)
                        game.enemybullet_group.add(game.ebullet)
                        self.previousattacktime = self.currentattacktime
                while game.bosscount != 10:
                    #Create 5 melee enemies that randomly spawn in the level
                    xpos = random.randint(1,23)
                    ypos = random.randint(1,23)
                    #Check if the random number has the same coordinates as a wall or spike and if not then create an enemy
                    if game.levels[game.level][xpos][ypos] !=1 and game.levels[game.level][xpos][ypos] != 2 and game.levels[game.level][xpos][ypos] != 7:
                        game.menemy = MeleeEnemy(random.randint(0,10),40,40, xpos*40, ypos*40, 40)
                        game.all_sprites_group.add(game.menemy)
                        game.enemy_group.add(game.menemy)
                        game.bosscount = game.bosscount +1
                
            #Check if the boss collides with a player bullet then subtract 5 health from the boss.
            enemybullet_hit_group = pygame.sprite.groupcollide(game.boss_group, game.bullet_group, False, True)
            for self in enemybullet_hit_group:
                self.getdamage(5)

            #Check for a collision with the sword and only allow the sword to inflict 20 damage per second on the boss.
            enemysword_hit_group = pygame.sprite.groupcollide(game.boss_group, game.sword_group, False, False)
            for self in enemysword_hit_group:
                self.currentdamagetime = pygame.time.get_ticks()
                if self.currentdamagetime - self.previousdamagetime > 1000:
                    self.getdamage(20)
                    self.previousdamagetime = self.currentdamagetime

            #Check for collision with player.
            player_hit_group = pygame.sprite.groupcollide(game.player_group, game.boss_group, False, False)
            for game.player in player_hit_group:
                self.currentattacktime = pygame.time.get_ticks()
                #if the player collides with the boss then subtract 30 health from the player every 2 seconds 
                if self.currentattacktime - self.previousattacktime > 1000:
                    game.player.getdamage(30)
                    self.previousattacktime = self.currentattacktime



        #Method used to make the boss move towards the player
        def movetoplayer(self, Player):
            #compare the player's position to the boss' position and change the speed of the boss to move it towards the player
            if Player.rect.x  > self.rect.x:
                self.speed_x = 1
            if Player.rect.x  < self.rect.x:
                self.speed_x = -1
            if Player.rect.y  > self.rect.y:
                self.speed_y = 1
            if Player.rect.y < self.rect.y:
                self.speed_y = -1
            if Player.rect.x == self.rect.x:
                self.speed_x = 0
            if Player.rect.y == self.rect.y:
                self.speed_y = 0

             # Move along x axis
            self.rect.x += self.speed_x

            # Did enemy hit a wall
            block_hit_list = pygame.sprite.spritecollide(self, game.wall_group, False)  # false so it doesn't remove the wall, true would
            for wall in block_hit_list:
                # If moving right, place enemy to the left side of wall

                if self.speed_x > 0:
                    self.rect.right = wall.rect.left
                    
                else:
                    #  if  moving left, do the opposite.
                    self.rect.left = wall.rect.right
                    


            # Move along y axis
            self.rect.y += self.speed_y

            # Did enemy hit a wall
            block_hit_list = pygame.sprite.spritecollide(self, game.wall_group, False)
            for wall in block_hit_list:
                # Do same as above but on the y axis
                if self.speed_y > 0:
                    self.rect.bottom = wall.rect.top

                else:
                    self.rect.top = wall.rect.bottom





    #Create an instance of the Game class used for the game loop
    game = Game()
    
    #walls = [(10, 7), (11, 7), (12, 7), (13, 7), (14, 7), (15, 7), (16, 7), (7, 7), (6, 7), (5, 7), (5, 5), (5, 6), (1, 6), (2, 6), (3, 6), (5, 10), (5, 11), (5, 12), (5, 9), (5, 8), (12, 8), (12, 9), (12, 10), (12, 11), (15, 14), (15, 13), (15, 12), (15, 11), (15, 10), (17, 7), (18, 7), (21, 7), (21, 6), (21, 5), (21, 4), (21, 3), (22, 5), (23, 5), (24, 5), (25, 5), (18, 10), (20, 10), (19, 10), (21, 10), (22, 10), (23, 10), (14, 4), (14, 5), (14, 6), (14, 0), (14, 1), (9, 2), (9, 1), (7, 3), (8, 3), (10, 3), (9, 3), (11, 3), (2, 5), (2, 4), (2, 3), (2, 2), (2, 0), (2, 1), (0, 11), (1, 11), (2, 11), (21, 2), (20, 11), (20, 12), (23, 13), (23, 14), (24, 10), (25, 10), (6, 12), (7, 12), (10, 12), (11, 12), (12, 12), (5, 3), (6, 3), (5, 4)]
    #for wall in walls:
        #g.walls.append(vec(wall))
    #goal = vec(15, 8)
    #start = vec(20,1)
    #path = breadth_first_search(g, goal, start)
    

    # -------- Main Program Loop -----------
    while not done:
            # --- Main event loop
            #Declare done = True when the game_over is true returning the player to the Menu
        done = game.eventprocess()
        
            # --- Game logic should go here
            #Runs all the logic for the game loop
        game.runlogic()

            #draw the screen
            #Draws everything for the game and updates the screen
        game.display(screen)
        
            # --- Limit to 60 frames per second
        clock.tick(60)
        
#Initiate the Menu function to start with the menu
game_intro()    
# Close the window and quits.
pygame.quit()

