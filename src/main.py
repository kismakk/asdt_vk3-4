import math
import os
import random
import tkinter as tk
from tkinter.constants import *
from pygame import mixer
from PIL import ImageTk, Image
from entities import Player
from utilities import convert_png_to_photoImage

# Initialize mixer and sounds
mixer.init()

throw_path = os.path.join("sounds", "throwing.wav")
smack_path = os.path.join("sounds", "smack.mp3")

throw_sound = mixer.Sound(throw_path)
smack_sound = mixer.Sound(smack_path)

# Constants
TK_WINDOW_DIMENSIONS = "1024x720+500+0"
WINDOW_X = 1024
WINDOW_Y = 720

PLAYER_PNG = ["pictures/erne.png", "pictures/kerne.png"]
TARGET_PNG = "pictures/maalitaulu.png"
THROWABLES_PNG = ["pictures/tomaatti.png", "pictures/splat.png"]

# Initialize Tkinter
root = tk.Tk()
root.title("Ernestin ja Kernestin tomaattiskaba")
root.geometry(TK_WINDOW_DIMENSIONS)


def update_score():
    """ Refresh the score label """
    score_label.config(text=f"Kernesti: {kernesti.get_score()}  |  Ernesti: {ernesti.get_score()}")


def reset_score():
    """ Reset the score for both players and refresh the score label. """
    kernesti.reset_score()
    ernesti.reset_score()
    update_score()


def move_character(player: Player, label: tk.Label):
    """ Moves the characters randomly and places the image accordingly """
    player.place()
    label.place(x=player.coord_x, y=player.coord_y)
    
    root.update_idletasks()


def throw_tomato(player: Player):
    """
    Function that throws the tomato by the player given as a parameter
    """
    
    # Create tomato image
    tomato_label = tk.Label(root, image=tomato_img)
    tomato_label.place(x=player.coord_x, y=player.coord_y)
    
    # Update root to display tomato
    root.update_idletasks()
    
    # Get the tomato coordinates
    current_x, current_y = tomato_label.winfo_x(), tomato_label.winfo_y()
    
    # Get the targets coordinates, we're aiming for the center
    target_center_x = target_label.winfo_x() + (target_label.winfo_width() // 2)
    target_center_y = target_label.winfo_y() + (target_label.winfo_height() // 2)

    # Calculate the distance between target and tomato
    delta_x = target_center_x - current_x
    delta_y = target_center_y - current_y

    variance = random.uniform(-0.1, 0.1) # Variance so not all tomatoes hit the target and trajectories differ
    angle = math.atan2(delta_y, delta_x) + variance # Calculate the angle of the throw

    speed = 10

    # Step sizes for updating the tomato position
    step_x = math.cos(angle) * speed
    step_y = math.sin(angle) * speed 
    
    def move_tomato():
        """
        Inner function responsible for the throw animation.
        """
        nonlocal current_x, current_y, player

        # Update the coordinates by adding the step
        current_x += step_x
        current_y += step_y

        # Update tomato position
        tomato_label.place(x=current_x, y=current_y)

        # Condition that checks if the tomato hit the target within a certain range
        if (abs(current_x - target_center_x) < 10) and (abs(current_y - target_center_y) < 10):
            tomato_label.config(image=splash_img)  # Change the image to splash image
            smack_sound.play()
            player.increase_score()
            update_score() 
            tomato_label.after(500, tomato_label.destroy) # Destroying the tomato after 500 ms
            return 
        
        # Condition to check if the tomato flew out of bounds and destroying it
        if (current_x < 0 or current_x > WINDOW_X or current_y < 0 or current_y > WINDOW_Y):
            tomato_label.destroy()
            return

        root.after(50, move_tomato) # Calling the function after 50 ms for smooth animation

    player.sound.play()
    move_tomato()


ernesti_img, kernesti_img = [convert_png_to_photoImage(img, (100, 100)) for img in PLAYER_PNG]
target_img = convert_png_to_photoImage(TARGET_PNG, (150, 150))
tomato_img, splash_img = [convert_png_to_photoImage(img, (50, 50)) for img in THROWABLES_PNG]

target_x = (WINDOW_X // 2) - 75
target_y = (WINDOW_Y // 2) - 75

target_label = tk.Label(root, image=target_img)
target_label.place(x=target_x, y=target_y)

kernesti = Player("Kernesti", kernesti_img, throw_sound, WINDOW_X, WINDOW_Y)
ernesti = Player("Ernesti", ernesti_img, throw_sound, WINDOW_X, WINDOW_Y)

kernesti_label = tk.Label(root, image=kernesti.get_image())
kernesti_label.place(x=kernesti.coord_x, y=kernesti.coord_y)

ernesti_label = tk.Label(root, image=ernesti.get_image())
ernesti_label.place(x=ernesti.coord_x, y=ernesti.coord_y)

button_frame = tk.Frame(root)
button_frame.pack(side="top", pady=10, anchor=N)

move_kernesti = tk.Button(button_frame, text="Liikuta Kernestiä", command=lambda: move_character(kernesti, kernesti_label))
move_kernesti.pack(side="left", padx=10)

move_ernesti = tk.Button(button_frame, text="Liikuta Ernestiä", command=lambda: move_character(ernesti, ernesti_label))
move_ernesti.pack(side="left", padx=10)

throw_kernesti = tk.Button(button_frame, text="Heitä tomaatti Kernestiltä", command=lambda: throw_tomato(kernesti))
throw_kernesti.pack(side="left", padx=10)

throw_ernesti = tk.Button(button_frame, text="Heitä tomaatti Ernestiltä", command=lambda: throw_tomato(ernesti))
throw_ernesti.pack(side="left", padx=10)

score_label = tk.Label(root, text=f"Kernesti: {kernesti.get_score()}  |  Ernesti: {ernesti.get_score()}", font=("Helvetica", 16))
score_label.pack(pady=10, side="top", anchor=N)

reset_button = tk.Button(root, text="Nollaa pisteet", command=reset_score)
reset_button.pack(pady=10, side="top", anchor=N)

root.mainloop()
