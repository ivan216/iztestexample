from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place, repeat
from rpze.flow.utils import until, delay
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant, PlantType
from rpze.iztest.plant_modifier import randomize_generate_cd

def until_plant_last_shoot(plant: Plant, wait_until_mbd: bool = False) -> AwaitableCondFunc[int]:
    shoot_next_gcd = 1 if plant.type_ is not PlantType.split_pea else 26  # 修正裂荚攻击时机
    mbd = plant.max_boot_delay

    def _await_func(fm: FlowManager, v=VariablePool(
            try_to_shoot_time=None,
            last_shooting_time=None,
            until_mbd_ret=None)):
        if v.until_mbd_ret is not None:  # until mbd flag开了就走: 等到最大攻击间隔后再返回
            if fm.time >= v.last_shooting_time + mbd:
                return True, v.until_mbd_ret
            return False
        if plant.generate_cd == shoot_next_gcd:  # 下一帧开打
            v.try_to_shoot_time = fm.time + 1
        if v.try_to_shoot_time == fm.time:
            if plant.launch_cd > 15:  # 判断大于15则处于攻击状态, 目的是兼容忧郁菇
                v.last_shooting_time = fm.time
                return False
            else:  # 不处于攻击状态
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
        ...o.
        .....
        .....
        xt 
        0  
        3-4''')
    
    #单发35;双发26(25,0);喷,海29;大50;胆25;裂右26(25);星40;菜32;玉30;瓜36;机100;忧200;猫50(50,0);
    #刺100->75;钢刺100->70->32

    plant = None
    shoot = adj = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm:FlowManager):
        nonlocal plant,shoot,adj
        shoot = 0
        print()
        plant = randomize_generate_cd(iz_test.game_board.new_plant(2,2,PlantType.split_pea))
        adj = 1 if plant.type_ is not PlantType.split_pea else 26

        ti = await until_plant_last_shoot(plant,1)
        print("间隔 = ",ti)
        print("返回时间 ",fm.time)
        place("xg 3-4")

    @iz_test.flow_factory.add_tick_runner()
    def printfun(fm:FlowManager):
        nonlocal shoot
        if fm.time >0:
            if plant.generate_cd == adj:
                shoot = fm.time + 1
            if shoot == fm.time and plant.launch_cd > 15:
                print("植物攻击 ",fm.time)
        
    @iz_test.flow_factory.add_tick_runner()
    def check(fm:FlowManager):
        if fm.time > 1200:
            if plant.is_dead:
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)

    iz_test.start_test(jump_frame=0, speed_rate=0.2,print_interval=1e2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
