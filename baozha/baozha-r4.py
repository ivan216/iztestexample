from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until
from rpze.iztest.operations import place
from rpze.iztest.dancing import partner
from rpze.structs.zombie import ZombieStatus
from random import randint
from rpze.iztest.sun_num_utils import get_sunflower_remaining_sun

# 待测：4无相位补刀，1有相位补刀，2有相位补刀

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0 4-0 5-0
        tppzz
        zpptz
        ttttz
        pphts
        tptzz
        mj 
        0  
        4-9''')
    
    _50_count = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _50_count
        iz_test.game_board.sun_num = 2000
        mj = iz_test.game_board.zombie_list[0]
        # mjc = 90   #90 47%
        # iz_test.game_board.mj_clock = randint(mjc,mjc+10)

    iz_test.start_test(jump_frame=1, speed_rate=2)
    print(_50_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)