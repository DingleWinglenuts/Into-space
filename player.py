import pygame, spritesheet, controller, random, pygame._sdl2.controller; from math import sqrt

# This file contains a player object that handles all player interactions and movement

ss = spritesheet.Spritesheet(pygame.image.load("./Assets/Player/SpaceshipSpritesheet.png")) # Creates a spritesheet from spritesheet.py
fontPath = "./Assets/Fonts/pixeboy.ttf"

# Loading sounds that the playable character makes

hitSound = pygame.mixer.Sound("./Assets/Sounds/playerHit.wav")
powerupSound = pygame.mixer.Sound("./Assets/Sounds/powerupPickup.wav")
boostSound = pygame.mixer.Sound("./Assets/Sounds/boost.wav")

class Player(pygame.sprite.Sprite):
    def __init__(self, WIN, dimensions, bfont, mode):
        super().__init__() # For an explanation, please see the usage of the same thing in powerup.py
        self.pFont = pygame.font.Font(fontPath, int(dimensions[1]//16))
        self.defaultDamage = 0 # Sets the minimum damage taken of the player (used for one life mode)
        self.WIN = WIN
        self.sprites = ss.getSprites(64, 4, dimensions[1]/512) # Splits the sprites into individual images and stores them in a 2d list
        self.dimensions = dimensions
        self.currentImg = self.sprites[0][0] # Sets the current image of the player to full health with no boosting
        self.size = (self.currentImg.get_width(), self.currentImg.get_height())
        self.smallImg = pygame.transform.scale_by(self.currentImg, 0.5).convert_alpha()
        self.mult = 1 # Multiplier for when the player picks up a speed boost (1 by default)
        self.speed = dimensions[1] * 0.6
        self.boost = 1000
        self.lastBoost = 0 # Amount of time passed since the player last boosted (used for boost refill cooldown)
        self.unitX = dimensions[0]/1920
        self.unitY = dimensions[1]/1080
        self.offset = (self.unitX * 10, dimensions[1] - 4 * self.unitY * 10)
        self.damage = 0 # Holds the amount of asteroid hits the player has taken
        self.boostFont = bfont
        self.boostTxt = bfont.render("Boost", True, (255, 255, 255))
        self.mainMask= pygame.mask.from_surface(self.currentImg) # Mask for collisions
        self.smallMask = pygame.mask.from_surface(self.smallImg)
        self.mask = self.mainMask
        self.rect = pygame.Rect((dimensions[0]//2 - self.currentImg.get_width()//2, 7 * dimensions[1]//8 - self.currentImg.get_height()), self.size) # Holds position and scale of player
        self.heart = pygame.transform.scale(pygame.image.load("./Assets/Player/heart.png"), (dimensions[1]//10, dimensions[1]//10)).convert_alpha() # Heart image to show player health (shown in top right)
        self.currentNum = 0 # Used to determine the sprite to show at any moment
        self.powTxts = [] # Used to store the text that appears when a powerup is picked up and information about it
        self.powQueue = []
        self.controller = None
        self.dt = 0
        
        if pygame._sdl2.controller.get_count() > 0:
            self.controller = controller.Controller(self.speed)
        self.powTimes = {
            "speed boost": 20,
            "shield": 20,
            "shrink": 20
        }
        self.mode = mode
        self.gameOver = None # Used to determine what to output on the game over screen (None means the mode isnt story, False means a failed story attempt and True means a story mode win)

        if mode == 3: # Sets the game over screen to the loss screen on story mode by default
            self.gameOver = False

    def move(self, deltaTime, eventQueue):
        keys = pygame.key.get_pressed()
        moveX = 0
        moveY = 0
        self.currentNum = self.damage # Sets the image to display to correspond to how much damage the ship has taken
        self.dt = deltaTime

        if self.controller:
            self.controller.update()

        if "shield" in self.powQueue:
            self.currentNum = 3

        self.currentImg = self.sprites[self.currentNum][0] # Sets the current image to be displayed to what it needs to be (read above for more details)

        # Moving the player (accounting for the speed boost mutiplier) and keeping them within visible boundaries

        if (keys[pygame.K_w] or keys[pygame.K_UP]):
            moveY += self.speed * deltaTime * self.mult
        if (keys[pygame.K_s] or keys[pygame.K_DOWN]):
            moveY -= self.speed * deltaTime * self.mult
        if (keys[pygame.K_a] or keys[pygame.K_LEFT]):
            moveX -= self.speed * deltaTime * self.mult
        if (keys[pygame.K_d] or keys[pygame.K_RIGHT]):
            moveX += self.speed * deltaTime * self.mult
        
        if self.controller and self.controller.moved:
            moveX = self.controller.speedX * deltaTime * self.mult
            moveY = self.controller.speedY * deltaTime * self.mult

        if moveX != 0 and moveY != 0 and not self.controller: # Makes the player displacement consistent if moving in both x and y directions
            moveX *= sqrt(2)/2
            moveY *= sqrt(2)/2

        if ((keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_SPACE]) or (self.controller and self.controller.rightTrigger)) and self.boost > 0: # Increases distance moved by player if speed boost is active
            moveX *= 1.8
            moveY *= 1.8
            self.boost -= 320 * deltaTime
            self.lastBoost = 0
            self.currentImg = self.sprites[self.currentNum][1]

        popped = 0
        
        for i in range(len(self.powQueue)):
            if i > len(self.powQueue) - popped:
                break

            if self.powQueue[i] == "shield": # Sets the image to the shielded image and counts the time since shield was activated if shield is active
                self.powTimes["shield"] -= deltaTime

                if self.powTimes["shield"] < 0: # Deactivates shield if timer runs out
                    self.powTimes["shield"] = 20
                    self.powQueue.pop(i)
                    popped += 1

            elif self.powQueue[i] == "speed boost": # Counts time passed since a speed boost was activated and nullifies its effect if the timer runs out
                self.powTimes["speed boost"] -= deltaTime

                if self.powTimes["speed boost"] < 0:
                    self.powTimes["speed boost"] = 20
                    self.mult = 1
                    self.powQueue.pop(i)
                    popped += 1

            elif self.powQueue[i] == "shrink":
                self.smallImg = pygame.transform.scale_by(self.currentImg, 0.5).convert_alpha()
                self.currentImg = self.smallImg
                self.mask = self.smallMask
                self.powTimes["shrink"] -= deltaTime

                if self.powTimes["shrink"] < 0:
                    self.powTimes["shrink"] = 20
                    self.mask = self.mainMask
                    self.powQueue.pop(i)
                    popped += 1

        for i in eventQueue: # Plays/stops boost sound when the player is boosting
            if (i.type == pygame.KEYDOWN and (i.key == pygame.K_LSHIFT or i.key == pygame.K_SPACE or i.key == pygame.K_RSHIFT)) or (self.controller and self.controller.firstPress):
                boostSound.play(-1)
            elif (i.type == pygame.KEYUP and (i.key == pygame.K_LSHIFT or i.key == pygame.K_SPACE or i.key == pygame.K_RSHIFT)) or self.boost <= 0 or (self.controller and self.controller.released):
                boostSound.stop()
        
        # Executes the movement based on variables used above

        self.rect.x += moveX
        self.rect.y -= moveY

        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > self.dimensions[0] - self.currentImg.get_width():
            self.rect.x = self.dimensions[0] - self.currentImg.get_width()
        
        if self.rect.y < 0:
            self.rect.y = 0
        elif self.rect.y > self.dimensions[1] - self.currentImg.get_height():
            self.rect.y = self.dimensions[1] - self.currentImg.get_height()

        self.lastBoost += deltaTime 

        if self.lastBoost > 3 and self.boost < 1000: # Adds boost if the player hasnt boosted for at least 3 seconds and the boost isnt at maximum
            self.boost += 550 * deltaTime

        # Making sure the boost cannot go above or below its maximum and minimum

        if self.boost < 0:
            self.boost = 0

        if self.boost > 1000:
            self.boost = 1000

        # Shifting the colours of the boost bar based on boost remaining

        red = ((1 - self.boost/1000) * 255)//1
        green =  ((self.boost/1000) * 255)//1

        boostCalc = self.dimensions[1]//2.5 * self.boost/1000 # Calculates the position at which the boost bar should be displayed

        # Displaying all boost bar assets and the player

        self.WIN.blit(self.currentImg, self.rect)
        pygame.draw.rect(self.WIN, (255, 255, 255), pygame.Rect(self.offset[0], self.offset[1] - self.dimensions[1]//2.5 - 8 * self.unitX, self.dimensions[0]//32 + 8 * self.unitX, self.dimensions[1]//2.5 + 6 * self.dimensions[0]/1080))
        pygame.draw.rect(self.WIN, (red, green, 0), pygame.Rect((4 * self.unitX + self.offset[0], self.offset[1] - boostCalc - 4 * self.unitX), (self.dimensions[0]//32, boostCalc)))
        self.WIN.blit(self.boostTxt, (self.offset[0], self.offset[1] + 3/1080 * self.dimensions[1]))

        # Displaying the amount of health the player has left

        for i in range(3 - self.damage):
            self.WIN.blit(self.heart, (self.dimensions[0] - ((i+1) * self.heart.get_width()) - self.offset[0], self.unitX * 3))

        # Removing powerup texts if they have exceeded their active time and changing the size of the powerup texts 

        for i in range(len(self.powTxts)):
            if i >= len(self.powTxts):
                break

            if self.powTxts[i][2] <= 0:
                self.powTxts.pop(i)
                continue

            font = pygame.font.Font(fontPath, int((self.dimensions[1]/36 * self.powTxts[i][2])//1))
            txt = font.render(self.powTxts[i][0], True, (255, 255, 255))

            self.powTxts[i][2] -= deltaTime

            self.WIN.blit(txt, (self.powTxts[i][1][0] - txt.get_width()/2, self.powTxts[i][1][1]))

        # Displaying the amount of time left with boost and/or shield

        for i in range(len(self.powQueue)):
            txt = self.pFont.render(self.powQueue[i] + ": " + str(self.powTimes[self.powQueue[i]])[:6], True, (255, 255, 255))
            self.WIN.blit(txt, (self.offset[0] + self.dimensions[0]//32 + 20 * self.unitX, self.offset[1] + i * 3/1080 * self.dimensions[1] - (i + 1) * txt.get_height()))

    # Function for player collisions

    def col(self, astManager, powManager):
        asteroid = False

        for i in range(len(astManager.activeAsteroids)):
            if i >= len(astManager.activeAsteroids): # Contingency for if the list has been modified during looping
                break
            
            if pygame.sprite.collide_mask(self, astManager.activeAsteroids[i]): # Checking for collisions with existing objects
                if astManager.activeAsteroids[i].type == "asteroid": # Dealing damage (or not if the shield is active) if the collision object is an asteroid and spawning a new asteroid
                    self.damage += 1
                    if "shield" in self.powQueue:
                        self.damage -= 1
                        astManager.score += 10
                    astManager.activeAsteroids.pop(i)
                    astManager.newAst()
                    if self.controller:
                        asteroid = True
                    hitSound.play()
                    if self.damage >= 3: # Preventing boost sound in the menu if the player dies while boosting
                        boostSound.stop()
                
                elif astManager.activeAsteroids[i].type == "planet": # Ends game in victory if the player collides with a planet object
                    self.gameOver = True

        powerup = False

        for i in range(len(powManager.powerups)): # Checking for collisions with powerups
            if i >= len(powManager.powerups): # Contingency like with the previous for loop
                break

            if pygame.sprite.collide_mask(self, powManager.powerups[i]): # Executing the corresponding benefit upon picking up a powerup
                if self.controller:
                    powerup = True
                if powManager.powerups[i].type == "health": # Refills health
                    self.damage = self.defaultDamage
                elif powManager.powerups[i].type == "shield": # Activates shield
                    if powManager.powerups[i].type in self.powQueue:
                        self.powTimes["shield"] += 20
                    else:
                        self.powQueue.append(powManager.powerups[i].type)
                elif powManager.powerups[i].type == "score": # Adds score
                    score = random.randint(20, 75) * 10
                    astManager.score += score
                    powManager.powerups[i].type = f"+{score} score"
                elif powManager.powerups[i].type == "speed boost": # Adds a speed boost
                    if powManager.powerups[i].type in self.powQueue:
                        self.powTimes["speed boost"] += 20
                    else:
                        self.powQueue.append(powManager.powerups[i].type)
                    self.mult = 1.5
                elif powManager.powerups[i].type == "shrink": # Shrinks the player
                    self.shrink = True
                    if powManager.powerups[i].type in self.powQueue:
                        self.powTimes["shrink"] += 20
                    else:
                        self.powQueue.append(powManager.powerups[i].type)

                self.powTxts.append([powManager.powerups[i].type.upper(), (self.rect.x, self.rect.y), 2]) # Adding the text spawned on pickup of powerups to a list
                powManager.powerups.pop(i) # Despawning the powerup
                powerupSound.play() # Playing the powerup pickup sound

        if self.controller:
            self.controller.rumble(self.dt, self.boost, asteroid, powerup)