from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_die,until_plant_n_shoot
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        5000 -1
        3-0
        .....
        .....
        ddpcc
        .....
        .....
        lz 
        0  
        3-6''') #2.73倍75 = 205
    
    _75_count = 0
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal _75_count
        c = iz_test.ground["3-4"]
        d = iz_test.ground["3-2"]
        lz = iz_test.game_board.zombie_list[0]

        await (until_plant_die(c) | until(lambda _:lz.hp < 90))
        if not c.is_dead:
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

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)