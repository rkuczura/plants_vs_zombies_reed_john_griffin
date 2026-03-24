#defining the config class
class LawnConfig:
    def __init__(self, width:int, height:int, columns:int, rows:int, plant_radius:int):
        self.width: int = width
        self.height: int = height
        self.columns: int = columns
        self.rows: int = rows
        self.plant_radius: int = plant_radius


#defining the game state. 
# 
"""Not sure what else to put in here"""
class LawnState:
    def __init__(self):
        self.round_num: int
        self.zombies_present: int
        self.running: bool