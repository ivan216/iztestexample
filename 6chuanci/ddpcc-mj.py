from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager
from rpze.structs.zombie import ZombieStatus,Zombie
from rpze.iztest.dancing import partner
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_last_shoot

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        2-0 3-0 4-0
        .....
        ddpcc
        dd...
        ddpcc
        .....
        mj 
        0  
        3-6 ''')
    
    _125_count = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm: FlowManager):
        nonlocal _125_count

    iz_test.start_test(jump_frame=0, speed_rate=1)
    print(_125_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
