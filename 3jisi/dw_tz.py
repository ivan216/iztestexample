from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint
from rpze.iztest.cond_funcs import until_plant_n_shoot

# 45%补杆，较差

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0 
        .....
        .....
        dw_.s
        .....
        .....
        lz 
        0  
        3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        d = iz_test.ground["3-1"]
        s = iz_test.ground["3-5"]

        await until(lambda _:s.is_dead)
        await until_plant_n_shoot(d).after(40+randint(0,10))
        place("xg 3-6")
    
    iz_test.start_test(jump_frame=1, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)