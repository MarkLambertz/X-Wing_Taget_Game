# -*- coding: utf-8 -*-
# X-Wing Target Game

import random  
import pygame
from RPi import GPIO
from time import sleep
from pygame.locals import *

# Define some colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
GREEN    = (   0, 255,   0)
RED      = ( 255,   0,   0)

random.seed()

pygame.mixer.pre_init(44100, -16, 2, 2048)
     
pygame.init()

# GPIO Setmode & Setup
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.setup(7, GPIO.IN)
GPIO.setup(5, GPIO.IN)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(7,False)
GPIO.setup(5,False)
   
# Set the width and height of the screen [width,height]
size = [800, 600]
screen = pygame.display.set_mode(size)
  
pygame.display.set_caption("X-Wing Target Mode")
  
#Loop until the user clicks the close button.
done = False
  
# Used to manage how fast the screen updates
clock = pygame.time.Clock()


# FX Section
shot_sound = pygame.mixer.Sound("X-Wing-Laser.wav")

# Schalter FX-Sounds
sound1 = pygame.mixer.Sound("LAZER.wav")
sound2 = pygame.mixer.Sound("specFX.wav")
sound3 = pygame.mixer.Sound("xwing.wav")

# Background Sound
pygame.mixer.music.load("X-Wing_fly_normal.mp3")
pygame.mixer.music.play(-1)

# Image Names
myTie = pygame.image.load("Tiefighter_Shape.png")
myBG = pygame.image.load("BG.png").convert()


# Start position Joystick - actually not used right now
x_coord = 400
y_coord = 300

# Start position Tiefighter
tie_start_x = random.randint(100,300)  
tie_start_y = random.randint(100,300)  

# Tie Speed in Pixels per Second
tie_speed = 50

#Frame counter
frame_no = 0

#Distance moved
distance_moved_x = 0
distance_moved_y = 0


# Count the joysticks the computer has
joystick_count = pygame.joystick.get_count()
if joystick_count == 0:
# No joysticks!
    print ("Error, I didn't find any joysticks.")
else:
# Use joystick #0 and initialize it
    my_joystick = pygame.joystick.Joystick(0)
    my_joystick.init()
             
while not done:
 
    # ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.JOYBUTTONDOWN:
          shot_sound.play()
          GPIO.output(10, True)
      
    # ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
 
    # ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
             
    # As long as there is a joystick
    if joystick_count != 0:
     
        # This gets the position of the axis on the game controller
        # It returns a number between -1.0 and +1.0
        horiz_axis_pos = my_joystick.get_axis(0)
        vert_axis_pos = my_joystick.get_axis(1)   

        # Joystick Coords ---- Move x according to the axis. Mltiply by 10 to speed up the movement.
        x_coord = x_coord + int(horiz_axis_pos * 10)
        y_coord = y_coord + int(vert_axis_pos * 10)

        
        # Tie Fighter Änderungsvektor
        
        time_passed = clock.tick(60)
        seconds = time_passed / 1000.0

        distance_moved = seconds * tie_speed

        opzahl_x = random.randint(1,2)
        if opzahl_x == 1:
#            tie_start_x = tie_start_x + random.randint(1,tie_speed)
            tie_start_x += distance_moved_x

        elif opzahl_x == 2:
#            tie_start_x = tie_start_x - random.randint(1,tie_speed)
            tie_start_x -= distance_moved_x


        opzahl_y = random.randint(1,2)
        if opzahl_y == 1:
        #    tie_start_y = tie_start_y + random.randint(1,tie_speed)
            tie_start_y += distance_moved_y

        elif opzahl_y == 2:
        #    tie_start_y = tie_start_y - random.randint(1,tie_speed)
            tie_start_y -= distance_moved_y


        if (frame_no % 3) == 0: # Definition which frames are displayed/skipped
            distance_moved_x = seconds * tie_speed
            distance_moved_y = seconds * tie_speed
    

##        Old code of my second version
##        opzahl_x = random.randint(1,2)
##        if opzahl_x == 1:
##            tie_start_x = tie_start_x + random.randint(1,1)
##            if tie_start_x < 200:
##                tie_start_x = 200 
##            elif tie_start_x > 600:
##                tie_start_x = 600
##        elif opzahl_x == 2:
##            tie_start_x = tie_start_x - random.randint(1,1)
##            if tie_start_x < 200:
##                tie_start_x = 200
##            if tie_start_x > 600:
##                tie_start_x = 600
##                
##        opzahl_y = random.randint(1,2)
##        if opzahl_y == 1:
##            tie_start_y = tie_start_y + random.randint(1,1)
##            if tie_start_y < 200:
##                tie_start_y = 200
##            if tie_start_y > 400:
##                tie_start_y = 400
##        elif opzahl_y == 2:
##            tie_start_y = tie_start_y - random.randint(1,1) 
##            if tie_start_y < 200:
##                tie_start_y = 200
##            if tie_start_y > 400:
##                tie_start_y = 400


        # Resultierender Bewegungsvektor Joystick Testing

##        tie_start_x += x_coord
##        tie_start_y += y_coord

			# Limit x/y-Coordinates 
            if tie_start_x < 200:
                tie_start_x = 200
            if tie_start_x > 600:
                tie_start_x = 600

            if tie_start_y < 200:
                tie_start_y = 200
            if tie_start_y > 400:
                tie_start_y = 400

        # GPIO Fun
    if GPIO.input(5):
        sound2.play()
        sleep(0.05)
        while GPIO.input(5):
            sleep(0.05)

        GPIO.output(10, True)
        sleep(1)
              
        GPIO.output(10, False)
    
    if GPIO.input(7): 
        sound1.play()
        sleep(0.05)
        while GPIO.input(7):
            sleep(0.05)

        # Lampe einschalten
            GPIO.output(10, True)
            sleep(1)
        
        # Lampe ausschalten   
        GPIO.output(10, False)
        sound3.play()


     
    # ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT    

    
    # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
      
    # First, clear the screen to WHITE. Don't put other drawing commands
    # above this, or they will be erased with this command.

    screen.fill(BLACK)    

    # Blit BG Image - could be done nicer, but the Pi is fast enough
    screen.blit(myBG, [0,0])
 
 
    # Draw the item at the proper coordinates
    screen.blit(myTie, [tie_start_x, tie_start_y])

    # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT    

    pygame.display.update()
    frame_no += 1
    # pygame.display.flip()
     
pygame.quit()
