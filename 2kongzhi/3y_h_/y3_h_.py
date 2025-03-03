from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.flow.utils import until
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0 3-2
        .....
        .....
        y3_s_
        .....
        .....
        tt 
        0  
        3-6''')
    
    ts_fail_count = 0 #没吃掉三线的次数
    tp_fail_2zb = 0
    tp_fail_tt = 0
    _125_count = 0 #补铁桶次数
    _75_count = 0 #补75的次数

    ###应当考虑时间点：
    #啃伞就掉许多血，补杆？障？桶？
    #走到3与4列间掉很多血，补杆？障？桶？
    #是否啃掉三线，补杆？障？桶？
    #是否啃掉玉米，杆

    ####结论：不禁铁，橄榄176 为唯一正解。
    #禁铁：双杆，三线都未啃完，双障；啃完三线，放小鬼，看情况补杆。205

    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal _75_count , _125_count,tp_fail_2zb,tp_fail_tt
        tt = iz_test.game_board.zombie_list[0]
        tp = iz_test.ground["3-2"]
        y = iz_test.ground["3-1"]
        s = iz_test.ground["3-4"]

        await until(lambda _:tt.accessories_hp_1 <= 340)
        if tt.int_x >=300 :
            lz = place("lz 3-6")
            _75_count += 1
            await (until(lambda _:lz.hp < 90) & until(lambda _:tt.hp < 90))
            if not tp.is_dead:
                tp_fail_2zb += 1
        else:
            await until(lambda _:tt.accessories_hp_1 <= 220)
            if tt.int_x >= 220 :
                lz = place("lz 3-6")
                _75_count += 1
                await (until(lambda _:lz.hp < 90) & until(lambda _:tt.hp < 90))
                if not tp.is_dead:
                    tp_fail_2zb += 1
            else :
                await (until(lambda _:tt.hp < 90) | until(lambda _:tp.is_dead))
                if not tp.is_dead :
                    tt = place("tt 3-6")
                    _125_count += 1
                    await until(lambda _:tt.hp < 90)
                    if not tp.is_dead:
                        tp_fail_tt += 1
                else :
                    await until(lambda _:tt.hp < 90)
                    place("cg 3-6")
                    _75_count += 1

    @iz_test.on_game_end()
    def _(_):
        nonlocal ts_fail_count
        plant_list = iz_test.ground
        if plant_list["3-2"] is not None:
            ts_fail_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=3)

    print("补桶:",_125_count)
    print("补75:",_75_count)
    print("漏三线(算作补150):",ts_fail_count)
    print("其中 障桶死亡:",tp_fail_2zb)
    print("     补桶死亡:",tp_fail_tt)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)