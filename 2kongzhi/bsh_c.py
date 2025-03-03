from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint
from rpze.iztest.cond_funcs import until_plant_n_shoot

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-0
        bsh_c
        .....
        .....
        .....
        .....
        lz 
        0  
        1-6''')

    @iz_test.flow_factory.add_flow()
    async def _(_):
        zlist = iz_test.game_board.zombie_list
        lz = zlist[0]
        plist = iz_test.ground
        c = plist["1-5"]
        b = plist["1-1"]
        await until(lambda _:lz.int_x <= 340)
        await until_plant_n_shoot(b).after(0)
        place("cg 1-6")
    
    iz_test.start_test(jump_frame=1, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)