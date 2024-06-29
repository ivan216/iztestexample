from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        5000 -1
        3-0
        .....
        .....
        ppblp
        .....
        .....
        tt
        0  
        3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        # zlist = iz_test.game_board.zombie_list
        plist = iz_test.ground
        # zb = zlist[0]
        pl = plist["3-4"]
        await until(lambda _:pl.is_dead).after(130+ randint(0,10))
        place("cg 3-6")
    
    iz_test.start_test(jump_frame=1, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)