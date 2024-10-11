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
        3-3
        .....
        .....
        ..t5o
        .....
        .....
        lz 
        0  
        4-5''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        star = iz_test.ground["3-4"]
        lz = iz_test.game_board.zombie_list[0]

        ##其实只能用until_plant_last_shoot

        await until_plant_last_shoot(star).after(30 + randint(0,10))
        lz.die_no_loot()
        cg = place("cg 3-6")
        cg.hp = 270

    iz_test.start_test(jump_frame=1, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)