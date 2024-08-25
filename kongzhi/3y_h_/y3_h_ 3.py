from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.flow.utils import AwaitableCondFunc, VariablePool ,until,delay
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant ,PlantStatus
from rpze.rp_extend import Controller
from random import randint

def count_butter(plant: Plant, n:int = 1) -> AwaitableCondFunc:         #通过状态数黄油数量
    def _cond_func(fm: FlowManager,v = VariablePool( projs = 0, try_to_shoot_time=None )):
        if plant.generate_cd == 1:                                      # 下一帧开打
            v.try_to_shoot_time = fm.time + 1
        if v.try_to_shoot_time == fm.time :
            if plant.status is PlantStatus.kernelpult_launch_butter :
                v.projs += 1
            elif plant.launch_cd == 0 :
                v.projs = 0
        if v.projs == n:
            return True 
        return False
    return AwaitableCondFunc(_cond_func)

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        y3_s_
        .....
        .....
        lz lz 
        0  20
        3-6 3-6''')
    
    _75_count = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _75_count
        y = iz_test.ground["3-1"]
        l = iz_test.ground["3-2"]

        await count_butter(y,2)
        if l.is_dead :
            place("cg 3-6")
        else:
            place("lz 3-6")
        _75_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=3)
    print(_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
