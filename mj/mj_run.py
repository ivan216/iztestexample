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
        d..t.
        .....
        .....
        mj 
        0  
        3-8''')
    
    mj = None
    oldx = 0
    dm = get_dancing_manipulator(iz_test)

    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal mj
        mj = iz_test.ground.zombie(0)
        await until(lambda _:mj.status is ZombieStatus.dancing_walking)

        while True:
            dm.next_phase("m")
            await delay(26)
            dm.next_phase("d")
            await delay(1)
    
    @iz_test.flow_factory.add_flow()
    async def _(fm):
        mj = iz_test.ground.zombie(0)
        await until(lambda _:mj.status is ZombieStatus.dancing_walking)
        print(fm.time)
        await until(lambda _:mj.is_eating)
        print(fm.time)

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)