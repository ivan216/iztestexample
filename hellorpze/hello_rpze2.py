from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        1ssss
        .....
        .....
        lz
        0  
        3-6 ''')
    
    iz_test.start_test(jump_frame=True, speed_rate=5)

with InjectedGame(game_path) as game:
    fun(game.controller)