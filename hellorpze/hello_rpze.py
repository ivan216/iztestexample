from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    iz_test = IzTest(game.controller).init_by_str('''
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
    