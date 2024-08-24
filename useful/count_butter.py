from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.flow.flow import FlowManager
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.structs.plant import Plant , PlantStatus
from rpze.structs.projectile import ProjectileType
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
    
    def count_butter2(plant: Plant, n:int = 1) -> AwaitableCondFunc:         #通过子弹数黄油数量
        def _cond_func(fm: FlowManager,v = VariablePool( projs = 0, count_down = 0,try_to_shoot_time=None)):
            if plant.generate_cd == 1:                                      # 下一帧可能开打
                v.try_to_shoot_time = fm.time + 1
            if (v.try_to_shoot_time == fm.time) and (plant.launch_cd == 0): #并没有攻击，计数重置
                v.projs = 0
                v.count_down = 0
            if (v.try_to_shoot_time == fm.time) and (plant.launch_cd != 0): #确定要攻击，把launch_cd传给count_down
                v.count_down = plant.launch_cd
            if v.count_down == 1 :                                          #在count_down到1时，黄油才可以被获得。
                for proj in ~iz_test.game_board.projectile_list:
                    if proj.type_ == ProjectileType.butter :
                        v.projs += 1
            if v.projs == n:
                return True 
            if v.count_down !=0:
                v.count_down -= 1
            return False
        return AwaitableCondFunc(_cond_func)

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        # zb = iz_test.game_board.zombie_list[0]
        pl = iz_test.ground["2-1"]
        await count_butter(pl,2)
        place("lz 3-6")

    iz_test.start_test(jump_frame=False, speed_rate=2) 

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
