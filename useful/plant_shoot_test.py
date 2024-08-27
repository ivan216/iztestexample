from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant

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
        2-0
        .....
        dbl5o
        .....
        .....
        .....
        tz 
        0  
        2-6''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        d = iz_test.ground["2-1"]
        await until_plant_n_shoot(d,2).after(30)
        place("tz 2-6")

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    