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
        4-0 3-0 5-0
        .s...
        .....
        ....w
        d..t.
        ....z
        mj 
        0  
        4-8''')
    
    mj = None
    oldx = None
    dm = get_dancing_manipulator(iz_test)

    @iz_test.flow_factory.add_flow()
    async def _(fm):
        nonlocal mj
        mj = iz_test.ground.zombie(0)

        dm.start("move")
        await dm.until_next_phase("summon",lambda _:mj.is_eating)

    # @iz_test.flow_factory.add_flow()
    # async def _(fm):
    #     mj = iz_test.ground.zombie(0)
    #     await until(lambda _:mj.status is ZombieStatus.dancing_walking)
    #     print(fm.time," x:",mj.x)
    #     await until(lambda _:mj.is_eating)
    #     print(fm.time)

    @iz_test.flow_factory.add_tick_runner()
    def _(fm):
        nonlocal oldx
        if mj is not None:
            if mj.status is ZombieStatus.dancing_walking:
                newx = mj.x
                if oldx is None:
                    oldx = mj.x
                if (dx:= oldx-newx) != 0:
                    print(fm.time," x:",mj.x, " dx=",dx)
                oldx = newx

    iz_test.start_test(jump_frame=0, speed_rate=2)


with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)