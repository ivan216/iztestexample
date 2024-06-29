from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place ,delay
from rpze.flow.flow import FlowManager
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.structs.plant import Plant , PlantStatus
from rpze.rp_extend import Controller

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
        2-0
        .....
        y...o
        .....
        .....
        .....
        xg lz tt
        0  0  1200
        2-9 4-9 2-9''')

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        # zlist = iz_test.game_board.zombie_list
        # zb = zlist[0]
        pl = iz_test.ground["2-1"]
        await count_butter(pl,2)
        place("lz 3-6")
        iz_test.game_board.frame_duration = 200 #201变成暂停
        await delay(60)
        iz_test.game_board.frame_duration = 3
        
    iz_test.start_test(jump_frame=False, speed_rate=3)   #最小 0.05

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
