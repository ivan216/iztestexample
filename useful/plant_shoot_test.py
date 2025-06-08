from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.structs.plant import Plant, PlantType
from rpze.flow.utils import AwaitableCondFunc,FlowManager,VariablePool
# from rpze.iztest.cond_funcs import until_plant_n_shoot
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def until_plant_n_shoot(plant: Plant, n: int = 1, non_stop: bool = True) -> AwaitableCondFunc[None]:
    """
    生成一个 等到植物n次攻击 的函数

    Args:
        plant: 要判断的植物
        n: 攻击次数
        non_stop: 是否为不间断攻击
    """

    match plant.type_:  # 修正连发植物攻击时机
        case PlantType.repeater | PlantType.split_pea:
            shoot_next_gcd = 26
        case PlantType.cattail:
            shoot_next_gcd = 51
        case _:
            shoot_next_gcd = 1
    
    def _await_func(fm: FlowManager,
                    v=VariablePool(try_to_shoot_time=None, shots=0)):
        if plant.generate_cd == shoot_next_gcd:  # 下一帧开打
            v.try_to_shoot_time = fm.time + 1
        if v.try_to_shoot_time == fm.time:
            if plant.launch_cd > 15:  # 在攻击时
                v.shots += 1
            else:  # 不再攻击时
                if non_stop:  # 设置了不停止标志，则计数清零
                    v.shots = 0
        if v.shots == n:
            return True
        return False
    
    return AwaitableCondFunc(_await_func)

def fun(ctler):
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
    async def _(_):
        d = iz_test.ground["2-1"]
        await until_plant_n_shoot(d,2).after(30)
        place("tz 2-6")

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(game_path) as game:
    fun(game.controller)
    