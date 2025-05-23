from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until
from rpze.iztest.operations import place
from random import randint
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        b2hhl
        .....
        .....
        kg 
        0  
        3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        kg = iz_test.game_board.zombie_list[0]
        # kg = iz_test.ground.zombie(0)
        b = iz_test.ground["3-1"]
        await (until(lambda _: kg.hp <= 230).after(45) 
               | until(lambda _: b.hp <= 32)).after(randint(0,10))
        place("lz 3-6")

    iz_test.start_test(jump_frame=1, speed_rate=2)

with InjectedGame(game_path) as game:
    fun(game.controller)