from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until
from rpze.iztest.operations import place
from rpze.iztest.dancing import partner
from rpze.structs.zombie import ZombieStatus
from rpze.flow.flow import FlowManager
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-0
        .s...
        .....
        .....
        .....
        .....
        mj 
        0  
        2-6''')
    
    print()
    mjx = .0
    mj = None
    stuck = False
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal mj
        mj = iz_test.ground.zombie(0)
    
    @iz_test.flow_factory.add_tick_runner()
    def count(fm:FlowManager):
        nonlocal mjx,stuck
        if fm.time >0:
            if mj.status is ZombieStatus.dancing_walking:
                if mj.x == mjx:
                    stuck = True
                    print("\033[A\033[K"+"stuck")
                else:
                    mjx = mj.x
                    stuck = False
                    print("\033[A\033[K"+"not stuck")
            else:
                mjx = mj.x
                stuck = False
                print("\033[A\033[K"+"not walking")
    
    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)