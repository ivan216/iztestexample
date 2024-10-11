from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_die,until_plant_n_shoot
from rpze.flow.flow import FlowManager
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        3-0
        .....
        .....
        ddpcc
        .....
        .....
        lz 
        0  
        3-6''') #82.6%铁桶 + 0.383倍75 = 207
    
    _75_count = 0
    _125_count = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm: FlowManager):
        nonlocal _75_count,_125_count
        c = iz_test.ground["3-4"]
        d = iz_test.ground["3-2"]
        lz = iz_test.game_board.zombie_list[0]

        await (until_plant_die(c) | until(lambda _:lz.hp < 90))
        if c.is_dead :
            _125_count += 1
            return iz_test.end(True)
        else:
            place("lz 3-6")
            _75_count += 1
            await until_plant_die(c)
            await until_plant_n_shoot(d).after(50)
            cg = place("cg 3-6")
            _75_count += 1
            await until(lambda _:cg.hp < 170)
            place("cg 3-6")
            _75_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=3)
    print(_75_count)
    print(_125_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)