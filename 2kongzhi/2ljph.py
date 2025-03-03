from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        4-0 5-0
        .....
        .....
        .....
        byy_l
        2ljph
        tz
        0  
        5-6 ''')
    # 400
    @iz_test.flow_factory.add_flow()
    async def _(_):
        tz = iz_test.game_board.zombie_list[0]
        h = iz_test.ground["5-5"]
        p = iz_test.ground["5-4"]
        p.x = 280 -5 # -5 +4

        await until(lambda _:h.is_dead).after(80) #80
        mj = place("mj 5-6")

    iz_test.start_test(jump_frame=1, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)