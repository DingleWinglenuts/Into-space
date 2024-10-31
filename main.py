import pygame, ui, pyTime, fontManager, scrollController, player, asteroids, powerup, leaderboard, cutscene
pygame.init()

# Creating the window
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Into Space")
pygame.display.set_icon(pygame.image.load("./Assets/Icon/icon.png"))

# Getting fonts ready for use

fonts = fontManager.FontManager()
fonts.add(pygame.font.Font("./Assets/Fonts/pixeboy.ttf", int(HEIGHT//5)), "menuTxt")
fonts.add(pygame.font.Font("./Assets/Fonts/pixeboy.ttf", int(HEIGHT//8)), "scoreTxt")
fonts.add(pygame.font.Font("./Assets/Fonts/pixeboy.ttf", int(HEIGHT//18)), "nextTxt")
fonts.add(pygame.font.Font("./Assets/Fonts/pixeboy.ttf", int(HEIGHT//36)), "barTxt")
fonts.add(pygame.font.Font("./Assets/Fonts/pixeboy.ttf", int(HEIGHT//10)), "boxTxt")

# Rendering the text for the main menu

titleTxt = fonts.render("menuTxt", "Into Space", (255, 255, 255))
titlePos = (WIDTH//2 - titleTxt.get_width()//2, HEIGHT//2 - titleTxt.get_height() * 3/2)

# Loading and setting up the scrolling background

bg = pygame.transform.scale(pygame.image.load("./Assets/Backgrounds/bg.png"), (WIDTH, HEIGHT)).convert()
scroller = scrollController.Scroll(bg, WIN)

# These variables all control different while loops within the game

run = True # Main loop (if set to false the window will close)
fullBreak = False # Variable used to break out of all while loops if set to true and close the window
backToMenu = False # Variable used to break out of all while loops but not the main menu

# Loading and playing the main menu theme and preloading the game over sounds

pygame.mixer.music.load("./Assets/Sounds/mainTheme.mp3")
pygame.mixer.music.play(-1)

winSound = pygame.mixer.Sound("./Assets/Sounds/winTune.wav")
loseSound = pygame.mixer.Sound("./Assets/Sounds/loseTune.wav")

# Creating an object that allows movements to be consistent across devices with different framerates

time = pyTime.PyTime()

# Creating the buttons for the main menu

playButton = ui.Button("Play", (0, 0, 0), HEIGHT//10, WIDTH//2 - WIDTH//6, HEIGHT//2 + -2 * HEIGHT//18 + 1.6 * HEIGHT//24, WIDTH//3, HEIGHT//9)
controlsButton = ui.Button("How to play", (0, 0, 0), HEIGHT//10, WIDTH//2 - WIDTH//6, HEIGHT//2 + -1 * HEIGHT//18 + 3.2 * HEIGHT//24, WIDTH//3, HEIGHT//9)
lbButton = ui.Button("Leaderboards", (0, 0, 0), HEIGHT//10, WIDTH//2 - WIDTH//6, HEIGHT//2 + 0 * HEIGHT//18 + 4.8 * HEIGHT//24, WIDTH//3, HEIGHT//9)
quitButton = ui.Button("Quit", (0, 0, 0), HEIGHT//10, WIDTH//2 - WIDTH//6, HEIGHT//2 + 1 * HEIGHT//18 + 6.4 * HEIGHT//24, WIDTH//3, HEIGHT//9)

board = leaderboard.init((WIDTH, HEIGHT))

# Main menu

while run:
    runQueue = pygame.event.get()

    # Displaying the scrolling background and the main title text

    WIN.fill((0, 0, 0))
    scroller.scrollBG(time.deltaTime)
    WIN.blit(titleTxt, titlePos)

    # Displaying the buttons that were just created

    playButton.render(WIN)
    controlsButton.render(WIN)
    lbButton.render(WIN)
    quitButton.render(WIN)

    # Checking if the "Quit game" button was pressed

    run = not quitButton.pressed(runQueue)
    backToMenu = False

    # Leaderboards

    if lbButton.pressed(runQueue):
        optionRun = True # Variable used to control the loop for the leaderboards
        optionTxt = fonts.render("menuTxt", "Select Mode:", (255, 255, 255))

        mode = None

        # Creating buttons for mode selection

        endlessLbButton = ui.Button("Endless", (0, 0, 0), HEIGHT//8, WIDTH//2 - WIDTH//4 - WIDTH//64, HEIGHT//2 + HEIGHT//32, WIDTH//4, HEIGHT//6)
        oneLifeLbButton = ui.Button("One Life", (0, 0, 0), HEIGHT//8, WIDTH//2 + WIDTH//64, HEIGHT//2 + HEIGHT//32, WIDTH//4, HEIGHT//6)

        # This loop will run to let the player view scores for different modes

        while optionRun:
            # Displaying the background and the "Select mode" text

            WIN.fill((0, 0, 0))
            scroller.scrollBG(time.deltaTime)
            WIN.blit(optionTxt, (WIDTH//2 - optionTxt.get_width()//2, HEIGHT//2 - optionTxt.get_height()))

            # Displaying the buttons

            endlessLbButton.render(WIN)
            oneLifeLbButton.render(WIN)

            # Checking if the player has closed application or tried to go back to main menu

            eventQueue = pygame.event.get()

            for i in eventQueue:
                if i.type == pygame.QUIT:
                    fullBreak = True
                    break

                elif i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                    optionRun = False
                    break

            # Checking for button presses

            if endlessLbButton.pressed(eventQueue):
                mode = 1
            elif oneLifeLbButton.pressed(eventQueue):
                mode = 2

            # Loading the corresponding leaderboard upon button press

            if mode != None:
                # Creating an object from the leaderboard.py file and loading scores for the correct mode

                board = leaderboard.init((WIDTH, HEIGHT))
                board.load(mode)

                # Creating buttons to let users navigate between pages of leaderboards

                leftButton = ui.Button("<", (0, 0, 0), HEIGHT//10, WIDTH//2 - WIDTH//24 - WIDTH//15, HEIGHT - 2 * HEIGHT//10, WIDTH//15, WIDTH//15)
                rightButton = ui.Button(">", (0, 0, 0), HEIGHT//10, WIDTH//2 + WIDTH//24, HEIGHT - 2 * HEIGHT//10, WIDTH//15, WIDTH//15)
                
                # Loop for displaying the leaderboards

                while mode != None:
                    # Displaying the background and the leaderboards

                    WIN.fill((0, 0, 0))
                    scroller.scrollBG(time.deltaTime)
                    board.display(WIN)

                    eventQueue = pygame.event.get()

                    # Rendering the navigation buttons

                    leftButton.render(WIN)
                    rightButton.render(WIN)

                    # Loading pages based on navigation button presses

                    if board.current >= 10 and leftButton.pressed(eventQueue):
                        board.page -= 1
                        board.current -= 10
                        board.loadPage()

                    if board.current < len(board.data)//10 * 10 and rightButton.pressed(eventQueue):
                        board.page += 1
                        board.current += 10
                        board.loadPage()

                    # Checking if the player has closed application or pressed the escape key to go back

                    for i in eventQueue:
                        if i.type == pygame.QUIT:
                            fullBreak = True
                            break
                        elif i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                            mode = None
                            break
                
                    pygame.display.update()
                
                    if fullBreak:
                        mode = None

                # Deleting objects to save memory

                del board, leftButton, rightButton
            
            pygame.display.update()

            if fullBreak:
                optionRun = False
            
        # Deleting objects to save memory

        del optionRun, optionTxt, endlessLbButton, oneLifeLbButton

    # Controls menu

    elif controlsButton.pressed(runQueue):
        # Loading the image with control instructions

        htp = pygame.transform.scale(pygame.image.load("./Assets/Backgrounds/h2p.png"), (WIDTH, HEIGHT)).convert()

        controlRun = True

        # Loop for showing controls

        while controlRun:
            # Displaying the controls image

            WIN.fill((0, 0, 0))
            WIN.blit(htp, (0, 0))

            # Checking if the player has closed application or pressed escape to return to menu

            for i in pygame.event.get():
                if i.type == pygame.QUIT:
                    fullBreak = True
                    break

                if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                    controlRun = False
                    break

            if fullBreak:
                controlRun = False

            pygame.display.update()

        # Deleting an object to save memory

        del htp

    # Upon play button being pressed

    elif playButton.pressed(runQueue):
        selectRun = True # This will control the loop for the mode selection menu

        # Creating and positioning the header for the mode selection menu

        selectTxt = fonts.render("menuTxt", "Select mode:", (255, 255, 255))
        selectTxtPos = (WIDTH//2 - selectTxt.get_width()//2, HEIGHT//3 - selectTxt.get_height())

        # Creating buttons for mode selection

        endlessButton = ui.Button("Endless", (0, 0, 0), HEIGHT//10, WIDTH//2 - WIDTH//6, HEIGHT//3 - selectTxt.get_height() + HEIGHT//8 + HEIGHT//64, WIDTH//3, HEIGHT//8)
        oneLifeButton = ui.Button("One Life", (0, 0, 0), HEIGHT//10, WIDTH//2 - WIDTH//6, HEIGHT//3 - selectTxt.get_height() + 2 * HEIGHT//8 + 2 * HEIGHT//64, WIDTH//3, HEIGHT//8)
        storyButton = ui.Button("Story", (0, 0, 0), HEIGHT//10, WIDTH//2 - WIDTH//6, HEIGHT//3 - selectTxt.get_height() + 3 * HEIGHT//8 + 3 * HEIGHT//64, WIDTH//3, HEIGHT//8)
        backToMenuButton = ui.Button("Back to menu", (0, 0, 0), HEIGHT//10, WIDTH//2 - WIDTH//6, HEIGHT//3 - selectTxt.get_height() + 4 * HEIGHT//8 + 4 * HEIGHT//64, WIDTH//3, HEIGHT//8)

        mode = None

        # Mode selection loop

        while selectRun:
            # Displaying the background and header

            WIN.fill((0, 0, 0))
            scroller.scrollBG(time.deltaTime)
            WIN.blit(selectTxt, selectTxtPos)

            eventQueue = pygame.event.get()

            # Rendering the mode selection buttons
            
            endlessButton.render(WIN)
            oneLifeButton.render(WIN)
            storyButton.render(WIN)
            backToMenuButton.render(WIN)

            # Setting the mode upon button press (or going back to menu)

            if endlessButton.pressed(eventQueue):
                mode = 1
            elif oneLifeButton.pressed(eventQueue):
                mode = 2
            elif storyButton.pressed(eventQueue):
                mode = 3

            if backToMenuButton.pressed(eventQueue):
                backToMenu = True

            for i in eventQueue:
                if i.type == pygame.QUIT:
                    fullBreak = True
                    break
                elif i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                    backToMenu = True
                    break

            # Starting the game if a mode has been selected

            if mode != None:
                # Initialising requirements for gameplay

                gameRun = True # Controls the game loop
                p = player.Player(WIN, (WIDTH, HEIGHT), fonts.fonts["barTxt"], mode) # Player object from player.py
                asteroidManager = asteroids.AsteroidManager((WIDTH, HEIGHT), mode) # Asteroid manager object from asteroids.py
                offset = (15 * WIDTH/1920, 15 * HEIGHT/1080) # How much to offset the boost bar by from the corner of the screen
                powerupManager = powerup.Manager((WIDTH, HEIGHT), mode) # Powerup manager from powerup.py
                scoreTxt = fonts.render("scoreTxt", "Score: " + str(asteroidManager.score), (255, 255, 255)) # Showing the score in the corner
                nextTxtPos = (offset[0], 2 * offset[1] + scoreTxt.get_height()) # Position of the text that tells when the next asteroid spawns
                pygame.mouse.set_visible(False) # Hiding the mouse cursor
                endSound = loseSound # Setting the game over sound to be the losing sound by default
                paused = False # For pausing the game

                fpsFont = pygame.font.Font("./Assets/Fonts/pixeboy.ttf", HEIGHT//16)

                # Setting the players health to 1 and max health to 1 if playing the one life mode

                if mode == 2:
                    p.damage = 2
                    p.defaultDamage = 2

                # Game loop

                while gameRun:
                    # Displaying the background

                    WIN.fill((0, 0, 0))
                    scroller.scrollBG(time.deltaTime)

                    mainQueue = pygame.event.get()
                    
                    # Checking if application was closed or game was paused

                    for i in mainQueue:
                        if i.type == pygame.QUIT:
                            fullBreak = True
                            break

                        if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                            paused = True

                    # Moving all asteroids, powerups and the player and checking for any player collisions

                    powerupManager.move(time.deltaTime)
                    powerupManager.blit(WIN)

                    asteroidManager.posUpdate(time.deltaTime)
                    asteroidManager.blit(WIN)

                    p.move(time.deltaTime, mainQueue)
                    p.col(asteroidManager, powerupManager)

                    # Ending the game if the player has taken too much damage or won the story mode

                    if p.damage > 2:
                        gameRun = False
                        break

                    if p.gameOver:
                        gameRun = False

                    # Displaying the score and the score at which the next asteroid will spawn
                    
                    scoreTxt = fonts.render("scoreTxt", "Score: " + str(asteroidManager.score), (255, 255, 255))
                    nextTxt = fonts.render("nextTxt", f"Next asteroid spawns at {asteroidManager.next} score", (255, 255, 255))
                    WIN.blit(scoreTxt, offset)
                    WIN.blit(nextTxt, nextTxtPos)

                    fps = fpsFont.render(str(int((1/time.deltaTime)//1)), True, (255, 255, 255))
                    WIN.blit(fps, (WIDTH - fps.get_width(), HEIGHT - fps.get_height()))

                    # Pause menu

                    if paused:
                        # Loading the "paused" text and the translucent black background#

                        pauseTxt = fonts.render("menuTxt", "Paused", (255, 255, 255))
                        pauseTxtPos = (WIDTH//2 - pauseTxt.get_width()//2, HEIGHT//2 - pauseTxt.get_height())
                        bgP = pygame.transform.scale(pygame.image.load("./Assets/Backgrounds/bgTransparent2.png"), (WIDTH, HEIGHT)).convert_alpha()

                        # Creating all buttons that are needed on the pause menu

                        resumeButton = ui.Button("Resume", (0, 0, 0), HEIGHT//10, WIDTH//2 - WIDTH//8, HEIGHT//2 + offset[1], WIDTH//4, HEIGHT//8)
                        bButton = ui.Button("Menu", (0, 0, 0), HEIGHT//10, WIDTH//2 - WIDTH//8, HEIGHT//2 + 2 * HEIGHT//8 + 3 * offset[1], WIDTH//4, HEIGHT//8)
                        cButton = ui.Button("controls", (0, 0, 0), HEIGHT//10, WIDTH//2 - WIDTH//8, HEIGHT//2 + HEIGHT//8 + 2 * offset[1], WIDTH//4, HEIGHT//8)

                        # Pausing all music/sounds and making the mouse cursor visible

                        pygame.mouse.set_visible(True)
                        pygame.mixer.pause()
                        pygame.mixer.music.pause()
                    
                        # Pause menu loop

                        while paused:
                            # Filling the background

                            WIN.fill((0, 0, 0))
                            scroller.idleBlit()

                            # Displaying the player, asteroids and powerups in the background

                            WIN.blit(p.currentImg, p.rect)
                            asteroidManager.blit(WIN)
                            powerupManager.blit(WIN)

                            # Displaying the translucent background and the "paused" text

                            WIN.blit(bgP, (0, 0))
                            WIN.blit(pauseTxt, pauseTxtPos)

                            # Displaying the buttonsd

                            bButton.render(WIN)
                            resumeButton.render(WIN)
                            cButton.render(WIN)

                            evQueue = pygame.event.get()

                            # Checking for button presses

                            if resumeButton.pressed(evQueue): # Resuming if the resume button is pressed
                                paused = False

                            elif bButton.pressed(evQueue): # Going back to menu if the menu button is pressed
                                backToMenu = True

                            elif cButton.pressed(evQueue): # Loading the controls menu if the controls button is pressed
                                # Loading the image

                                htp = pygame.transform.scale(pygame.image.load("./Assets/Backgrounds/h2p.png"), (WIDTH, HEIGHT)).convert()

                                controlRun = True

                                # Controls menu loop

                                while controlRun:
                                    # Displaying the controls image

                                    WIN.fill((0, 0, 0))
                                    WIN.blit(htp, (0, 0))
                                    
                                    # Checking if the application has been closed or the escape key has been pressed

                                    for i in pygame.event.get():
                                        if i.type == pygame.QUIT:
                                            fullBreak = True
                                            break

                                        if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE: # If escape pressed, go back to pause menu
                                            controlRun = False
                                            break

                                    if fullBreak:
                                        controlRun = False

                                    pygame.display.update()

                                del htp, controlRun

                            # Checking if the application has been closed or the escape button has been pressed to resume the game
                
                            for i in evQueue:
                                if i.type == pygame.QUIT:
                                    fullBreak = True
                                    break

                                if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE:
                                    paused = False
                                    break

                            if fullBreak or backToMenu:
                                paused = False

                            pygame.display.update()
                            time.update()

                        # Rehiding the mouse cursor and unpausing music/sounds

                        pygame.mouse.set_visible(False)
                        pygame.mixer.unpause()
                        pygame.mixer.music.unpause()

                        # Deleting objects to save memory

                        del pauseTxt, pauseTxtPos, resumeButton, bButton, cButton, bgP
                        
                    pygame.display.update()
                    time.update()

                    if fullBreak or backToMenu:
                        gameRun = False

                goRun = True # This looks like it says go, but its short for game over

                # Loading the cutscene if the player has won (surpassed 2500 score on story mode)

                if p.gameOver:
                    deathMsg = "You win!" # Setting the message shown on screen to "you win!"
                    pygame.mixer.music.pause() # Pausing music for the cutscene
                    cmd = cutscene.play(WIN, (WIDTH, HEIGHT), p.sprites[0][0]) # Storing the return value of the cutscene in a variable and closing application if it returns "fullbreak"
                    pygame.mixer.music.unpause() # Resuming music after the cutscene
                    endSound = winSound # Changing the game over sound to the victory sound

                    if cmd == "fullbreak":
                        fullBreak = True
                else:
                    cmd = None
                    deathMsg = "You died!" # Setting the message shown on screen to "you died!"

                pygame.mouse.set_visible(True) # Making the mouse cursor visible again

                if fullBreak or backToMenu:
                    goRun = False
                    break

                # Rendering the game over message

                deathTxt = fonts.render("menuTxt", deathMsg, (255, 255, 255))
                
                # Creating the "play again" button and the text for the players score

                scoreMsg = fonts.render("nextTxt", "Your score was: " + str(asteroidManager.score), (255, 255, 255))
                againButton = ui.Button("Play again", (0, 0, 0), HEIGHT//10, WIDTH//2 - 1.5 * deathTxt.get_width()//4, HEIGHT//2 + HEIGHT//25 + HEIGHT//60, 3 * deathTxt.get_width()//4, 5 * deathTxt.get_height()//6)

                # Creating the save score button if the mode isnt story mode and repositioning the menu button if the mode is story mode

                if p.mode != 3:
                    saveButton = ui.Button("Save score", (0, 0, 0), HEIGHT//10, WIDTH//2 - 1.5 * deathTxt.get_width()//4, HEIGHT//2 + (5 * deathTxt.get_height()//6) + HEIGHT//25 + 2 * (HEIGHT//60), 3 * deathTxt.get_width()//4, 5 * deathTxt.get_height()//6)
                    menuButton = ui.Button("Menu", (0, 0, 0), HEIGHT//10, WIDTH//2 - 1.5 * deathTxt.get_width()//4, HEIGHT//2 + 2 * (5 * deathTxt.get_height()//6) + HEIGHT//25 + 3 * (HEIGHT//60), 3 * deathTxt.get_width()//4, 5 * deathTxt.get_height()//6)
                else:
                    saveButton = None
                    menuButton = ui.Button("Menu", (0, 0, 0), HEIGHT//10, WIDTH//2 - 1.5 * deathTxt.get_width()//4, HEIGHT//2 + (5 * deathTxt.get_height()//6) + HEIGHT//25 + 2 * (HEIGHT//60), 3 * deathTxt.get_width()//4, 5 * deathTxt.get_height()//6)

                # Playing the game over sound

                endSound.play()

                # Game over loop

                while goRun and not fullBreak and not backToMenu:
                    # Displaying the background

                    WIN.fill((0, 0, 0))
                    scroller.scrollBG(time.deltaTime)

                    goQueue = pygame.event.get()

                    # Checking for button presses

                    if againButton.pressed(goQueue): # Restarts the game if "play again" is pressed
                        goRun = False

                    elif menuButton.pressed(goQueue): # Goes back to menu if the menu button is pressed
                        mode = None
                        backToMenu = True

                    elif mode != 3 and saveButton.pressed(goQueue): # Allowing users to enter their name if the save score button is pressed
                        saveRun = True

                        # Loading the transparent background

                        saveBg = pygame.transform.scale(pygame.image.load("./Assets/Backgrounds/bgTransparent2.png"), (WIDTH//1.2, HEIGHT//1.2)).convert_alpha()

                        # Creating a text box and header for the text box

                        txtBox = ui.TextBox(12, pygame.Rect(WIDTH//2 - WIDTH//6, HEIGHT//2 - HEIGHT//24, WIDTH//3, HEIGHT//12), (WIDTH, HEIGHT), WIN, fonts.fonts["boxTxt"])
                        nameTxt = fonts.render("nextTxt", "Enter your name:", (255, 255, 255))

                        # Creating a leaderboard object to save the score

                        board = leaderboard.init((WIDTH, HEIGHT))
                        
                        # Save menu loop

                        while saveRun:
                            # Displaying the background

                            WIN.fill((0, 0, 0))
                            scroller.scrollBG(time.deltaTime)

                            queue = pygame.event.get()

                            # Displaying the headers and buttons in the background

                            WIN.blit(deathTxt, (WIDTH//2 - deathTxt.get_width()//2, HEIGHT//2 - deathTxt.get_height()))
                            WIN.blit(scoreMsg, (WIDTH//2 - scoreMsg.get_width()//2, HEIGHT//2 + scoreMsg.get_height()//8))
                    
                            againButton.render(WIN)
                            saveButton.render(WIN)
                            menuButton.render(WIN)

                            # Displaying the translucent background stacked 3 times to make it look more opaque

                            WIN.blit(saveBg, (WIDTH//12, HEIGHT//12))
                            WIN.blit(saveBg, (WIDTH//12, HEIGHT//12))
                            WIN.blit(saveBg, (WIDTH//12, HEIGHT//12))

                            # Displaying the text box and its header

                            txtBox.blit()
                            WIN.blit(nameTxt, (WIDTH//2 - WIDTH//6, HEIGHT//2 - HEIGHT//24 - nameTxt.get_height()))

                            # Adding the name and score if the user presses the enter key

                            if txtBox.enter(queue):
                                board.load(mode)
                                board.add(mode, txtBox.txt, asteroidManager.score)
                                board.mode = None
                                break

                            # Checking if the application has been closed or the escape key has been pressed

                            for i in queue:
                                if i.type == pygame.QUIT:
                                    fullBreak = True

                                if i.type == pygame.KEYDOWN and i.key == pygame.K_ESCAPE: # if escape pressed, go back to game over screen
                                    saveRun = False

                            pygame.display.update()
                            time.update()

                            if fullBreak or backToMenu:
                                saveRun = False

                        del saveRun, saveBg, txtBox, nameTxt, board

                    # Checking if application has been closed

                    for i in pygame.event.get():
                        if i.type == pygame.QUIT:
                            fullBreak = True
                            break

                    # Displaying the game over text
                    
                    WIN.blit(deathTxt, (WIDTH//2 - deathTxt.get_width()//2, HEIGHT//2 - deathTxt.get_height()))

                    # Displaying the score if the player hasnt beaten the game

                    if p.gameOver != True:
                        WIN.blit(scoreMsg, (WIDTH//2 - scoreMsg.get_width()//2, HEIGHT//2 + scoreMsg.get_height()//8))
                    
                    # Displaying the buttons (ignoring the save button if the mode isnt story mode)
                    againButton.render(WIN)
                    if mode != 3 and mode != None:
                        saveButton.render(WIN)
                    menuButton.render(WIN)
                    
                    pygame.display.update()
                    time.update()
                    
                    if fullBreak or backToMenu:
                        goRun = False

                goRun = False

                # Deleting objects to save memory

                del gameRun, p, asteroidManager, offset, powerupManager, scoreTxt, nextTxtPos, endSound, mainQueue, paused, goRun, deathMsg, cmd, deathTxt, scoreMsg, againButton, menuButton, saveButton
                    
            pygame.display.update()
            time.update()

            if fullBreak or backToMenu:
                selectRun = False

        # Deleting objects to save memory

        del selectRun, selectTxt, selectTxtPos, endlessButton, oneLifeButton, storyButton, backToMenuButton

    # Checking if application has been closed

    for i in runQueue:
        if i.type == pygame.QUIT:
            run = False
            break

    pygame.display.update()
    time.update()

    if fullBreak:
        run = False

pygame.quit()
