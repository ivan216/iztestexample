from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-0 2-0
        tppzs
        zpptz
        ttttz
        pphtz
        tptzz
        mj 
        0  
        1-9''')
    
    _50_count = 0
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal _50_count
        iz_test.game_board.sun_num = 2000
        mj = iz_test.game_board.zombie_list[0]
        mjc = 60
        iz_test.game_board.mj_clock = randint(mjc,mjc+10)

    iz_test.start_test(jump_frame=0, speed_rate=2)
    print(_50_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)