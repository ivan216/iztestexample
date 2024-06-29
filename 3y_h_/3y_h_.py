from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.operations import place
from rpze.flow.utils import until
from rpze.rp_extend import Controller
from random import randint

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        3y_s_
        .....
        .....
        tt 
        0  
        3-6''')
    
    ts_fail_count = 0 #没吃掉三线的次数
    _125_count = 0 #补铁桶次数
    _75_count = 0 #补75的次数

###结论：橄榄176，铁桶174，障（补障）杆（补杆）出第二黄油直接补障 173

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal _75_count,_125_count
        zlist = iz_test.game_board.zombie_list
        plist = iz_test.ground
        tt = zlist[0]
        ts = plist["3-1"]
        y = plist["3-2"]
        s = plist["3-4"]

        while not s.is_dead:
            await (until(lambda _:s.is_dead) | until(lambda _:tt.hp <= 89)) #伞先死还是桶先死
            if not s.is_dead :
                tt = place("tt 3-6") #补桶补到啃完为止
                _125_count += 1     
        if tt.accessories_hp_1 <= 420 : #啃完伞但铁桶已经比较残
            await (until(lambda _:tt.hp <= 130) | until(lambda _:tt.int_x <= 210))
            cg = place("cg 3-6")     #等到铁桶快死或者比较近补杆
            _75_count += 1
            await until(lambda _:cg.hp <= 210) 
            if ts.hp >=300 :     #杆也过不去
                place("cg 3-6") #补第二杆
                _75_count += 1
        else :
            await until(lambda _:tt.accessories_hp_1 <= 280)
            if tt.int_x >= 210 :         #补障不太靠谱，凭感觉增加一个补杆的判断点，减少补障的概率，大概在铁桶走到3列4列间
                cg = place("cg 3-6")        #铁桶已经下到一定血量，且比较靠后，那么直接补杆 280
                _75_count += 1
                await until(lambda _:cg.hp <= 210) 
                if ts.hp >=300:     #杆也过不去
                    place("cg 3-6") #补第二杆
                    _75_count += 1
            else :
                await (until(lambda _:y.is_dead) | until(lambda _:tt.hp <= 89)) #玉米先死还是桶先死
                if (tt.hp <= 89) & (not y.is_dead) :    #桶先死
                    cg = place("cg 3-6")     #补杆
                    _75_count += 1
                    await until(lambda _:cg.hp <= 210) 
                    if ts.hp >=300:     #杆也过不去
                        place("cg 3-6") #补第二杆
                        _75_count += 1
                elif tt.hp <= 210:    #啃完玉米但铁桶已经比较残
                    lz = place("lz 3-6")     #补障
                    _75_count += 1
                    await until(lambda _:lz.hp <= 190) 
                    if (ts.hp >=300) & (lz.int_x >= 120) :    #障也过不去
                        place("lz 3-6")     #补第二障
                        _75_count += 1
                else:
                    await until(lambda _:tt.hp <= 190) 
                    if (ts.hp >=300) & (tt.int_x >= 120) :  #看是否需要补障
                        lz = place("lz 3-6")     #补障
                        _75_count += 1
                        await until(lambda _:lz.hp <= 190) 
                        if (ts.hp >=300) & (lz.int_x >= 120) :    #障也过不去
                            place("lz 3-6")     #补第二障
                            _75_count += 1
        
    @iz_test.on_game_end()
    def end_callback(result: bool):
        if not result:
            nonlocal ts_fail_count
            plant_list = iz_test.ground
            if plant_list["3-1"] is not None:
                ts_fail_count += 1
    
    iz_test.start_test(jump_frame=0, speed_rate=10)
    print("漏三线或失败:",ts_fail_count)
    print("补桶:",_125_count)
    print("补75:",_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
