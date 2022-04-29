# --------------------------------------
# Title: Shooter.py
# Purpose: An example shooting game 
# Author: Sarah Herzog
# Date: 01/04/2022
# --------------------------------------


# --------------------------------------
# Import Libraries
# --------------------------------------
import pygame, random, pygame.freetype, math
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
bulletDirList = []
BULLETSPEED = 400
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

# Set up health
health = 100
damagePerEnemy = 50

# Set up player rotation
mousePos = (0,0)
firingDir = (0,-1)
playerAngle = 0

# Set up sound effects
fireSound = pygame.mixer.Sound("audio/fire.ogg")

# Set up and play music
pygame.mixer.music.load("audio/music.ogg")
pygame.mixer.music.play(0)

# Example dino animation
dinoAnimRun = [
    pygame.image.load("images/dino-run-1.png"),
    pygame.image.load("images/dino-run-2.png")
]
dinoAnimIndex = 0
dinoAnimFrameTime = 0.5
timeSinceDinoAnim = 0

# Box for solid collisions
boxImage = pygame.image.load("images/box.png")
boxRect = pygame.Rect(300, 300, boxImage.get_width(), boxImage.get_height())

# Camera stuff
cameraOffset = [WINDOWWIDTH/2, WINDOWHEIGHT/2] # Used to determine where the player will be on the screen for player follow
cameraPos = playerPos   # Assumes camera centred on player, change as desired

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

    # Pause the game if we won or lost
    if not playerAlive or winGame :
        frameSec = 0
    # END if for game pause

    # Process Movement
    # Scale move speed by time passed since the last frame for consistant movement
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        playerPos[0] -= PLAYERSPEED * frameSec
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        playerPos[0] += PLAYERSPEED * frameSec
    if keys[pygame.K_RIGHT] or keys[pygame.K_w]:
        playerPos[1] -= PLAYERSPEED * frameSec
    if keys[pygame.K_RIGHT] or keys[pygame.K_s]:
        playerPos[1] += PLAYERSPEED * frameSec

    # Rotate to face the mouse
    mousePos = pygame.mouse.get_pos()
    firingDir = (mousePos[0]-(playerPos[0]-cameraPos[0]),mousePos[1]-(playerPos[1]-cameraPos[1]))
    firingMag = math.sqrt(firingDir[0]*firingDir[0]+firingDir[1]*firingDir[1])
    firingDir = (firingDir[0]/firingMag, firingDir[1]/firingMag)
    angle = 270-math.atan2(firingDir[1],firingDir[0])*180/math.pi
    playerImageRot = pygame.transform.rotate(playerImage,angle)

    # Get new rect from rotated image and use position variable
    playerRect = playerImageRot.get_rect(center = playerPos)

    # Increase time since last bullet fired
    timeSinceFire += frameSec


    
    # Firing
    if keys[pygame.K_SPACE] and playerAlive and timeSinceFire >= FIRINGCOOLDOWN:
        # Fire the bullet!
        newBulletX = playerPos[0] + 20
        newBulletY = playerPos[1]
        bulletPosList.append([newBulletX,newBulletY])
        bulletDirList.append(firingDir)
        timeSinceFire = 0
        pygame.mixer.Sound.play(fireSound)
    # END if space pressed
    
    # Update for bullets
    for i in range(len(bulletPosList)):
        bulletPos = bulletPosList[i]
        bulletDir = bulletDirList[i]
        
        # Move bullet in the correct direction
        bulletPos[0] += BULLETSPEED * frameSec * bulletDir[0]
        bulletPos[1] += BULLETSPEED * frameSec * bulletDir[1]

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
    # END if for checking enemy spawn
    
    # Update enemies
    for enemyPos in enemyPosList[:]:
        # Move enemy down
        enemyPos[1] += enemySpeed * frameSec
        
        # Update the enemy rectangle
        enemyRect.left = enemyPos[0]
        enemyRect.top = enemyPos[1]
        
        # Check if the enemy hit the player
        if pygame.Rect.colliderect(playerRect,enemyRect):
            # Damage the player
            health -= damagePerEnemy

            # Is the player dead?
            if health <= 0 :
                playerAlive = False
                pygame.mixer.music.stop()
            # END if statement for player death

            # Remove the enemy so it doesn't hit us twice
            enemyPosList.remove(enemyPos)
        # END if statement for collision

        # Check if the enemy is off the screen
        if enemyPos[1] > WINDOWHEIGHT:
            # Remove the enemy from the list
            enemyPosList.remove(enemyPos)
        # END if for enemy off screen check
            
    # END for loop for enemy update

    # Update animation
    timeSinceDinoAnim += frameSec
    # Is it time to change the animation image?
    if timeSinceDinoAnim >= dinoAnimFrameTime :
        timeSinceDinoAnim = 0
        # Go to the next frame in the animation
        dinoAnimIndex += 1
        # If we have gone past the last frame in the animation...
        if dinoAnimIndex >= len(dinoAnimRun) :
            # ... Then loop the animation back to the beginning
            # (or take some other action if desired)
            dinoAnimIndex = 0
        # END if for checking last frame
    # END if for checking animation


    # Solid collision with box
    if pygame.Rect.colliderect(playerRect,boxRect):
        # Determine the overlap between these two objects
        xOverlap = min(playerRect.right - boxRect.left, boxRect.right - playerRect.left)
        yOverlap = min(playerRect.bottom - boxRect.top, boxRect.bottom - playerRect.top)

        # The smaller overlap will be the direction we move
        # We move based on the direction of the player and
        # the amount overlapped
        if xOverlap < yOverlap :
            if playerRect.left < boxRect.left :
                playerPos[0] -= xOverlap
            else:
                playerPos[0] += xOverlap
        else:
            if playerRect.top < boxRect.top :
                playerPos[1] -= yOverlap
            else:
                playerPos[1] += yOverlap
    # END if for box collisions

    # Update camera position based on player position
    cameraPos= (playerRect.centerx -WINDOWWIDTH/2,playerRect.centery-WINDOWHEIGHT/2)

    
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
        screen.blit(playerImageRot,(playerRect.left-cameraPos[0],playerRect.top-cameraPos[1]))

        # Draw all of the enemies
        for enemyPos in enemyPosList:
            screen.blit(enemyImage,(enemyPos[0]-cameraPos[0],enemyPos[1]-cameraPos[1]))
        # END for loop for enemy drawing
        
        # Draw all of the bullets
        for bulletPos in bulletPosList:
            screen.blit(bulletImage,(bulletPos[0]-cameraPos[0],bulletPos[1]-cameraPos[1]))
        # END for loop for enemy drawing

        # Draw box
        screen.blit(boxImage, (boxRect.left-cameraPos[0],boxRect.top-cameraPos[1]))
        
    # END if for checking game state

    # Draw the UI text
    UIFont.render_to(screen, (10, 10), "Score: "+str(score), BLACK)

    textRect = UIFont.get_rect("Health: 9999")
    UIFont.render_to(screen, (WINDOWWIDTH - 10 - textRect.width, 10), "Health: "+str(health), BLACK)

    # Draw example dino animation
    #screen.blit(dinoAnimRun[dinoAnimIndex],(0,0))

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
