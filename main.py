from rpze.basic.inject import InjectedGame
from rpze.examples.botanical_clock import botanical_clock

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    botanical_clock(game.controller)
