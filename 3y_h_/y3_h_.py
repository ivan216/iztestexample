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
    async def place_zombie(_):
        nonlocal _75_count , _125_count
        zlist = iz_test.game_board.zombie_list
        plist = iz_test.ground
        tt = zlist[0]
        ts = plist["3-2"]
        y = plist["3-1"]
        s = plist["3-4"]

        await until(lambda _:tt.accessories_hp_1 <= 360)
        if tt.int_x >=300 :
            lz = place("lz 3-6")
            _75_count += 1
            await (until(lambda _:lz.hp < 90) & until(lambda _:tt.hp < 90))
            place("cg 3-6")
            _75_count += 1
        else:
            await until(lambda _:tt.accessories_hp_1 <= 220)
            if tt.int_x >= 220 :
                lz = place("lz 3-6")
                _75_count += 1
                await (until(lambda _:lz.hp < 90) & until(lambda _:tt.hp < 90))
                place("cg 3-6")
                _75_count += 1
            else :
                await (until(lambda _:tt.hp < 90) | until(lambda _:ts.is_dead))
                if not ts.is_dead :
                    tt = place("tt 3-6")
                    _125_count += 1
                    await until(lambda _:tt.hp < 90)
                    place("cg 3-6")
                    _75_count += 1
                else :
                    await until(lambda _:tt.hp < 90)
                    place("cg 3-6")
                    _75_count += 1

    @iz_test.on_game_end()
    def end_callback(result: bool):
        nonlocal ts_fail_count
        plant_list = iz_test.ground
        if plant_list["3-2"] is not None:
            ts_fail_count += 1

    iz_test.start_test(jump_frame=0, speed_rate=10)
    print("漏三线:",ts_fail_count)
    print("补桶:",_125_count)
    print("补75:",_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)