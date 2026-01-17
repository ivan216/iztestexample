from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place
from rpze.rp_extend import Controller
from rpze.iztest.dancing import get_dancing_manipulator
from rpze.structs.zombie import ZombieStatus

# 0-26, 68-93(fast), 129-161, 203-228(fast)
# 240,260,320,380,440,

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
    
    mj = None
    
    dm = get_dancing_manipulator(iz_test, "move")

    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal mj
        mj = iz_test.ground.zombie(0)
    
    @iz_test.flow_factory.add_tick_runner()
    def _(fm):
        if fm.time > 0 and (mj.status is not ZombieStatus.dancing_moonwalk)\
            and (mj.status is not ZombieStatus.dancing_point)\
            and (mj.status is not ZombieStatus.dancing_summoning)\
            and (mj.status is not ZombieStatus.dancing_wait_summoning):
            print("time:",fm.time," CLOCK:",iz_test.game_board.mj_clock%460," STA:",hex(mj.status)," X:",mj.x)
    
    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)