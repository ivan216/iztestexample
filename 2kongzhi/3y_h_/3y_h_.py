from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place
from rpze.flow.utils import until

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
    
    tp_fail_count = 0 #没吃掉三线的次数
    _125_count = 0 #补铁桶次数
    _75_count = 0 #补75的次数

    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal _75_count,_125_count
        bu_gan = False  #补刀标记
        bu_zhang = False
        tt = iz_test.game_board.zombie_list[0]
        tp = iz_test.ground["3-1"]
        y = iz_test.ground["3-2"]
        s = iz_test.ground["3-4"]
        
        while not s.is_dead:
            await until(lambda _: tt.hp <= 89 or s.is_dead) #伞先死还是桶先死
            if not s.is_dead :
                tt = place("tt 3-6") #补桶补到啃完为止
                _125_count += 1     

        if tt.accessories_hp_1 <= 420 : #啃完伞但铁桶已经比较残
            await until(lambda _:tt.hp <= 130 or tt.int_x <= 210)  #等到铁桶快死或者比较近补杆
            bu_gan = True   # 进入循环补杆阶段
        else :
            await until(lambda _:tt.accessories_hp_1 <= 280)#增加一个补杆的判断点，减少补障的概率，大概在铁桶走到3列4列间
            if tt.int_x >= 210 :         #铁桶已经下到一定血量，且比较靠后，那么直接补杆
                bu_gan = True
            else :
                await until(lambda _: tt.hp <= 89 or y.is_dead) #玉米先死还是桶先死
                if tt.hp <= 89 and not y.is_dead :    #桶先死
                    bu_gan = True
                elif tt.hp <= 210:    #啃完玉米但铁桶已经比较残
                    bu_zhang = True
                else:
                    await until(lambda _:tt.hp <= 190) 
                    if tp.hp >= 300 and tt.int_x >= 120 :  #看是否需要补障
                        bu_zhang = True

        if bu_gan :
            while not tp.is_dead:
                cg = place("cg 3-6")    #继续补杆
                _75_count += 1
                await until(lambda _:cg.hp <= 210) 
                if tp.hp < 300 :     #不用再补了
                    break           

        if bu_zhang :
            while not tp.is_dead:
                lz = place("lz 3-6")     #继续补障
                _75_count += 1
                await until(lambda _:lz.hp <= 190) 
                if tp.hp < 300 or lz.int_x < 120 :  #不用再补
                    break
                    
    @iz_test.on_game_end()
    def _(_):
        nonlocal tp_fail_count
        if iz_test.ground["3-1"] is not None :
            tp_fail_count += 1
    
    iz_test.start_test(jump_frame=1, speed_rate=5)
    print("漏三线:",tp_fail_count)
    print("补桶:",_125_count)
    print("补75:",_75_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
