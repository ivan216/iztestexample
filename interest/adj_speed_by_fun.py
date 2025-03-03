from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place ,delay
from rpze.rp_extend import Controller

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        2-0
        .....
        .....
        1....
        .....
        .....
        lz 
        0  
        3-6 ''')

    @iz_test.flow_factory.add_flow()
    async def _(_):
        pl = iz_test.ground["2-1"]
        await delay(200)
        place("lz 3-6")
        iz_test.game_board.frame_duration = 200 #201变成暂停
        await delay(60)
        iz_test.game_board.frame_duration = 3
        
    iz_test.start_test(jump_frame=False, speed_rate=3)   #最小 0.05

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
