from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.flow.flow import FlowManager
from random import randint
from rpze.iztest.cond_funcs import until_plant_n_shoot

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        2000 -1
        3-0
        .....
        .....
        blphh
        .....
        .....
        gl 
        0  
        3-6''')
    
    xg_count = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm: FlowManager):
        nonlocal xg_count
        b = iz_test.ground["3-1"]

        await until_plant_n_shoot(b)
        if fm.time < 136:
            await delay(randint(20,30))
            place("xg 3-6")
            xg_count += 1
        
    iz_test.start_test(jump_frame=1, speed_rate=4)
    print(xg_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
