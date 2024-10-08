from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.flow.utils import AwaitableCondFunc, VariablePool, delay
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant,PlantStatus
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

##暂时没有完善

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        y3_s_
        .....
        .....
        cg cg 
        0  20
        3-6 3-6''')

    cg1 = None
    cg2 = None

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal cg1,cg2
        zlist = iz_test.game_board.zombie_list
        cg1 = zlist[0]
        await delay(20)
        cg2 = zlist[1]

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        plist = iz_test.ground
        y = plist["3-1"]
        await count_butter(y).after(142)
        if cg1.butter_cd ==0 and cg2.butter_cd ==0 :
            await count_butter(y,2).after(142)
            if (cg1.int_x >= 143) & (cg2.int_x >= 143):
                place("lz 3-6")
        else :
            await count_butter(y).after(142)
            if (cg1.int_x >= 143) | (cg2.int_x >= 143) :
                place("lz 3-6")

    iz_test.start_test(jump_frame=0, speed_rate=5)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
