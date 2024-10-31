import pygame, random
pygame.init()

# This function plays the cutscene upon the win condition of the story mode (touching the planet after attaining 2500 score)
# I am aware that the loops here couldve been used in functions instead, but i found this to make closing the application more difficult and instead opted to do some copying and pasting with changes made

def play(WIN, dimensions, ship):
    clock = pygame.time.Clock() # Clock object here used to cap framerate to 60 fps (useful for the timer variables introduced later)

    # Loading the first background

    bg = pygame.transform.scale(pygame.image.load("./Assets/Cutscene/sky1.png"), dimensions).convert_alpha()

    # Creating text for if the player presses a key (displays "press enter to skip" for a short time when a key is pressed)

    font = pygame.font.Font("./Assets/Fonts/pixeboy.ttf", dimensions[1]//18)
    txt = font.render("press enter to skip", True, (0,0,0), (255,255,255))
    txtTimer = 0

    # Loading the ship noises (repurposed the boost sound and modified it for the muffled sound)

    shipSound = pygame.mixer.Sound("./Assets/Sounds/boost.wav")
    muffledSound = pygame.mixer.Sound("./Assets/Sounds/boostMuffled.wav")

    # Setting the ships default y co-ordinate and playing the boost noise indefinitely

    shipHeight = -ship.get_height()
    shipSound.play(-1)

    # Lowering the ship into the next scene

    while shipHeight < dimensions[1]: # This will loop until the ship leaves the screen
        # Displaying the background

        WIN.fill((0, 0, 0))
        WIN.blit(bg, (0, 0))
        clock.tick(60)

        for i in pygame.event.get(): # This block of code will be repeated several times, hence i will only comment it here
            if i.type == pygame.QUIT: # Checking if application is closed
                return "fullbreak"
            elif i.type == pygame.KEYDOWN: # Skipping cutscene or starting the timer for the aforementioned "press enter to skip" text
                if i.key != pygame.K_RETURN:
                    txtTimer = 240
                else:
                    pygame.mixer.stop()
                    return

        shipHeight += dimensions[1]/1080 * 6 # Lowering the ship 

        WIN.blit(ship, (dimensions[0]//8, shipHeight)) # Displaying the ship

        # Displaying the skip text and counting down its timer if applicable
        
        if txtTimer > 0: # This section will also be repeated several times, hence no explanations later in the code
            txtTimer -= 1
            WIN.blit(txt, (dimensions[0] - txt.get_width(), dimensions[1] - txt.get_height()))

        pygame.display.update()

    # This next loop works in literally the same way as the previous. For comments on this bit, read the above loop as it is the same, just with a different asset

    # Resetting the ships position for the next scene and changing the background

    shipHeight = -ship.get_height()
    bg = pygame.transform.scale(pygame.image.load("./Assets/Cutscene/sky2.png"), dimensions).convert_alpha()

    while shipHeight < dimensions[1]:
        WIN.fill((0, 0, 0))
        WIN.blit(bg, (0, 0))
        clock.tick(60)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return "fullbreak"
            elif i.type == pygame.KEYDOWN:
                if i.key != pygame.K_RETURN:
                    txtTimer = 240
                else:
                    pygame.mixer.stop()
                    return

        shipHeight += dimensions[1]/1080 * 6

        WIN.blit(ship, (dimensions[0]//8, shipHeight))
        
        if txtTimer > 0:
            txtTimer -= 1
            WIN.blit(txt, (dimensions[0] - txt.get_width(), dimensions[1] - txt.get_height()))

        pygame.display.update()

    # Displaying the next scene (holding the picture)

    # Changing the background, sound and setting a timer for how long the scene will be displayed

    bg = pygame.transform.scale(pygame.image.load("./Assets/Cutscene/picture.png"), (dimensions[0] + dimensions[0]/1920 * 8, dimensions[1] + dimensions[1]/1080 * 8)).convert_alpha()
    timer = 300 # Because the framerate is capped at 60 frames per second, we can make a 5 second timer by doing 5 x 60 frames, which is 300 frames and looping for that many times
    shipSound.stop()
    muffledSound.play(-1)

    while timer > 0: # This will loop for 5 seconds
        # Displaying the image, but at random positions to give the screen shake effect

        WIN.fill((0, 0, 0))
        offsetX = random.randint(-1, 1) * dimensions[0]/1920 * 4
        offsetY = random.randint(-1, 1) * dimensions[1]/1080 * 4

        WIN.blit(bg, (-dimensions[0]/1920 * 4 + offsetX, -dimensions[1]/1080 * 4 + offsetY))
        clock.tick(60)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return "fullbreak"
            elif i.type == pygame.KEYDOWN:
                if i.key != pygame.K_RETURN:
                    txtTimer = 240
                else:
                    pygame.mixer.stop()
                    return

        timer -= 1 # Counting the timer down every frame
        
        if txtTimer > 0:
            txtTimer -= 1
            WIN.blit(txt, (dimensions[0] - txt.get_width(), dimensions[1] - txt.get_height()))

        pygame.display.update()

    # Final scene (on the ground)

    # Loading the final background and changing the scale of the ship image

    bg = pygame.transform.scale(pygame.image.load("./Assets/Cutscene/ground.png"), dimensions).convert_alpha()
    ship = pygame.transform.scale(ship, (dimensions[1]//1.2, dimensions[1]//1.2)).convert_alpha()

    # Setting the ships position and getting a constant for the ships height a

    shipHeight = -ship.get_height()
    heightConst = ship.get_height()

    # Playing the unmuffled boost noise again

    muffledSound.stop()
    shipSound.play(-1)

    while shipHeight + heightConst < dimensions[1] + dimensions[1]//32: # This will loop until the ship is in its final position
        WIN.fill((0, 0, 0))
        WIN.blit(bg, (0, 0))
        clock.tick(60)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return "fullbreak"
            elif i.type == pygame.KEYDOWN:
                if i.key != pygame.K_RETURN:
                    txtTimer = 240
                else:
                    pygame.mixer.stop()
                    return

        shipHeight += dimensions[1]/1080 * 3

        WIN.blit(ship, (-dimensions[0]//16, shipHeight))
        
        if txtTimer > 0:
            txtTimer -= 1
            WIN.blit(txt, (dimensions[0] - txt.get_width(), dimensions[1] - txt.get_height()))

        pygame.display.update()

    # Reusing the timer segment to have a very short delay

    timer = 45
    shipSound.stop() # The ship has landed, so the boost noise can be turned off

    while timer > 0:
        WIN.fill((0, 0, 0))
        WIN.blit(bg, (0, 0))
        clock.tick(60)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return "fullbreak"
            elif i.type == pygame.KEYDOWN:
                if i.key != pygame.K_RETURN:
                    txtTimer = 240
                else:
                    pygame.mixer.stop()
                    return

        timer -= 1

        WIN.blit(ship, (-dimensions[0]//16, shipHeight))
        
        if txtTimer > 0:
            txtTimer -= 1
            WIN.blit(txt, (dimensions[0] - txt.get_width(), dimensions[1] - txt.get_height()))

        pygame.display.update()

    # Astronaut exiting ship bit

    # Loading the astronaut and the ship leaving noise, as well as resetting the timer

    dude = pygame.transform.scale(pygame.image.load("./Assets/Cutscene/Astronaut.png"), (dimensions[1] * 0.4, dimensions[1] * 0.4)).convert_alpha()
    timer = 60
    dudeX = dimensions[0]//4
    dudeY = dimensions[1] - dude.get_height()
    leaveSound = pygame.mixer.Sound("./Assets/Sounds/exitShip.wav")
    leaveSound.play()

    while timer > 0: # Another short delay
        WIN.fill((0, 0, 0))
        WIN.blit(bg, (0, 0))
        clock.tick(60)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return "fullbreak"
            elif i.type == pygame.KEYDOWN:
                if i.key != pygame.K_RETURN:
                    txtTimer = 240
                else:
                    pygame.mixer.stop()
                    return

        timer -= 1

        WIN.blit(ship, (-dimensions[0]//16, shipHeight))
        WIN.blit(dude, (dudeX, dudeY)) # Displaying the astronaut
        
        if txtTimer > 0:
            txtTimer -= 1
            WIN.blit(txt, (dimensions[0] - txt.get_width(), dimensions[1] - txt.get_height()))

        pygame.display.update()

    # Astronaut walking bit
    # This will use a timer between the astronauts steps, but will run indefinitely until the astronaut reaches his final position

    # Loading the astronauts side asset and the footstep noise

    dude = pygame.transform.scale(pygame.image.load("./Assets/Cutscene/AstronautSide.png"), (dimensions[1] * 0.4, dimensions[1] * 0.4)).convert_alpha()
    stepSound = pygame.mixer.Sound("./Assets/Sounds/walk.wav")
    moveTimer = 45

    while dudeX < dimensions[0]//2:
        WIN.fill((0, 0, 0))
        WIN.blit(bg, (0, 0))
        clock.tick(60)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return "fullbreak"
            elif i.type == pygame.KEYDOWN:
                if i.key != pygame.K_RETURN:
                    txtTimer = 240
                else:
                    pygame.mixer.stop()
                    return
                
        moveTimer -= 1 # Decreasing the astronaut movement timer. When this reaches 0, the astronaut will move

        if moveTimer <= 0:
            stepSound.play() # Playing the footstep sound upon astronaut movement
            moveTimer = 45 # Resetting the astronaut movement timer
            dudeX += dimensions[0]//32 # Changing the astronauts X co-ordinate

        WIN.blit(ship, (-dimensions[0]//16, shipHeight))
        WIN.blit(dude, (dudeX, dudeY))
        
        if txtTimer > 0:
            txtTimer -= 1
            WIN.blit(txt, (dimensions[0] - txt.get_width(), dimensions[1] - txt.get_height()))

        pygame.display.update()

    # Astronauts wife walking bit
    # This works very similarly to the code above, bar a few changes

    # Loading the astronauts wife side asset and setting her initial position

    dudette = pygame.transform.scale(pygame.image.load("./Assets/Cutscene/AstronautinaSide.png"), (dimensions[1] * 0.4, dimensions[1] * 0.4)).convert_alpha()
    dudetteX = dimensions[0] + dudette.get_width()//2
    dudetteY = dimensions[1] - dudette.get_height()

    moveTimer = 45 # The movement timer will be reused for the astronauts wifes movement as well

    while dudetteX > 3 * dimensions[0]//4 - dudette.get_width()//3:
        WIN.fill((0, 0, 0))
        WIN.blit(bg, (0, 0))
        clock.tick(60)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return "fullbreak"
            elif i.type == pygame.KEYDOWN:
                if i.key != pygame.K_RETURN:
                    txtTimer = 240
                else:
                    pygame.mixer.stop()
                    return
                
        moveTimer -= 1

        if moveTimer <= 0:
            stepSound.play()
            moveTimer = 45
            dudetteX -= dimensions[0]//32 # The + in the section before changes to a - here to change movement direction

        WIN.blit(ship, (-dimensions[0]//16, shipHeight))

        WIN.blit(dude, (dudeX, dudeY))
        WIN.blit(dudette, (dudetteX, dudetteY)) # Displaying the astronauts wife
        
        if txtTimer > 0:
            txtTimer -= 1
            WIN.blit(txt, (dimensions[0] - txt.get_width(), dimensions[1] - txt.get_height()))

        pygame.display.update()

    timer = 60 # Reusing the timer loop to add another delay

    while timer > 0:
        WIN.fill((0, 0, 0))
        WIN.blit(bg, (0, 0))
        clock.tick(60)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return "fullbreak"
            elif i.type == pygame.KEYDOWN:
                if i.key != pygame.K_RETURN:
                    txtTimer = 240
                else:
                    pygame.mixer.stop()
                    return

        timer -= 1

        WIN.blit(ship, (-dimensions[0]//16, shipHeight))
        WIN.blit(dude, (dudeX, dudeY))
        WIN.blit(dudette, (dudetteX, dudetteY))
        
        if txtTimer > 0:
            txtTimer -= 1
            WIN.blit(txt, (dimensions[0] - txt.get_width(), dimensions[1] - txt.get_height()))

        pygame.display.update()

    # Final change (both people face forward)

    # Changing the assets for the people

    dudette = pygame.transform.scale(pygame.image.load("./Assets/Cutscene/Astronautina.png"), (dimensions[1] * 0.4, dimensions[1] * 0.4)).convert_alpha()
    dude = pygame.transform.scale(pygame.image.load("./Assets/Cutscene/Astronaut.png"), (dimensions[1] * 0.4, dimensions[1] * 0.4)).convert_alpha()
    timer = 150 # Adding another delay

    while timer > 0:
        WIN.fill((0, 0, 0))
        WIN.blit(bg, (0, 0))
        clock.tick(60)

        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                return "fullbreak"
            elif i.type == pygame.KEYDOWN:
                if i.key != pygame.K_RETURN:
                    txtTimer = 240
                else:
                    pygame.mixer.stop()
                    return

        timer -= 1

        WIN.blit(ship, (-dimensions[0]//16, shipHeight))
        WIN.blit(dude, (dudeX, dudeY))
        WIN.blit(dudette, (dudetteX, dudetteY))
        
        if txtTimer > 0:
            txtTimer -= 1
            WIN.blit(txt, (dimensions[0] - txt.get_width(), dimensions[1] - txt.get_height()))

        pygame.display.update()
    pygame.mixer.stop() # Precaution in case any sounds keep playing
