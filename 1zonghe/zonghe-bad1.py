from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0 4-0 5-0
        .....
        .....
        p5ptz
        31sjh
        bpcph
        lz mj xt
        0  360 670
        4-6 4-6 3-2''')

    # @iz_test.flow_factory.add_flow()
    # async def _(_):
    #     plist = iz_test.game_board.plant_list
    #     h = plist["4-5"]
    #     await until(lambda _:h.hp <= 20)
    #     mj = place("mj 4-6")
    #     await delay(310)
    #     place("xt 3-2")

    iz_test.start_test(jump_frame=1, speed_rate=5)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)