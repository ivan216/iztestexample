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
        2-3
        .....
        bsc_s
        .3...
        .....
        .....
        lz
        0  
        2-6 ''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        zlist = iz_test.game_board.zombie_list
        lz = zlist[0]        
        plist = iz_test.ground
        s = plist["2-5"]
        b = plist["2-1"]
        await until(lambda _:s.is_dead)
        await until_plant_n_shoot(b).after(30)
        cg = place("cg 2-6")
        await until(lambda _:cg.int_x < 350)
        place("cg 2-6")
    
    iz_test.start_test(jump_frame=1, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)