from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place, repeat
from rpze.flow.utils import until, delay
from rpze.iztest.cond_funcs import until_plant_n_shoot

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-3
        .....
        .....
        szp_s
        .....
        .....
        lz 
        0  
        3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        lz = iz_test.game_board.zombie_list[0]
        p = iz_test.ground["3-3"]
        dc = iz_test.ground["3-4"]

        await until(lambda _:dc.status_cd > 0)
        if lz.dx < 0.33:
            await until(lambda _:dc.status_cd == 0)
        place("xg 3-6")

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)