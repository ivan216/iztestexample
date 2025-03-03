from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-1 
        .....
        .....
        p5p..
        31jhs
        .....
        kg 
        0  
        4-6''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        zlist = iz_test.game_board.zombie_list
        kg = zlist[0]
        plist = iz_test.ground
        star = plist["3-2"]
        await until(lambda _:kg.int_x < 40)
        await until(lambda _:kg.int_x >= 80)
        await until_plant_last_shoot(star).after(58 + randint(0,10))
        place("cg 3-6")
        kg.die_no_loot()
    
    iz_test.start_test(jump_frame=0, speed_rate=5)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)