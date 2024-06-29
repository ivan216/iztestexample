from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.flow.flow import FlowManager
from rpze.flow.utils import AwaitableCondFunc, VariablePool ,until ,delay
from rpze.structs.plant import Plant, PlantStatus
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
        3y_s_
        .....
        .....
        lz  
        0  
        3-6 ''')
    
    _75_count = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _75_count
        zlist = iz_test.game_board.zombie_list
        lz = zlist[0]
        plist = iz_test.ground
        ts = plist["3-1"]
        y = plist["3-2"]
        s = plist["3-4"]
        await (count_butter(y,2).after(115) | until(lambda _:s.is_dead) | until(lambda _:lz.hp < 90))
        if not s.is_dead:
            place("lz 3-6")
            _75_count += 1
            await until(lambda _:s.is_dead)
        cg = place("cg 3-6")
        _75_count += 1
        await until(lambda _:cg.hp <= 210) 
        if ts.hp >=300:     #杆也过不去
            place("cg 3-6") #补第二杆
            _75_count += 1

    iz_test.start_test(jump_frame=0, speed_rate=5)
    print("补75:",_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)