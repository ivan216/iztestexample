from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.structs.zombie import ZombieStatus
from rpze.iztest.dancing import partner

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0 2-0 4-0
        .....
        ddpcc
        dppph
        ddpcc
        .....
        lz 
        0  
        3-6  ''')   # +25
    
    _125_count = 0
    three_count = 0
    _205_count = 0
    _150_count = 0
    _75_count = 0
    _50_count = 0
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal _125_count
        h = iz_test.ground["3-5"]
        p = iz_test.ground["3-4"]

        await until(lambda _:h.hp < 4)
        place("cg 3-6")
        await until(lambda _:p.hp < 150)    #150
        mj = place("mj 3-6")
        await until(lambda _:mj.status is ZombieStatus.dancing_summoning)
        wb = partner(mj,"a")
        await until(lambda _:wb.hp < 90)
        place("xt 3-1")
        _125_count += 1
    
    @iz_test.on_game_end()
    def _(_):
        nonlocal three_count,_50_count,_75_count,_150_count,_205_count
        if iz_test.ground["3-0"] is not None:
            three_count += 1
        if iz_test.ground["2-0"] is not None:
            i = 0
            if iz_test.ground["2-1"] is not None:
                i += 1
            if iz_test.ground["2-2"] is not None:
                i += 1
            if iz_test.ground["2-3"] is not None:
                i += 1

            if i == 0:
                _50_count += 1
            elif i == 1:
                _75_count += 1
            elif i == 2:
                _150_count += 1
            else:
                _205_count += 1

        if iz_test.ground["4-0"] is not None:
            i = 0
            if iz_test.ground["4-1"] is not None:
                i += 1
            if iz_test.ground["4-2"] is not None:
                i += 1
            if iz_test.ground["4-3"] is not None:
                i += 1

            if i == 0:
                _50_count += 1
            elif i == 1:
                _75_count += 1
            elif i == 2:
                _150_count += 1
            else:
                _205_count += 1

    iz_test.start_test(jump_frame=0, speed_rate=1)
    print(_125_count)
    print(three_count)
    print(_50_count)
    print(_75_count)
    print(_150_count)
    print(_205_count)
    
with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)