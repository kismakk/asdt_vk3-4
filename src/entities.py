import random

from PIL.ImageTk import PhotoImage
from pygame.mixer import Sound


class Player:
    def __init__(self, name: str, image: PhotoImage, sound: Sound, window_x, window_y):
        self.name = name
        self.image = image
        self.sound = sound
        self.score = 0
        self.coord_y = random.randint(50, window_y - 50)

        if self.name == "Kernesti":
            self.coord_x = 50
        else:
            self.coord_x = window_x - 200
            
    def place(self):
        self.coord_y = random.randint(100, 600)
        print(f"Name: {self.name}, Coords: {self.coord_x} {self.coord_y}")

    def get_score(self) -> int:
        return self.score

    def increase_score(self) -> None:
        self.score += 1
        
    def reset_score(self) -> None:
        self.score = 0

    def get_sound(self) -> Sound:
        return self.sound

    def get_image(self) -> PhotoImage:
        return self.image


