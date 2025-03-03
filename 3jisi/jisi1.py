from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        4-0 5-0
        dpwpt
        .....
        p__sw
        dtp_s
        dtpzz
        mj 
        0  
        2-7''')
    
    _41_fail = 0
    _51_fail = 0
    _52_success = 0
    _53_fail = 0
    _53_success = 0
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        d = iz_test.ground["4-1"]
        p = iz_test.ground["4-3"]
        z = iz_test.ground["4-5"]

        await delay(20)
        lz = place("lz 4-6")

        await until(lambda _:lz.x < 310)    #310
        await until(lambda _:110 <= iz_test.game_board.mj_clock%460 <= 170) # 110 - 140 - 170
        mj2 = place("mj 4-6")
    
    @iz_test.on_game_end()
    def _(res:bool):
        nonlocal _41_fail,_51_fail,_52_success,_53_fail,_53_success
        if not res:
            if iz_test.ground["4-0"] is not None:
                _41_fail += 1
            if iz_test.ground["5-0"] is not None:
                if iz_test.ground["5-2"] is None:
                    _52_success += 1
                else:
                    if iz_test.ground["5-3"] is None:
                        _53_success += 1
                    else:
                        _53_fail += 1
    
    iz_test.start_test(jump_frame=0, speed_rate=3)
    print("4喷失败 ",_41_fail)
    print("5喷失败 ",_51_fail)
    print("其中；")
    print(" 引雷(175) ",_52_success)
    print(" 没引雷没吃喷(260) ",_53_fail)
    print(" 没引雷有吃喷(229)",_53_success)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
