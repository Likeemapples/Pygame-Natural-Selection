import pygame, sys, os, random, math, time, colorsys
from pygame.locals import *

pygame.init()
pygame.font.init() 
my_font = pygame.font.SysFont('Comic Sans MS', 30)

# Constants
WIDTH, HEIGHT = 800,600
FPS = 60

# Sound making
snd_COIN_COLLECT = pygame.mixer.Sound('Coin.wav')
snd_COIN_COLLECT.set_volume(0.5)

# This is for coin spawning
tick = 0

# For scaling the penguin img 
square_size = 50 

# Make base coins
quantum_coin = []
# Named quantum coin because theres only one that zips around really quick
for i in range(0, 10):
    quantum_coin.append( 
        [
            round(random.randrange(0, WIDTH)), 
            round(random.randrange(0, HEIGHT)), 
            10
        ] 
    )

# Penguin setup
PENGUIN_LOAD = pygame.image.load('penguin.jpg')
PENGUIN_IMG = pygame.transform.scale(PENGUIN_LOAD, (square_size, square_size))

penguins = []
penguinIds = []

highestId = -1

# Functions
def find_in_array(index, array):
    '''Find reference in array, returns none if doesn't exist'''
    for i in range(0, len(array)):
        if index == array[i]:
            return i

# Colors, handy
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Penguin():
    '''Evolution handling class'''

    def __init__(self):
        global highestId
        self.image = PENGUIN_IMG
        self.id = highestId+1
        highestId += 1
        self.rect = pygame.Rect(
                                    (WIDTH - square_size) // 2, 
                                    (HEIGHT - square_size) // 2, 
                                    square_size, square_size
                                )
        self.chosen_coin_index = (random.randrange(0,len(quantum_coin))) if (len(quantum_coin) > 0) else (0)
        self.chosen_coin = quantum_coin[self.chosen_coin_index]
        self.health = 300
        self.reproductionLimit = 350
        self.reproductionGive = 100
        self.speed = 5
        self.color = 10
        self.dead = False


    def update(self):
        # Find index, this is for dying
        self.index = find_in_array(self.id, penguinIds)

        # Quantum Coin stuff, complicated

        

        # Move towards quantum coin on the x axis
        if (abs(self.chosen_coin[0] - (self.rect.x + square_size/2)) > 2):
            if (self.chosen_coin[0] < self.rect.x + square_size/2):
                self.rect.x -= self.speed
            elif (self.chosen_coin[0] > self.rect.x + square_size/2):
                self.rect.x += self.speed

        # Move towards quantum coin on the y axis
        if (abs(self.chosen_coin[1] - (self.rect.y + square_size/2)) > 2):        
            if (self.chosen_coin[1] < self.rect.y + square_size/2):
                self.rect.y -= self.speed
            elif (self.chosen_coin[1] > self.rect.y + square_size/2):
                self.rect.y += self.speed

        # Handle finding new quantum coins        
        if (self.chosen_coin_index < len(quantum_coin)):
            if (self.chosen_coin != quantum_coin[self.chosen_coin_index]):
                self.chosen_coin_index = random.randrange(0,len(quantum_coin))
                self.chosen_coin = quantum_coin[self.chosen_coin_index]
        elif (len(quantum_coin) > 0):
            self.chosen_coin_index = random.randrange(0,len(quantum_coin))
            self.chosen_coin = quantum_coin[self.chosen_coin_index]

        # Handle collisions with coins
        for position in quantum_coin:
            # I have to split up the sections here into dedicated and not dedicated
            # Or else it doesnt work right, this is because of how
            # The penguins decide to go to their coins
            
            # Handle collision with dedicated coin
            if (self.rect.colliderect(self.chosen_coin[0], self.chosen_coin[1], 10, 10)):
                quantum_coin.pop(self.chosen_coin_index)
                # If no coins exist, make one
                # This avoids crashing
                if (len(quantum_coin) == 0):
                    quantum_coin.append( 
                        [
                            round(random.randrange(0, WIDTH)), 
                            round(random.randrange(0, HEIGHT)), 
                            1
                        ] 
                    )
                self.chosen_coin_index = random.randrange(0,len(quantum_coin))
                self.chosen_coin = quantum_coin[self.chosen_coin_index]
                #while (self.rect.colliderect(position[0], position[1], 10, 10)):
                #    position[0], position[1] = round(random.randrange(0, WIDTH)), round(random.randrange(0, HEIGHT))
                self.health += 50
                pygame.mixer.Sound.play(snd_COIN_COLLECT, 0, 0, 0)

            # Handle collision with other coins            
            if (self.rect.colliderect(position[0], position[1], 10, 10)):
                coin_id = find_in_array(position, quantum_coin)
                if (coin_id != None):
                    quantum_coin.pop(coin_id)
                    self.health += 50
                    pygame.mixer.Sound.play(snd_COIN_COLLECT, 0, 0, 0)

        # Decrement health, woah, so useful, thanks comment
        self.health -= 1
        
        if (self.health >= self.reproductionLimit):
            self.health -= self.reproductionGive
            tempPen = Penguin()

            # Mutations
            tempPen.color = self.color + (random.randrange(-1000, 1000)/10000)

            tempPen.health = self.reproductionGive
            tempPen.reproductionGive = self.reproductionGive + random.randrange(-5,5)

            tempPen.reproductionLimit = self.reproductionLimit + random.randrange(-5,5)

            tempPen.speed = self.speed + random.randrange(-5,5)
            #if (tempPen.speed > 10):
            #    tempPen.speed = 10
            #elif (tempPen.speed < 5):
            #    tempPen.speed = 5

            # This makes the new penguin work. yay
            tempPen.index = len(penguins)
            tempPen.rect.x, tempPen.rect.y = self.rect.x, self.rect.y

            penguins.append(tempPen)
            penguinIds.append(tempPen.id)

        # Drawing, in this case im drawing over the penguin image, but there is a penguin i swear
        h, s, v = colorsys.hsv_to_rgb(self.color, 1, 1)
        self.image.fill((abs(h*255), abs(s*255), abs(v*255)))
        screen.blit(self.image, (self.rect.x, self.rect.y))
        screen.blit(my_font.render(str(self.health), False, (0, 0, 0)), (self.rect.x, self.rect.y))
        
        # Die
        if (self.health <= 0):
            if (not self.dead):
                penguins.pop(self.index)
                penguinIds.pop(self.index)
                self.dead = True
            del self

