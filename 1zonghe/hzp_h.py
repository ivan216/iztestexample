from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.flow.utils import until
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
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
    async def _(_):
        lz = iz_test.game_board.zombie_list[0]
        dc = iz_test.ground["3-4"]

        await until(lambda _:dc.status_cd > 0)
        if lz.dx < 0.33:
            await until(lambda _:dc.status_cd == 0)
        place("xg 3-6")

    iz_test.start_test(jump_frame=1, speed_rate=2)

with InjectedGame(game_path) as game:
    fun(game.controller)
