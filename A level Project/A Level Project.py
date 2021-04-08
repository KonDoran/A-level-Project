import pygame
import random
import os
import sys
import math
from collections import deque
vec = pygame.math.Vector2

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
ORANGE = (230,165,0)
GREY = (180,180,180)
BACKGROUND_IMAGE = pygame.image.load(os.path.join(image_path, 'Menu background.png'))
TILESIZE = 40
GRIDWIDTH = 25
GRIDHEIGHT = 25
WIDTH = TILESIZE * GRIDWIDTH
HEIGHT = TILESIZE * GRIDHEIGHT
icon_dir = os.path.join(current_path, 'icons')
goal = vec(14, 8)
start = vec(20, 0)
pygame.init()

# Set the width and height of the screen [width, height]
size = (1200, 1000)
screen_width = 1200
screen_height = 1000
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Tile Movement Game")
clock = pygame.time.Clock()

home_img = pygame.image.load(os.path.join(icon_dir, 'home.png')).convert_alpha()
home_img = pygame.transform.scale(home_img, (50, 50))
home_img.fill((0, 255, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
cross_img = pygame.image.load(os.path.join(icon_dir, 'cross.png')).convert_alpha()
cross_img = pygame.transform.scale(cross_img, (50, 50))
cross_img.fill((255, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MULT)
arrows = {}
arrow_img = pygame.image.load(os.path.join(icon_dir, 'arrowRight.png')).convert_alpha()
arrow_img = pygame.transform.scale(arrow_img, (50, 50))
for dir in [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
    arrows[dir] = pygame.transform.rotate(arrow_img, vec(dir).angle_to(vec(1, 0)))





def text_objects(text,font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

def button_1(message,xpos,ypos,width,height,inactivecolor,activecolor,action1=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if xpos+width >mouse[0] > xpos and ypos+height > mouse[1] > ypos:
        pygame.draw.rect(screen, inactivecolor,(xpos,ypos,width,height),5)
        if click[0] == 1 and action1 !=None:
            if action1 == "1":
                gameloop()
            elif action1 == "Q":
                    pygame.quit()
    else:
        pygame.draw.rect(screen, activecolor,(xpos,ypos,width,height),5)
        
    smallText = pygame.font.Font("freesansbold.ttf",30)
    textSurf, textRect = text_objects(message, smallText)
    textRect.center = ( (xpos+(width/2)), (ypos+(height/2)) )
    screen.blit(textSurf, textRect)



def game_intro():
    intro = True
    while intro:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
              intro = False # Flag that we are done so we exit this loop
            elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE: 
                         intro=False
                         
#Drawing the menu screen
        screen.fill(BLACK)
        screen.blit(BACKGROUND_IMAGE, [0,0])
        font = pygame.font.Font('freesansbold.ttf', 84)
        text = font.render(str("DUNGEON ESCAPE"), 1, WHITE)
        text_rect = text.get_rect(center=(screen_width/2, screen_height/6))
        screen.blit(text, text_rect)
        button_1("START GAME",475,420,250,60,WHITE,GREY,"1")
        button_1("QUIT",475,490,250,60,WHITE,GREY,"Q")
            
        pygame.display.flip()
        clock.tick(60)





def vec2int(v):
    return (int(v.x), int(v.y))
    

def breadth_first_search(graph, start, end):
    frontier = deque()
    frontier.append(start)
    path = {}
    path[vec2int(start)] = None
    while len(frontier) > 0:
        current = frontier.popleft()
        if current == end:
            break
        for next in graph.find_neighbors(current):
            if vec2int(next) not in path:
                frontier.append(next)
                path[vec2int(next)] = current - next
    return path





def gameloop():

    def draw_icons():
        start_center = (game.menemy.goal.x * TILESIZE + TILESIZE / 2, game.menemy.goal.y * TILESIZE + TILESIZE / 2)
        screen.blit(home_img, home_img.get_rect(center=start_center))
        goal_center = (game.menemy.start.x * TILESIZE + TILESIZE / 2, game.menemy.start.y * TILESIZE + TILESIZE / 2)
        screen.blit(cross_img, cross_img.get_rect(center=goal_center))









    #Loop until the user clicks the close button.
    done = False
        
        # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    class SquareGrid:
        def __init__(self, width, height):
            self.width = width
            self.height = height
            self.walls = []
            self.connections = [vec(1, 0), vec(-1, 0), vec(0, 1), vec(0, -1)]
            # comment/uncomment this for diagonals:
            # self.connections += [vec(1, 1), vec(-1, 1), vec(1, -1), vec(-1, -1)]

        def in_bounds(self, node):
            return 0 <= node.x < self.width and 0 <= node.y < self.height

        def passable(self, node):
            return node not in self.walls

        def find_neighbors(self, node):
            neighbors = [node + connection for connection in self.connections]
            # don't use this for diagonals:
            if (node.x + node.y) % 2:
                neighbors.reverse()
            neighbors = filter(self.in_bounds, neighbors)
            neighbors = filter(self.passable, neighbors)
            return neighbors





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
                        g.walls.append(vec((self.outsidewall.rect.x/40), (self.outsidewall.rect.y/40)))
                    if char == 2:
                        self.innerwall = InnerWall(RED,40,40,i*40, j*40, i, j)
                        self.all_sprites_group.add(self.innerwall)
                        self.wall_group.add(self.innerwall)
                        self.innerwall_group.add(self.innerwall)
                        g.walls.append(vec((self.innerwall.rect.x/40), (self.innerwall.rect.y/40)))
                    if char == 3:
                        if self.levelcomplete[self.level] == False:
                            self.benemy = BowEnemy(random.randint(0,10),40,40, i*40, j*40, 40)
                            self.all_sprites_group.add(self.benemy)
                            self.enemy_group.add(self.benemy)
                    if char == 4:
                        if self.levelcomplete[self.level] == False:
                            self.menemy = MeleeEnemy(random.randint(0,10),40,40, i*40, j*40, 40)
                            self.all_sprites_group.add(self.menemy)
                            self.enemy_group.add(self.menemy)
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
            self.player.advanced_health()
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
                health = font.render(str(self.player.current_health), 1, WHITE)
                screen.blit(score, (1050,500))
                screen.blit(money, (1050,550))
                screen.blit(keys, (1050,600))
                screen.blit(health, (1081, 51))
                # --- Drawing code should go here
                
                self.all_sprites_group.draw(screen)
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
            self.current_health = 50
            self.maximum_health = health
            self.health_bar_length = 180
            self.target_health = 100
            self.health_change_speed = 2
            self.health_bar_color = GREEN
            self.health_ratio = self.maximum_health/ self.health_bar_length
            self.score = score
            self.money = money
            self.gamekeys = gamekeys
            self.rect.x = x
            self.rect.y = y
            self.directionx = 0
            self.directiony = 5
            self.previoushealthtime = pygame.time.get_ticks()
            self.previousbullettime = pygame.time.get_ticks()
            
        #end procedure
        def gethealth(self, amount):
            if self.target_health < self.maximum_health:
                self.target_health += amount
            if self.target_health >= self.maximum_health:
                self.target_health = self.maximum_health
        #endprocedure

        def getdamage(self,amount):
            if self.target_health > 0:
                self.target_health -= amount
            if self.target_health <=0:
                self.target_health = 0

        def advanced_health(self):
            transition_width = 0
            transition_color = RED
            

            if self.current_health < self.target_health:
                self.current_health += self.health_change_speed
                transition_width = int((self.target_health - self.current_health)/ self.health_ratio)
                transition_color = GREEN

            if self.current_health > self.target_health:
                self.current_health -= self.health_change_speed
                transition_width = int((self.target_health - self.current_health)/ self.health_ratio)
                transition_color = YELLOW

            if self.current_health >= 70:
                self.health_bar_color = GREEN
            if self.current_health >= 50 and self.current_health < 70:
                self.health_bar_color = ORANGE
            if self.current_health < 30 and self.current_health >=0:
                self.health_bar_color = RED

            health_bar_width = int(self.current_health/ self.health_ratio)
            health_bar = pygame.Rect(1005,45, health_bar_width, 25)
            transition_bar = pygame.Rect(health_bar.right, 45, transition_width, 25)

            pygame.draw.rect(screen, self.health_bar_color, health_bar)
            pygame.draw.rect(screen,transition_color, transition_bar)
            pygame.draw.rect(screen, WHITE, (1005, 45, self.health_bar_length, 25), 4)



        def getscore(self):
            return self.score
        #endprocedure

        def getpos(self):
            return vec(self.rect.x/40, self.rect.y/40)
        #endfunction

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
                self.currentbullettime = pygame.time.get_ticks()
                if self.currentbullettime - self.previousbullettime > 500:
                    bullet = Bullet(RED, self.directionx, self.directiony)
                    game.bullet_group.add(bullet)
                    game.all_sprites_group.add(bullet)
                    self.previousbullettime = self.currentbullettime
            if keys[pygame.K_e]:
                if len(game.sword_group) == 0:
                    sword = Sword(GREEN)
                    game.sword_group.add(sword)
                    game.all_sprites_group.add(sword)
                    


            #end if

            self.currenthealthtime = pygame.time.get_ticks()
            if self.currenthealthtime -self.previoushealthtime > 10000:
                self.gethealth(10)
                self.previoushealthtime = self.currenthealthtime



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
            return [self.positionx/40, self.positiony/40]

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
            self.speed_x = 0
            self.speed_y = 0
            self.goal = vec(13,3)
            self.start = vec(self.rect.x, self.rect.y)
            self.previouspathtime = pygame.time.get_ticks()
            self.move = 3
        #end procedure

        def changespeed(self,x,y):
            self.speed_x += x
            self.speed_y += y



        def update(self):


            if self.is_close() == True:
                self.movetoplayer(game.player)
            elif self.is_close() == False:
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
                #endif
            #next

            self.currentpathtime = pygame.time.get_ticks()
            if self.currentpathtime - self.previouspathtime > 500:                  
                #self.g = SquareGrid(GRIDWIDTH, GRIDHEIGHT)
                #self.goal = vec((game.player.rect.x/40),(game.player.rect.y/40))
                #self.start = vec(self.rect.x, self.rect.y)
                #print(self.start)
                #self.path = breadth_first_search(g,self.goal, self.start)
                #self.previouspathtime = self.currentpathtime
                pass

                
                
        
        def getpos(self):
            return vec(self.rect.x/40, self.rect.y/40)

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


        def movetoplayer(self, Player):

            if Player.rect.x - 10 > self.rect.x:
                self.speed_x = 2
            if Player.rect.x - 10 < self.rect.x:
                self.speed_x = -2
            if Player.rect.y - 10 > self.rect.y:
                self.speed_y = 2
            if Player.rect.y - 10< self.rect.y:
                self.speed_y = -2

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

        def is_close(self):
            lengthx = self.rect.x - game.player.rect.x
            lengthy = self.rect.y - game.player.rect.y
            distance = math.sqrt((lengthx ** 2) + (lengthy ** 2))
            if distance < 300:
                return True
            else:
                return False

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
    
    g = SquareGrid(GRIDWIDTH, GRIDHEIGHT)
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
        done = game.eventprocess()
        
            # --- Game logic should go here
        game.runlogic()

            #draw the screen
        game.display(screen)
        
            # --- Limit to 60 frames per second
        clock.tick(60)
        

game_intro()
# Close the window and quit.
pygame.quit()

