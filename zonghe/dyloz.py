from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

# 301,千分之6补双杆

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-3 3-2
        .....
        .....
        dyloz
        .....
        .....
        kg 
        0  
        3-6''')

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        zlist = iz_test.game_board.zombie_list
        kg = zlist[0]
        await until(lambda _:kg.hp <= 250)  #250
        place("xt 3-3")
    
    iz_test.start_test(jump_frame=0, speed_rate=3)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)