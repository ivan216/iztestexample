from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from random import randint
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant
from rpze.structs.zombie import ZombieStatus

def until_pea_last_shoot(plant: Plant) -> AwaitableCondFunc:
    def _cond_func(fm: FlowManager,
                   v=VariablePool(try_to_shoot_time=None, wait_time = 0)):
        if plant.generate_cd == 1:  # 下一帧开打
            v.try_to_shoot_time = fm.time + 1
        if v.try_to_shoot_time != fm.time:
            v.wait_time += 1
        if v.try_to_shoot_time == fm.time and plant.launch_cd != 0:  # 在攻击时
            v.wait_time = 0     #重置等待时间
        if v.wait_time > 150:
            return True
        return False
    return AwaitableCondFunc(_cond_func)

def print_fail_clock_result(clock_result:list):
    for i in range(0,46):
        print("出生相位%d~%d失败次数：%d"%(i*10,i*10+9,clock_result[i]))

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        10000 -1
        3-0 4-0 5-0
        dyloz
        p__pw
        p5pzh
        31sjh
        bpctp
        lz 
        0  
        4-6 ''')
    
    ## 3mj,<1075

    clock_result = [0 for x in range(0,46)]
    i = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
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
        def end_callback(result: bool):
            nonlocal clock_result,i
            if not result:
                clock_result[i] += 1

    iz_test.start_test(jump_frame=1, speed_rate=2)
    print_fail_clock_result(clock_result)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)