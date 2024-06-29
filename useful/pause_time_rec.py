from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place,delay
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
        iz_test.game_board.sun_num = 9876
        await count_butter(pl,2)
        await delay(100)
        place("lz 3-6")

    no_pause_time = 0
    
    @iz_test.flow_factory.add_tick_runner()
    def print_no_pause_time(fm:FlowManager):
        nonlocal no_pause_time
        if no_pause_time == 0 :
            print("不含暂停时间：",no_pause_time)
            print("真实时间",fm.time)
        else:
            print("\033[2A\r"+"不含暂停时间：",no_pause_time)
            print("真实时间",fm.time)
        if not ctler.read_bool(0x6a9ec0, 0x768, 0x164) :
            no_pause_time += 1

    @iz_test.on_game_end()
    def clear_fun(_):
        nonlocal no_pause_time
        no_pause_time = 0
        print()

    iz_test.start_test(jump_frame=0, speed_rate=1)   #最小 0.05

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)