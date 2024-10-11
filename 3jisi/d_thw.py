from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place

def fun(ctler: Controller):
    n = 10000
    iz_test = IzTest(ctler).init_by_str(f'''
        {n} -1
        3-1 
        .....
        .....
        d_th.
        .....
        .....
        lz 
        0  
        3-6 ''')

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        lz = iz_test.game_board.zombie_list[0]
        h = iz_test.ground["3-4"]

        await until(lambda _:h.is_dead).after(4)
        speed = lz.dx
        await delay(167.5/speed - 410)
        place("cg 3-6")

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)