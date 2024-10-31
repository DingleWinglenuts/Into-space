import pygame, csv
pygame.init()

# This file contains an object for a leaderboard, which manages pretty much everything to do with leaderboards (with some things being required on implementation)

class init():
    # Storing key information and sets up variables that will be used later

    def __init__(self, dim):
        self.mode = None
        self.dimensions = dim
        self.font = pygame.font.Font("./Assets/Fonts/pixeboy.ttf", int(self.dimensions[1]//12))
        headerFont = pygame.font.Font("./Assets/Fonts/pixeboy.ttf", int(self.dimensions[1]//10))
        self.current = 0
        self.loadedData = []
        self.loadedImgs = []
        self.transparentBg = pygame.transform.scale(pygame.image.load("./Assets/Backgrounds/bgTransparent2.png"), (self.dimensions[0] - self.dimensions[0]//8, self.dimensions[1] - self.dimensions[1]//8)).convert_alpha()
        self.headers = (headerFont.render("name", True, (200, 200, 200)), headerFont.render("score", True, (200, 200, 200)))
        self.page = 1
        self.pageCount = None
        self.pageImg = None

    # Loading the leaderboard for the selected mode and also the first page of this leaderboard

    def load(self, mode):

        # Selecting the file depending on the mode

        self.mode = mode
        
        if mode == 1:
            fileType = "./Assets/Scores/endless.csv"
        elif mode == 2:
            fileType = "./Assets/Scores/one_life.csv"

        # Loading the data from the file and storing it into a list

        file = open(fileType, "r")
        dat = csv.DictReader(file)

        self.data = []
        self.loadedData = []
        self.loadedImgs = []
        self.page = 1
        self.pageImg = None
        self.pageCount = None

        for i in dat:
            self.data.append(i)
        file.close()

        # Contingency for if there are less than 10 scores in the page

        endPointer = 10
        
        while endPointer > len(self.data):
            endPointer -= 1

        # Adding the data for the first page to a separate list

        for i in range(endPointer):
            self.loadedData.append(self.data[i])

        # Creating font images for the scores and adding them to dictionaries stored within a list that holds the rendered scores and names

        for i in range(len(self.loadedData)):
            self.loadedImgs.append({})
            self.loadedImgs[i]["name"] = self.font.render(self.loadedData[i]["name"], True, (255, 255, 255))
            self.loadedImgs[i]["score"] = self.font.render(self.loadedData[i]["score"], True, (255, 255, 255))

        # Getting the number of pages required for the page counter

        self.pageCount = len(self.data)//10

        if len(self.data) % 10 != 0:
            self.pageCount += 1

        # Rendering the page counter text

        self.pageImg = self.font.render(f"{self.page}/{self.pageCount}", True, (255, 255, 255))

    # Loading pages upon pressing the corresponding button

    def loadPage(self):
        self.loadedData = []
        self.loadedImgs = []

        # Getting the correct number of scores for the page

        endPointer = self.current + 10

        while endPointer > len(self.data):
            endPointer -= 1

        # Storing the data for the new page in a list

        for i in range(self.current, endPointer):
            self.loadedData.append(self.data[i])

        # Rendering the scores for the new page

        for i in range(len(self.loadedData)):
            self.loadedImgs.append({})
            self.loadedImgs[i]["name"] = self.font.render(self.loadedData[i]["name"], True, (255, 255, 255))
            self.loadedImgs[i]["score"] = self.font.render(self.loadedData[i]["score"], True, (255, 255, 255))

        # Updating the page counter for the next page

        self.pageImg = self.font.render(f"{self.page}/{self.pageCount}", True, (255, 255, 255))

    # Adding a new score to the leaderboard when a player saves their score
        
    def add(self, mode, name, score):
        added = False

        if mode == 1:
            fileType = "./Assets/Scores/endless.csv"
        elif mode == 2:
            fileType = "./Assets/Scores/one_life.csv"
        
        for i in range(len(self.data)):
            if score >= int(self.data[i]["score"]):
                self.data.insert(i, {"name":name,"score":score})
                added = True
                break

        if not added:
            self.data.append({"name":name,"score":str(score)})

        file = open(fileType, "w")
        writer = csv.DictWriter(file, ["name", "score"])
        writer.writeheader()
        writer.writerows(self.data)
        file.close()

    # Displaying the leaderboard

    def display(self, WIN):

        # Displaying the background and headers

        WIN.blit(self.transparentBg, (self.dimensions[0]//16, self.dimensions[1]//16))
        WIN.blit(self.headers[0], (self.dimensions[0]//16 + self.dimensions[0]//64, self.dimensions[1]//16 + self.dimensions[1]//64))
        WIN.blit(self.headers[1], (self.dimensions[0]//2 + self.dimensions[0]//64, self.dimensions[1]//16 + self.dimensions[1]//64))

        # Displaying the scores for the current page

        for i in range(len(self.loadedImgs)):
            WIN.blit(self.loadedImgs[i]["name"], (self.dimensions[0]//16 + self.dimensions[0]//64, self.dimensions[1]//12 + (i + 1) * self.dimensions[1]//64 + i * self.loadedImgs[i]["name"].get_height() + self.headers[1].get_height()))
            WIN.blit(self.loadedImgs[i]["score"], (self.dimensions[0]//2 + self.dimensions[0]//64, self.dimensions[1]//12 + (i + 1) * self.dimensions[1]//64 + i * self.loadedImgs[i]["name"].get_height() + self.headers[1].get_height()))#

        # Displaying the page counter

        WIN.blit(self.pageImg, (self.dimensions[0]//2 - self.pageImg.get_width()//2, self.dimensions[1] - 1.2 * self.dimensions[1]//10 - self.pageImg.get_height()))
