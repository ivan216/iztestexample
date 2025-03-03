from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_n_shoot
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        5000 -1
        3-0
        .....
        .....
        ddppc
        .....
        .....
        cg lz
        0  180
        3-6 3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        d = iz_test.ground["3-2"]
        await delay(180)
        lz = iz_test.game_board.zombie_list[1]

        await until(lambda _:lz.x < 310)
        await until_plant_n_shoot(d).after(48)
        place("cg 3-6")

    iz_test.start_test(jump_frame=1, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)