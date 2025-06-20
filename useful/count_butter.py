from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.flow.flow import FlowManager
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.structs.plant import Plant, PlantStatus
from rpze.structs.projectile import ProjectileType
from rpze.rp_extend import Controller

from typing import Literal

CountButterModeLiteral = Literal[0, 1, 2, "total", "nonstop", "continuous"]
"""数黄油函数的计数方法

    - 0 或 "total" 表示允许攻击中断
    - 1 或 "nonstop" 表示攻击不中断
    - 2 或 "continuous" 表示攻击不中断, 而且黄油必须连续投出
"""


def until_n_butter(plant: Plant, n: int = 1, mode: CountButterModeLiteral = 1) -> AwaitableCondFunc[None]:
    """
    生成一个 等到玉米攻击n发黄油 的函数

    await 调用后返回"总攻击次数"

    Args:
        plant: 要判断的植物
        n: 攻击黄油次数
        mode: 字面量, 表示计数方法
    """
    match mode:
        case "total" | 0:
            mode_index = 0
        case "nonstop" | 1:
            mode_index = 1
        case "continuous" | 2:
            mode_index = 2
        case _:
            raise ValueError(" invalid mode !")

    def _await_func(fm: FlowManager, v=VariablePool(butters=0, projs=0, try_to_shoot_time=None)):
        if plant.generate_cd == 1:  # 下一帧开打
            v.try_to_shoot_time = fm.time + 1
        if v.try_to_shoot_time == fm.time:
            if plant.status is PlantStatus.kernelpult_launch_butter:  # 出黄油
                v.butters += 1
                v.projs += 1
            elif plant.launch_cd == 0:  # 攻击停止
                if mode_index != 0:
                    v.butters = 0
            else:  # 出玉米粒
                v.projs += 1
                if mode_index == 2:
                    v.butters = 0
        if v.butters == n:
            return True, v.projs
        return False
    
    return AwaitableCondFunc(_await_func)


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
    
    def until_n_butter2(plant: Plant, n:int = 1, mode:int = 1) -> AwaitableCondFunc[None]: #通过子弹数黄油数量
        "mode = 0 or 1 or 2"
        def _cond_func(fm: FlowManager,v = VariablePool( projs = 0, count_down = 0,try_to_shoot_time=None)):
            if plant.generate_cd == 1:                                      # 下一帧可能开打
                v.try_to_shoot_time = fm.time + 1
            if (v.try_to_shoot_time == fm.time) and (plant.launch_cd == 0): #并没有攻击，计数重置
                if mode != 0 :
                    v.projs = 0
            if (v.try_to_shoot_time == fm.time) and (plant.launch_cd != 0): #确定要攻击，把launch_cd传给count_down
                v.count_down = plant.launch_cd
            if v.count_down == 1 :                                          #在count_down到1时，黄油才可以被获得。
                for proj in ~iz_test.game_board.projectile_list:
                    if proj.type_ == ProjectileType.butter :
                        v.projs += 1
                    elif mode == 2:
                        v.projs = 0
            if v.projs == n:
                return True 
            if v.count_down !=0:
                v.count_down -= 1
            return False
        return AwaitableCondFunc(_cond_func)

    @iz_test.flow_factory.add_flow()
    async def _(_):
        # zlist = iz_test.game_board.zombie_list
        # zb = zlist[0]
        plist = iz_test.ground
        pl = plist["2-1"]
        shots = await until_n_butter(pl,2,1)
        place("lz 3-6")
        print(shots)

    iz_test.start_test(jump_frame=0, speed_rate=3) 

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
