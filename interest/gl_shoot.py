from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place, repeat
from rpze.flow.utils import until, delay
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant, PlantType
from rpze.iztest.plant_modifier import randomize_generate_cd
from rpze.iztest.cond_funcs import until_plant_last_shoot

def until_gl_last_shoot(plant: Plant, wait_until_mbd: bool = False) -> AwaitableCondFunc[int]:
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
        if v.try_to_shoot_time == fm.time and plant.launch_cd == 200:  # 在攻击时
            v.last_shooting_time = fm.time
            return False
        if v.try_to_shoot_time == fm.time and plant.launch_cd != 200:  # 不在攻击时
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
    
    i = 0   # 没有  <0x14c=332
    #单发35;双发26(25,0);喷,海29;大50;胆25;裂26(25);星40;菜32;玉30;瓜36;机100;忧200;猫50(50,0);
    #刺100->75;钢刺100->70->32

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal i
        plant = randomize_generate_cd(iz_test.game_board.new_plant(2,2,PlantType.pea_shooter))
        # pl2 = iz_test.game_board.new_plant(4,3,PlantType.pea_shooter)
        # print(hex(pl2.base_ptr - plant.base_ptr))

        if iz_test.controller.read_i32(plant.base_ptr + 4*i) == 35:
            print("i= ",i)
            print(iz_test.controller.read_i32(plant.base_ptr + 4*i))

        # if i > 322:
        #     return iz_test.check_tests_end(1)

        await until_plant_last_shoot(plant)
        place("xg 1-5")

        i += 1
        
    @iz_test.flow_factory.add_tick_runner()
    def check(fm:FlowManager):
        if fm.time > 1100:
            if iz_test.ground["1-0"] is None:
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)

    iz_test.start_test(jump_frame=1, speed_rate=2,print_interval=1e2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)