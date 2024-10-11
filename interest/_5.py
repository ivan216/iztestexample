from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        2-0
        .....
        ..._.
        ...5.
        .....
        .....
        lz 
        0  
        4-5''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        star = iz_test.ground["3-4"]
        lz = iz_test.game_board.zombie_list[0]

        await until_plant_last_shoot(star).after(100 + randint(0,10))   #100-110
        xg = place("xg 2-6")

    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)