# Setup up the first two penguins, this is poor code, but writing a function doesn't make sense
# for so few lines of code
pen = Penguin()
pen.color = 1
pen.index = 0
pen2 = Penguin()
pen2.color = 0.5
pen.index = 1

penguins.append(pen)
penguins.append(pen2)
penguinIds = [0, 1]

# Can be changed
BG_COLOR = (0,0,0)

# Window Init
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.mixer.init()
pygame.mixer.set_num_channels(64)

pygame_icon = pygame.image.load('icon.png')
pygame.display.set_icon(pygame_icon)
pygame.display.set_caption("Challenge 1")

# Main game loop
running = True
while running:

    # Set timers
    clock.tick(FPS)
    tick += 1

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Screen fill
    screen.fill(BG_COLOR)

    # Handle penguins
    for penguin in penguins:
        penguin.update()
        
    # Quantum Coins
    for position in quantum_coin:
        h, s, v = colorsys.hsv_to_rgb(position[2], 1, 1)
        position[2] += 0.025
        pygame.draw.circle(screen, (h*255, s*255, v*255), (position[0], position[1]), 10)

    if (tick % 1 == 0):
        quantum_coin.append( 
            [
                round(random.randrange(0, WIDTH)), 
                round(random.randrange(0, HEIGHT)), 
                1
            ] 
        )
    
    # If dead
    if (len(penguins) == 0):
        screen.blit(my_font.render("ALL DEAD", False, (255, 0, 0)), ((WIDTH - square_size) // 2, 
                                    (HEIGHT - square_size) // 2))
        

    # Update
    pygame.display.flip()

# :(
pygame.quit()
sys.exit()
