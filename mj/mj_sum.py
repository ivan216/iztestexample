from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place
from rpze.rp_extend import Controller
from rpze.iztest.dancing import get_dancing_manipulator
from rpze.structs.zombie import ZombieStatus

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        2-0 3-0 4-0
        .s...
        .....
        .....
        .....
        .....
        mj 
        0  
        3-9''')
    
    dm = get_dancing_manipulator(iz_test)

    @iz_test.flow_factory.add_flow()
    async def _(_):
        dm.start("summon")
    
    @iz_test.flow_factory.add_flow()
    async def _(fm):
        mj = iz_test.ground.zombie(0)
        while True:
            await until(lambda _:mj.status is not ZombieStatus.dancing_summoning)
            place("t 3-5")
            last = True
            await until(lambda _:mj.status is ZombieStatus.dancing_summoning)
            if last:
                print(fm.time)
                last = False
    
    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)