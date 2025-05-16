from rpze.basic.inject import InjectedGame
from rpze.examples.botanical_clock import botanical_clock
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

with InjectedGame(game_path) as game:
    botanical_clock(game.controller)
