# --------------------------------------
# Title: Shooter.py
# Purpose: An example shooting game 
# Author: Sarah Herzog
# Date: 01/04/2022
# --------------------------------------


# --------------------------------------
# Import Libraries
# --------------------------------------
import pygame, random, pygame.freetype
# --------------------------------------


# --------------------------------------
# Spawning Function
# --------------------------------------
def spawn_enemy() :
    newEnemyX = random.randint(0,WINDOWWIDTH-enemyImage.get_width()) #
    newEnemyY = -enemyImage.get_height() # just barely above the screen
    enemyPosList.append([newEnemyX,newEnemyY])
# END spawn_enemy function


# --------------------------------------
# Initialisation and Setup
# --------------------------------------
# Initialize python so we can use it
pygame.init()

# Set up the game clock
mainClock = pygame.time.Clock()

# Set up the drawing window
WINDOWWIDTH = 700
WINDOWHEIGHT = 700
screen = pygame.display.set_mode([WINDOWWIDTH, WINDOWHEIGHT])
pygame.display.set_caption('Shooter')

# Set up some variables to use later in our game
running = True

# Set up colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Set up player
playerImage = pygame.image.load("images/player.png")
playerPos = [WINDOWWIDTH/2 - playerImage.get_width()/2, WINDOWHEIGHT - 100]
playerRect = pygame.Rect(playerPos[0], playerPos[1], playerImage.get_width(), playerImage.get_height())
PLAYERSPEED = 300
playerAlive = True

# Set up enemies
enemyImage = pygame.image.load("images/enemy.png")
enemyRect = pygame.Rect(0, 0, enemyImage.get_width(), enemyImage.get_height())
enemySpeed = 100
enemyPosList = []
enemySpawnCooldown = 3
timeSinceSpawn = 0
# Spawn a single enemy to start with
spawn_enemy()

# Set up bullets
bulletImage = pygame.image.load("images/bullet.png")
bulletRect = pygame.Rect(0, 0, bulletImage.get_width(), bulletImage.get_height())
bulletPosList = []
BULLETSPEED = 500
FIRINGCOOLDOWN = 0.5
timeSinceFire = 0

# Set up UI Font
UIFont = pygame.freetype.Font("fonts/PressStart2P-Regular.ttf",24)

# Set up Score
score = 0
scorePerEnemy = 100

# Set up win condition
scoreToWin = 200
winGame = False
# --------------------------------------


# --------------------------------------
# Game Loop
# --------------------------------------
# Run over and over until the user asks to quit
while running:
    
    # ----------------------------------
    # Input
    # ----------------------------------
    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update our key list
    keys = pygame.key.get_pressed()
    # ----------------------------------

    
    # ----------------------------------
    # Update
    # ----------------------------------
    # Get the frame time in miliseconds
    frameMs = mainClock.tick(60)
    frameSec = frameMs / 1000

    # Process Movement
    # Scale move speed by time passed since the last frame for consistant movement
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        playerPos[0] -= PLAYERSPEED * frameSec
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        playerPos[0] += PLAYERSPEED * frameSec
        
    # Move the player's rectangle based on the position variable
    playerRect.left = playerPos[0]
    playerRect.top = playerPos[1]

    # Increase time since last bullet fired
    timeSinceFire += frameSec

    # Spawn bullets if the player presses space
    if keys[pygame.K_SPACE] and playerAlive and timeSinceFire >= FIRINGCOOLDOWN:
        bulletPosList.append([playerPos[0],playerPos[1]])
        timeSinceFire = 0
    # END if for firing

    # Update bullets
    for bulletPos in bulletPosList[:]:
        # Move bullet up
        bulletPos[1] -= BULLETSPEED * frameSec

        # If it's gone off screen, remove it from the list
        if bulletPos[1] < -bulletImage.get_height():
            bulletPosList.remove(bulletPos)
        # END off screen if

        # Update bullet rect
        bulletRect.left = bulletPos[0]
        bulletRect.top = bulletPos[1]

        # Loop through enemies and check if our bullet has hit one
        # Note the special way of writing this for loop! It makes
        # a copy of our list so we can remove things from it.
        for enemyPos in enemyPosList[:]:
            # Update the enemy rectangle
            enemyRect.left = enemyPos[0]
            enemyRect.top = enemyPos[1]

            # If a bullet collides with an enemy...
            if pygame.Rect.colliderect(bulletRect,enemyRect):
                # Remove the enemy from the list
                enemyPosList.remove(enemyPos)

                # Add to the score
                score += scorePerEnemy

                # Check if we won
                if score >= scoreToWin :
                    winGame = True
                # END if for checking win state
            # END if for collision
            
        # END for loop for enemy/bullet collision
    # END for loop for updating bullets

    # Increase the time since last spawned an enemy
    timeSinceSpawn += frameSec

    # Is it time to spawn an enemy?
    if timeSinceSpawn >= enemySpawnCooldown :
        spawn_enemy()
        timeSinceSpawn = 0
    # END if for enemy spawning
        
    # Update enemies
    for enemyPos in enemyPosList[:]:
        # Move enemy down
        enemyPos[1] += enemySpeed * frameSec
        
        # Update the enemy rectangle
        enemyRect.left = enemyPos[0]
        enemyRect.top = enemyPos[1]
        
        # Check if the enemy hit the player
        if pygame.Rect.colliderect(playerRect,enemyRect):
            # If so, kill the player!
            playerAlive = False
        # END if statement for collision

        # Check if the enemy is off the screen
        if enemyPos[1] > WINDOWHEIGHT:
            # Remove the enemy from the list
            enemyPosList.remove(enemyPos)
        # END if for enemy off screen check
            
    # END for loop for enemy update
    
    
    # ----------------------------------

    
    # ----------------------------------
    # Draw
    # ----------------------------------
    # Fill the background with a colour
    screen.fill(WHITE)

    # Draw Everything

    # Draw items based on the game state
    if winGame : #Player has won!

        #Draw win message
        textRect = UIFont.get_rect("YOU WIN!")
        UIFont.render_to(screen, (WINDOWWIDTH/2 - textRect.width/2, WINDOWHEIGHT/2 - textRect.height/2), "YOU WIN!", BLACK)

    elif not playerAlive : #Player is dead

        #Draw game over message
        textRect = UIFont.get_rect("GAME OVER!")
        UIFont.render_to(screen, (WINDOWWIDTH/2 - textRect.width/2, WINDOWHEIGHT/2 - textRect.height/2), "GAME OVER!", BLACK)

    else : #Player is alive and has not yet won:
        # Draw player
        screen.blit(playerImage,playerPos)

        # Draw all of the enemies
        for enemyPos in enemyPosList:
            screen.blit(enemyImage,enemyPos)
        # END for loop for enemy drawing
        
        # Draw all of the bullets
        for bulletPos in bulletPosList:
            screen.blit(bulletImage,bulletPos)
        # END for loop for enemy drawing
        
    # END if for checking game state

    # Draw the UI text
    UIFont.render_to(screen, (10, 10), "Score: "+str(score), BLACK)

    # Flip the display to put it all onscreen
    pygame.display.flip()
    # ----------------------------------


# END of Game Loop
# --------------------------------------


# --------------------------------------
# Program Exit
# --------------------------------------
pygame.quit()
# --------------------------------------
