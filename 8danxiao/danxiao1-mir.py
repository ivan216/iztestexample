from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        1-0
        xpxxh
        sssss
        .....
        .....
        .....
        lz 
        0  
        2-6  ''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        lz = iz_test.game_board.zombie_list[0]
        xi = iz_test.ground["2-2"]
        await until(lambda _:lz.x < 152).after(randint(0,10))    #152 93% 5k 91.5%
        # await until(lambda _:xi.hp < 300)  #300 92%
        place("lz 1-6")
    
    iz_test.start_test(jump_frame=1, speed_rate=3)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)