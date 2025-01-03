from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until
from rpze.iztest.operations import place
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
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

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    