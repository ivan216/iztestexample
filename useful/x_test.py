from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place
from rpze.rp_extend import Controller
from rpze.structs.zombie import ZombieStatus,ZombieType
from rpze.flow.flow import FlowManager

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        xxxxx
        ..._.
        xxxxx
        .....
        tt 
        0  
        3-8''')
    
    zb = pl = None
    print()
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal zb,pl
        zb = iz_test.game_board.zombie_list[0]
        # pl = iz_test.ground["3-1"]

        # zb.x = 765.0
        # pl.generate_cd = 2

    @iz_test.flow_factory.add_tick_runner()
    def output(fm:FlowManager):
        if zb is not None:
            print("\033[A\033[K"+"%.2f"%zb.x)
            # print("\033[A\033[K"+"%.2f"%zb.dx)
        # if pl is not None:
        #     print("\033[A\033[K"+"%.2f"%pl.hp)

    @iz_test.on_game_end()
    def count(_):
        print()
    
    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    