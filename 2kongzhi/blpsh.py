from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        blpsh
        .._._
        byy_l
        .....
        mj
        0  
        3-6 ''')
    
    mj = None
    p = None
    count = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal mj,p
        mj = iz_test.game_board.zombie_list[0]
        p = iz_test.ground["2-3"]

    @iz_test.on_game_end()
    def end_callback(result: bool):
        nonlocal mj,p,count
        if not mj.is_dead :
            if p.is_dead :
                count += 1

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)