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
        bphl2
        .....
        .....
        kg 
        0  
        3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        b = iz_test.ground["3-1"]
        await until(lambda _: b.hp <= 220).after(randint(0,10)) 
        place("cg 3-6")

    iz_test.start_test(jump_frame=1, speed_rate=1)

with InjectedGame(game_path) as game:
    fun(game.controller)
    