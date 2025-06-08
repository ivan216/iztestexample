from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import repeat, place
from rpze.flow.utils import until, delay
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant, PlantType
from rpze.iztest.plant_modifier import randomize_generate_cd
from rpze.iztest.cond_funcs import until_plant_die
from random import randint

def until_plant_last_shoot(plant: Plant, wait_until_mbd: bool = False) -> AwaitableCondFunc[int]:
    
    mbd = plant.max_boot_delay
    match plant.type_:  # 修正连发植物攻击时机
        case PlantType.repeater | PlantType.split_pea:
            shoot_next_gcd = 26
        case PlantType.cattail:
            shoot_next_gcd = 51
        case _:
            shoot_next_gcd = 1

    def _await_func(fm: FlowManager, v=VariablePool(
            try_to_shoot_time=None,
            last_shooting_time=None,
            until_mbd_ret=None)):
        if v.until_mbd_ret is not None:  # until mbd flag开了就走: 等到最大攻击间隔后再返回
            if fm.time >= v.last_shooting_time + mbd:
                return True, v.until_mbd_ret
        elif plant.generate_cd == shoot_next_gcd:  # 下一帧开打
            v.try_to_shoot_time = fm.time + 1
        elif v.try_to_shoot_time == fm.time:
            if plant.launch_cd > 15:  # 判断大于15则处于攻击状态, 目的是兼容忧郁菇
                # 一般植物处于非攻击状态launch_cd为0, 忧郁菇处于非攻击状态的launch_cd最大值为14
                v.last_shooting_time = fm.time
            else:  # 不处于攻击状态
                if v.last_shooting_time is not None:
                    if not wait_until_mbd or fm.time == v.last_shooting_time + mbd:
                        return True, fm.time - v.last_shooting_time
                    # 如果等最大攻击间隔再返回 flag改not None开始走until逻辑
                    v.until_mbd_ret = fm.time - v.last_shooting_time
        return False

    return AwaitableCondFunc(_await_func)

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        1-2 5-4
        zh_j5
        cptoh
        .....
        3lyp_
        hhwz1
        lz 
        0  
        2-6''')
    
    #单发35;双发26(gcd 25,0);喷,海29;大50;胆25;裂右26(25);星40;菜32;玉30;瓜36;机100;忧200;猫50(50,0);
    #刺100->75;钢刺100->70->32

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        ground = iz_test.ground
        flower = ground["2-5"]
        await until(lambda _: flower.hp <= 4)
        place("cg 2-6")  # 2-5花死前一瞬放撑杆
        star = ground["1-5"]
        await until_plant_last_shoot(star,True).after(151 - 96)
        # 上面randint不加是必过, 实际上需要判断星星打几下而不是直接找最后一下不攻击再放
        await repeat("xg 1-6")  # 星星最后一发攻击发出后1双鬼
        await until_plant_die(star).after(100)
        await repeat("cg 4-6")  # 星星死后4双杆
        await until_plant_die(ground["4-1"])
        place("cg 5-9")  # 三线死后5-9撑杆
        await until_plant_last_shoot(ground["5-5"],True).after(151 + randint(0, 14))
        place("xg 5-6")  # 5-5最后一发攻击发出后5双鬼

    row_one_fail_count = 0
    row_five_fail_count = 0

    @iz_test.on_game_end()
    def _(result: bool):
        if not result:
            nonlocal row_five_fail_count, row_one_fail_count
            if iz_test.ground["1-2"] is not None:
                row_one_fail_count += 1
            if iz_test.ground["5-4"] is not None:
                row_five_fail_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=5)
    print(row_one_fail_count, row_five_fail_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)