from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        4-0
        .....
        .....
        .5...
        31sjh
        .....
        cg
        0  
        4-6''')

    @iz_test.flow_factory.add_flow()
    async def _(_):
        cg = iz_test.game_board.zombie_list[0]
        h = iz_test.ground["4-5"]

        await until(lambda _:cg.hp <= 460)
        place("xg 4-6")
        await until(lambda _:h.is_dead)
        place("cg 4-6")

    iz_test.start_test(jump_frame=1, speed_rate=3)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)