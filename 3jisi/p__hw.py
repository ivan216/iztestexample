from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0 4-0 2-0
        .....
        dpptw
        p__h.
        dtp_z
        .....
        mj 
        0  
        3-9 ''')
    
    r2 = 0
    r3 = 0
    r4 = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        mj = iz_test.game_board.zombie_list[0]
        await until(lambda _:mj.x < 380)
        lz = place("lz 3-6")

    @iz_test.on_game_end()
    def count(_):
        nonlocal r2,r3,r4
        if iz_test.ground["2-0"] is not None:
            r2 += 1
        if iz_test.ground["3-0"] is not None:
            r3 += 1
        if iz_test.ground["4-0"] is not None:
            r4 += 1

    iz_test.start_test(jump_frame=1, speed_rate=3)
    print(r2,"\n",r3,"\n",r4)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)