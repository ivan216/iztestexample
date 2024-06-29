from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.structs.zombie import ZombieType
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.flow.utils import delay
from rpze.flow.flow import FlowManager
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.structs.plant import Plant
from rpze.rp_extend import Controller
from rpze.iztest.operations import place

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
        1-2
        zzh31
        ...yw
        .....
        .....
        .....
        lz
        0
        5-9''')
    
    #2024图九；2021特殊一

    @iz_test.flow_factory.add_flow()
    async def place_zombies(_):
        ts = iz_test.ground["1-4"]
        xg = place("xg 2-6")
        # await until_plant_n_shoot(ts)
        # await until_plant_last_shoot(ts)
        await until_plant_n_shoot(ts).after(34) #豌豆生成
        await delay(92)
        if not xg.is_dead:
            await delay(143)
        iz_test.game_board.zombie_list.set_next_idx(3)
        iz_test.game_board.iz_place_zombie(0,5,ZombieType.imp)

        await delay(48)
        iz_test.game_board.zombie_list.set_next_idx(2)
        iz_test.game_board.iz_place_zombie(0,5,ZombieType.imp)

        await delay(118)
        iz_test.game_board.zombie_list.set_next_idx(1)
        iz_test.game_board.iz_place_zombie(0,5,ZombieType.imp)

    iz_test.start_test(jump_frame=1, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    
