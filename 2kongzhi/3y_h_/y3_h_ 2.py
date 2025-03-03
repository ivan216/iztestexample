from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.flow.utils import delay
from rpze.rp_extend import Controller
from rpze.iztest.cond_funcs import until_n_butter
from random import randint

##暂时没有完善

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        y3_s_
        .....
        .....
        cg cg 
        0  20
        3-6 3-6''')

    cg1 = None
    cg2 = None

    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal cg1,cg2
        zlist = iz_test.game_board.zombie_list
        cg1 = zlist[0]
        await delay(20)
        cg2 = zlist[1]

    @iz_test.flow_factory.add_flow()
    async def _(_):
        plist = iz_test.ground
        y = plist["3-1"]
        await until_n_butter(y).after(142)
        if cg1.butter_cd ==0 and cg2.butter_cd ==0 :
            await until_n_butter(y,2).after(142)
            if (cg1.int_x >= 143) & (cg2.int_x >= 143):
                place("lz 3-6")
        else :
            await until_n_butter(y).after(142)
            if (cg1.int_x >= 143) | (cg2.int_x >= 143) :
                place("lz 3-6")

    iz_test.start_test(jump_frame=0, speed_rate=5)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)