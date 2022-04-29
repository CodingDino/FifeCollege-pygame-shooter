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
# END function definition
# --------------------------------------


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
playerRunAnim = [
    pygame.image.load("images/player_walk1.png"),
    pygame.image.load("images/player_walk2.png")
]
playerCurrentAnim = playerRunAnim
playerImage = playerCurrentAnim[0]
playerPos = [WINDOWWIDTH/2 - playerImage.get_width()/2, WINDOWHEIGHT - 300]
playerRect = pygame.Rect(playerPos[0], playerPos[1], playerImage.get_width(), playerImage.get_height())
PLAYERSPEED = 300
playerAlive = True
playerAnimIndex = 0
playerAnimFrameTime = 0.2
timeSincePlayerAnim = 0

# Set up enemies
enemyImage = pygame.image.load("images/enemy.png")
enemyRect = pygame.Rect(0, 0, enemyImage.get_width(), enemyImage.get_height())
enemySpeed = 100
enemyPosList = []
NUM_ENEMIES = 5
for i in range(NUM_ENEMIES):
    spawn_enemy()
# END for loop for enemy spawning
SPAWNCOOLDOWN = 2
timeSinceSpawn = 0


# Set up bullets
bulletImage = pygame.image.load("images/bullet.png")
bulletRect = pygame.Rect(0,0, bulletImage.get_width(), bulletImage.get_height())
bulletPosList = []
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
health = 50
damagePerEnemy = 30

# Set up sound effects
fireSound = pygame.mixer.Sound("audio/fire.ogg")

# Set up and play music
pygame.mixer.music.load("audio/music.mp3")
pygame.mixer.music.play(0)

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
        
    # Move the player's rectangle based on the position variable
    playerRect.left = playerPos[0]
    playerRect.top = playerPos[1]

    # Increase time since last bullet was fire
    # based on how much time passed this frame
    timeSinceFire += frameSec
        
    # Firing
    if keys[pygame.K_SPACE] and playerAlive and timeSinceFire >= FIRINGCOOLDOWN:
        # Fire the bullet!
        newBulletX = playerPos[0] + 20
        newBulletY = playerPos[1]
        bulletPosList.append([newBulletX,newBulletY])
        timeSinceFire = 0
        pygame.mixer.Sound.play(fireSound)
    # END if space pressed


    # Update for bullets
    for bulletPos in bulletPosList:
        # Move bullet up
        bulletPos[1] -= BULLETSPEED * frameSec

        # Update Bullet Rectangle
        bulletRect.left = bulletPos[0]
        bulletRect.top = bulletPos[1]

        # Loop through all enemies and check if THIS
        # particular bullet has hit each enemy
        for enemyPos in enemyPosList[:]:

            # Update enemy rectangle
            enemyRect.left = enemyPos[0]
            enemyRect.top = enemyPos[1]

            # If a bullet collides with an enemy...
            if pygame.Rect.colliderect(bulletRect,enemyRect) :
                # Remove THIS enemy from the list
                enemyPosList.remove(enemyPos)

                score += scorePerEnemy

                # Check if we won!
                if score >= scoreToWin :
                    winGame = True
                # END if for checking if we won

            # END if for bullet/enemy collision
            
        # END enemy loop (for bullet/enemy collision)
        
    # END bullet loop
    
    # Add to time since last enemy spawned
    timeSinceSpawn += frameSec

    # Check if it is time to spawn a new enemy
    if timeSinceSpawn >= SPAWNCOOLDOWN :
        spawn_enemy()
        timeSinceSpawn = 0
    # END if for checking enemy spawn

    # Update enemies
    for enemyPos in enemyPosList:
        # Move enemy down
        enemyPos[1] += enemySpeed * frameSec
        
        # Update the enemy rectangle
        enemyRect.left = enemyPos[0]
        enemyRect.top = enemyPos[1]
        
        # Check if the enemy hit the player
        if pygame.Rect.colliderect(playerRect,enemyRect):
            # Deal damage to the player
            health -= damagePerEnemy

            # Get rid of the enemy
            enemyPosList.remove(enemyPos)

            # Did they die?
            if health <= 0:
                # If so, kill the player!
                playerAlive = False
                pygame.mixer.music.stop()
            # END if for health
        # END if statement for collision

        # Check if the enemy is off the screen
        if enemyPos[1] > WINDOWHEIGHT:
            # Reposition the enemy at the top of the screen
            enemyPos[0] = random.randint(0,WINDOWWIDTH-enemyImage.get_width()) #
            enemyPos[1] = -enemyImage.get_height() # just barely above the screen
        # END if for enemy off screen check
            
    # END for loop for enemy update


    # Update animation
    timeSincePlayerAnim += frameSec
    # If it's time to switch frames...
    if timeSincePlayerAnim >= playerAnimFrameTime:
        timeSincePlayerAnim = 0
        # Switch frames!
        playerAnimIndex += 1
        # Did we go past the last frame?
        if playerAnimIndex >= len(playerCurrentAnim):
            # Loop back to the first frame!
            playerAnimIndex = 0
        # END if for last frame check
        playerImage = playerCurrentAnim[playerAnimIndex]
    # END if for frame switching
    
    # ----------------------------------

    
    # ----------------------------------
    # Draw
    # ----------------------------------
    # Fill the background with a colour
    screen.fill(WHITE)

    # Draw Everything

    # Draw items based on the game state
    if winGame : # Player has won!

        textRect = UIFont.get_rect("YOU WIN!")
        
        UIFont.render_to(screen, (WINDOWWIDTH/2-textRect.width/2, WINDOWHEIGHT/2-textRect.height/2), "YOU WIN!", BLACK )

    elif not playerAlive : # Player has lost!

        textRect = UIFont.get_rect("GAME OVER!")
        UIFont.render_to(screen, (WINDOWWIDTH/2-textRect.width/2, WINDOWHEIGHT/2-textRect.height/2), "GAME OVER!", BLACK )

    else :
        
        screen.blit(playerImage,playerPos)

        # Draw all of the enemies
        for enemyPos in enemyPosList:
            screen.blit(enemyImage,enemyPos)
        # END for loop for enemy drawing
        
        # Draw all of the bullets
        for bulletPos in bulletPosList:
            screen.blit(bulletImage,bulletPos)
        # END for loop for bullet drawing

    # END if for game state drawing

    # Draw the UI Text
    UIFont.render_to(screen, (10,10), "Score: "+str(score), (0, 0, 0) )

    # Draw the UI Text
    UIFont.render_to(screen, (10,50), "Health: "+str(health), (0, 0, 0) )

        
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
