from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place ,repeat
from rpze.flow.utils import until, delay

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        .t__.
        .....
        .....
        lz 
        0  
        3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        dc = iz_test.ground["3-4"]
        lz = iz_test.game_board.zombie_list[0]

        print(lz.accessories_hp_1)
        await until(lambda _:lz.accessories_hp_1 < 370)
        lzdx = lz.dx
        

        place("xg 3-6")
    
    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
