from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        5000 -1
        4-0 5-0
        dwptz
        .....
        p__sw
        dtp_s
        dpwpt
        mj 
        0  
        2-7''')
    
    _4_fail = _52_fail = _52_suc = 0
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        d = iz_test.ground["4-1"]
        p = iz_test.ground["4-3"]
        z = iz_test.ground["4-5"]

        await delay(20)
        lz = place("lz 4-6")

        await until(lambda _:lz.x < 310)    #310
        await until(lambda _:230 <=iz_test.game_board.mj_clock%460 <=290) # 230-290 90%
        mj2 = place("mj 4-6")
    
    @iz_test.on_game_end()
    def _(res:bool):
        nonlocal _4_fail,_52_fail,_52_suc
        if not res:
            if iz_test.ground["4-0"] is not None:
                _4_fail += 1
            if iz_test.ground["5-0"] is not None:
                if iz_test.ground["5-2"] is None:
                    _52_suc += 1
                else:
                    _52_fail += 1
    
    iz_test.start_test(jump_frame=1, speed_rate=3)
    print("4补(75) ",_4_fail)
    print("5补鬼桶(175) ",_52_fail)
    print("5补鬼杆(125)",_52_suc)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
