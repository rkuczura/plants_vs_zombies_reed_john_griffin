#Main file to be run in order to start the game

import pygame
from pvz_model import LawnConfig
from pvz_controller import startgame
from pvz_view import build_ui


def main() -> None:
    """Initialize and start the game"""
    config = LawnConfig(
        width=1350,
        height=750,
        columns=9,
        rows=5,
        plant_radius=20,
    )
    
    # Initialize pygame display window
    screen = build_ui(config)

    # Run the game
    startgame(screen, config)


if __name__ == "__main__":
    main()
