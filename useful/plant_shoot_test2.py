from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place, repeat
from rpze.flow.utils import until
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant

def until_plant_last_shoot(plant: Plant, wait_until_mbd: bool = False) -> AwaitableCondFunc[int]:

    mbd = plant.max_boot_delay

    def _await_func(fm: FlowManager, v=VariablePool(
            try_to_shoot_time=None,
            last_shooting_time=None,
            until_mbd_ret=None)):
        if v.until_mbd_ret is not None:  # until mbd flag开了就走: 等到最大攻击间隔后再返回
            if fm.time >= v.last_shooting_time + mbd:
                return True, v.until_mbd_ret
            return False
        if plant.generate_cd == 1:  # 下一帧开打
            v.try_to_shoot_time = fm.time + 1
        if v.try_to_shoot_time == fm.time and plant.launch_cd != 0:  # 在攻击时
            v.last_shooting_time = fm.time
            return False
        if v.try_to_shoot_time == fm.time and plant.launch_cd == 0:  # 不在攻击时
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
        2-0
        .....
        .....
        ....y
        .....
        .....
        lz xg
        0  0
        2-3 3-9''')
    
    pl = None
    shoot = 0
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm:FlowManager):
        print()
        nonlocal pl,shoot
        shoot = 0

        pl = iz_test.ground["3-5"]
        t = await until_plant_last_shoot(pl,True)
        print("t = ",t)
        print("返回时间 ",fm.time)

    @iz_test.flow_factory.add_tick_runner()
    def printfun(fm:FlowManager):
        nonlocal shoot
        if fm.time >0:
            if pl.generate_cd == 1:
                shoot = fm.time + 1
            if shoot == fm.time and pl.launch_cd != 0:
                print("植物攻击 ",fm.time)

    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)