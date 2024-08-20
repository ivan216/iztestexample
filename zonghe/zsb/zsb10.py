from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.flow.utils import until, delay
from rpze.iztest.operations import place ,repeat
from rpze.rp_extend import Controller
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant

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
        1000 -1
        3-0 4-0 5-0
        y_p_h
        dpczh
        bs5tz
        13jlo
        ppwph
        tt 
        0  
        1-6 ''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        plist = iz_test.ground
        c = plist["2-3"]
        star = plist["3-3"]
        await until(lambda _:c.status_cd >0).after(30)
        kg = place("kg 4-6")
        await delay(20)
        place("kg 2-6")
        await delay(20)
        place("cg 4-6")
        await until(lambda _:kg.int_x < 40)
        await until(lambda _:kg.int_x >= 260)
        await until_plant_n_shoot(star).after(60)
        place("mj 4-6")

    iz_test.start_test(jump_frame=0, speed_rate=3)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
