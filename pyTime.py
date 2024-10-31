import time

# This file contains an object that is used to allow for unlimited framerates by getting the time passed since the last frame and the total runtime of the application

class PyTime():
    def __init__(self):
        self.prevTime = time.perf_counter()
        self.totalTime = 0
        self.deltaTime = 0 # This variable stores the time passed since the previous frame (named deltaTime as a game engine named Unity has a similarly named function for the same purpose and due to my familiarity with Unity, it made it easier to understand in practice)

    def update(self): # This function must be called every frame to update the time passed since the last frame
        currentTime = time.perf_counter()
        self.deltaTime = currentTime - self.prevTime
        self.prevTime = currentTime
        self.totalTime += self.deltaTime
