from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place, repeat
from rpze.flow.utils import until, delay
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant, PlantType

def until_l_right_last_shoot(plant: Plant, wait_until_mbd: bool = False) -> AwaitableCondFunc[int]:
    mbd = plant.max_boot_delay

    def _await_func(fm: FlowManager, v=VariablePool(
            last_shooting_time=None,
            until_mbd_ret=None)):
        if v.until_mbd_ret is not None:  # until mbd flag开了就走: 等到最大攻击间隔后再返回
            if fm.time >= v.last_shooting_time + mbd:
                return True, v.until_mbd_ret
            return False
        if plant.generate_cd == 25 and plant.launch_cd > 15:
            v.last_shooting_time = fm.time
            return False
        if plant.generate_cd == 25 and plant.launch_cd < 15:
            if v.last_shooting_time is not None:
                if not wait_until_mbd or fm.time == v.last_shooting_time + mbd:
                    return True, fm.time - v.last_shooting_time
                # 如果等最大攻击间隔再返回 flag改not None开始走until逻辑
                v.until_mbd_ret = fm.time - v.last_shooting_time
                return False
            v.last_shooting_time = None
            return False  # 上一轮是攻击的 且 这一轮不攻击 返回True
        return False
    
    return AwaitableCondFunc(_await_func)

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        .....
        ....l
        .....
        .....
        xg 
        0  
        3-9''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        l = iz_test.ground["3-5"]

        await until_l_right_last_shoot(l)
        place("xg 3-6")

    @iz_test.flow_factory.add_tick_runner()
    def check(fm:FlowManager):
        if fm.time > 800:
            if iz_test.ground["3-5"] is None:
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)
        
    iz_test.start_test(jump_frame=0, speed_rate=2,print_interval=1e2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    