from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.rp_extend import Controller
from random import randint
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant
from rpze.structs.zombie import ZombieStatus

def until_plant_n_shoot(plant: Plant, n:int = 1, non_stop :bool = True) -> AwaitableCondFunc:
    def _cond_func(fm: FlowManager,
                v=VariablePool(try_to_shoot_time=None, shots = 0)):
        if plant.generate_cd == 1:  # 下一帧开打
            v.try_to_shoot_time = fm.time + 1
        if v.try_to_shoot_time == fm.time and plant.launch_cd != 0:  # 在攻击时
            v.shots += 1
        if v.try_to_shoot_time == fm.time and plant.launch_cd == 0: #不再攻击时，计数清零
            if non_stop:
                v.shots = 0
        if v.shots == n:
            return True
        return False
    return AwaitableCondFunc(_cond_func)

# 1026

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        5000 -1
        1-0 2-0 3-0 4-0 5-0
        dpwpt
        .ppt.
        p__hw
        dtp_s
        dtpzz
        lz 
        0  
        4-6''')
    
    _1_gan = 0
    _1_tong = 0
    _2_fail = 0
    _3_fail = 0
    _4_fail = 0
    _52_success = 0
    _53_fail = 0
    _53_success = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        d = iz_test.ground["4-1"]
        lz = iz_test.game_board.zombie_list[0]

        await until(lambda _:lz.x < 310)    #310
        await until_plant_n_shoot(d).after(33 + randint(0,10))
        mj = place("mj 4-6")
        await until(lambda _:mj.status is ZombieStatus.dancing_walking).after(250)
        await until(lambda _:iz_test.game_board.mj_clock%460 ==456).after(randint(0,10))
        mj2 = place("mj 2-8")

    @iz_test.on_game_end()
    def count(res:bool):
        nonlocal _1_gan,_1_tong,_2_fail,_3_fail,_4_fail,_52_success,_53_fail,_53_success
        if not res:
            if iz_test.ground["1-0"] is not None:
                if (iz_test.ground["1-2"] is not None) \
                    and (iz_test.ground["1-4"] is not None):
                    _1_tong += 1
                else:
                    _1_gan += 1
            if iz_test.ground["2-0"] is not None:
                _2_fail += 1
            if iz_test.ground["3-0"] is not None:
                _3_fail += 1
            if iz_test.ground["4-0"] is not None:
                _4_fail += 1
            if iz_test.ground["5-0"] is not None:
                if iz_test.ground["5-2"] is None:
                    _52_success += 1
                else:
                    if iz_test.ground["5-3"] is None:
                        _53_success += 1
                    else:
                        _53_fail += 1
    
    iz_test.start_test(jump_frame=0, speed_rate=1)
    print("1补杆(75) ",_1_gan)
    print("1补桶(125) ",_1_tong)
    print("2补(75)",_2_fail)
    print("3补(75)",_3_fail)
    print("4失败(75) ",_4_fail)
    print("5失败 ")
    print(" 引雷(175) ",_52_success)
    print(" 没引雷没吃喷(260) ",_53_fail)
    print(" 没引雷有吃喷(229)",_53_success)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
