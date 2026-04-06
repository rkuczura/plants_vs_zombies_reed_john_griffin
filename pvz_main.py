#Main file to be ran in order to start the game

#importing pygame module
import pygame

#importing the config class and game starting function from other modules
from pvz_model import LawnConfig
from pvz_controller import startgame
from pvz_view import build_ui

#define our config values to modify the game
def main() -> None:
    config = LawnConfig(
        width = 1350,
        height = 750,
        columns = 9,
        rows = 5,
        plant_radius = 20,
    )
    #Initialize pygame display window
    screen = build_ui(config)

    #Calls function from controller which runs the game loop
    startgame(screen, config)

if __name__ == "__main__":
    main()
