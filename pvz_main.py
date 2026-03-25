#Main file to be ran in order to start the game

#importing in tkinter library which will be used often
import tkinter as tk

#importing the config class and game starting function from other modules
from pvz_model import LawnConfig
from pvz_controller import startgame

#define our config values to modify the game
def main() -> None:
    config = LawnConfig(
        width = 1350,
        height = 750,
        columns = 9,
        rows = 5,
        plant_radius = 20,
    )
    #creates the main application window and initializes Tkinter enviroment
    root = tk.Tk()
    tk.title=("Plants vs Zombies")
    startgame(root,config)
    root.mainloop()

if __name__ == "__main__":
    main()
