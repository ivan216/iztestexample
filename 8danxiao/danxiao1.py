from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        5-0
        .....
        .....
        .....
        sssss
        xpxxh
        lz 
        0  
        4-6  ''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        lz = iz_test.game_board.zombie_list[0]
        xi = iz_test.ground["4-2"]
        await until(lambda _:lz.x < 151).after(randint(0,10))    #151 93% 5k 93%
        # await until(lambda _:xi.hp < 292)  #300 94%
        place("lz 5-6")
    
    iz_test.start_test(jump_frame=1, speed_rate=3)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)