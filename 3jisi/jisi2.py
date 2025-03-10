from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint
from rpze.iztest.cond_funcs import until_plant_n_shoot

# 497

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        4-0 5-0
        .....
        .....
        p__hw
        dtp_s
        dpwpt
        lz 
        0  
        4-6''')
    
    _4_fail = 0
    _52_fail = 0
    _52_suc = 0
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        d = iz_test.ground["4-1"]
        lz = iz_test.game_board.zombie_list[0]

        await until(lambda _:lz.x < 310)    #310
        await until_plant_n_shoot(d).after(33 + randint(0,10))
        mj = place("mj 4-6")

    @iz_test.on_game_end()
    def _(_):
        nonlocal _4_fail,_52_fail,_52_suc
        if iz_test.ground["4-0"] is not None:
            _4_fail += 1
        if iz_test.ground["5-0"] is not None:
            if iz_test.ground["5-2"] is None:
                _52_suc += 1
            else:
                _52_fail += 1

    iz_test.start_test(jump_frame=1, speed_rate=4)
    print("4补(75) ",_4_fail)
    print("5补(175) ",_52_fail)
    print("5补(125) ",_52_suc)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)