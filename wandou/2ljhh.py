from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.flow.flow import FlowManager
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.structs.plant import Plant
from random import randint

def until_plant_n_shoot(plant: Plant, n:int = 1) -> AwaitableCondFunc:
    def _cond_func(fm: FlowManager,
                v=VariablePool(try_to_shoot_time=None, shots = 0)):
        if plant.generate_cd == 1:  # 下一帧开打
            v.try_to_shoot_time = fm.time + 1
        if v.try_to_shoot_time == fm.time and plant.launch_cd != 0:  # 在攻击时
            v.shots += 1
        if v.try_to_shoot_time == fm.time and plant.launch_cd == 0: #不再攻击时，计数清零
            v.shots = 0
        if v.shots == n:
            return True
        return False
    return AwaitableCondFunc(_cond_func)

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        2000 -1
        3-0
        .....
        .....
        2ljhh
        .....
        .....
        gl 
        0  
        3-6''')
    
    xg_count = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm: FlowManager):
        nonlocal xg_count
        rp = iz_test.ground["3-1"]
        j = iz_test.ground["3-3"]

        await until_plant_n_shoot(rp)
        if fm.time < 140:
            await until(lambda _:j.hp < 216)  #216
            place("xg 3-6")
            xg_count += 1
        
    iz_test.start_test(jump_frame=1, speed_rate=4)
    print(xg_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
