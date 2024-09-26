from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until,delay
from rpze.iztest.operations import place
from rpze.structs.zombie import ZombieStatus
from random import randint
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant
from rpze.iztest.cond_funcs import until_plant_last_shoot

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

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        spptz
        .....
        .....
        .....
        xg 
        0  
        2-6''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        p = iz_test.ground["2-3"]
        z = iz_test.ground["2-5"]

        await (until_plant_last_shoot(p) | delay(300))
        lz = place("lz 2-6")
        await until(lambda _:z.hp < 80)
        await until_plant_n_shoot(p).after(40)
        place("xg 2-6")
    
    @iz_test.flow_factory.add_tick_runner()
    def check(fm:FlowManager):
        if fm.time > 300:
            if iz_test.ground["2-1"] is None:
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)
    
    iz_test.start_test(jump_frame=1,speed_rate=10)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)