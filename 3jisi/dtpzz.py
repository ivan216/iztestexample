from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place 
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.rp_extend import Controller
from random import randint

#补13%

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0 
        .....
        .....
        dtpzz
        .....
        .....
        xg lz
        0  0
        3-7 5-6''') 
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        d = iz_test.ground["3-1"]
        p = iz_test.ground["3-3"]
        z = iz_test.ground["3-5"]

        await (until_plant_last_shoot(p) | delay(300))
        place("xg 3-6")
        await until_plant_last_shoot(p).after(randint(0,10))
        place("lz 3-6")
        await until(lambda _:z.hp < 4).after(randint(0,10)) 
        place("cg 3-6")
    
    iz_test.start_test(jump_frame=0, speed_rate=4)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)