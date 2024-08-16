from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.rp_extend import Controller

def fun(ctler: Controller):
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
        3-6''')

    @iz_test.flow_factory.add_destructor()
    def end_print_time(fm):
        print(fm.time)

    iz_test.start_test(jump_frame=0, speed_rate=5) 

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)