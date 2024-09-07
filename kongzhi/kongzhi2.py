from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from rpze.structs.zombie import ZombieStatus
from rpze.iztest.sun_num_utils import get_sunflower_remaining_sun
from rpze.iztest.dancing import partner
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        -1 -1
        1-0 2-0 3-0
        bppch
        blpsh
        3y_h_
        .....
        .....
        cg
        0  
        2-6 ''')
    
    # 补偷不具有合理性?
    
    sun_num = [0] * 9
    tp_fail = _1_fail = _2_fail = _3_fail = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        await delay(180)
        place("lz 2-6")
        await delay(20)
        place("lz 2-6")
        await delay(20)
        place("mj 2-6")
        
    
    @iz_test.on_game_end()
    def count_sun(res:bool):
        nonlocal tp_fail,_1_fail,_2_fail,_3_fail
        if iz_test.ground["3-4"] is None:
            i = 0
        else:
            h = iz_test.ground["3-4"]
            i = get_sunflower_remaining_sun(h) // 25
        sun_num[i] += 1
        if iz_test.ground["3-1"] is not None:
            tp_fail += 1
        if not res:
            if iz_test.ground["1-0"] is not None:
                _1_fail += 1
            if iz_test.ground["2-0"] is not None:
                _2_fail += 1
            if iz_test.ground["3-0"] is not None:
                _3_fail += 1
    
    @iz_test.check_tests_end()
    def end_test_callback(n, ns):
        if n%100 == 0:
            print("漏花 ",[round(x/n,2) for x in sun_num])
            print("漏三线 %.2f"%(tp_fail/n))
            print("漏一 %.2f"%(_1_fail/n))
            print("漏二 %.2f"%(_2_fail/n))
            print("漏三 %.2f"%(_3_fail/n))
        if n < 1000:
            return None
        return True
    
    iz_test.start_test(jump_frame=1, speed_rate=5)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)