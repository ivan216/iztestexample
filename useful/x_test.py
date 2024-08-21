from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until
from rpze.iztest.operations import place
from rpze.rp_extend import Controller

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        2-0
        .....
        .....
        ssl_s
        .....
        .....
        tz 
        0  
        3-6''')
    
    zb = pl = None
    print()
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal zb,pl
        zb = iz_test.game_board.zombie_list[0]
        pl = iz_test.ground["3-3"]

    @iz_test.flow_factory.add_tick_runner()
    def output(_):
        # if zb is not None:
        #     print("\033[A\033[K"+"%.2f"%zb.x)
        if pl is not None:
            print("\033[A\033[K"+"%.2f"%pl.hp)
    
    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    