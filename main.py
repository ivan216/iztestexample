# -*- coding: utf_8 -*-
from rpze.basic.inject import InjectedGame
from rpze.examples.dancing_example import dancing_example
# from rpze.examples.end_callback_example import end_test

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    dancing_example(game.controller)
    # end_test(game.controller)
