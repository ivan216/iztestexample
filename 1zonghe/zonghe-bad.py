from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint
from rpze.structs.zombie import ZombieStatus

def print_fail_clock_result(clock_result:list):
    for i in range(0,46):
        print("出生相位%d~%d失败次数：%d"%(i*10,i*10+9,clock_result[i]))

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        3-0 4-0 5-0
        .....
        .....
        p5pzh
        31sjh
        bpctp
        lz 
        0  
        4-6 ''')
    
    ## 3mj,<1075

    clock_result = [0 for _ in range(0,46)]
    i = 0
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal clock_result,i
        plist = iz_test.ground
        ts = plist["4-1"]
        s = plist["4-3"]
        h = plist["4-5"]
        await until(lambda _:h.hp <= 20)
        mj = place("mj 4-6")
        await delay(310)
        place("xt 3-2")
        await until(lambda _:mj.status == ZombieStatus.dancing_walking)
        clock_record = iz_test.game_board.mj_clock % 460
        i =int(clock_record / 10)

        @iz_test.on_game_end()
        def _(result: bool):
            nonlocal clock_result,i
            if not result:
                clock_result[i] += 1

    iz_test.start_test(jump_frame=1, speed_rate=2)
    print_fail_clock_result(clock_result)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)