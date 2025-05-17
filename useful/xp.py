from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.plant_modifier import set_puff_x_offset
from random import randint
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-1
        .....
        .....
        pblh2
        .....
        .....
        gl 
        0  
        3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        xp = iz_test.ground["3-1"]
        # set_puff_x_offset(xp,range(-5,-2))
        xp.x = randint(35,37)

    iz_test.start_test(jump_frame=1, speed_rate=2)

with InjectedGame(game_path) as game:
    fun(game.controller)
    